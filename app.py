from pathlib import Path
import json, html
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from models import power,rlc,rc,diode,rectifier,bjt,jfet

st.set_page_config(page_title='Electronic Devices & Circuits Lab',page_icon='🔬',layout='wide')
ROOT=Path(__file__).parent
NAMES=['Maximum power transfer','Sinusoidal steady-state RLC','Series RLC resonance','RC transient response','PN and Zener diode characteristics','Half-wave and bridge rectifiers','BJT characteristics','Single-stage BJT amplifier','BJT RC phase-shift oscillator','JFET as a switch']
AIMS=['Verify the load resistance for maximum power.','Calculate impedance, current, phase and power in an RLC circuit.','Determine resonance, quality factor and half-power bandwidth.','Examine charging and discharging and estimate the RC time constant.','Plot diode characteristics and analyse current limiting.','Compare rectified waveforms and capacitor filtering.','Explore common-emitter output and input characteristics.','Study voltage gain, frequency response and clipping.','Design an approximate equal-section RC feedback network.','Explore gate control of an n-channel JFET.']
QUESTIONS=[['Why does maximum power occur at RL = Rth?','Why is efficiency only 50% at matching?'],['When does current lead the applied voltage?','How does reactive power differ from real power?'],['Why does series current peak at resonance?','How does resistance change bandwidth?'],['What fraction of the final voltage is reached at one time constant?','Why is capacitor voltage continuous?'],['How does a series resistor limit diode current?','How does Zener breakdown differ from forward conduction?'],['Why is bridge ripple frequency twice the supply frequency?','Why does a larger filter capacitor reduce ripple?'],['How is DC current gain obtained from measured currents?','How can saturation be identified?'],['Why is the CE output inverted?','What sets the lower and upper cutoff frequencies?'],['What are the Barkhausen conditions?','Why is startup gain greater than the steady oscillation gain?'],['Why must the n-channel gate not be forward biased?','How does cutoff differ from drain pinch-off?']]
manuals=json.loads((ROOT/'assets/manuals.json').read_text())
st.sidebar.title('🔬 EDC Virtual Lab')
st.sidebar.caption('PSG Institute of Technology and Applied Research')
idx=st.sidebar.selectbox('Experiment',range(10),format_func=lambda x:f'{x+1:02d} · {NAMES[x]}',key='experiment')
student=st.sidebar.text_input('Student name')
reg=st.sidebar.text_input('Register number')
section=st.sidebar.text_input('Class / batch')
st.sidebar.info('25IC111 · Circuits and Devices Laboratory\n\nPrepared for Dr. Arivoli S')
st.title('Electronic Devices & Circuits Laboratory')
st.caption('Explore • simulate • measure • interpret')
st.subheader(f'Experiment {idx+1}: {NAMES[idx]}')
st.write(AIMS[idx])
st.info('All computed readings are educational simulations. Enter actual bench measurements separately. These simplified models do not certify component ratings or hardware performance.')
learn,sim,record,viva,manual=st.tabs(['📖 Learn & procedure','🎛️ Simulator','📝 Observation & record','💬 Viva prompts','📚 Source manuals'])
with learn:
    st.markdown('**Bench workflow**\n1. Review the circuit and device pinout in the source manual.\n2. Calculate expected values and select suitable component ratings.\n3. With the supply off, wire the circuit and obtain faculty approval.\n4. Apply a current-limited, isolated low-voltage supply. Sweep one variable at a time.\n5. Record measurements with units; compare with the model and explain differences.')
    st.warning('Use isolated low-voltage bench supplies only. Turn off power before rewiring; discharge capacitors through a resistor. Never connect the breadboard directly to mains. Verify actual transistor pinouts from its datasheet.')
    st.write('The Source manuals tab contains the supplied circuit diagrams and experiment instructions. The simulator below states the model used for each experiment.')

def number(label,value,minv=.001,step=None):
    return st.number_input(label,min_value=float(minv),value=float(value),step=float(step or max(value/10,.001)),key=f'{idx}-{label}')
