import pikepdf, time
src = r"C:/Uner/Lomba/Campus Data Week/Semifinal/Contoh Paper/Executive Summary IFEST Teen Tensors.pdf"
t=time.time()
pdf = pikepdf.open(src)
root = pdf.Root.StructTreeRoot
figs=[]
seen=set()
def walk(node, depth=0):
    if isinstance(node, pikepdf.Array):
        for k in node: walk(k, depth)
        return
    if not isinstance(node, pikepdf.Dictionary): return
    og = node.objgen
    if og in seen: return
    seen.add(og)
    if node.get("/S") == "/Figure": figs.append(node)
    if "/K" in node: walk(node.K, depth+1)
walk(root)
print("Figure elems:", len(figs), "with Alt:", sum(1 for f in figs if "/Alt" in f))
# patch: add alt to all figures, set doc lang
for i,f in enumerate(figs):
    f.Alt = pikepdf.String(f"Gambar {i+1}: [deskripsi hasil verifikasi]")
pdf.Root.Lang = pikepdf.String("id-ID")
if "/ViewerPreferences" not in pdf.Root: pdf.Root.ViewerPreferences = pikepdf.Dictionary()
pdf.Root.ViewerPreferences.DisplayDocTitle = True
pdf.save("ifest_patched.pdf")
p2=pikepdf.open("ifest_patched.pdf")
n=0
def w(node,seen2=set()):
    global n
    if isinstance(node,pikepdf.Array):
        for k in node:w(k)
        return
    if not isinstance(node,pikepdf.Dictionary):return
    if node.objgen in seen2:return
    seen2.add(node.objgen)
    if node.get("/S")=="/Figure" and "/Alt" in node:n+=1
    if "/K" in node:w(node.K)
w(p2.Root.StructTreeRoot)
print("after patch, figures with Alt:", n, "| time %.2fs"%(time.time()-t))
