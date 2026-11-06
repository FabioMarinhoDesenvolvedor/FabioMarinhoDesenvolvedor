#!/usr/bin/env python3
"""Generate the profile using public GitHub data only. Python standard library."""
import json, os, urllib.request, time, html, argparse
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
ROOT = Path(__file__).resolve().parents[1]
USER = 'FabioMarinhoDesenvolvedor'
def api(path):
    headers = {'Accept':'application/vnd.github+json','User-Agent':'fabio-profile','X-GitHub-Api-Version':'2022-11-28'}
    if os.getenv('GH_TOKEN'): headers['Authorization'] = 'Bearer '+os.environ['GH_TOKEN']
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request('https://api.github.com'+path,headers=headers), timeout=40) as r: return json.load(r)
        except Exception:
            if attempt == 2: raise
            time.sleep(2**attempt)
def collect():
    user=api('/users/'+USER); repos=[]; page=1
    while True:
        batch=api(f'/users/{USER}/repos?type=owner&per_page=100&page={page}')
        repos.extend(r for r in batch if not r['private'])
        if len(batch)<100: break
        page+=1
    langs=Counter()
    for repo in repos:
        if not repo['fork'] and repo['name'] != USER:
            langs.update(api(f"/repos/{USER}/{repo['name']}/languages"))
    return dict(updated=datetime.now(timezone.utc).strftime('%Y-%m-%d'),repos=len(repos),stars=sum(r['stargazers_count'] for r in repos if not r['fork']),followers=user['followers'],following=user['following'],languages=dict(langs.most_common()))
# Original ASCII sphere: latitude/longitude density, not an external image.
def sphere():
    import math
    lines=[]
    for row in range(27):
        y=(row-13)/13.5; line=''
        for col in range(48):
            x=(col-23.5)/24
            r=x*x+y*y
            if r>1: line+=' '; continue
            z=math.sqrt(1-r)
            longitude=math.atan2(x,z)
            grid=abs(math.sin(longitude*7))<.19 or abs(math.sin(math.asin(y)*9))<.19
            light=max(0,min(1, .25+.55*z-.25*x-.15*y))
            line+=('#' if grid else ' .:-=+*'[min(6,int(light*7))])
        lines.append(line)
    return lines

def render(data, mobile=False):
    w=360 if mobile else 1040; h=1080 if mobile else 770
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">', '<title id="title">Fábio Marinho — Full-Stack Developer</title><desc id="desc">Terminal profile with original ASCII globe, verified technologies and public GitHub statistics.</desc>',f'<rect width="{w}" height="{h}" rx="8" fill="#0c1016"/>',f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="8" fill="none" stroke="#263343"/>','<g font-family="DejaVu Sans Mono, Consolas, monospace" font-size="15" fill="#c9d1dc">']
    def text(x,y,s,color='#c9d1dc',size=15): out.append(f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" xml:space="preserve">{html.escape(str(s))}</text>')
    def line(y): out.append(f'<path d="M24 {y} H{w-24}" stroke="#263343"/>')
    text(24,34,'fabio@github:~$','#7cadd9',16);text(204,34,'fastfetch','#dde6ef',16);line(53)
    if not mobile:
        for i,s in enumerate(sphere()): text(20,112+i*13,s,'#659ac6' if i<19 else '#466680',12)
        text(70,491,'F / M','#d4e1ed',26);text(65,519,'BUILD. SHIP. ITERATE.','#728395',11)
        for i,c in enumerate(['#243445','#436582','#659ac6','#a9bfd3','#4d786b','#7da594']):out.append(f'<rect x="{73+i*32}" y="545" width="32" height="13" fill="{c}"/>')
    x=24 if mobile else 390; y=89
    def row(label,value):
        nonlocal y
        if mobile:
            text(x,y,label,'#7cadd9',13);y+=23;text(x,y,value,size=16);y+=31
        else:
            text(x,y,label,'#7cadd9',14);text(x+135,y,value,size=14);y+=27
    text(x,y,'Fábio Marinho','#edf3fa',23);y+=28
    text(x,y,USER,'#728395',13);y+=39
    row('Role','Full-Stack Developer')
    row('Location','São Paulo, Brazil')
    row('Focus','Web applications / APIs / SaaS')
    y+=7
    row('Languages','TypeScript / JavaScript / Rust')
    row('Frontend','React / Next.js / Vite')
    row('Backend','Node.js / NestJS / Prisma')
    row('Data','PostgreSQL / SQLite')
    row('Tools','Git / Docker / Tauri')
    row('Environment','Linux / Windows')
    y+=11
    text(x,y,'github --public-stats','#7da594',14);y+=29
    row('Repositories',str(data['repos'])+' public')
    row('Stars',str(data['stars'])+' received')
    row('Network',f"{data['followers']} followers / {data['following']} following")
    if mobile:
        # Reflow to a separate readable block, never scale a desktop panel down.
        y+=8
    else:y=623
    text(24,y,'languages --by-code-size','#7da594',14);y+=28
    total=sum(data['languages'].values()); top=list(data['languages'].items())[:4]
    labels=[f'{k} {v/total*100:.1f}%' for k,v in top] if total else ['No language data']
    if mobile:
        for s in labels:text(24,y,s,size=13);y+=23
    else:text(24,y,'   /   '.join(labels),size=13);y+=25
    text(24,y,'Public, non-fork repos · GitHub Linguist bytes','#728395',11);y+=27
    line(y-10);text(24,y+12,f"updated {data['updated']} UTC  /  source: api.github.com",'#728395',10)
    out.append('</g></svg>')
    # Size follows actual content to prevent overflow on mobile.
    return '\n'.join(out).replace(f'height="{h}" viewBox="0 0 {w} {h}"',f'height="{y+32}" viewBox="0 0 {w} {y+32}"').replace(f'height="{h}" rx',f'height="{y+32}" rx').replace(f'height="{h-1}" rx',f'height="{y+31}" rx')
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--offline',action='store_true');args=parser.parse_args()
    (ROOT/'assets').mkdir(exist_ok=True)
    path=ROOT/'assets/stats.json'
    data=json.loads(path.read_text()) if args.offline else collect()
    # Fetch everything successfully before replacing the last known good assets.
    outputs={ROOT/'assets/terminal.svg':render(data),ROOT/'assets/terminal-mobile.svg':render(data,True),path:json.dumps(data,indent=2)+'\n'}
    for path,content in outputs.items():path.write_text(content)
if __name__=='__main__': main()
