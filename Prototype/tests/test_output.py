import json
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

from simak import listen, output, pipeline


class Structure(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.images = []
        self.external = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'img':
            self.images.append(attrs)
        if tag in ('link', 'script') and any(attrs.get(k, '').startswith('http') for k in ('src', 'href')):
            self.external.append(attrs)


class ReaderTests(unittest.TestCase):
    def setUp(self):
        self.state = json.loads((Path(__file__).parent / 'fixtures' / 'ui_states.json').read_text(encoding='utf-8'))['completed']
        self.tmp = tempfile.TemporaryDirectory(dir=Path(__file__).parents[1] / "work")
        self.addCleanup(self.tmp.cleanup)
        self.state['_job'] = self.tmp.name
        image_dir = Path(self.tmp.name) / 'img'
        image_dir.mkdir()
        png = (Path(__file__).parents[1] / 'data' / 'synth' / 'charts' / 'syn043.png').read_bytes()
        for e in self.state['elements']:
            if e['kind'] == 'image':
                (image_dir / (e['id'] + '.png')).write_bytes(png)

    def test_standalone_semantics_and_status_provenance(self):
        html = output.build_html(self.state, pipeline.alt_for)
        parsed = Structure()
        parsed.feed(html)
        self.assertIn('lang="id"', html)
        self.assertIn('data:font/woff2;base64,', html)
        self.assertTrue(all(i['src'].startswith('data:image/png;base64,') for i in parsed.images))
        self.assertEqual(parsed.external, [])
        self.assertEqual(len(parsed.ids), len(set(parsed.ids)))
        self.assertIn('Diubah dan disetujui ULD', html)
        self.assertIn('Ditolak ULD · deskripsi belum tersedia', html)
        self.assertIn('1 gambar menunggu tinjauan; 1 deskripsi ditolak', html)
        self.assertNotIn('Draf sintetis yang belum diverifikasi.', html)
        self.assertEqual(sum(i.get('alt') == '' for i in parsed.images), 1)
        self.assertIn("scope='col'", html)
        self.assertIn("role='region'", html)

    def test_rejected_image_not_narrated_as_pending(self):
        seg = next(s for s in listen.remediated(self.state) if s.get('el') == 'e4')
        self.assertIn('ditolak', seg['text'])
        self.assertNotIn('menunggu tinjauan', seg['text'])


if __name__ == '__main__':
    unittest.main()
