import pcbnew as k,json,shutil
from pathlib import Path
P=Path(__file__).resolve().parents[1];D=json.loads((P/'hardware/design.json').read_text());b=k.LoadBoard(str(P/'hardware/EPD_C6_RevA.kicad_pcb'));lib=P/'hardware/Carrier.pretty';src=Path('/Users/hector/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints/Fiducial.pretty/Fiducial_1mm_Mask2mm.kicad_mod');shutil.copy2(src,lib/src.name)
for p in D['parts']:
 if p['ref'].startswith('FID') and not any(f.GetReference()==p['ref'] for f in b.GetFootprints()):
  f=k.FootprintLoad(str(lib),'Fiducial_1mm_Mask2mm');f.SetFPID(k.LIB_ID('Carrier','Fiducial_1mm_Mask2mm'));f.SetReference(p['ref']);f.SetValue(p['value']);f.SetPosition(k.VECTOR2I(k.FromMM(p['pcb'][0]),k.FromMM(p['pcb'][1])));f.SetPath(k.KIID_PATH('/'+D['root_uuid']+'/'+p['uuid']));f.SetAttributes(k.FP_SMD|k.FP_EXCLUDE_FROM_BOM);f.Value().SetVisible(False);f.Reference().SetVisible(False);f.SetLocked(True);b.Add(f)
# Refresh properties from sourced schematic for assembly traceability.
for f in b.GetFootprints():
 p=next(p for p in D['parts'] if p['ref']==f.GetReference());f.SetValue(p['value'])
 if p['ref'].startswith('FID'):f.SetAttributes(k.FP_SMD|k.FP_EXCLUDE_FROM_BOM);f.SetPosition(k.VECTOR2I(k.FromMM(p['pcb'][0]),k.FromMM(p['pcb'][1])))

b.GetDesignSettings().SetAuxOrigin(k.VECTOR2I(k.FromMM(100),k.FromMM(150)))
k.ZONE_FILLER(b).Fill(b.Zones());k.SaveBoard(str(P/'hardware/EPD_C6_RevA.kicad_pcb'),b)
