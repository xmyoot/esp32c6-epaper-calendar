"""Final layout polish and explicit fixes; native DRC remains the acceptance gate."""
import pcbnew as k
from pathlib import Path
P=Path(__file__).resolve().parents[1];path=P/'hardware/EPD_C6_RevA.kicad_pcb';b=k.LoadBoard(str(path));V=lambda x,y:k.VECTOR2I(k.FromMM(x),k.FromMM(y));fps={f.GetReference():f for f in b.GetFootprints()}
# FPC ground contacts use solid connections: narrow contacts cannot support two relief spokes.
for p in fps['J3'].Pads():
 if p.GetNetname()=='GND':p.SetLocalZoneConnection(k.ZONE_CONNECTION_FULL)
# Human-readable silk reference positions, outside pad openings and component outlines.
refs={'C1':(155.8,124),'C2':(144,127.2),'C3':(129,118),'C4':(151,111),'C5':(144,114),'C6':(141,113.5),'C7':(139.5,117),'C8':(139.2,113.5),'C9':(129.6,108),'C10':(135.5,124.5),'C11':(146.5,113.5),'C12':(156.7,130),'Q1':(149,117),'L1':(148,126),'D1':(144,117),'D2':(140,122),'D3':(140,131),'R1':(129,120.6),'R2':(128,114.5),'R3':(128,110),'R4':(133,124),'R5':(134,127),'R6':(152,113),'R7':(154,117),'J1':(107.8,111),'J2':(127.4,106.5),'J3':(144,102),'TP1':(131,135.5),'TP2':(137,135.5),'TP3':(132,121),'TP4':(134,132.5),'TP5':(126.7,132.5),'TP6':(130.5,132.5)}
for ref,p in refs.items():
 r=fps[ref].Reference();r.SetPosition(V(*p));r.SetTextAngle(k.EDA_ANGLE(0,k.DEGREES_T));r.SetTextSize(V(.8,.8));r.SetTextThickness(k.FromMM(.12))
# Drawn fabrication statements reflect connector insertion at the upper edge.
for d in b.GetDrawings():
 if isinstance(d,k.PCB_TEXT):
  if d.GetText()=='FLEX OUT ->':d.SetText('FLEX EXITS TOP');d.SetPosition(V(144,99))
# Remove the redundant isolated upper-edge ground via, then suppress floating copper islands.
for t in list(b.GetTracks()):
 if isinstance(t,k.PCB_VIA) and t.GetNetname()=='GND' and abs(k.ToMM(t.GetPosition().x)-136.35)<.001 and abs(k.ToMM(t.GetPosition().y)-101)<.001:b.Delete(t)
for z in b.Zones():
 if not z.GetIsRuleArea():z.SetIslandRemovalMode(k.ISLAND_REMOVAL_MODE_ALWAYS)
# Native zone refill stores actual ground copper in the deliverable.
k.ZONE_FILLER(b).Fill(b.Zones());k.SaveBoard(str(path),b)
print('Finalization written')
