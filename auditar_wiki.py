from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import unquote
from collections import Counter
BASE=Path(__file__).resolve().parent
files=list(BASE.rglob('*.html'))
missing=[]; anchors=[]; external=0; internal=0
for f in files:
    soup=BeautifulSoup(f.read_text(encoding='utf-8'), 'html.parser')
    for element in soup.select('[href],script[src],link[href]'):
        target=element.get('href') or element.get('src')
        if not target or target.startswith(('http:','https:','mailto:','data:','javascript:','tel:')):external+=1;continue
        if target.startswith('//'):external+=1;continue
        path,_,fragment=target.partition('#');path=unquote(path.split('?',1)[0]);
        if not path and fragment:
            if not soup.find(id=unquote(fragment)): anchors.append((str(f.relative_to(BASE)),target))
            continue
        if not path:continue
        internal+=1
        dest=(f.parent/path).resolve()
        if not dest.is_relative_to(BASE.resolve()) or not dest.exists():missing.append((str(f.relative_to(BASE)),target));continue
        if fragment and dest.suffix.lower()=='.html':
            target_soup=BeautifulSoup(dest.read_text(encoding='utf-8'),'html.parser')
            if not target_soup.find(id=unquote(fragment)):anchors.append((str(f.relative_to(BASE)),target))
print('páginas_html',len(files),'referências_relativas',internal,'sem_arquivos',len(missing),'sem_âncoras',len(anchors),'externos',external)
for typ,data in [('MISSING',missing),('ANCHOR',anchors)]:
    for row in data[:40]:print(typ,row)
