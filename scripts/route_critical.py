"""Explicit reviewed critical routes, locked against automatic rip-up."""
import pcbnew as k,json
from pathlib import Path
P=Path(__file__).resolve().parents[1];path=P/'hardware/EPD_C6_RevA.kicad_pcb';b=k.LoadBoard(str(path));fps={f.GetReference():f for f in b.GetFootprints()};F=k.F_Cu;B=k.B_Cu
V=lambda x,y:k.VECTOR2I(k.FromMM(x),k.FromMM(y))
def pad(r,n):return next(p for p in fps[r].Pads() if p.GetNumber()==str(n))
def pt(r,n):p=pad(r,n).GetPosition();return (k.ToMM(p.x),k.ToMM(p.y))
nets={n.GetNetname():n.GetNetCode() for n in b.GetNetInfo().NetsByNetcode().values()}
def track(net,pts,width=.4,layer=F):
 for a,z in zip(pts,pts[1:]):
  if a==z:continue
  t=k.PCB_TRACK(b);t.SetStart(V(*a));t.SetEnd(V(*z));t.SetWidth(k.FromMM(width));t.SetLayer(layer);t.SetNetCode(nets[net]);t.SetLocked(True);b.Add(t)
def via(net,p):
 v=k.PCB_VIA(b);v.SetPosition(V(*p));v.SetWidth(k.FromMM(.6));v.SetDrill(k.FromMM(.3));v.SetViaType(k.VIATYPE_THROUGH);v.SetLayerPair(F,B);v.SetNetCode(nets[net]);v.SetLocked(True);b.Add(v)
def link(r,n,r2,n2,mids=[],width=.4,layer=F):
 net=pad(r,n).GetNetname();assert net==pad(r2,n2).GetNetname(),(r,n,r2,n2);track(net,[pt(r,n)]+mids+[pt(r2,n2)],width,layer)
# Small high-current loop, all front copper and no switching-node vias.
link('Q1',3,'D1',2,[(147.3,119)],.45)
link('Q1',3,'L1',2,[(148.1125,121.3625)],.5)
link('L1',2,'C2',1,[(145.7,122.525)],.5)
link('L1',1,'C1',1,[(151,123),(151.475,122.525)],.6)
link('C1',1,'C12',1,[(156,122.525),(156,126.525)],.6)
# Q1 source to current-sense resistor: short front copper; Kelvin net shared at source.
link('Q1',2,'R7',1,[(151.8875,118.35)],.4)
# Flying capacitor / clamp loop; all top copper.
link('C2',2,'D2',2,[(142.525,125.475)],.45)
link('D2',2,'D3',1,[(138.35,127.3)],.4)
# Ground return stitching remains close to switching power components.
for p in [(136.35,101),(151.65,101),(155.5,120.5),(154,126.5),(150,126.5),(138,123),(139,114.2),(134,106),(134.5,112.6),(142,112.5),(144,113),(148.5,113),(153,113),(134,127),(105,110),(105,139),(155,139)]:via('GND',p)
k.SaveBoard(str(path),b)
print('Locked critical copper:',len(list(b.GetTracks())),'tracks/vias')
