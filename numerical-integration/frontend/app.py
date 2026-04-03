import streamlit as st
import requests
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Config
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Numerical Integration Solver", layout="wide")

st.title("📈 Numerical Integration Solver")
st.markdown("Compute the definite integral of mathematical functions using various numerical methods.")

# Modern UI Styles
st.markdown("""
<style>
    /* Hide Streamlit default header, footer, and menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden !important; display: none !important;}
    .stDeployButton {display: none !important;}

    /* Premium Typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Main background */
    .stApp {
        background: radial-gradient(circle at top left, #e0c3fc 0%, #8ec5fc 100%);
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.4);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.4);
    }
    
    /* Gradient Title */
    h1 {
        background: -webkit-linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3rem !important;
        animation: fadeInDown 0.8s ease-out;
    }

    /* Styling action buttons */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        color: white;
        padding: 0.6rem 2rem;
        border-radius: 50px;
        font-size: 1rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(118, 75, 162, 0.4);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) 0s;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton>button:hover {
        box-shadow: 0 10px 25px rgba(118, 75, 162, 0.6);
        transform: translateY(-4px) scale(1.02);
        color: white;
    }

    /* Inputs Focus Effects */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        border-radius: 10px;
        border: 2px solid transparent;
        background: rgba(255, 255, 255, 0.8);
        transition: all 0.3s ease;
    }
    .stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus {
        border-color: #764ba2;
        background: white;
        box-shadow: 0 0 0 3px rgba(118, 75, 162, 0.2);
    }

    /* Styling metric cards with Glassmorphism */
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.65);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.6);
        padding: 10%;
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);
        transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-8px) scale(1.03);
        border: 1px solid rgba(255, 255, 255, 0.8);
    }

    /* Keyframes */
    @keyframes fadeInDown {
        0% { opacity: 0; transform: translateY(-20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for inputs
with st.sidebar:
    st.header("Input Parameters")
    function_input = st.text_input("Mathematical Function f(x)", value="x**2 + sin(x)")
    col1, col2 = st.columns(2)
    with col1:
        a_input = st.number_input("Lower Bound (a)", value=0.0, format="%f")
    with col2:
        b_input = st.number_input("Upper Bound (b)", value=2.0, format="%f")
        
    method_input = st.selectbox("Numerical Method", ["Trapezoidal", "Simpson", "Gaussian"])
    n_input = st.slider("Number of Subintervals (n)", min_value=2, max_value=1000, value=10, step=2)

st.header("Actions")
col_compute, col_compare = st.columns(2)

if col_compute.button("Compute Integral", type="primary"):
    if b_input <= a_input:
        st.error("Upper bound 'b' must be greater than lower bound 'a'.")
    else:
        payload = {
            "function": function_input,
            "a": a_input,
            "b": b_input,
            "method": method_input.lower(),
            "n": n_input
        }
        with st.spinner("Computing..."):
            try:
                response = requests.post(f"{API_URL}/integrate", json=payload)
                if response.status_code == 200:
                    data = response.json()
                    res_val = data.get('result')
                    res_str = f"{res_val:.10f}" if res_val is not None else "Undefined (NaN/Inf)"
                    st.success(f"**Result ({method_input}):** {res_str}")
                    
                    # Graphing
                    x_vals = np.array(data['x'], dtype=float)
                    y_vals = np.array(data['y'], dtype=float)
                    
                    fig, ax = plt.subplots(figsize=(10, 5))
                    
                    # Beautiful modern plotting style
                    ax.plot(x_vals, y_vals, label=f"f(x) = {function_input}", color="#764ba2", linewidth=2.5)
                    ax.fill_between(x_vals, y_vals, alpha=0.25, color="#667eea")
                    
                    # Text styling
                    ax.set_title(f"Integration Profile from {a_input} to {b_input}", fontsize=16, fontweight='bold', color='#2d3748', pad=15)
                    ax.set_xlabel("x axis", fontsize=12, fontweight='bold', color="#4a5568")
                    ax.set_ylabel("f(x)", fontsize=12, fontweight='bold', color="#4a5568")
                    
                    # Legend and Grid
                    ax.legend(frameon=True, fancybox=True, shadow=True, framealpha=0.9, borderpad=1, loc='best')
                    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.6, color="#a0aec0")
                    
                    # Remove harsh borders
                    ax.spines['top'].set_visible(False)
                    ax.spines['right'].set_visible(False)
                    ax.spines['left'].set_color('#cbd5e1')
                    ax.spines['bottom'].set_color('#cbd5e1')
                    
                    # White chart area, transparent background outline
                    fig.patch.set_facecolor('none')
                    ax.set_facecolor('#ffffff')
                    
                    st.pyplot(fig)
                else:
                    st.error(f"Error {response.status_code}: {response.json().get('detail', 'Unknown error')}")
            except requests.exceptions.ConnectionError:
                st.error("Connection Error: Is the FastAPI backend running on port 8000? Try starting it with `uvicorn backend.main:app --reload`")

if col_compare.button("Compare Methods"):
    if b_input <= a_input:
        st.error("Upper bound 'b' must be greater than lower bound 'a'.")
    else:
        payload = {
            "function": function_input,
            "a": a_input,
            "b": b_input,
            "method": "trapezoidal", # Ignored by backend for compare
            "n": n_input
        }
        with st.spinner("Comparing..."):
            try:
                response = requests.post(f"{API_URL}/compare", json=payload)
                if response.status_code == 200:
                    data = response.json()
                    st.subheader("Comparison Results")
                    col1, col2, col3 = st.columns(3)
                    
                    def fmt_val(v):
                        return f"{v:.10f}" if v is not None else "Undefined"
                        
                    col1.metric("Trapezoidal Rule", fmt_val(data.get('trapezoidal')))
                    col2.metric("Simpson's Rule", fmt_val(data.get('simpson')))
                    col3.metric("Gaussian Quad.", fmt_val(data.get('gaussian')))
                    
                    # Highlight if they are all close to each other
                    valid_vals = [v for v in data.values() if isinstance(v, (int, float))]
                    if valid_vals:
                        spread = max(valid_vals) - min(valid_vals)
                        st.info(f"The maximum difference between valid methods is **{spread:e}**.")
                    else:
                        st.warning("All methods returned Undefined due to a mathematical singularity or out-of-bounds error.")
                else:
                    st.error(f"Error {response.status_code}: {response.json().get('detail', 'Unknown error')}")
            except requests.exceptions.ConnectionError:
                st.error("Connection Error: Is the FastAPI backend running on port 8000?")
