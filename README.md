# ⚡ RLC Circuit Simulator using Runge-Kutta 4th Order (RK4)

An interactive, web-based RLC circuit simulator built with Python and Streamlit. This tool bridges the gap between complex differential equations and real-world circuit analysis by numerically solving the circuit's transient and steady-state behaviors using the RK4 mathematical algorithm.

## 🚀 Features
* **Instant Waveform Visualization:** Instantly generates high-quality static plots of capacitor voltage and circuit current, optimized for fast and seamless performance on cloud deployments.
* **AC & DC Source Support:** Analyzes both transient responses (Overdamped, Underdamped, Critically Damped) for DC and steady-state responses (Resonance, Inductive, Capacitive) for AC.
* **Single-Cycle Peak Detection:** Implements precise phase-shift and peak-value calculations using DSP techniques.
* **Dynamic Time Scaling:** Automatically calculates the optimal simulation timeframe based on the natural frequency and RC/RL time constants.

## 🛠️ Tech Stack
* **Language:** Python
* **UI Framework:** Streamlit
* **Data Visualization:** Matplotlib (Static Plotting)
* **Mathematical Core:** Custom Runge-Kutta 4 (RK4) implementation for solving ordinary differential equations (ODEs).

## 💡 How to Run Locally
1. Clone this repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `streamlit run app.py`
