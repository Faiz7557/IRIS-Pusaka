import re, numpy as np
def delta(T1,T2):  # Pers. (2)
    return float(np.mean([abs(a-b)/max(abs(a),abs(b),1) for a,b in zip(T1,T2)]))
def fnum(desc, T, eps=0.02):  # Pers. (5): angka mana pun yang ada di T
    nums=[float(x.replace(",",".")) for x in re.findall(r"\d+(?:[.,]\d+)?",desc)]
    hit=sum(any(abs(n-t)<=eps*max(abs(t),1) for t in T) for n in nums)
    return hit/len(nums) if nums else 1.0


lab=["Q1","Q2","Q3","Q4"]; T=[40,55,62,48]
good="Nilai tertinggi terjadi pada Q3 sebesar 62."
bad ="Nilai tertinggi terjadi pada Q1 sebesar 62."   # 62 sebenarnya milik Q3
print("   benar  Fnum =",fnum(good,T)); print("   SALAH  Fnum =",fnum(bad,T),"<- lolos gerbang")

print("B. Data berskala kecil (proporsi 0-1): dua ekstraksi sangat berbeda")
T1=[0.12,0.31,0.27]; T2=[0.20,0.25,0.35]   # selisih relatif per titik ~ 30-65%
print("   delta =",round(delta(T1,T2),3),"(ambang tipikal 0,05-0,10 -> LOLOS meski ekstraksi tidak konsisten)")
T1p=[x*100 for x in T1]; T2p=[x*100 for x in T2]
print("   data sama dalam persen: delta =",round(delta(T1p,T2p),3),"-> gerbang bergantung SKALA satuan, bukan ketepatan")
print("   Fnum: deskripsi '0,31' vs T=[0.12,0.31,0.27] tetapi klaim '0,34':",fnum("naik menjadi 0,34",[0.12,0.31,0.27]),"(eps=0.02 -> 0,34 dianggap cocok dengan 0,31? )")

print("C. Kesalahan SISTEMATIK (mis. salah baca skala sumbu, x10) pada kedua ekstraksi")
Ttrue=[40,55,62,48]; Tm=[x*10 for x in Ttrue]
print("   delta antar-ekstraksi =",delta(Tm,Tm),"; Fnum =",fnum("Tertinggi 620 pada Q3.",Tm),"-> lolos, padahal salah 10x")
