import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np, io, torch
from PIL import Image
from torchmetrics.functional import structural_similarity_index_measure as ssim

def render(tex, fontset, dpi=200):
    plt.rcParams["mathtext.fontset"]=fontset
    fig=plt.figure(figsize=(4,1)); fig.text(0.02,0.5,f"${tex}$",fontsize=28,va="center")
    b=io.BytesIO(); fig.savefig(b,format="png",dpi=dpi,facecolor="white"); plt.close(fig)
    return Image.open(b).convert("L")

def norm(im, H=64, W=320):
    a=np.array(im); m=a<200
    ys,xs=np.where(m); a=a[ys.min():ys.max()+1, xs.min():xs.max()+1]
    im=Image.fromarray(a); w=max(1,int(im.width*H/im.height)); im=im.resize((min(w,W),H),Image.LANCZOS)
    c=Image.new("L",(W,H),255); c.paste(im,(0,0))
    return torch.tensor(np.array(c),dtype=torch.float32)[None,None]/255

def S(a,b): return float(ssim(a,b,data_range=1.0))

cases=[
 (r"\frac{a+b}{c}",           r"\frac{a-b}{c}"),
 (r"\sum_{i=1}^{n} x_i^{2}",  r"\sum_{i=1}^{n} x_i^{3}"),
 (r"\int_{0}^{1} x^{2}\,dx",  r"\int_{0}^{2} x^{2}\,dx"),
 (r"\hat{\beta}=\frac{\sum (x_i-\bar{x})(y_i-\bar{y})}{\sum (x_i-\bar{x})^{2}}",
  r"\hat{\beta}=\frac{\sum (x_i-\bar{x})(y_i-\bar{y})}{\sum (x_i+\bar{x})^{2}}"),
 (r"\sqrt{x^{2}+y^{2}}",      r"\sqrt{x^{2}-y^{2}}"),
]
print(f"{'formula':32s} {'benar,font beda':>16s} {'SALAH,font sama':>16s} {'SALAH,font beda':>16s}")
ok=0
for good,bad in cases:
    orig=norm(render(good,"dejavusans"))          # 'dokumen asli' (font A)
    cand_ok=norm(render(good,"cm"))               # rumus BENAR dirender ulang (font B)
    cand_bad_same=norm(render(bad,"dejavusans"))  # rumus SALAH, font sama dengan asli
    cand_bad_diff=norm(render(bad,"cm"))          # rumus SALAH, font beda
    a,b,c=S(orig,cand_ok),S(orig,cand_bad_same),S(orig,cand_bad_diff)
    ok+= a>b
    print(f"{good[:30]:32s} {a:16.3f} {b:16.3f} {c:16.3f}")
