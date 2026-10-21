"""Generate editable native KiCad schematic and local symbol library."""
from design import *
import sexpdata as sx
S=sx.Symbol
q=lambda a:json.dumps(str(a))
def tag(x,n):return isinstance(x,list) and x and str(x[0])==n
def one(x,n):return next((a for a in x if tag(a,n)),None)
def alltag(x,n):return [a for a in x if tag(a,n)]
def custom(name,names):
 h=(len(names)+1)*1.27
 txt=f'(symbol {q(name)} (pin_names (offset 0.508)) (in_bom yes) (on_board yes) (property "Reference" "J" (at 0 {h+3} 0) (effects (font (size 1.27 1.27)))) (property "Value" {q(name)} (at 0 {h+1} 0) (effects (font (size 1.27 1.27)))) (symbol {q(name+"_0_1")} (rectangle (start -12.7 {h}) (end 12.7 {-h}) (stroke (width 0.254) (type default)) (fill (type background)))) (symbol {q(name+"_1_1")}'
 for i,pin in enumerate(names,1):
  y=(len(names)-1)*1.27-(i-1)*2.54
  txt+=f' (pin passive line (at -15.24 {y} 0) (length 2.54) (name {q(pin)} (effects (font (size 1.016 1.016)))) (number {q(i)} (effects (font (size 1.016 1.016)))))'
 return sx.loads(txt+'))')
customs={'Socket_Left':custom('Socket_Left',['D0 / GPIO0','D1 / GPIO1','D2 / GPIO2','D3 / GPIO21','D4 / GPIO22','D5 / GPIO23','D6 / GPIO16']), 'Socket_Right':custom('Socket_Right',['5V / NC','GND','3V3 OUT','D10 / GPIO18','D9 / GPIO20','D8 / GPIO19','D7 / GPIO17']), 'GDEY075T7_FPC24':custom('GDEY075T7_FPC24',['NC','GDR','RESE','NC / alias VGL','VSHR / alias VGH','TSCL / unused','TSDA / unused','BS1','BUSY_N','RST_N','DC','CS_N','SCK','MOSI','VDDIO','VCI','VSS','VDD_INTERNAL','VPP / TEST NC','VSH1','PREVGH','VSL','PREVGL','VCOM'])}
# Connector anchor tabs are explicitly grounded in both schematic and board.
customs['GDEY075T7_FPC24'][-1].append(sx.loads('(pin passive line (at 0 -36.83 90) (length 2.54) (name "SHIELD_TABS" (effects (font (size 1.016 1.016)))) (number "MP" (effects (font (size 1.016 1.016)))))'))
libdata={};symbols={}
for p in parts:
 lib,name=p['symbol'].split(':')
 if p['symbol'] in symbols:continue
 if lib=='Carrier':v=copy.deepcopy(customs[name])
 else:
  if lib not in libdata: libdata[lib]=sx.loads((KICAD/'symbols'/(lib+'.kicad_sym')).read_text())
  v=copy.deepcopy(next(a for a in libdata[lib] if tag(a,'symbol') and a[1]==name))
  assert not one(v,'extends'),p['symbol']
 v[1]=p['symbol'];symbols[p['symbol']]=v
carrier=[copy.deepcopy(v) for v in customs.values()]
for lib,items in libdata.items():
 used={p['symbol'].split(':')[1] for p in parts if p['symbol'].split(':')[0]==lib}
 subset=[a for a in items if not tag(a,'symbol') or a[1] in used]
 (ROOT/'hardware'/(lib+'.kicad_sym')).write_text(sx.dumps(subset))
