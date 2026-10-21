import pcbnew as k,json
b=k.LoadBoard('hardware/EPD_C6_RevA.kicad_pcb');out={}
for z in b.Zones():
 if z.GetIsRuleArea():continue
 polys=z.GetFilledPolysList(z.GetLayer());arr=[]
 for i in range(polys.OutlineCount()):
  chain=polys.COutline(i);pts=[(k.ToMM(chain.CPoint(j).x),k.ToMM(chain.CPoint(j).y)) for j in range(chain.PointCount())];arr.append(pts)
 out[str(z.GetLayer())]=arr
out['pads']=[{'x':k.ToMM(p.GetPosition().x),'y':k.ToMM(p.GetPosition().y),'sx':k.ToMM(p.GetSize().x),'sy':k.ToMM(p.GetSize().y)} for f in b.GetFootprints() for p in f.Pads()]
open('analysis/ground-polygons.json','w').write(json.dumps(out))
