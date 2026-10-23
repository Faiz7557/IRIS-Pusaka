param([int]$Port = 8017)
$ErrorActionPreference = 'Stop'
$simakPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $simakPython)) {
    throw 'Environment belum ada. Jalankan python -m venv .venv lalu .\.venv\Scripts\python.exe -m pip install -r requirements.txt dari folder Prototype.'
}
Push-Location -LiteralPath $PSScriptRoot
try { & $simakPython -m uvicorn app:app --host 127.0.0.1 --port $Port }
finally { Pop-Location }
