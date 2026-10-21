"""Cache LCSC data and manufacturer PDF evidence; stock is a dated snapshot."""
import json,time,urllib.request,subprocess
from pathlib import Path
codes=['C202112','C3289597','C503307','C77102','C77083','C77336','C1525','C17168','C11702','C25769','C25741','C106237','C17477']
out={}
for code in codes:
 try:
  u='https://wmsc.lcsc.com/ftps/wm/product/detail?productCode='+code
  req=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'})
  d=json.load(urllib.request.urlopen(req,timeout=30));r=d.get('result') or {};out[code]=r
  print(code,r.get('productModel'),r.get('encapStandard'),r.get('stockNumber'),flush=True)
  if r.get('pdfUrl'):
   p=Path('datasheets')/(code+'.pdf');urllib.request.urlretrieve(r['pdfUrl'],p)
   subprocess.run(['pdftotext','-layout',str(p),str(p.with_suffix('.txt'))],stderr=subprocess.DEVNULL)
 except Exception as e:print(code,e,flush=True)
 time.sleep(.5)
 Path('analysis/lcsc-detail.json').write_text(json.dumps(out,indent=2))
