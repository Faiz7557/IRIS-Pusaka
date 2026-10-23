import copy
import json
import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import patch

from simak import pipeline


FIXTURE = Path(__file__).parent / 'fixtures' / 'ui_states.json'


class ReviewTransactionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=Path(__file__).parents[1] / "work")
        self.addCleanup(self.tmp.cleanup)
        self.job = Path(self.tmp.name)
        self.state = json.loads(FIXTURE.read_text(encoding='utf-8'))['completed']
        pipeline.save(self.job, self.state)
        (self.job / 'simak.pdf').write_bytes(b'old-pdf')
        (self.job / 'simak.html').write_text('old-html', encoding='utf-8')
        self.assemble = patch.object(pipeline, 'assemble', side_effect=self.fake_assemble).start()
        patch.object(pipeline.pdfa11y, 'verapdf', return_value={'compliant': True}).start()
        patch.object(pipeline.pdfa11y, 'g1_audit', return_value={'pass': True}).start()
        self.addCleanup(patch.stopall)

    def fake_assemble(self, job, state, output):
        snapshot = json.dumps({e['id']: e.get('status') for e in state['elements']})
        (output / 'simak.pdf').write_text(snapshot, encoding='utf-8')
        (output / 'simak.html').write_text(snapshot, encoding='utf-8')

    def test_two_concurrent_decisions_both_survive(self):
        barrier = threading.Barrier(2)

        def decide(el, text):
            barrier.wait(timeout=5)
            return pipeline.review(self.job, el, 'ubah', text)

        with ThreadPoolExecutor(2) as pool:
            a = pool.submit(decide, 'e1', 'Keputusan A')
            b = pool.submit(decide, 'e2', 'Keputusan B')
            a.result(timeout=10)
            b.result(timeout=10)
        state = pipeline.load(self.job)
        elements = {e['id']: e for e in state['elements']}
        self.assertEqual(elements['e1']['alt_final'], 'Keputusan A')
        self.assertEqual(elements['e2']['alt_final'], 'Keputusan B')
        self.assertEqual(len(elements['e1']['log']), 1)
        self.assertEqual(len(elements['e2']['log']), 1)
        pdf = pipeline.output_path(self.job, 'simak.pdf')
        html = pipeline.output_path(self.job, 'simak.html')
        self.assertEqual(pdf.parent, html.parent)
        self.assertEqual(json.loads(pdf.read_text())['e1'], 'diubah')
        self.assertEqual(json.loads(html.read_text())['e2'], 'diubah')

    def test_assembly_failure_keeps_old_state_and_outputs(self):
        def fail(job, state, output):
            (output / 'simak.pdf').write_bytes(b'incomplete')
            raise RuntimeError('simulated assembly failure')

        self.assemble.side_effect = fail
        with self.assertRaises(RuntimeError):
            pipeline.review(self.job, 'e1', 'ubah', 'Tidak boleh terbit')
        self.assertEqual(pipeline.load(self.job), self.state)
        self.assertEqual(pipeline.output_path(self.job, 'simak.pdf').read_bytes(), b'old-pdf')
        self.assertEqual((self.job / 'simak.html').read_text(), 'old-html')
        self.assertEqual(list((self.job / 'versions').iterdir()), [])

    def test_pointer_save_failure_does_not_publish_staged_outputs(self):
        with patch.object(pipeline, 'save', side_effect=OSError('disk full')):
            with self.assertRaises(OSError):
                pipeline.review(self.job, 'e1', 'ubah', 'Tidak terbit')
        self.assertEqual(pipeline.load(self.job), self.state)
        self.assertEqual(list((self.job / 'versions').iterdir()), [])

    def test_unknown_element_and_blank_vector_alt_are_rejected(self):
        for action in ('setujui', 'ubah'):
            with self.assertRaises(ValueError):
                pipeline.review(self.job, 'e1', action, '   ')
        with self.assertRaises(LookupError):
            pipeline.review(self.job, 'missing', 'tolak')
        with self.assertRaises(ValueError):
            pipeline.review(self.job, 'e1', 'invalid')
        self.assertEqual(pipeline.load(self.job), self.state)

    def test_old_version_survives_next_publication(self):
        pipeline.review(self.job, 'e1', 'ubah', 'Versi pertama')
        first = pipeline.output_path(self.job, 'simak.pdf')
        content = first.read_bytes()
        pipeline.review(self.job, 'e1', 'ubah', 'Versi kedua')
        self.assertNotEqual(first, pipeline.output_path(self.job, 'simak.pdf'))
        self.assertEqual(first.read_bytes(), content)
        self.assertEqual(pipeline.load(self.job)['elements'][4]['alt_final'], 'Versi kedua')

    def test_invalid_version_pointer_does_not_escape_job(self):
        state = copy.deepcopy(self.state)
        state['output_version'] = '../outside'
        pipeline.save(self.job, state)
        with self.assertRaises(ValueError):
            pipeline.output_path(self.job, 'simak.pdf')


if __name__ == '__main__':
    unittest.main()
