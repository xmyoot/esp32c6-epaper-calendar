"""Revision A design definition: physical pin numbers are explicit."""
from pathlib import Path
import json,uuid,copy,math
ROOT=Path(__file__).resolve().parents[1]
KICAD=Path('/Users/hector/Applications/KiCad/KiCad.app/Contents/SharedSupport')
NAME='EPD_C6_RevA'
def uid(k):return str(uuid.uuid5(uuid.NAMESPACE_URL,'epd-c6-reva/'+k))
parts=[]
def add(ref,value,sym,fp,nets,sch,pcb,code='',mpn='',mfr='',notes=''):
 parts.append(dict(ref=ref,value=value,symbol=sym,footprint=fp,nets={str(k):v for k,v in nets.items()},sch=sch,pcb=pcb,lcsc=code,mpn=mpn,manufacturer=mfr,notes=notes,uuid=uid(ref)))
R4='Resistor_SMD:R_0402_1005Metric';C8='Capacitor_SMD:C_0805_2012Metric';C12='Capacitor_SMD:C_1206_3216Metric';C10='Capacitor_SMD:C_1210_3225Metric'
add('J1','XIAO LEFT / USB UP','Carrier:Socket_Left','Connector_PinSocket_2.54mm:PinSocket_1x07_P2.54mm_Vertical',{1:'EPD_CS_N',2:'EPD_DC',3:'EPD_RST_N',4:'EPD_BUSY_N',5:None,6:None,7:None},[45.72,60.96,0],[110,104,0],mpn='SSW-107-01-G-S',mfr='Samtec',notes='Hand solder; pin1=D0, USB toward top edge. Two rows spaced 15.24mm.')
add('J2','XIAO RIGHT / USB UP','Carrier:Socket_Right','Connector_PinSocket_2.54mm:PinSocket_1x07_P2.54mm_Vertical',{1:None,2:'GND',3:'3V3_MODULE',4:'MOSI_SRC',5:None,6:'SCK_SRC',7:None},[114.3,60.96,0],[125.24,104,0],mpn='SSW-107-01-G-S',mfr='Samtec',notes='Hand solder; pin1=5V (unused), pin7=D7. Male headers fitted to XIAO separately.')
fpc={1:None,2:'GDR',3:'RESE',4:None,5:'VSHR',6:None,7:None,8:'GND',9:'EPD_BUSY_N',10:'EPD_RST_N',11:'EPD_DC',12:'EPD_CS_N',13:'EPD_SCK',14:'EPD_MOSI',15:'3V3_EPD',16:'3V3_EPD',17:'GND',18:'VDD_INT',19:None,20:'VSH1',21:'PREVGH',22:'VSL',23:'PREVGL',24:'VCOM','MP':'GND'}
add('J3','GDEY075T7 / BOTTOM CONTACT','Carrier:GDEY075T7_FPC24','Connector_FFC-FPC:Hirose_FH12-24S-0.5SH_1x24-1MP_P0.50mm_Horizontal',fpc,[340.36,68.58,0],[153,122,90],'C202112','FH12-24S-0.5SH(55)','Hirose','24 contacts / 0.5mm / 0.3mm flex; pin4 NC despite reference alias VGL; pin5 VSHR independent of pin21.')
add('R1','0R / ISOLATE','Device:R','Resistor_SMD:R_0805_2012Metric',{1:'3V3_MODULE',2:'3V3_EPD'},[55.88,104.14,90],[130,110,0],'C17477','0805W8F0000T5E','UNI-ROYAL','Remove for current measurement or isolated carrier testing.')
add('R2','33R','Device:R',R4,{1:'SCK_SRC',2:'EPD_SCK'},[55.88,124.46,90],[127.5,117,0],'C25105','0402WGF330JTCE','UNI-ROYAL')
add('R3','33R','Device:R',R4,{1:'MOSI_SRC',2:'EPD_MOSI'},[55.88,139.7,90],[127.5,112,0],'C25105','0402WGF330JTCE','UNI-ROYAL')
add('R4','100k','Device:R',R4,{1:'3V3_EPD',2:'EPD_CS_N'},[109.22,109.22,0],[132,116,90],'C25741','0402WGF1003TCE','UNI-ROYAL')
add('R5','100k','Device:R',R4,{1:'EPD_RST_N',2:'GND'},[109.22,139.7,0],[132,120,90],'C25741','0402WGF1003TCE','UNI-ROYAL')
add('L1','10uH / 1.3A','Device:L','Inductor_SMD:L_Bourns-SRN4018',{1:'3V3_EPD',2:'SW'},[193.04,129.54,90],[138,110,0],'C503307','SRN4018-100M','Bourns','Isat 1.4A (30% drop), DCR <=180mR; reference specifies 1A.')
add('Q1','Si1308EDL','Transistor_FET:Q_NMOS_GSD','Package_TO_SOT_SMD:SOT-323_SC-70',{1:'GDR',2:'RESE',3:'SW'},[210.82,154.94,0],[140,115,0],'C469327','SI1308EDL-T1-GE3','Vishay','1=G 2=S 3=D; 30V; 185mR max at Vgs=2.5V.')
add('R6','1M','Device:R',R4,{1:'GDR',2:'GND'},[187.96,180.34,0],[136,115,90],'C26083','0402WGF1004TCE','UNI-ROYAL')
add('R7','0.47R / 0.5W','Device:R','Resistor_SMD:R_1206_3216Metric',{1:'RESE',2:'GND'},[215.9,180.34,0],[140,119,90],'C859932','RL1206FR-7W0R47L','Yageo','Kelvin RESE takeoff at Q1 source; keep ground return local.')
add('D1','MBR0530','Device:D_Schottky','Diode_SMD:D_SOD-123',{1:'PREVGH',2:'SW'},[246.38,129.54,180],[144,110,180],'C77336','MBR0530','JSCJ','Cathode pad1; positive rectifier.')
add('D2','MBR0530','Device:D_Schottky','Diode_SMD:D_SOD-123',{1:'GND',2:'PUMP'},[246.38,104.14,180],[144,104,180],'C77336','MBR0530','JSCJ','Cathode pad1 to GND; pump clamp.')
add('D3','MBR0530','Device:D_Schottky','Diode_SMD:D_SOD-123',{1:'PUMP',2:'PREVGL'},[246.38,78.74,0],[148,104,180],'C77336','MBR0530','JSCJ','Anode pad2 to PREVGL; cathode pad1 to PUMP.')
# Rail capacitors use physical sizes appropriate to voltage / effective capacitance.
def cap(ref,val,n1,n2,sch,pcb,kind='1u'):
 if kind=='10u':fp,code,mpn,mfr=C10,'C77102','GRM32ER71H106KA12L','Murata'
 elif kind=='4u7':fp,code,mpn,mfr=C12,'C132170','CC1206KKX7R9BB475','Yageo'
 elif kind=='100n':fp,code,mpn,mfr='Capacitor_SMD:C_0402_1005Metric','C1525','CL05B104KO5NNNC','Samsung'
 else:fp,code,mpn,mfr=C8,'C77083','GRM21BR71H105KA12L','Murata'
 add(ref,val,'Device:C',fp,{1:n1,2:n2},sch,pcb,code,mpn,mfr)
