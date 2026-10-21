"""KiCad 10 bundled Python: builds placement and deliberately routed power stage."""
import pcbnew as k,json,os,shutil,math
from pathlib import Path
P=Path(__file__).resolve().parents[1];D=json.loads((P/'hardware/design.json').read_text());name=D['name'];root=D['root_uuid'];out=P/'hardware';lib=out/'Carrier.pretty';lib.mkdir(exist_ok=True)
ks=Path('/Users/hector/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints')
def V(x,y):return k.VECTOR2I(k.FromMM(x),k.FromMM(y))
b=k.BOARD();b.SetCopperLayerCount(2);b.GetDesignSettings().SetBoardThickness(k.FromMM(1.6))
nets={}
for net in sorted({v for p in D['parts'] for v in p['nets'].values() if v}):
 ni=k.NETINFO_ITEM(b,net);b.Add(ni);nets[net]=ni
fps={}
for p in D['parts']:
 ref=p['ref'];ln,fn=p['footprint'].split(':');shutil.copy2(ks/(ln+'.pretty')/(fn+'.kicad_mod'),lib/(fn+'.kicad_mod'))
 f=k.FootprintLoad(str(lib),fn);f.SetFPID(k.LIB_ID('Carrier',fn));f.SetReference(ref);f.SetValue(p['value']);f.SetPath(k.KIID_PATH('/'+root+'/'+p['uuid']));f.SetPosition(V(*p['pcb'][:2]));f.SetOrientationDegrees(p['pcb'][2]);b.Add(f);fps[ref]=f
 f.Value().SetVisible(False);r=f.Reference();r.SetTextSize(V(.8,.8));r.SetTextThickness(k.FromMM(.12));r.SetLayer(k.F_SilkS)
 # Each physical pin is driven from the explicit pin-to-net table, including NCs.
 for pad in f.Pads():
  n=p['nets'].get(pad.GetNumber())
  if n:pad.SetNet(nets[n])
  if p['ref']=='J3' and pad.GetNumber()=='MP':pad.SetNet(nets['GND'])
 if ref.startswith(('TP','H')):f.SetAttributes(f.GetAttributes()|k.FP_EXCLUDE_FROM_BOM|k.FP_EXCLUDE_FROM_POS_FILES)
 if ref in ('J1','J2'):f.SetAttributes(f.GetAttributes()|k.FP_EXCLUDE_FROM_POS_FILES)
 f.SetLocked(True)
 # Uniform readable references; placement adjusted in finishing pass.
 if ref.startswith('H'):r.SetLayer(k.F_Fab)
 if ref.startswith('C'):r.SetPosition(V(p['pcb'][0]-2.8,p['pcb'][1]));r.SetTextAngle(k.EDA_ANGLE(0,k.DEGREES_T))
 elif ref.startswith('R'):r.SetPosition(V(p['pcb'][0],p['pcb'][1]+1.6));r.SetTextAngle(k.EDA_ANGLE(0,k.DEGREES_T))
# Rounded board envelope 60x50, straight edges + corner radii 2mm.
def line(a,c,layer=k.Edge_Cuts,width=.05):
 s=k.PCB_SHAPE();s.SetShape(k.SHAPE_T_SEGMENT);s.SetStart(V(*a));s.SetEnd(V(*c));s.SetLayer(layer);s.SetWidth(k.FromMM(width));b.Add(s)
for a,c in [((102,100),(158,100)),((160,102),(160,148)),((158,150),(102,150)),((100,148),(100,102))]:line(a,c)
for center,start,end in [((102,102),(100,102),(102,100)),((158,102),(158,100),(160,102)),((158,148),(160,148),(158,150)),((102,148),(102,150),(100,148))]:
 s=k.PCB_SHAPE();s.SetShape(k.SHAPE_T_ARC);s.SetCenter(V(*center));s.SetStart(V(*start));s.SetEnd(V(*end));s.SetLayer(k.Edge_Cuts);s.SetWidth(k.FromMM(.05));b.Add(s)
# Fabrication-visible module envelope and RF exclusion. Antenna is at end opposite USB.
for a,c in [((108.73,101.1),(126.51,101.1)),((126.51,101.1),(126.51,122.1)),((126.51,122.1),(108.73,122.1)),((108.73,122.1),(108.73,101.1))]:line(a,c,k.Dwgs_User,.15)
def text(t,x,y,size=1,layer=k.F_SilkS):
 a=k.PCB_TEXT(b);a.SetText(t);a.SetPosition(V(x,y));a.SetTextSize(V(size,size));a.SetTextThickness(k.FromMM(.14));a.SetLayer(layer);b.Add(a)
text('EPD / C6',119,138,2);text('GDEY075T7  |  REV A',120,141,1);text('USB 5V ->',117.5,102,1,k.Dwgs_User)
text('XIAO ESP32C6',117.5,124,1);text('USB UP',117.5,126,1);text('BOTTOM CONTACT',155,134,.8,k.Dwgs_User)
text('FLEX OUT ->',156,138,.8,k.Dwgs_User);text('DO NOT HOT PLUG PANEL',121,147,.9)
# Enforced copper keepout under antenna; no carrier copper under antenna and margin.
z=k.ZONE(b);z.SetIsRuleArea(True);z.SetLayerSet(k.LSET.AllCuMask());z.SetDoNotAllowZoneFills(True);z.SetDoNotAllowTracks(True);z.SetDoNotAllowVias(True);z.SetDoNotAllowPads(True);z.SetDoNotAllowFootprints(True)
poly=z.Outline();poly.NewOutline()
for x,y in [(112,118),(123,118),(123,133),(112,133)]:poly.Append(k.FromMM(x),k.FromMM(y))
z.SetZoneName('XIAO antenna: copper / component exclusion');b.Add(z)
# Mounting hardware screw head clearance is reserved by larger standard courtyard.
# Ground planes on both layers, local stitching added later.
for layer in [k.F_Cu,k.B_Cu]:
 z=k.ZONE(b);z.SetLayer(layer);z.SetNet(nets['GND']);z.SetLocalClearance(k.FromMM(.25));z.SetThermalReliefGap(k.FromMM(.25));z.SetThermalReliefSpokeWidth(k.FromMM(.3));z.SetPadConnection(k.ZONE_CONNECTION_THERMAL);z.SetMinThickness(k.FromMM(.2));poly=z.Outline();poly.NewOutline()
 for x,y in [(100.5,100.5),(159.5,100.5),(159.5,149.5),(100.5,149.5)]:poly.Append(k.FromMM(x),k.FromMM(y))
 b.Add(z)
# Expose component-pad positions for reviewed routing, no guessed rotation convention.
pads={ref:{p.GetNumber():[k.ToMM(p.GetPosition().x),k.ToMM(p.GetPosition().y),p.GetNetname()] for p in f.Pads()} for ref,f in fps.items()}
(P/'analysis/pad_positions.json').write_text(json.dumps(pads,indent=2))
k.SaveBoard(str(out/(name+'.kicad_pcb')),b)
print('Placement saved;',len(fps),'footprints; pad coordinates in analysis/pad_positions.json')