def chart(df,x,ys,log=False):
    st.plotly_chart(px.line(df,x=x,y=ys,log_x=log),use_container_width=True)
def metrics(values):
    cols=st.columns(len(values))
    for col,(k,v) in zip(cols,values.items()):col.metric(k,v)

with sim:
    if idx==0:
        v=number('Thevenin voltage (V)',10);r=number('Thevenin resistance (Ω)',1000)
        load=np.unique(np.r_[np.linspace(.05*r,5*r,200),r]);i,p=power(v,r,load)
        df=pd.DataFrame({'Load resistance (Ω)':load,'Load current (mA)':i*1000,'Load power (mW)':p*1000})
        st.latex(r'P_L=\frac{V_{th}^2R_L}{(R_{th}+R_L)^2},\quad P_{max}=\frac{V_{th}^2}{4R_{th}}')
        metrics({'Matching load':f'{r:g} Ω','Maximum power':f'{v*v/(4*r)*1000:.3f} mW'})
        chart(df,df.columns[0],[df.columns[2]])
    elif idx in (1,2):
        r=number('Resistance (Ω)',100);l=number('Inductance (mH)',100)*1e-3;c=number('Capacitance (µF)',1)*1e-6
        v=number('Supply RMS (V)',5);f0=1/(2*np.pi*np.sqrt(l*c))
        parallel=st.checkbox('Explore parallel RLC (supplementary)',False,key=f'{idx}-parallel') if idx==1 else False
        f=np.geomspace(f0/20,f0*20,500);z=rlc(r,l,c,f,parallel)
        df=pd.DataFrame({'Frequency (Hz)':f,'Current RMS (mA)':v/np.abs(z)*1000,'Impedance (Ω)':np.abs(z),'Current phase (deg)':-np.angle(z,deg=True)})
        q=r*np.sqrt(c/l) if parallel else np.sqrt(l/c)/r
        bw=f0/q
        fl=(np.sqrt(bw*bw+4*f0*f0)-bw)/2;fh=fl+bw
        metrics({'Resonance':f'{f0:.2f} Hz','Q':f'{q:.3f}','Bandwidth':f'{bw:.2f} Hz'})
        st.write(f'Half-power frequencies: {fl:.2f} Hz and {fh:.2f} Hz. Ideal R, L and C model.')
        chart(df,'Frequency (Hz)',['Current RMS (mA)'],True)
        fs=number('Analysis frequency (Hz)',float(round(f0,2)));zs=rlc(r,l,c,fs,parallel);ir=v/abs(zs);ph=np.angle(zs)
        st.write(f'At {fs:g} Hz: I = {ir:.5f} A; real power = {v*ir*np.cos(ph):.5f} W; reactive power = {v*ir*np.sin(ph):.5f} var; power factor = {np.cos(ph):.4f}.')
        st.latex(r'Z_s=R+j(\omega L-1/\omega C),\quad f_0=1/(2\pi\sqrt{LC})')
    elif idx==3:
        v=number('Step voltage (V)',5);r=number('Resistance (kΩ)',10)*1000;c=number('Capacitance (µF)',100)*1e-6
        t=np.linspace(0,5*r*c,300);a,b=rc(v,r,c,t)
        df=pd.DataFrame({'Time (s)':t,'Charging voltage (V)':a,'Discharging voltage (V)':b})
        metrics({'Time constant':f'{r*c:.4g} s','Charging at τ':f'{v*(1-np.exp(-1)):.3f} V'})
        st.latex(r'v_C=V(1-e^{-t/RC}),\quad v_{dis}=Ve^{-t/RC}')
        chart(df,'Time (s)',list(df.columns[1:]))
    elif idx==4:
        mode=st.radio('Device',['PN forward','PN reverse','Zener reverse'],horizontal=True,key=f'{idx}-device')
        rs=number('Series resistor (Ω)',330);supply=number('Maximum supply magnitude (V)',10)
        vs=np.linspace(0,supply,240)
        if mode=='PN forward':
            vd,cur=diode(vs,rs);st.caption('Shockley diode with n = 2, Is = 1 nA, T ≈ 300 K; series resistor load-line solution.')
        elif mode=='PN reverse':
            vd=-vs;cur=-1e-9*(1-np.exp(-vs/.02585));st.caption('Ideal 1 nA reverse leakage; breakdown and temperature effects excluded.')
        else:
            vz=number('Zener voltage (V)',5.1);rz=number('Dynamic Zener resistance (Ω)',10)
            cur=-np.maximum(vs-vz,0)/(rs+rz);vd=-(vs-np.abs(cur)*rs)
            st.caption('Piecewise breakdown model; no sub-breakdown leakage. Check actual Zener power ratings on the bench.')
        df=pd.DataFrame({'Supply magnitude (V)':vs,'Device voltage (V)':vd,'Device current (mA)':cur*1000})
        chart(df,'Device voltage (V)',['Device current (mA)'])
        metrics({'Peak |current|':f'{max(abs(cur))*1000:.3f} mA','Peak device power':f'{max(abs(vd*cur))*1000:.3f} mW'})
    elif idx==5:
        bridge=st.radio('Rectifier',['Half-wave','Bridge'],horizontal=True,key=f'{idx}-rectifier')=='Bridge'
        v=number('Secondary RMS voltage (V)',6);f=number('Supply frequency (Hz)',50);rl=number('Load resistance (Ω)',1000)
        cap=st.select_slider('Filter capacitance (µF)',[0,10,47,100,470,1000],value=100,key=f'{idx}-filter-uF')*1e-6
        t,vi,vo=rectifier(v,f,rl,cap,bridge);dc=vo.mean();rms=np.sqrt(np.mean(vo**2));ac=np.sqrt(max(rms*rms-dc*dc,0))
        df=pd.DataFrame({'Time (ms)':t*1000,'Input (V)':vi,'Output (V)':vo})
        metrics({'DC output':f'{dc:.3f} V','Ripple factor':f'{ac/dc:.4f}' if dc>0 else 'undefined','Ripple p-p':f'{np.ptp(vo):.3f} V'})
        st.caption('Fixed 0.7 V per conducting diode; ideal transformer/source, exponential load discharge. Metrics use the final three of 30 cycles. Source resistance and surge current excluded.')
        chart(df,'Time (ms)',['Input (V)','Output (V)'])
    elif idx==6:
        beta=number('DC gain β',100);mode=st.radio('Characteristic',['Output','Input'],horizontal=True,key=f'{idx}-characteristic')
        if mode=='Output':
            ib=number('Base current step (µA)',10)*1e-6;vce=np.linspace(0,10,200)
            df=pd.DataFrame({'VCE (V)':vce})
            for k in range(1,6):df[f'IC at IB={ib*k*1e6:g} µA (mA)']=bjt(vce,ib*k,beta)*1000
            chart(df,'VCE (V)',list(df.columns[1:]))
            st.caption('Teaching output model: β·IB, linear knee to 0.2 V, Early voltage 100 V. Not a fitted transistor model.')
        else:
            vbe=np.linspace(0,.75,240);ib=1e-14*np.expm1(vbe/.02585)/beta
            df=pd.DataFrame({'VBE (V)':vbe,'IB (µA)':ib*1e6});chart(df,'VBE (V)',['IB (µA)'])
            st.caption('Ideal exponential junction at 300 K; collector saturation current 10 fA; IB = IC/β.')
    elif idx==7:
        vcc=number('VCC (V)',12);ic=number('Quiescent collector current (mA)',2)*1e-3
        rcval=number('Collector resistance (kΩ)',2.2)*1000;re=number('Unbypassed emitter resistance (Ω)',100,minv=0)
        rl=number('Load resistance (kΩ)',22)*1000;fl=number('Lower cutoff (Hz)',50);fh=number('Upper cutoff (Hz)',100000)
        if fh<=fl:st.error('Upper cutoff must exceed lower cutoff.');st.stop()
        vceq=vcc-ic*(rcval+re)
        if vceq<=.2:st.error('Bias is saturated in this approximation. Reduce IC or resistance, or increase VCC.');st.stop()
        gain=-(1/(1/rcval+1/rl))/(.02585/ic+re)
        f=np.geomspace(fl/20,fh*20,400);h=gain*(1j*f/fl)/(1+1j*f/fl)/(1+1j*f/fh)
        df=pd.DataFrame({'Frequency (Hz)':f,'Gain (dB)':20*np.log10(abs(h))})
        metrics({'Midband gain':f'{gain:.2f} V/V','Approx. VCEQ':f'{vceq:.2f} V','Nominal bandwidth':f'{fh-fl:g} Hz'})
        chart(df,'Frequency (Hz)',['Gain (dB)'],True)
        vin=number('Input peak amplitude (mV)',10)*1e-3;freq=number('Input frequency (Hz)',1000)
        tt=np.linspace(0,3/freq,500);hf=gain*(1j*freq/fl)/(1+1j*freq/fl)/(1+1j*freq/fh)
        out=np.clip(abs(hf)*vin*np.sin(2*np.pi*freq*tt+np.angle(hf)),.2-vceq,vcc-vceq)
        chart(pd.DataFrame({'Time (ms)':tt*1000,'Input (V)':vin*np.sin(2*np.pi*freq*tt),'Output AC (V)':out}),'Time (ms)',['Input (V)','Output AC (V)'])
        st.caption('Small-signal CE approximation with independently chosen single-pole cutoff frequencies and approximate rail clipping. Bias-divider, capacitor sizing and full device nonlinearities are not solved.')
    elif idx==8:
        r=number('Equal-section resistance (kΩ)',4.7)*1000;c=number('Equal-section capacitance (nF)',10)*1e-9
        gain=number('Amplifier gain magnitude',35);f0=1/(2*np.pi*r*c*np.sqrt(6))
        st.latex(r'f_0\approx\frac{1}{2\pi RC\sqrt{6}},\quad |A|\geq29')
        metrics({'Approx. frequency':f'{f0:.2f} Hz','Ideal loop gain':f'{gain/29:.3f}'})
        st.caption('Equal-component, unloaded-network approximation. BJT input/output loading changes frequency and required gain. Waveform is an illustrative ideal sinusoid, not a transient startup solution.')
        if gain<=29:st.warning('No startup margin in the ideal model. Gain greater than 29 is normally needed to start; nonlinear limiting then sets amplitude.')
        t=np.linspace(0,5/f0,500);df=pd.DataFrame({'Time (ms)':t*1000,'Normalized illustrative output':np.sin(2*np.pi*f0*t) if gain>29 else np.zeros_like(t)})
        chart(df,'Time (ms)',['Normalized illustrative output'])
    else:
        idss=number('IDSS (mA)',10)*1e-3;vp=-number('|VGS(off)| (V)',4);vdd=number('Drain supply (V)',5);rd=number('Drain resistor (Ω)',1000)
        vg=st.slider('Gate-source voltage (V)',float(vp-1),0.,0.,.1,key=f'{idx}-VGS')
        vds=np.linspace(0,vdd,400);idcurve=jfet(vds,vg,idss,vp);load=(vdd-vds)/rd
        # Bisection intersection of device characteristic and load line.
        lo=0.;hi=vdd
        for _ in range(70):
            mid=(lo+hi)/2
            if float(jfet(np.array(mid),vg,idss,vp))>(vdd-mid)/rd:hi=mid
            else:lo=mid
        op=(lo+hi)/2;current=(vdd-op)/rd
        df=pd.DataFrame({'VDS (V)':vds,'Device ID (mA)':idcurve*1000,'Load-line current (mA)':load*1000})
        metrics({'Operating VDS':f'{op:.3f} V','Drain current':f'{current*1000:.3f} mA','State':'Cutoff' if vg<=vp else ('Ohmic / on' if op<vg-vp else 'Saturation')})
        chart(df,'VDS (V)',['Device ID (mA)','Load-line current (mA)'])
        st.caption('Square-law n-channel JFET with ohmic and saturation regions; no channel-length modulation. VGS = 0 turns the device on; VGS ≤ VGS(off) cuts it off.')
    st.download_button('Download simulated data (CSV)',df.to_csv(index=False).encode(),f'experiment_{idx+1}_simulated.csv','text/csv')
