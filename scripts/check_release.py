"""Fail on stale exported fabrication outputs or BOM/CPL mismatch."""
from pathlib import Path
import json,hashlib,csv,re
P=Path(__file__).resolve().parents[1];errors=[]
for file,digest in json.loads((P/'manufacturing/SHA256.json').read_text()).items():
 if hashlib.sha256((P/file).read_bytes()).hexdigest()!=digest:errors.append('Stale release: '+file)
a=json.loads((P/'analysis/pin-audit.json').read_text());assert a['status']=='PASS'
for file,needles in {'drc.rpt':['Found 0 DRC violations','Found 0 unconnected pads','Found 0 Footprint errors'],'erc.rpt':['Errors 0  Warnings 0']}.items():
 t=(P/'analysis'/file).read_text()
 for s in needles:
  if s not in t:errors.append(file+': '+s)
bom=list(csv.DictReader((P/'manufacturing/BOM-JLCPCB.csv').open()));cpl=list(csv.DictReader((P/'manufacturing/CPL-JLCPCB.csv').open()));refs={r for row in bom for r in row['Designator'].split(',')}
if refs!={r['Designator'] for r in cpl}:errors.append('BOM/CPL reference sets differ')
if len(cpl)!=25:errors.append('Unexpected SMT fitted count')
# Fail if a fabricated hole file or core layer is missing.
names=[p.name for p in (P/'manufacturing/gerbers').iterdir()]
for fragment in ['F_Cu','B_Cu','F_Paste','F_Mask','B_Mask','Edge_Cuts','PTH.drl','NPTH.drl']:
 if not any(fragment in n for n in names):errors.append('Missing manufacturing file '+fragment)
b=(P/'analysis/firmware-build.log').read_text()
if 'Sketch uses' not in b or 'Error during build' in b or 'error:' in b:errors.append('Firmware did not compile')
r={'status':'PASS' if not errors else 'FAIL','native_pin_audit':a['status'],'smts':len(cpl),'bom_groups':len(bom),'hashed_files':len(json.loads((P/'manufacturing/SHA256.json').read_text())),'errors':errors}
(P/'analysis/release-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2));raise SystemExit(bool(errors))
