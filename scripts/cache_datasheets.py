import json,requests,subprocess,time
from pathlib import Path
D=json.load(open('analysis/lcsc-detail.json'))
for code,r in D.items():
 if not r or code in ['C106237','C11702','C25769','C17168']:continue
 p=Path('datasheets')/(code+'.pdf')
 if not p.exists():
  try:
   a=requests.get(r['pdfUrl'],timeout=30);a.raise_for_status();assert a.content[:4]==b'%PDF';p.write_bytes(a.content)
  except Exception as e: print(code,e,flush=True);continue
 subprocess.run(['pdftotext','-layout',str(p),str(p.with_suffix('.txt'))],stderr=subprocess.DEVNULL)
 print(code,p.stat().st_size,flush=True);time.sleep(.5)
