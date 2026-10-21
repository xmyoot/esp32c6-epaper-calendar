# Local schematic labels carry the root-sheet '/' path in native KiCad net names.
import pcbnew as k
p='hardware/EPD_C6_RevA.kicad_pcb';b=k.LoadBoard(p)
for n in b.GetNetInfo().NetsByNetcode().values():
 name=n.GetNetname()
 if name and not name.startswith('/'):n.SetNetname('/'+name)
k.SaveBoard(p,b)
