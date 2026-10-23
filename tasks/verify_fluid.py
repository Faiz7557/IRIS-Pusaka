"""Tes lokal dan manifes source; tidak membaca kredensial atau memakai API live."""
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'tasks/evidence/fluid'
OUT.mkdir(parents=True, exist_ok=True)
commands = [
    [sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v'],
    ['node', 'tests/test_frontend.cjs'],
    ['node', 'tests/test_speech.cjs'],
    ['node', 'tests/test_motion.cjs'],
    ['node', '--check', 'web/speech.js'],
    ['node', '--check', 'web/common.js'],
    ['node', '--check', 'web/motion.js'],
    ['node', '--check', 'web/sill-scenes.js'],
]
checks = []
for n, cmd in enumerate(commands):
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
    log = f'test-{n+1}.log'
    (OUT/log).write_text(p.stdout + p.stderr, encoding='utf-8')
    checks.append({'command': cmd[1:], 'exit_code': p.returncode, 'log': log})
files = [ROOT/'app.py', *(ROOT/'simak').glob('*.py'), *(ROOT/'web').glob('*.js'), *(ROOT/'web').glob('*.css'), *(ROOT/'web').glob('*.html'), *(ROOT/'web/vendor').glob('*.js')]
hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
secret_files = [str(p.relative_to(ROOT)) for p in files if re.search(r'sk_[a-zA-Z0-9]{30,}', p.read_text(encoding='utf-8'))]
remote_refs = []
for p in files:
    if p.parent.name == 'web' and p.suffix in ('.js', '.css', '.html'):
        refs = re.findall(r'(?:src|href)=[\'"](https?://[^\'"]+)', p.read_text(encoding='utf-8'))
        remote_refs.extend({'file': str(p.relative_to(ROOT)), 'url': u} for u in refs)
result = {'checked_at': datetime.now(timezone(timedelta(hours=7))).isoformat(), 'checks': checks,
          'source_sha256': hashes, 'source_files_with_secret_pattern': secret_files,
          'external_src_or_href': remote_refs,
          'eval_results_sha256': hashlib.sha256((ROOT/'eval/results.json').read_bytes()).hexdigest(),
          'static_web_bytes': sum(p.stat().st_size for p in (ROOT/'web').rglob('*') if p.is_file())}
(OUT/'verification.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps({'tests': checks, 'secret_patterns_in_source': len(secret_files),
                  'external_src_or_href': remote_refs, 'web_bytes': result['static_web_bytes']}, indent=2))
assert not secret_files
assert all(c['exit_code'] == 0 for c in checks)
