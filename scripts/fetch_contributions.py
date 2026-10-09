"""Fetch the public GitHub calendar; keep previous data if upstream is invalid."""
from html.parser import HTMLParser
from pathlib import Path
from datetime import datetime, timezone, date
from urllib.request import Request, urlopen
import json,re
class Calendar(HTMLParser):
    def __init__(self):super().__init__();self.cells={};self.labels={};self.target=None
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='td' and 'data-date' in a:
            self.cells[a['id']]={'date':a['data-date'],'level':int(a['data-level'])}
        if tag=='tool-tip':self.target=a.get('for');self.labels[self.target]=''
    def handle_data(self,data):
        if self.target:self.labels[self.target]+=data
    def handle_endtag(self,tag):
        if tag=='tool-tip':self.target=None
r=Request('https://github.com/users/yMScorpion/contributions',headers={'User-Agent':'builder-profile-calendar'})
p=Calendar();p.feed(urlopen(r,timeout=30).read().decode())
days=[]
for id,cell in p.cells.items():
    label=p.labels.get(id,'').strip()
    m=re.match(r'([\d,]+) contributions? on ',label)
    if m:count=int(m[1].replace(',',''))
    elif label.startswith('No contributions on '):count=0
    else:raise ValueError('Unknown calendar count format; preserving previous output')
    date.fromisoformat(cell['date'])
    if not 0<=cell['level']<=4:raise ValueError('Invalid level')
    days.append({**cell,'count':count})
days.sort(key=lambda d:d['date'])
if len(days)<350 or len({d['date'] for d in days})!=len(days):raise ValueError('Incomplete calendar')
for a,b in zip(days,days[1:]):
    if (date.fromisoformat(b['date'])-date.fromisoformat(a['date'])).days!=1:raise ValueError('Non-contiguous calendar')
R=Path(__file__).resolve().parents[1];out=R/'data/contributions.json';out.parent.mkdir(exist_ok=True)
result={'updated':datetime.now(timezone.utc).strftime('%Y-%m-%d UTC'),'total':sum(d['count'] for d in days),'days':days}
out.write_text(json.dumps(result,indent=2)+'\n')
print(f'Validated {len(days)} days, {result["total"]} contributions')