cap('C1','4.7u / 50V','3V3_EPD','GND',[162.56,157.48,0],[133,110,90],'4u7')
cap('C2','4.7u / 50V','SW','PUMP',[215.9,116.84,180],[140,105,90],'4u7')
cap('C3','10u / 50V','PREVGH','GND',[271.78,157.48,0],[149,110,90],'10u')
cap('C4','1u / 50V','VSHR','GND',[43.18,223.52,0],[148,115,90])
cap('C5','1u / 50V','3V3_EPD','GND',[81.28,223.52,0],[147,122,90])
cap('C6','1u / 50V','VDD_INT','GND',[119.38,223.52,0],[147,126,90])
cap('C7','10u / 50V','VSH1','GND',[157.48,223.52,0],[146,131,90],'10u')
cap('C8','10u / 50V','VSL','GND',[195.58,223.52,0],[151,136,90],'10u')
cap('C9','10u / 50V','PREVGL','GND',[233.68,223.52,0],[145,140,90],'10u')
cap('C10','1u / 50V','VCOM','GND',[271.78,223.52,0],[151,141,90])
cap('C11','100n / 16V','3V3_EPD','GND',[139.7,109.22,0],[149,122,90],'100n')
# Bulk input and logic, 10u/50V part reused to reduce distinct BOM lines.
cap('C12','10u / 50V','3V3_EPD','GND',[139.7,139.7,0],[133,105,90],'10u')
for i,(net,pcb) in enumerate([('3V3_EPD',[131,113,0]),('GND',[137,123,0]),('PREVGH',[152,108,0]),('PREVGL',[142,143,0]),('EPD_BUSY_N',[134,127,0]),('EPD_RST_N',[131,125,0])],1):
 add('TP'+str(i),net,'Connector:TestPoint','TestPoint:TestPoint_Pad_D1.0mm',{1:net},[317.5+((i-1)%3)*27.94,203.2+((i-1)//3)*25.4,0],pcb,notes='PCB test pad; no fitted component.')
for i,pos in enumerate([[104,104,0],[156,104,0],[104,146,0],[156,146,0]],1):
 add('H'+str(i),'M2.5 NPTH','Mechanical:MountingHole','MountingHole:MountingHole_2.7mm_M2.5',{},[322.58+(i-1)*20.32,247.65,0],pos,notes='Mechanical; M2.5 non-plated mounting hole.')
for i,pos in enumerate([[104,134,0],[156,134,0],[148,146,0]],1):
 add('FID'+str(i),'1mm FIDUCIAL','Mechanical:Fiducial','Fiducial:Fiducial_1mm_Mask2mm',{},[43.18+(i-1)*38.1,279.4,0],pos,notes='Optical PCB fiducial, no fitted component.')
from floorplan import POSITIONS
for p in parts:
 if p['ref'] in POSITIONS:p['pcb']=list(POSITIONS[p['ref']])
if __name__=='__main__':
 (ROOT/'hardware/design.json').write_text(json.dumps({'name':NAME,'root_uuid':uid('root'),'parts':parts},indent=2))
 print(len(parts),'components')
