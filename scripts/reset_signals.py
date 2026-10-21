import pcbnew as k
from pathlib import Path
P=Path(__file__).resolve().parents[1];b=k.LoadBoard(str(P/'hardware/EPD_C6_RevA.kicad_pcb'))
ns={'SCK_SRC','MOSI_SRC','EPD_SCK','EPD_MOSI','EPD_CS_N','EPD_DC','EPD_RST_N','EPD_BUSY_N'}
for t in list(b.GetTracks()):
 if t.GetNetname() in ns:b.Delete(t)
k.SaveBoard(str(P/'analysis/routing/signal-reset.kicad_pcb'),b)
