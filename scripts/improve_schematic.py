p='scripts/generate_schematic.py'
s=open(p).read().replace("('3  /  24-PIN DISPLAY CONNECTOR',309.88,7.62)","('3  /  24-PIN DISPLAY CONNECTOR',309.88,15.24)")
s=s.replace("(at {xx} {yy} 0) (effects (font (size 1.016", "(at {xx} {yy} {a if k in ('Reference','Value') else 0}) (effects (font (size 1.016")
s=s.replace("pins=[]\n for sub", "if ref in {'L1','Q1','R6','R7','C1','C2','C3','D1','D2','D3'}:continue\n pins=[]\n for sub")
idx=s.index("text('J1/J2")
extra='''# Draw the boost topology as actual connected wires; labels only at named ports.
def wire(points):
 for j,(a,b) in enumerate(zip(points,points[1:])):
  out.append(f'(wire (pts (xy {a[0]} {a[1]}) (xy {b[0]} {b[1]})) (stroke (width 0) (type default)) (uuid {q(uid("bw"+str(a)+str(b)))}))')
def lab(t,x,y):out.append(f'(label {q(t)} (at {x} {y} 0) (effects (font (size 1.016 1.016)) (justify left bottom)) (uuid {q(uid("bl"+t))}))')
def junction(x,y):out.append(f'(junction (at {x} {y}) (diameter 0) (color 0 0 0 0) (uuid {q(uid("bj"+str(x)+str(y)))}))')
wire([(162.56,153.67),(162.56,129.54),(189.23,129.54)])
lab('3V3_EPD',162.56,129.54)
wire([(196.85,129.54),(215.9,129.54),(242.57,129.54)])
wire([(215.9,120.65),(215.9,129.54),(215.9,149.86)])
lab('SW',215.9,129.54);junction(215.9,129.54)
wire([(215.9,113.03),(228.6,113.03),(228.6,104.14),(242.57,104.14)])
wire([(228.6,104.14),(228.6,78.74),(242.57,78.74)])
lab('PUMP',228.6,113.03);junction(228.6,104.14)
wire([(250.19,78.74),(271.78,78.74)]);lab('PREVGL',271.78,78.74)
wire([(250.19,104.14),(271.78,104.14)]);lab('GND',271.78,104.14)
wire([(250.19,129.54),(271.78,129.54),(271.78,153.67)]);lab('PREVGH',271.78,129.54)
wire([(205.74,154.94),(187.96,154.94),(187.96,176.53)]);lab('GDR',187.96,154.94)
wire([(215.9,160.02),(215.9,176.53)]);lab('RESE',215.9,176.53)
wire([(162.56,161.29),(162.56,193.04),(187.96,193.04),(215.9,193.04),(271.78,193.04),(271.78,161.29)])
wire([(187.96,184.15),(187.96,193.04)]);wire([(215.9,184.15),(215.9,193.04)])
for x in [187.96,215.9]:junction(x,193.04)
lab('GND',162.56,193.04)
'''
s=s[:idx]+extra+s[idx:]
open(p,'w').write(s)
p='scripts/design.py';s=open(p).read().replace("[215.9,104.14,0]","[215.9,116.84,180]").replace("[322.58+(i-1)*20.32,254,0]","[322.58+(i-1)*20.32,247.65,0]")
open(p,'w').write(s)
