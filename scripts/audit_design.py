"""Independent expected physical mappings checked against native netlist + PCB."""
import json,sexpdata as s
from pathlib import Path
P=Path(__file__).resolve().parents[1]
def tag(x,n):return isinstance(x,list) and x and str(x[0])==n
def child(x,n):return next(y for y in x if tag(y,n))
def field(x,n):return str(child(x,n)[1])
d=s.loads((P/'analysis/schematic.net').read_text());actual={}
for net in child(d,'nets')[1:]:
 name=field(net,'name').removeprefix('/')
 for node in net:
  if tag(node,'node'):actual[(field(node,'ref'),field(node,'pin'))]=name
# This table is transcribed separately from panel datasheet p8/p40 and Seeed's native U2.
fpc={2:'GDR',3:'RESE',5:'VSHR',8:'GND',9:'EPD_BUSY_N',10:'EPD_RST_N',11:'EPD_DC',12:'EPD_CS_N',13:'EPD_SCK',14:'EPD_MOSI',15:'3V3_EPD',16:'3V3_EPD',17:'GND',18:'VDD_INT',20:'VSH1',21:'PREVGH',22:'VSL',23:'PREVGL',24:'VCOM','MP':'GND'}
expect={('J3',str(k)):v for k,v in fpc.items()}
for ref,nets in {'J1':{1:'EPD_CS_N',2:'EPD_DC',3:'EPD_RST_N',4:'EPD_BUSY_N'},'J2':{2:'GND',3:'3V3_MODULE',4:'MOSI_SRC',6:'SCK_SRC'},'Q1':{1:'GDR',2:'RESE',3:'SW'},'D1':{1:'PREVGH',2:'SW'},'D2':{1:'GND',2:'PUMP'},'D3':{1:'PUMP',2:'PREVGL'}}.items():expect.update({(ref,str(k)):v for k,v in nets.items()})
errors=[]
for (ref,pin),net in expect.items():
 if actual.get((ref,pin))!=net:errors.append(f'{ref}.{pin}: netlist {actual.get((ref,pin))}, expected {net}')
b=json.loads((P/'analysis/native-board.json').read_text());parts=json.loads((P/'hardware/design.json').read_text())['parts']
for p in parts:
 f=b['footprints'].get(p['ref'])
 if not f:errors.append('Missing footprint '+p['ref']);continue
 for num,expected in p['nets'].items():
  found=(f['pads'].get(num,{}).get('net') or '').removeprefix('/') or None
  if found!=expected:errors.append(f"PCB {p['ref']}.{num}: {found} != {expected}")
  if expected and actual.get((p['ref'],num))!=expected:errors.append(f"Schematic {p['ref']}.{num}: {actual.get((p['ref'],num))} != {expected}")
 if f['path']!='/'+json.loads((P/'hardware/design.json').read_text())['root_uuid']+'/'+p['uuid']:errors.append('Schematic path mismatch '+p['ref'])
# Deliberately unused panel contacts must remain isolated in both representations.
for pin in [1,4,6,7,19]:
 if actual.get(('J3',str(pin)),'').startswith('unconnected-'):continue
 if ('J3',str(pin)) in actual:errors.append('Unexpected panel NC connection '+str(pin))
# Check clock series resistor and the isolated internal VDD node.
for ref,nets in {'R2':{1:'SCK_SRC',2:'EPD_SCK'},'R3':{1:'MOSI_SRC',2:'EPD_MOSI'},'C6':{1:'VDD_INT',2:'GND'}}.items():
 for n,net in nets.items():
  if actual.get((ref,str(n)))!=net:errors.append(f'{ref}.{n} expected {net}')
if set(b['footprints'])!={p['ref'] for p in parts}:errors.append('Footprint set differs from design')
result={'status':'PASS' if not errors else 'FAIL','footprints':len(b['footprints']),'critical_pin_checks':len(expect),'all_design_pin_checks':sum(len(p['nets']) for p in parts),'errors':errors,'basis':'Native KiCad exported netlist and pcbnew pad data; physical tables transcribed from source documents. Not a bench test.'}
(P/'analysis/pin-audit.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));raise SystemExit(bool(errors))
