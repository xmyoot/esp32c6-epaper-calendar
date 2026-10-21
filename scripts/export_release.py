"""Export the final native board; all fabrication and placement data share its origin."""
from pathlib import Path
import subprocess,json,csv,hashlib,zipfile,collections,os
P=Path(__file__).resolve().parents[1];cli=os.environ.get('KICAD_CLI','/Users/hector/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli');hw=P/'hardware/EPD_C6_RevA.kicad_pcb';sch=P/'hardware/EPD_C6_RevA.kicad_sch';m=P/'manufacturing';(m/'gerbers').mkdir(parents=True,exist_ok=True)
def run(*args):
 r=subprocess.run([cli,*map(str,args)],capture_output=True,text=True);(P/'analysis/export-release.log').open('a').write(r.stdout+r.stderr);r.check_returncode()
run('pcb','export','gerbers',hw,'--output',m/'gerbers','--layers','F.Cu,B.Cu,F.Paste,F.Silkscreen,B.Silkscreen,F.Mask,B.Mask,Edge.Cuts','--use-drill-file-origin','--subtract-soldermask','--check-zones')
run('pcb','export','drill',hw,'--output',m/'gerbers','--drill-origin','plot','--excellon-units','mm','--excellon-separate-th','--generate-report','--report-path',m/'drill-report.txt')
run('sch','export','pdf',sch,'--output',P/'docs/EPD_C6_RevA-schematic.pdf')
run('pcb','export','pdf',hw,'--output',P/'docs/EPD_C6_RevA-assembly.pdf','--layers','F.Fab,F.Silkscreen','--common-layers','Edge.Cuts','--mode-multipage','--black-and-white','--scale','0','--sketch-pads-on-fab-layers')
run('pcb','export','svg',hw,'--output',P/'docs/board-svg','--layers','F.Cu,B.Cu,F.Silkscreen,Edge.Cuts')
parts=json.loads((P/'hardware/design.json').read_text())['parts'];groups=collections.defaultdict(list)
for p in parts:
 if p['lcsc']:groups[(p['value'],p['footprint'].split(':')[1],p['lcsc'],p['mpn'],p['manufacturer'])].append(p['ref'])
with (m/'BOM-JLCPCB.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['Comment','Designator','Footprint','LCSC Part #','MPN','Manufacturer'])
 for key,refs in groups.items():w.writerow([key[0],','.join(refs),*key[1:]])
with (P/'bom/BOM-engineering.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['Reference','Value','Footprint','MPN','Manufacturer','LCSC','Assembly','Notes'])
 for p in parts:
  w.writerow([p['ref'],p['value'],p['footprint'],p['mpn'],p['manufacturer'],p['lcsc'],'SMT' if p['lcsc'] else 'Hand fit' if p['ref'] in ['J1','J2'] else 'PCB feature',p['notes']])
# Use measured native footprint positions, rather than regenerating positions from a plan.
board=json.loads((P/'analysis/native-board.json').read_text())
with (m/'CPL-JLCPCB.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['Designator','Mid X','Mid Y','Layer','Rotation'])
 for p in parts:
  if not p['lcsc']:continue
  a=board['footprints'][p['ref']];w.writerow([p['ref'],f"{a['x']-100:.4f}mm",f"{150-a['y']:.4f}mm",'top',f"{a['rotation']%360:.1f}"])
with zipfile.ZipFile(m/'EPD_C6_RevA-fabrication.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted((m/'gerbers').iterdir()):z.write(p,p.name)
manifest={str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [hw,sch,P/'hardware/EPD_C6_RevA.kicad_pro',*(m/'gerbers').glob('*'),m/'BOM-JLCPCB.csv',m/'CPL-JLCPCB.csv'] if p.is_file()}
(m/'SHA256.json').write_text(json.dumps(manifest,indent=2))
print('Release exported:',len(groups),'SMT BOM lines')
