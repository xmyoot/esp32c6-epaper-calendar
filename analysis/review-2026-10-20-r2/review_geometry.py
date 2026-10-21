"""Extract critical routed geometry from the current full kicad-happy output."""
from pathlib import Path
import json
p=Path(__file__).resolve().parent
b=json.loads((p/'pcb.json').read_text())
names=['/GDR','/RESE','/SW','/PUMP','/EPD_SCK','/EPD_MOSI','/SCK_SRC','/MOSI_SRC']
r={'critical_nets':[{k:n[k] for k in ['net','total_length_mm','via_count']} for n in b['net_lengths'] if n['net'] in names], 'keepout_zones':b['keepout_zones'],'ground_fills':[{'layers':z['layers'],'filled':z.get('is_filled'),'fill_ratio':z.get('fill_ratio')} for z in b['zones'] if z['net']==10]}
(p/'review-geometry.json').write_text(json.dumps(r,indent=2))
print(json.dumps(r,indent=2))