with record:
    st.caption('Enter bench measurements here. These are separate from simulated data. Download your record before closing the browser; no server database is used.')
    defaults=pd.DataFrame({'Reading':range(1,6),'Independent value':[0.]*5,'Measured value':[0.]*5,'Theoretical value':[0.]*5})
    units=st.text_input('Quantities and units (e.g. load Ω, power mW)',key=f'units{idx}')
    obs=st.data_editor(defaults,num_rows='dynamic',key=f'obs{idx}',use_container_width=True)
    calc=obs.copy();den=pd.to_numeric(calc['Theoretical value'],errors='coerce').replace(0,np.nan)
    calc['Absolute relative error (%)']=abs((pd.to_numeric(calc['Measured value'],errors='coerce')-den)/den)*100
    st.dataframe(calc,use_container_width=True)
    st.caption('Relative error is undefined when the theoretical value is zero.')
    conclusion=st.text_area('Interpretation / conclusion',key=f'conclusion{idx}')
    esc=lambda s:html.escape(str(s))
    report=f'<!doctype html><html><head><meta charset="utf-8"><title>Lab record</title><style>body{{font:16px Arial;max-width:1000px;margin:40px auto}}table{{border-collapse:collapse}}td,th{{border:1px solid #aaa;padding:8px}}</style></head><body><h1>Electronic Devices & Circuits Lab</h1><p>PSG Institute of Technology and Applied Research</p><h2>{idx+1}. {esc(NAMES[idx])}</h2><p>{esc(student)} | {esc(reg)} | {esc(section)}</p><h3>Aim</h3><p>{esc(AIMS[idx])}</p><h3>Bench observations</h3><p>{esc(units)}</p>{calc.to_html(index=False)}<h3>Interpretation</h3><p>{esc(conclusion)}</p><h3>Simulation snapshot (first 20 rows)</h3><p>Educational model, not measured data. Parameters are listed below.</p>{df.head(20).to_html(index=False)}<h3>Model settings</h3><pre>{esc(json.dumps({k:v for k,v in st.session_state.items() if k.startswith(str(idx)+"-")},indent=2,default=str))}</pre><p>Faculty signature: ____________________</p></body></html>'
    st.download_button('Download lab record (HTML · print to PDF)',report.encode(),f'experiment_{idx+1}_record.html','text/html')
    st.download_button('Download bench observations (CSV)',calc.to_csv(index=False).encode(),f'experiment_{idx+1}_measured.csv','text/csv')
with viva:
    st.write('Discuss these questions with your lab partner and faculty:')
    for q in QUESTIONS[idx]:st.write('• '+q)
    st.text_area('Your reasoning',key=f'viva{idx}')
with manual:
    st.caption('Original supplied material. Numbering in the source manuals differs from the syllabus; the app follows the syllabus sequence. Where a source contains a simplification or typo, the simulator uses its stated model.')
    selected=st.selectbox('Supplied manual',list(manuals))
    info=manuals[selected]
    st.download_button('Download original manual',(ROOT/info['file']).read_bytes(),Path(info['file']).name)
    with st.expander('Extracted text (equations and tables may be omitted)'):st.text(info.get('text','See original PDF.'))
    for asset in info.get('images',[]):st.image(str(ROOT/asset),caption='Figure extracted from supplied manual; consult original for context.')
    st.download_button('Download course syllabus',(ROOT/'assets/syllabus.pdf').read_bytes(),'25IC111_syllabus.pdf')
st.divider()
st.caption('Department of Electrical and Electronics Engineering · Student learning and laboratory preparation')
