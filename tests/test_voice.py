import io
import os
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient
import app
from simak import pipeline, voice


class VoiceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.audio = Path(self.tmp.name)
        patch.object(voice, 'AUDIO', self.audio).start()
        patch.dict(os.environ, {'ELEVENLABS_API_KEY': 'test-only', 'ELEVENLABS_VOICE_ID': 'test-voice'}).start()
        self.addCleanup(patch.stopall)

    def test_audio_cached_and_voice_change_invalidates_cache(self):
        with patch.object(voice, '_eleven', side_effect=lambda text, out, rate: out.write_bytes(b'ID3fixture')) as convert:
            first = voice.synthesize('Nilai 12 persen.')
            self.assertEqual(voice.synthesize('Nilai 12 persen.'), first)
            os.environ['ELEVENLABS_VOICE_ID'] = 'another-voice'
            self.assertNotEqual(voice.synthesize('Nilai 12 persen.'), first)
            self.assertEqual(convert.call_count, 2)

    def test_failed_download_never_leaves_playable_cache(self):
        error = urllib.error.HTTPError('https://api.elevenlabs.io', 401, 'denied', {}, io.BytesIO(b'secret-response'))
        with patch.object(voice.urllib.request, 'urlopen', side_effect=error):
            with self.assertRaisesRegex(voice.VoiceError, 'Akses ElevenLabs ditolak'):
                voice.synthesize('Uji kegagalan')
        self.assertEqual(list(self.audio.iterdir()), [])

    def test_api_returns_actionable_error_without_provider_response(self):
        with patch.object(app, '_synth', side_effect=voice.VoiceError('Pilih suara peramban.')):
            r = TestClient(app.app).post('/api/suara', json={'teks': 'Uji'})
        self.assertEqual(r.status_code, 503)
        self.assertEqual(r.json()['detail'], 'Pilih suara peramban.')

    def test_invalid_vlm_response_holds_element(self):
        el = {'id': 'test', 'kind': 'image', 'page': 1, 'png_bytes': b'fixture'}
        with patch.object(pipeline, 'process_image', side_effect=ValueError('invalid JSON')), self.assertLogs(level='ERROR'):
            pipeline.process_or_hold(el, {})
        self.assertEqual(el['status'], 'antrean')
        self.assertEqual(el['checks'], {})


if __name__ == '__main__':
    unittest.main()
