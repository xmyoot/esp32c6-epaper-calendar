import pcbnew as k,json
b=k.LoadBoard('hardware/EPD_C6_RevA.kicad_pcb');net=next(p.GetNetCode() for f in b.GetFootprints() for p in f.Pads() if p.GetNetname()=='GND')
for x,y in json.load(open('analysis/ground-stitch.json')):
 v=k.PCB_VIA(b);v.SetPosition(k.VECTOR2I(k.FromMM(x),k.FromMM(y)));v.SetWidth(k.FromMM(.6));v.SetDrill(k.FromMM(.3));v.SetViaType(k.VIATYPE_THROUGH);v.SetLayerPair(k.F_Cu,k.B_Cu);v.SetNetCode(net);v.SetLocked(True);b.Add(v)
k.ZONE_FILLER(b).Fill(b.Zones());k.SaveBoard('hardware/EPD_C6_RevA.kicad_pcb',b)
