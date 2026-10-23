import pikepdf, sys
def finish(src, dst, title, lang="id-ID", alt="Gambar (deskripsi terverifikasi)"):
    pdf=pikepdf.open(src); seen=set(); n=0
    def w(x):
        nonlocal n
        if isinstance(x,pikepdf.Array):
            for k in x:w(k)
            return
        if not isinstance(x,pikepdf.Dictionary) or x.objgen in seen:return
        seen.add(x.objgen)
        if x.get("/S")=="/Figure": n+=1; x.Alt=pikepdf.String(alt)
        if "/K" in x:w(x.K)
    if "/StructTreeRoot" in pdf.Root: w(pdf.Root.StructTreeRoot)
    pdf.Root.MarkInfo=pikepdf.Dictionary(Marked=True)
    pdf.Root.Lang=pikepdf.String(lang)
    pdf.Root.ViewerPreferences=pikepdf.Dictionary(DisplayDocTitle=True)
    for p in pdf.pages: p.Tabs=pikepdf.Name.S
    pdf.docinfo["/Title"]=title
    with pdf.open_metadata(set_pikepdf_as_editor=False) as m:
        m.register_xml_namespace("http://www.aiim.org/pdfua/ns/id/","pdfuaid")
        m["dc:title"]=title; m["pdfuaid:part"]="1"
    pdf.save(dst); return n
if __name__=="__main__":
    print(finish(*sys.argv[1:4]))
