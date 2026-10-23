"""Buat ilustrasi SVG orisinal untuk SIMAK, tanpa gambar eksternal."""
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / 'web/assets'
OUT.mkdir(exist_ok=True)
INK, PAPER, ORANGE, VIOLET, SAGE, TAUPE = '#0b0a0a', '#fffaf0', '#cf6224', '#5a3cd4', '#80a89b', '#bca59d'

def svg(name, body, bg=TAUPE, view='0 0 900 1100'):
    (OUT / name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view}"><rect width="100%" height="100%" fill="{bg}"/>{body}</svg>', encoding='utf-8')

page = f'''<g stroke="{INK}" stroke-width="8" stroke-linejoin="round">
<path d="M168 225h410l132 132v560H168z" fill="{PAPER}"/>
<path d="M578 225v132h132" fill="{SAGE}"/>
<path d="M230 430h300M230 467h210M230 754h390M230 796h320M230 838h355" fill="none" stroke-width="14"/>
<path d="M234 674V553h70v121m33 0V514h70v160m33 0V584h70v90m33 0V484h70v190" fill="{VIOLET}"/>
<path d="M222 680h410" fill="none"/>
</g>'''
svg('material.svg', f'''<path d="M-40 960C170 620 520 1210 955 723v420H-40z" fill="{SAGE}"/>
<circle cx="735" cy="153" r="104" fill="{ORANGE}"/>
<g transform="translate(-28 -32) rotate(-9 450 550)"><path d="M161 259h525v662H161z" fill="{VIOLET}" stroke="{INK}" stroke-width="8"/></g>
<g transform="rotate(7 450 550)">{page}</g>
<g fill="none" stroke="{INK}" stroke-width="19" stroke-linecap="round"><path d="M645 719v-76a120 120 0 0 1 240 0v76"/><rect x="628" y="690" width="48" height="116" rx="20" fill="{ORANGE}"/><rect x="854" y="690" width="48" height="116" rx="20" fill="{ORANGE}"/><path d="M878 811v92q0 45-45 45H693q-86 0-86 84"/></g>''')
svg('reading.svg', f'''<circle cx="700" cy="240" r="220" fill="{ORANGE}"/><path d="M-70 900L900 480v620H-70z" fill="{SAGE}"/><g transform="rotate(-10 450 550)">{page}</g>''', bg=SAGE)
waves = ''.join(f'<path d="M{x} {550-h/2}v{h}"/>' for x,h in zip(range(180,761,48),[90,160,290,400,210,490,360,200,420,285,150,80,40]))
svg('listening.svg', f'''<circle cx="450" cy="500" r="320" fill="{PAPER}"/><g stroke="{INK}" stroke-width="21" stroke-linecap="round" fill="none">{waves}<path d="M175 510V383a275 275 0 0 1 550 0v127"/><rect x="141" y="460" width="65" height="195" rx="27" fill="{ORANGE}"/><rect x="694" y="460" width="65" height="195" rx="27" fill="{ORANGE}"/><path d="M728 663v97q0 75-75 75H415q-130 0-130 173"/></g>''', bg=VIOLET)
svg('evidence.svg', f'''<g transform="rotate(5 450 550)"><rect x="105" y="165" width="690" height="770" rx="2" fill="{PAPER}" stroke="{INK}" stroke-width="8"/>
<path d="M160 240h330M160 280h230" fill="none" stroke="{INK}" stroke-width="17"/>
<path d="M165 530V365h100v165m63 0V410h100v120m63 0V328h100v202m63 0V380h76v150" fill="{ORANGE}" stroke="{INK}" stroke-width="7"/>
<rect x="160" y="600" width="575" height="100" fill="{SAGE}"/>
<g stroke="{INK}" stroke-width="8"><path d="M160 600h575M160 700h575M160 780h575M160 860h575M410 600v260"/><path d="M190 650h120m145 0h180M190 744h120m145 0h180M190 824h120m145 0h180" stroke-width="13"/></g></g>
<circle cx="744" cy="901" r="98" fill="{VIOLET}" stroke="{INK}" stroke-width="8"/><path d="M696 904l33 33 67-74" fill="none" stroke="{PAPER}" stroke-width="14" stroke-linecap="round"/>''', bg=ORANGE)
for i,(bg,glyph) in enumerate([(TAUPE,'document'),(ORANGE,'structure'),(VIOLET,'data'),(SAGE,'check'),(TAUPE,'review'),(ORANGE,'output')]):
    if glyph == 'check':
        art=f'<circle cx="450" cy="560" r="245" fill="{PAPER}" stroke="{INK}" stroke-width="9"/><path d="M315 565l95 95 200-224" fill="none" stroke="{INK}" stroke-width="35" stroke-linecap="round"/>'
    elif glyph == 'review':
        art=page+f'<path d="M527 756l180-190 76 74-182 190-109 35z" fill="{ORANGE}" stroke="{INK}" stroke-width="9"/>'
    elif glyph == 'data':
        art=f'<rect x="130" y="260" width="640" height="580" fill="{PAPER}" stroke="{INK}" stroke-width="9"/><g stroke="{INK}" stroke-width="9"><path d="M130 410h640M130 555h640M130 700h640M350 260v580"/><path d="M176 340h115m130 0h250M176 485h115m130 0h250M176 630h115m130 0h250M176 775h115m130 0h250" stroke-width="16"/></g>'
    elif glyph == 'structure':
        art=''.join(f'<rect x="{x}" y="{y}" width="230" height="170" fill="{PAPER if j%2==0 else SAGE}" stroke="{INK}" stroke-width="9"/>' for j,(x,y) in enumerate([(150,230),(520,230),(150,650),(520,650)]))+f'<path d="M265 400v250m370-250v250M380 315h140M380 735h140" stroke="{INK}" stroke-width="15"/>'
    elif glyph == 'output':
        art=f'<rect x="135" y="220" width="630" height="680" fill="{PAPER}" stroke="{INK}" stroke-width="9"/><path d="M135 345h630" stroke="{INK}" stroke-width="9"/><circle cx="195" cy="282" r="15" fill="{VIOLET}"/><circle cx="250" cy="282" r="15" fill="{SAGE}"/><path d="M240 430h390M240 485h260M240 540h340" stroke="{INK}" stroke-width="18"/><path d="M378 630l150 90-150 90z" fill="{VIOLET}" stroke="{INK}" stroke-width="9"/>'
    else:
        art=page
    svg(f'step-{i+1}.svg',art,bg)
print('10 ilustrasi SVG lokal siap.')
