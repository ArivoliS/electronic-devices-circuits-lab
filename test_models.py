import numpy as np
from models import power,rlc,rc,diode,rectifier,jfet
_,p=power(10,1000,np.array([500,1000,2000]))
assert p[1]>p[0] and p[1]>p[2] and np.isclose(p[1],.025)
f=1/(2*np.pi*np.sqrt(.1*1e-6));assert np.isclose(rlc(100,.1,1e-6,f).imag,0,atol=1e-9)
a,b=rc(5,10000,100e-6,np.array([1.]));assert np.isclose(a[0]/5,1-np.exp(-1))
v=np.linspace(0,10,200);vd,i=diode(v);assert np.allclose(vd+330*i,v);assert np.all(np.diff(i)>=0)
for bridge,expected in [(False,1.211),(True,.483)]:
 _,_,out=rectifier(10000,50,1000,0,bridge)
 ripple=np.std(out)/np.mean(out);assert abs(ripple-expected)<.003
_,_,raw=rectifier(6,50,1000,0,True);_,_,filt=rectifier(6,50,1000,470e-6,True)
assert np.std(filt)/np.mean(filt)<np.std(raw)/np.mean(raw)
assert np.all(jfet(np.array([0,1,5]),-4,.01,-4)==0)
print('PASS: matching, resonance, RC, diode load line, rectifier ripple, filtering, JFET cutoff')
