import pikepdf, collections, json, glob, sys
for f in glob.glob("odl/*_tagged.pdf"):
    pdf=pikepdf.open(f)
    r=pdf.Root
    print("\n==",f[4:40], "| pages",len(pdf.pages))
    print("Marked:", r.get("/MarkInfo"), "| Lang:", r.get("/Lang"), "| has StructTreeRoot:", "/StructTreeRoot" in r, "| Title:", pdf.docinfo.get("/Title"))
    if "/StructTreeRoot" not in r: continue
    cnt=collections.Counter(); alt=0; seen=set(); th=0; figs=0
    def w(n):
        global alt,th,figs
        if isinstance(n,pikepdf.Array):
            for k in n:w(k)
            return
        if not isinstance(n,pikepdf.Dictionary):return
        if n.objgen in seen and n.objgen!=(0,0):return
        seen.add(n.objgen)
        s=n.get("/S")
        if s is not None:
            cnt[str(s)]+=1
            if s=="/Figure":
                figs+=1
                if "/Alt" in n: alt+=1
        if "/K" in n:w(n.K)
    w(r.StructTreeRoot)
    print(dict(cnt.most_common(12)))
    print("Figure:",figs,"Alt:",alt)
for f in glob.glob("odl/*.json"):
    j=json.load(open(f,encoding="utf-8"))
    kids=j.get("kids",[])
    c=collections.Counter(k.get("type") for k in kids)
    print("\nJSON",f[4:30],"top-level types:",dict(c), "| keys:",list(j.keys())[:8])
    for k in kids:
        if k.get("type") in ("image","picture","figure"):
            print("  sample image node:",{a:k[a] for a in list(k)[:8]}); break