(ROOT/'hardware/Carrier.kicad_sym').write_text('(kicad_symbol_lib (version 20241209) (generator "epd_project")\n'+'\n'.join(sx.dumps(v) for v in carrier)+')')
(ROOT/'hardware/sym-lib-table').write_text('(sym_lib_table (version 7) '+''.join('(lib (name '+q(n)+')(type "KiCad")(uri "${KIPRJMOD}/'+n+'.kicad_sym")(options "")(descr "Project-local library"))' for n in ['Carrier']+list(libdata))+')')
root=uid('root');out=[f'(kicad_sch (version 20250114) (generator "eeschema") (uuid {q(root)}) (paper "A3") (title_block (title "ESP32-C6 E-paper Calendar Carrier") (date "2026-10-20") (rev "A") (company "Hector | Portfolio Engineering") (comment 1 "GDEY075T7 / UC8179 | USB-powered socketed XIAO ESP32C6") (comment 2 "DESIGN REVISION A - PROTOTYPE NOT YET TESTED")) (lib_symbols '+'\n'.join(sx.dumps(v) for v in symbols.values())+')']
def text(t,x,y,size=1.27):out.append(f'(text {q(t)} (at {x} {y} 0) (effects (font (size {size} {size})) (justify left top)) (uuid {q(uid("text"+t))}))')
for t,x,y in [('1  /  SOCKETED XIAO - USB FACES TOP EDGE',25.4,27.94),('2  /  PANEL-CONTROLLED BOOST + CHARGE PUMP',162.56,27.94),('3  /  24-PIN DISPLAY CONNECTOR',309.88,15.24),('4  /  PANEL RAIL CAPACITORS',25.4,200.66),('5  /  PROBE POINTS',309.88,187.96)]:text(t,x,y,1.65)
for p in parts:
 ref=p['ref'];lib=p['symbol'];sym=symbols[lib];x,y,a=p['sch'];ang=math.radians(a)
 props={'Reference':ref,'Value':p['value'],'Footprint':'Carrier:'+p['footprint'].split(':')[1],'Datasheet':('https://www.lcsc.com/product-detail/'+p['lcsc']+'.html' if p['lcsc'] else ''),'MPN':p['mpn'],'Manufacturer':p['manufacturer'],'LCSC':p['lcsc'],'BOM Comments':p['notes']}
 if ref.startswith(('J','H','FID')):rx,ry=x,y-((len(p['nets'])+1)*1.27+6.35 if ref.startswith('J') else 5.08);vx,vy=rx,ry+2.54
 else:rx,ry=x+2.54,y-1.27;vx,vy=x+2.54,y+1.27
 st=f'(symbol (lib_id {q(lib)}) (at {x} {y} {a}) (unit 1) (in_bom {"no" if ref.startswith(("TP","H")) else "yes"}) (on_board yes) (dnp no) (uuid {q(p["uuid"])})'
 for k,v in props.items():
  xx,yy=(rx,ry) if k=='Reference' else (vx,vy) if k=='Value' else (x,y)
  st+=f' (property {q(k)} {q(v)} (at {xx} {yy} {a%180 if k in ("Reference","Value") else 0}) (effects (font (size 1.016 1.016)) (justify left){" (hide yes)" if k not in ("Reference","Value") else ""}))'
 st+=f' (instances (project {q(NAME)} (path {q("/"+root)} (reference {q(ref)}) (unit 1)))))'
 out.append(st)
 if ref in {'L1','Q1','R6','R7','C1','C2','C3','D1','D2','D3'}:continue
 pins=[]
 for sub in alltag(sym,'symbol'):pins.extend(alltag(sub,'pin'))
 for pin in pins:
  n=str(one(pin,'number')[1]);net=p['nets'].get(n);at=one(pin,'at');px,py=float(at[1]),float(at[2]);pa=float(at[3]);xx=round(x+px*math.cos(ang)-py*math.sin(ang),5);yy=round(y-px*math.sin(ang)-py*math.cos(ang),5)
  if net is None:out.append(f'(no_connect (at {xx} {yy}) (uuid {q(uid(ref+"nc"+n))}))');continue
  # Extend pin in the direction opposite its inward-pointing orientation.
  theta=math.radians(pa+a);ex=round(xx-5.08*math.cos(theta),5);ey=round(yy+5.08*math.sin(theta),5)
  out.append(f'(wire (pts (xy {xx} {yy}) (xy {ex} {ey})) (stroke (width 0) (type default)) (uuid {q(uid(ref+"w"+n))}))')
  justify='right' if math.cos(theta)>.5 else 'left'
  out.append(f'(label {q(net)} (at {ex} {ey} 0) (effects (font (size 1.016 1.016)) (justify {justify} bottom)) (uuid {q(uid(ref+"l"+n))}))')
