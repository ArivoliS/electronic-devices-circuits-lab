"""Teaching models; SI units throughout. No hardware device fitting is implied."""
import numpy as np

def power(v,r,rl):
    i=v/(r+rl)
    return i, i*i*rl

def rlc(r,l,c,f,parallel=False):
    w=2*np.pi*np.asarray(f)
    z=1/(1/r+1j*(w*c-1/(w*l))) if parallel else r+1j*(w*l-1/(w*c))
    return z

def rc(v,r,c,t):
    return v*(1-np.exp(-t/(r*c))),v*np.exp(-t/(r*c))

def diode(v,rs=330,isat=1e-9,n=2,vt=.02585):
    # Monotone load-line solve, including series current limiting.
    lo=np.zeros_like(v); hi=np.maximum(v,0)
    for _ in range(70):
        vd=(lo+hi)/2
        residual=vd+rs*isat*np.expm1(np.clip(vd/(n*vt),-100,100))-v
        hi=np.where(residual>0,vd,hi); lo=np.where(residual<=0,vd,lo)
    vd=(lo+hi)/2
    return vd,(v-vd)/rs

def rectifier(vrms,f,rl,cap,bridge):
    # 30 cycles; ideal source and fixed diode drops; final 3 cycles exported.
    t=np.arange(0,30/f,1/(f*1500))
    vi=np.sqrt(2)*vrms*np.sin(2*np.pi*f*t)
    raw=np.maximum((np.abs(vi) if bridge else vi)-(.7*(2 if bridge else 1)),0)
    out=raw.copy()
    if cap>0:
        decay=np.exp(-(t[1]-t[0])/(rl*cap))
        for k in range(1,len(t)):out[k]=max(raw[k],out[k-1]*decay)
    mask=t>=27/f
    return t[mask]-27/f,vi[mask],out[mask]

def bjt(vce,ib,beta=100,early=100):
    return beta*ib*np.minimum(np.maximum(vce,0)/.2,1)*(1+vce/early)

def jfet(vds,vgs,idss,vp):
    over=max(vgs-vp,0)
    k=idss/(vp*vp)
    return np.where(vds<over,k*(2*over*vds-vds*vds),k*over*over)
