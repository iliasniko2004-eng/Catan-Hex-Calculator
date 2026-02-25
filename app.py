import streamlit as st
import pandas as pd
import base64

def set_background(png_file):
    with open(png_file, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{data}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background("background.png")

st.markdown("""
    <style>
    .big-title {
    font-size: 50px;
    font-weight: 800;
    text-align: center;
    font-family: 'MinionPro-SemiboldSubh', monospace;
    color: #B09213;
    text-shadow: 2px 2px 4px black;
}
.welcome-text {
    font-size: 18px;       
    font-weight: 400;
    text-align: center;
    color: #FFD700;         
    text-shadow: 1px 1px 2px black; 
    margin-bottom: 5px;
    }
    .label-big {
    font-size: 26px;
    font-weight: 800;
    font-family: 'Courier New', serif;
    color: #B09213;
    margin-top: 15px;
    text-shadow: 2px 2px 4px black;
    }
    .prob-text {
    font-size: 22px;
    display: inline-block;        
    font-weight: bold;
    color: white;
    text-shadow: 2px 2px 4px black;
}
            
     .big-font {
        font-size:40px !important;
        font-weight:700;
        text-align:center;
    }
    .result-box {
        padding:20px;
        border-radius:15px;
        border:3px solid black;
        text-align:center;
        font-size:28px;
        font-weight:bold;
    }
    </style>
""", unsafe_allow_html=True)

excel_path = "calculator_project.xlsx"

df = pd.read_excel(excel_path, sheet_name="App")

df = df.dropna(subset=["Number", "Odds"])

df["Number"] = df["Number"].astype(int)

odds = dict(zip(df["Number"], df["Odds"]))

st.markdown('<div class="welcome-text">Welcome to the Catan Hex Probability Calculator! You can use the calculator to see the odds of the dice for your hex vs the odds ' \
'of the other 2 hexes for brick,stones and there is also a calculator with 4 hexes for wheat,wood and sheep! It will help you determine the advantage of ' \
'capturing a specific hex with a settlement. Enjoy!! </div>', unsafe_allow_html=True)
st.markdown('<div class="big-title">🎲 Catan Hex Calculator</div>', unsafe_allow_html=True)

left_col, right_col = st.columns(2)

numbers = sorted([n for n in odds.keys() if n != 7])
numbers_with_none = ["None"] + numbers
tolerance = 0.00001

# --- LEFT MENU ---
with left_col:
    st.markdown('<div class="label-big">Your Hex</div>', unsafe_allow_html=True)
    your_hex = st.selectbox("", numbers, key="your_hex1")
    st.markdown('<div class="label-big">Opponent Hex 1</div>', unsafe_allow_html=True)
    hex1 = st.selectbox("", numbers_with_none, key="hex1")
    st.markdown('<div class="label-big">Opponent Hex 2</div>', unsafe_allow_html=True)
    hex2 = st.selectbox("", numbers_with_none, key="hex2")
    
    # Υπολογισμός
    sum_others = sum([odds[int(h)] for h in [hex1, hex2] if h != "None"])
    your_odd = odds[int(your_hex)]
    advantage = your_odd - sum_others
    
    st.markdown(f'<div class="prob-text">Your Hex Probability: {your_odd*100:.2f}%</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="prob-text">Sum of Opponents: {sum_others*100:.2f}%</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="prob-text">Advantage: {advantage*100:.2f}%</div>', unsafe_allow_html=True)
    
    if advantage > tolerance:
        st.markdown('<div class="result-box" style="background-color:#0f5132;">WIN 💦</div>', unsafe_allow_html=True)
    elif advantage < -tolerance:
        st.markdown('<div class="result-box" style="background-color:#842029;">LOSE 🔴</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="result-box" style="background-color:#664d03;">EVEN ⚖️</div>', unsafe_allow_html=True)

with right_col:
    st.markdown('<div class="label-big">Your Hex 1</div>', unsafe_allow_html=True)
    your_hex_a = st.selectbox("", numbers, key="your_hex_a")
    st.markdown('<div class="label-big">Your Hex 2</div>', unsafe_allow_html=True)
    your_hex_b = st.selectbox("", numbers_with_none, key="your_hex_b")
    st.markdown('<div class="label-big">Opponent Hex 1</div>', unsafe_allow_html=True)
    opp_hex_a = st.selectbox("", numbers_with_none, key="opp_hex_a")
    st.markdown('<div class="label-big">Opponent Hex 2</div>', unsafe_allow_html=True)
    opp_hex_b = st.selectbox("", numbers_with_none, key="opp_hex_b")
    
    your_total = sum([odds[int(h)] for h in [your_hex_a, your_hex_b] if h != "None"])
    opp_total = sum([odds[int(h)] for h in [opp_hex_a, opp_hex_b] if h != "None"])
    advantage2 = your_total - opp_total
    
    st.markdown(f'<div class="prob-text">Your Total Probability: {your_total*100:.2f}%</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="prob-text">Opponents Total: {opp_total*100:.2f}%</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="prob-text">Advantage: {advantage2*100:.2f}%</div>', unsafe_allow_html=True)
    
    if advantage2 > tolerance:
        st.markdown('<div class="result-box" style="background-color:#0f5132;">WIN 💦</div>', unsafe_allow_html=True)
    elif advantage2 < -tolerance:
        st.markdown('<div class="result-box" style="background-color:#842029;">LOSE 🔴</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="result-box" style="background-color:#664d03;">EVEN ⚖️</div>', unsafe_allow_html=True)