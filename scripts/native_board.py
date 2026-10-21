import pcbnew as k,json
b=k.LoadBoard('hardware/EPD_C6_RevA.kicad_pcb');out={'footprints':{},'tracks':[],'nets':{}}
for f in b.GetFootprints():
 out['footprints'][f.GetReference()]={'x':k.ToMM(f.GetPosition().x),'y':k.ToMM(f.GetPosition().y),'rotation':f.GetOrientationDegrees(),'footprint':str(f.GetFPID().GetLibItemName()),'path':f.GetPath().AsString(),'pads':{}}
 for p in f.Pads():out['footprints'][f.GetReference()]['pads'][p.GetNumber()]={'net':p.GetNetname(),'x':k.ToMM(p.GetPosition().x),'y':k.ToMM(p.GetPosition().y)}
for t in b.GetTracks():out['tracks'].append({'net':t.GetNetname(),'width':k.ToMM(t.GetWidth(k.F_Cu) if isinstance(t,k.PCB_VIA) else t.GetWidth()),'via':isinstance(t,k.PCB_VIA),'locked':t.IsLocked(),'start':[k.ToMM(t.GetStart().x),k.ToMM(t.GetStart().y)],'end':[k.ToMM(t.GetEnd().x),k.ToMM(t.GetEnd().y)]})
open('analysis/native-board.json','w').write(json.dumps(out,indent=2))
