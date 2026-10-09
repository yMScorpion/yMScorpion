"""Render reproducible, self-contained profile artwork (no remote assets)."""
from pathlib import Path
from html import escape
import json, sys
R=Path(__file__).resolve().parents[1]
A=R/'assets'; A.mkdir(exist_ok=True)
BG='#101412'; FG='#f4f2e9'; LIME='#a3e635'; MUTED='#aeb8af'
STYLE='''<style>text{font-family:Arial,sans-serif}.mono{font-family:monospace}.reveal{animation:reveal 1.8s ease-out both}@keyframes reveal{from{opacity:0;transform:translateY(9px)}to{opacity:1;transform:translateY(0)}}.draw{stroke-dasharray:1400;stroke-dashoffset:1400;animation:draw 2s ease-out forwards}@keyframes draw{to{stroke-dashoffset:0}}@media(prefers-reduced-motion:reduce){.reveal,.draw{animation:none;opacity:1;stroke-dashoffset:0}}</style>'''
def svg(name,w,h,body,animated=True):
    style=STYLE if animated else '<style>text{font-family:Arial,sans-serif}.mono{font-family:monospace}</style>'
    (A/name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{escape(name.replace(".svg","").replace("-"," "))}</title>{style}<rect width="{w}" height="{h}" rx="16" fill="{BG}"/>{body}</svg>')
def text(x,y,t,size=16,color=FG,cls='',extra=''):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" class="{cls}" {extra}>{escape(t)}</text>'
def banner():
    body=''.join(f'<path d="M{x} 0V300" stroke="#263125" stroke-width=".5"/>' for x in range(32,961,48))
    body+=''.join(f'<path d="M0 {y}H960" stroke="#263125" stroke-width=".5"/>' for y in range(30,300,48))
    body+=text(38,40,'iv_',27,LIME,'mono')+text(105,39,'CHAPTER 00 / THE BUILDER',11,MUTED,'mono')
    body+='<path class="draw" d="M625 257L694 196L770 228L880 143L808 103L694 196V107L766 59L880 103V143M694 107L770 145L880 103M770 145V228" fill="none" stroke="#a3e635" stroke-width="1.5"/>'
    body+='<g class="reveal">'+text(38,110,'Behind every line of code,',35)+text(38,157,'there is a builder.',42,LIME)+text(38,214,'ISAAC VALERIANO',15,FG,'mono')+text(38,248,'Back-End Software Engineer · Applied AI & Cloud',15,MUTED)+'</g>'
    svg('builder-banner.svg',960,300,body);svg('builder-banner-static.svg',960,300,body,False)
    mobile=text(25,35,'iv_ / THE BUILDER',15,LIME,'mono')
    mobile+='<g class="reveal">'+text(25,105,'Behind every line',32)+text(25,149,'of code, there',32)+text(25,193,'is a builder.',38,LIME)+text(25,250,'ISAAC VALERIANO',14,FG,'mono')+text(25,278,'Back-End · Applied AI · Cloud',15,MUTED)+'</g>'
    svg('builder-banner-mobile.svg',480,310,mobile)
def identity(photo):
    from PIL import Image, ImageOps, ImageEnhance
    im=Image.open(photo).convert('RGB')
    # Face/shoulder crop of the approved portrait. Lime background becomes blank.
    im=im.crop((220,160,950,940)).resize((68,51))
    gray=ImageEnhance.Contrast(ImageOps.grayscale(im)).enhance(1.35)
    ramp='@%#*+=-:. '
    body=text(30,34,'01 / WHO BUILDS',11,LIME,'mono')
    for y in range(51):
        chars=''
        for x in range(68):
            r,g,b=im.getpixel((x,y)); v=gray.getpixel((x,y))
            chars+=' ' if g>r*1.25 and g>b*1.3 else ramp[min(9,int(v/256*10))]
        body+=text(26,61+y*6.5,chars,6.7,FG,'mono reveal',f'xml:space="preserve" style="animation-delay:{y*.016:.3f}s"')
    body+='<path d="M430 50V370" stroke="#334032"/>'
    body+=text(470,70,'isaac@builders-world',18,LIME,'mono')
    rows=[('focus','Back-End / Applied AI / Cloud'),('core','Go · Python · PostgreSQL'),('experience','DIT / IFAL — Backend'),('education','Economics + Data Science'),('location','Brazil'),('work','100% remote · Global teams'),('languages','Portuguese · Advanced English')]
    for i,(k,v) in enumerate(rows):
        body+=f'<g class="reveal" style="animation-delay:{.25+i*.1}s">'+text(470,116+i*33,k,12,MUTED,'mono')+text(577,116+i*33,v,13,FG,'mono')+'</g>'
    body+=text(470,382,'BUILD / TEST / UNDERSTAND / EVOLVE',10,LIME,'mono')
    svg('builder-identity.svg',960,420,body);svg('builder-identity-static.svg',960,420,body,False)
    # Portrait above the info card on narrow screens; no tiny desktop text.
    import re
    portrait=body.split('<path d="M430')[0]
    mobile=portrait+'<path d="M26 407H454" stroke="#334032"/>'+text(26,447,'isaac@builders-world',18,LIME,'mono')
    for i,(k,v) in enumerate(rows):
        mobile+=text(26,484+i*31,k,11,MUTED,'mono')+text(132,484+i*31,v,12,FG,'mono')
    svg('builder-identity-mobile.svg',480,710,mobile)
def cards():
    cards=[('01','STRUCTURE','EduRepo','Knowledge, versioned and traceable.','Next.js · TypeScript · PostgreSQL'),('02','INTELLIGENCE','StratHUB','Documents into validated specifications.','Python · FastAPI · LLMs · JSON Schema'),('03','SYSTEMS','Argus','Events, state and deterministic replay.','Rust · Order books · BLAKE3'),('04','INTEGRATION','AIBE','Task routing and agent coordination.','Python · FastAPI · SQLAlchemy'),('05','ORCHESTRATION','MERCURY','Feeds, risk and reconciliation.','Rust · Tokio · SQLite')]
    for n,label,name,desc,stack in cards:
        body=text(28,34,n+' / '+label,11,LIME,'mono')+text(28,83,name,28)+text(28,122,desc,13,MUTED)+text(28,162,stack,11,LIME,'mono')
        body+='<path d="M360 45H408V92M360 92L408 45" fill="none" stroke="#a3e635" stroke-width="1.2"/>'
        svg('project-'+n+'.svg',460,190,body,False)
def heatmap():
    d=json.loads((R/'data/contributions.json').read_text()); days=d['days']; cols=(len(days)+6)//7
    palette=['#202a22','#354c26','#53742c','#79ad30',LIME]
    body=text(30,34,'06 / CONSTRUCTION ACTIVITY',11,LIME,'mono')
    for i,day in enumerate(days):
        col=i//7; row=i%7
        body+=f'<rect class="reveal" x="{30+col*16}" y="{61+row*16}" width="11" height="11" rx="2" fill="{palette[day["level"]]}" style="animation-delay:{(col+row)*.012:.3f}s"><title>{day["date"]}: {day["count"]} contributions</title></rect>'
    body+=text(30,210,f'{d["total"]:,} contributions · {days[0]["date"]} → {days[-1]["date"]}',14)
    body+=text(30,240,'Public GitHub calendar · updated '+d['updated'],11,MUTED,'mono')
    body+=text(780,210,'LESS',9,MUTED,'mono')
    for i,c in enumerate(palette):body+=f'<rect x="{816+i*16}" y="199" width="11" height="11" rx="2" fill="{c}"/>'
    svg('construction-activity.svg',960,270,body);svg('construction-activity-static.svg',960,270,body,False)
if __name__=='__main__':
    if '--heatmap-only' not in sys.argv:
        banner(); identity(sys.argv[1]);cards()
    heatmap()
