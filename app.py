import math
import matplotlib.pyplot as plt
import streamlit as st

st.title('RLC Circuit Simulator')
st.markdown('### Runge-Kutta 4th Order (RK4) Numerical Analysis')

# Session State Setup
if 'simulated' not in st.session_state:
    st.session_state.simulated=False

# Getting inputs
st.sidebar.header('⚫ Circuit Parameters')
R_input=st.sidebar.number_input('◾ Resistance (Ohms)',value=10.0)
L_input=st.sidebar.number_input('◾ Inductance (mH)',value=10.0)
C_input=st.sidebar.number_input('◾ Capacitance (uF)',value=10.0)

V_input=st.sidebar.selectbox('◾ Type of voltage source',['DC','AC'])

if V_input=='AC':
    V_m=st.sidebar.number_input('◾ Peak voltage (V)',value=5.0)
    f=st.sidebar.number_input('◾ Frequency (Hz)',value=50.0)
    omega=2*math.pi*f


    def V_source(t):
        return V_m*math.sin(omega*t)

elif V_input=='DC':
    V=st.sidebar.number_input('◾ Source Voltage (V)',value=5.0)


    def V_source(t):
        return V

if st.sidebar.button('Run Simulation'):

    # Convert units to SI units
    R=R_input
    L=L_input*1e-3
    C=C_input*1e-6


    # ODE for q(t)
    def f1(t,q,i):
        return i


    # ODE for i(t)
    def f2(t,q,i):
        return (1/L)*(V_source(t)-i*R-q/C)


    t_array=[0]
    i_array=[0]
    q_array=[0]

    q=i=t=0

    # Set Dynamic Time for both AC and DC cases
    if V_input=='AC':
        t_end=20*(1/f)
        h=min(t_end/5000,1e-6)
    elif V_input=='DC':
        tau_RL=(2*L)/R
        tau_RC=R*C
        T_n=2*math.pi*math.sqrt(L*C)
        t_end=max(5*tau_RL,5*tau_RC,5*T_n)
        h=min(t_end/5000,1e-6)

    # Apply RK4 method
    with st.spinner('Calculating Data...'):
        while t<=t_end:
            kq1=h*f1(t,q,i)
            ki1=h*f2(t,q,i)

            kq2=h*f1(t+h/2,q+kq1/2,i+ki1/2)
            ki2=h*f2(t+h/2,q+kq1/2,i+ki1/2)

            kq3=h*f1(t+h/2,q+kq2/2,i+ki2/2)
            ki3=h*f2(t+h/2,q+kq2/2,i+ki2/2)

            kq4=h*f1(t+h,q+kq3,i+ki3)
            ki4=h*f2(t+h,q+kq3,i+ki3)

            q=q+(kq1+2*kq2+2*kq3+kq4)/6
            i=i+(ki1+2*ki2+2*ki3+ki4)/6
            t=t+h
            t_array.append(t)
            q_array.append(q)
            i_array.append(i)

    # Store calculated data in session state memory
    st.session_state.t_list=[t*1000 for t in t_array]
    st.session_state.vc_list=[q/C for q in q_array]
    st.session_state.i_list=[i*1000 for i in i_array]
    st.session_state.simulated=True

# --- Display UI after calculation is complete ---
if st.session_state.simulated:

    t_list=st.session_state.t_list
    vc_list=st.session_state.vc_list
    i_list=st.session_state.i_list

    # --- Single Cycle Peak Detection Method ---
    if V_input=='AC':
        T=1/f
        T_ms=T*1000

        h_ms=t_list[1]-t_list[0]
        points_per_cycle=int(T_ms/h_ms)

        vc_last_cycle=vc_list[-points_per_cycle:]
        i_last_cycle=i_list[-points_per_cycle:]
        t_last_cycle=t_list[-points_per_cycle:]

        vs_last_cycle=[V_source(t/1000) for t in t_last_cycle]

        vs_peak=max(vs_last_cycle)
        vc_peak=max(vc_last_cycle)
        i_peak=max(i_last_cycle)

        ind_vs=vs_last_cycle.index(vs_peak)
        ind_i=i_last_cycle.index(i_peak)

        delta_t=abs(t_last_cycle[ind_vs]-t_last_cycle[ind_i])/1000
        phase_shift=(delta_t/T)*360

    elif V_input=='DC':
        vc_peak=max(vc_list)
        i_peak=max(i_list)
        phase_shift=0

    # Plotting Key Measurements
    st.subheader('⚫ Key Measurements')
    col1,col2,col3=st.columns(3)

    col1.metric('Peak Voltage (Vc)',f'{vc_peak:.3f} V')
    col2.metric('Peak Current (Ic)',f'{i_peak:.3f} mA')

    if V_input=='AC':
        col3.metric('Phase Shift',f'{phase_shift:.2f}°')
    else:
        col3.metric('Phase Shift','N/A')

    st.markdown('---')

    # --- Final Static Matplotlib Graph ---
    # Calculate fixed Y-axis padding
    v_max=max(vc_list)
    v_min=min(vc_list)
    i_max=max(i_list)
    i_min=min(i_list)
    v_pad=(v_max-v_min)*0.1 if v_max!=v_min else 1.0
    i_pad=(i_max-i_min)*0.1 if i_max!=i_min else 1.0

    fig,ax1=plt.subplots(figsize=(10,6))
    ax1.set_xlim(0,t_list[-1])
    ax1.set_ylim(v_min-v_pad,v_max+v_pad)

    ax1.set_xlabel('Time(ms)',fontsize=12)
    ax1.set_ylabel('Capacitor Voltage(V)',color='blue',fontsize=12)
    ax1.plot(t_list,vc_list,color='blue',linewidth=1.5,label='Voltage(V)')
    ax1.tick_params(axis='y',labelcolor='blue')
    ax1.grid(True,linestyle='--',alpha=0.7)

    ax2=ax1.twinx()
    ax2.set_ylim(i_min-i_pad,i_max+i_pad)
    ax2.set_ylabel('Circuit Current(mA)',color='red',fontsize=12)
    ax2.plot(t_list,i_list,color='red',linewidth=1.5,label='Current(mA)')
    ax2.tick_params(axis='y',labelcolor='red')

    fig.subplots_adjust(top=0.9)
    plt.title('RLC Circuit: Voltage and Current Overlay',fontsize=14,pad=15)
    fig.tight_layout()

    st.pyplot(fig)
    plt.close(fig)
