import subprocess, re, sys
VP = r"C:\vpaudit\verapdf\verapdf.bat"
RULE = re.compile(r'<rule specification="[^"]*" clause="([^"]+)" testNumber="(\d+)" status="failed"[^>]*?failedChecks="(\d+)"')
DESC = re.compile(r'<rule specification="[^"]*" clause="([^"]+)" testNumber="(\d+)" status="failed"[^>]*>\s*<description>([^<]*)</description>')

def run(f):
    r = subprocess.run([VP, "--flavour", "ua1", "--format", "xml", f], capture_output=True, text=True, encoding="utf-8", errors="replace")
    x = r.stdout
    if "<validationReport" not in x:
        return "ERR " + (r.stderr or x)[:200]
    rules = RULE.findall(x)
    descs = {(c, t): d.strip() for c, t, d in DESC.findall(x)}
    ok = re.search(r'isCompliant="(\w+)"', x).group(1)
    out = f"compliant={ok} | aturan gagal={len(rules)} | pemeriksaan gagal={sum(int(n) for _,_,n in rules)}"
    for c, t, n in rules:
        out += f"\n     {c}-{t} x{n}: {descs.get((c,t),'')[:110]}"
    return out

if __name__ == "__main__":
    for f in sys.argv[1:]:
        print("===", f.replace("\\", "/").split("/")[-1])
        print("  ", run(f))
