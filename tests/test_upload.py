import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import fitz
from fastapi.testclient import TestClient

import app as application


class ApiBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(application.app)
        self.tmp = tempfile.TemporaryDirectory(dir=Path(__file__).parents[1] / "work")
        self.addCleanup(self.tmp.cleanup)
        patch.object(application, 'WORK', Path(self.tmp.name)).start()
        self.start = patch.object(application, '_start', return_value='fixturejob').start()
        self.addCleanup(patch.stopall)

    def pdf(self, pages=1, locked=False):
        with fitz.open() as doc:
            for _ in range(pages):
                doc.new_page()
            if locked:
                return doc.tobytes(encryption=fitz.PDF_ENCRYPT_AES_256, user_pw='secret', owner_pw='owner')
            return doc.tobytes()

    def upload(self, data):
        return self.client.post('/api/unggah', files={'file': ('fixture.pdf', data, 'application/pdf')})

    def test_valid_pdf_starts_once(self):
        self.assertEqual(self.upload(self.pdf()).json(), {'id': 'fixturejob'})
        self.start.assert_called_once()
        self.assertEqual(list(Path(self.tmp.name).glob('up_*')), [])

    def test_forged_pdf_is_rejected_before_processing(self):
        for data in (b'text', b'%PDF not a valid document'):
            self.assertEqual(self.upload(data).status_code, 400)
        self.start.assert_not_called()

    def test_oversize_pdf_is_rejected(self):
        with patch.object(application, 'MAX_UPLOAD', 1024):
            self.assertEqual(self.upload(b'%PDF' + b'x' * 1024).status_code, 413)
        self.start.assert_not_called()

    def test_encrypted_or_too_many_pages_is_rejected(self):
        self.assertEqual(self.upload(self.pdf(locked=True)).status_code, 400)
        self.assertEqual(self.upload(self.pdf(pages=201)).status_code, 400)
        self.start.assert_not_called()

    def test_unknown_review_target_is_404(self):
        self.assertEqual(self.client.post('/api/tinjau/missing/missing', json={'aksi': 'tolak'}).status_code, 404)

    def test_delete_active_job_is_409(self):
        with patch.dict(application.JOBS, {'fixturejob': {'tahap': 'gambar'}}):
            self.assertEqual(self.client.delete('/api/pekerjaan/fixturejob').status_code, 409)


if __name__ == '__main__':
    unittest.main()