# Draw the boost topology as actual connected wires; labels only at named ports.
def wire(points):
 for j,(a,b) in enumerate(zip(points,points[1:])):
  out.append(f'(wire (pts (xy {a[0]} {a[1]}) (xy {b[0]} {b[1]})) (stroke (width 0) (type default)) (uuid {q(uid("bw"+str(a)+str(b)))}))')
def lab(t,x,y):out.append(f'(label {q(t)} (at {x} {y} 0) (effects (font (size 1.016 1.016)) (justify left bottom)) (uuid {q(uid("bl"+t))}))')
def junction(x,y):out.append(f'(junction (at {x} {y}) (diameter 0) (color 0 0 0 0) (uuid {q(uid("bj"+str(x)+str(y)))}))')
wire([(162.56,153.67),(162.56,129.54),(189.23,129.54)])
lab('3V3_EPD',162.56,129.54)
wire([(196.85,129.54),(215.9,129.54),(242.57,129.54)])
wire([(215.9,120.65),(215.9,129.54),(215.9,146.05),(213.36,146.05),(213.36,149.86)])
lab('SW',215.9,129.54);junction(215.9,129.54)
wire([(215.9,113.03),(228.6,113.03),(228.6,104.14),(242.57,104.14)])
wire([(228.6,104.14),(228.6,78.74),(242.57,78.74)])
lab('PUMP',228.6,113.03);junction(228.6,104.14)
wire([(250.19,78.74),(271.78,78.74)]);lab('PREVGL',271.78,78.74)
wire([(250.19,104.14),(271.78,104.14)]);lab('GND',271.78,104.14)
wire([(250.19,129.54),(271.78,129.54),(271.78,153.67)]);lab('PREVGH',271.78,129.54)
wire([(205.74,154.94),(187.96,154.94),(187.96,176.53)]);lab('GDR',187.96,154.94)
wire([(213.36,160.02),(213.36,165.1),(215.9,165.1),(215.9,176.53)]);lab('RESE',215.9,176.53)
wire([(162.56,161.29),(162.56,193.04),(187.96,193.04),(215.9,193.04),(271.78,193.04),(271.78,161.29)])
wire([(187.96,184.15),(187.96,193.04)]);wire([(215.9,184.15),(215.9,193.04)])
for x in [187.96,215.9]:junction(x,193.04)
lab('GND',162.56,193.04)
text('J1/J2 are physical female sockets. Pin 1 is nearest USB.\nJ2 pins are numbered top-to-bottom, not module DIP order.\n15.24 mm row spacing; 2.54 mm pitch. No carrier 5V connection.',25.4,78.74)
text('R1: remove to isolate / measure display supply.\nHold RESET low and CS high before SPI starts.\nGPIO19=SCK, GPIO18=MOSI; start at 1 MHz.\nPower off Wi-Fi before refresh.',25.4,157.48)
text('Boost controlled by UC8179 through GDR / RESE.\nQ1: 1=gate, 2=source, 3=drain. D1-D3: 1=cathode.\nKelvin pickup on RESE; short SW loop; 50V bias MLCCs.\nReference: Good Display GDEY075T7 rev1.0 p40.',162.56,48.26)
text('Pin 4 is NC. Pin 5 VSHR is NOT pin 21 PREVGH.\nPin 18 VDD_INTERNAL receives only C6, never external 3V3.\nTSCL / TSDA / VPP unused per reference. BS1=GND.\nCheck flex orientation before inserting the panel.',309.88,119.38)
text('All rail capacitors non-polar MLCC. Bias-dependent capacitance must be checked against the exact panel lot.\nNo high-voltage rail is an external supply input. Fit panel and module only after inspection / resistance checks.',25.4,245.11)
text('Four M2.5 non-plated holes. USB supply 5V / >=1A.\nSMT top side only; sockets hand-soldered after reflow.',25.4,263)
(ROOT/'hardware'/(NAME+'.kicad_sch')).write_text('\n'.join(out)+')\n')
print('Schematic written:',len(parts),'symbols')
