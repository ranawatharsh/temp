import streamlit as st
import pandas as pd
import plotly.express as px
import json
import requests
import time
from datetime import datetime

# --- CONFIGURATION & STYLING ---
st.set_page_config(page_title="AuraFit | AI Fitness & Nutrition", page_icon="🌿", layout="wide")

# Custom CSS for a premium, modern look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3em;
        background-color: #2D3436;
        color: white;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #0984e3;
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    
    .card {
        padding: 1.5rem;
        border-radius: 20px;
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
        margin-bottom: 1rem;
    }
    
    .hero-text {
        font-size: 4rem;
        font-weight: 800;
        background: -webkit-linear-gradient(#2D3436, #0984e3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.2;
        margin-bottom: 1rem;
    }

    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: block;
    }

    .metric-card {
        text-align: center;
        padding: 1rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #0984e3;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #636e72;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'page' not in st.session_state:
    st.session_state.page = "Home"
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# --- API UTILITIES ---
const_api_key = "" # Execution environment provides the key

def call_gemini(prompt, system_instruction="You are a professional fitness coach and nutritionist."):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={const_api_key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "systemInstruction": {"parts": [{"text": system_instruction}]}
    }
    
    for delay in [1, 2, 4, 8, 16]:
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                result = response.json()
                return result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', "Error generating content.")
        except:
            time.sleep(delay)
    return "The AI is currently resting. Please try again in a moment."

# --- UI COMPONENTS ---

def home_page():
    # Hero Section
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown("<div style='padding-top: 50px;'>", unsafe_allow_html=True)
        st.markdown("<h1 class='hero-text'>Elevate Your Being with AuraFit</h1>", unsafe_allow_html=True)
        st.markdown("""
            <p style='font-size: 1.2rem; color: #636e72; margin-bottom: 2rem;'>
                The world's most intuitive AI-powered health sanctuary. 
                Personalized nutrition, adaptive workouts, and mental wellness 
                tracking designed specifically for your unique biology.
            </p>
        """, unsafe_allow_html=True)
        
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("Start Your Journey"):
                st.session_state.page = "Login"
                st.rerun()
        with btn_col2:
            st.markdown("<button style='width:100%; border-radius:12px; height:3em; background-color:transparent; color:#2D3436; border:2px solid #2D3436; font-weight:600;'>Watch Demo</button>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        # Abstract UI Representation or Image
        st.markdown("""
            <div class='card' style='margin-top: 50px; text-align: center; padding: 3rem;'>
                <span style='font-size: 5rem;'>🌿</span>
                <h3 style='margin-top: 1rem;'>AI Wellness Core</h3>
                <p style='color: #636e72;'>Scanning Vitality...</p>
                <div style='height: 10px; background: #dfe6e9; border-radius: 5px; overflow: hidden;'>
                    <div style='width: 75%; height: 100%; background: #0984e3;'></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    # Features Section
    f1, f2, f3 = st.columns(3)
    with f1:
        st.markdown("""
            <div class='card'>
                <span class='feature-icon'>🥗</span>
                <h4>AI Smart Nutrition</h4>
                <p style='font-size: 0.9rem; color: #636e72;'>Chef-quality meal plans that adapt to your allergies, diseases, and goals instantly.</p>
            </div>
        """, unsafe_allow_html=True)
    with f2:
        st.markdown("""
            <div class='card'>
                <span class='feature-icon'>⚡</span>
                <h4>Dynamic Workouts</h4>
                <p style='font-size: 0.9rem; color: #636e72;'>From pregnancy-safe yoga to elite strength training, our AI builds what you need today.</p>
            </div>
        """, unsafe_allow_html=True)
    with f3:
        st.markdown("""
            <div class='card'>
                <span class='feature-icon'>🧠</span>
                <h4>Sentimental Analysis</h4>
                <p style='font-size: 0.9rem; color: #636e72;'>We don't just track weights; we track how you feel to keep your motivation indestructible.</p>
            </div>
        """, unsafe_allow_html=True)

def login_page():
    st.markdown("<h1 style='text-align: center; margin-top: 2rem;'>🌿 Welcome Back</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            tab1, tab2 = st.tabs(["Login", "Sign Up"])
            
            with tab1:
                st.text_input("Email", key="login_email")
                st.text_input("Password", type="password", key="login_pass")
                if st.button("Let's Go"):
                    st.session_state.authenticated = True
                    st.session_state.page = "Onboarding"
                    st.rerun()
                if st.button("← Back to Home", key="back_home_l"):
                    st.session_state.page = "Home"
                    st.rerun()
            
            with tab2:
                st.text_input("Full Name", key="signup_name")
                st.text_input("Email", key="signup_email")
                st.text_input("Create Password", type="password")
                if st.button("Create Account"):
                    st.success("Account created! Please login.")
            st.markdown('</div>', unsafe_allow_html=True)

def onboarding_page():
    st.markdown("## 📋 Personalize Your Experience")
    st.info("Help our AI understand your body to create the perfect plan.")
    
    with st.form("onboarding_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Display Name", placeholder="e.g. Alex")
            age = st.number_input("Age", min_value=15, max_value=100, value=25)
            gender = st.selectbox("Gender", ["Male", "Female", "Other", "Prefer not to say"])
            weight = st.number_input("Current Weight (kg)", min_value=30.0, value=70.0)
            height = st.number_input("Height (cm)", min_value=100.0, value=170.0)
            goal_weight = st.number_input("Target Weight (kg)", min_value=30.0, value=65.0)
        
        with col2:
            is_pregnant = False
            pregnancy_month = 0
            if gender == "Female":
                is_pregnant = st.checkbox("Are you pregnant?")
                if is_pregnant:
                    pregnancy_month = st.slider("Which month?", 1, 9, 1)
            
            diseases = st.multiselect("Medical Conditions", ["Diabetes", "Hypertension", "PCOS", "Thyroid", "Heart Condition", "None"])
            allergies = st.text_area("Food Allergies", placeholder="e.g. Peanuts, Dairy, Gluten...")
            activity_level = st.select_slider("Current Activity Level", options=["Sedentary", "Lightly Active", "Moderate", "Very Active", "Athlete"])
        
        # BMI Calculation
        bmi = round(weight / ((height/100)**2), 2)
        
        submit = st.form_submit_button("Generate My AI Plan")
        if submit:
            st.session_state.user_data = {
                "name": name, "age": age, "gender": gender, "weight": weight, 
                "height": height, "bmi": bmi, "goal": goal_weight, 
                "pregnant": is_pregnant, "month": pregnancy_month,
                "conditions": diseases, "allergies": allergies, "activity": activity_level
            }
            st.session_state.page = "Dashboard"
            st.rerun()

def dashboard_page():
    data = st.session_state.user_data
    
    # Sidebar Navigation
    with st.sidebar:
        st.markdown(f"### Welcome, {data.get('name', 'User')}!")
        nav = st.radio("Navigation", ["Overview", "Diet Plan", "Workout Plan", "Progress", "AI Chatbot"])
        st.divider()
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.page = "Home"
            st.rerun()

    if nav == "Overview":
        st.markdown(f"## Dashboard Overview")
        
        # Metrics Row
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f'<div class="card metric-card"><div class="metric-label">Current BMI</div><div class="metric-value">{data["bmi"]}</div></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="card metric-card"><div class="metric-label">Target</div><div class="metric-value">{data["goal"]}kg</div></div>', unsafe_allow_html=True)
        with m3:
            st.markdown(f'<div class="card metric-card"><div class="metric-label">Status</div><div class="metric-value">{"Healthy" if 18.5 <= data["bmi"] <= 24.9 else "Action Needed"}</div></div>', unsafe_allow_html=True)
        with m4:
            st.markdown(f'<div class="card metric-card"><div class="metric-label">Activity</div><div class="metric-value" style="font-size:1.2rem">{data["activity"]}</div></div>', unsafe_allow_html=True)

        # History and Feedback
        col_left, col_right = st.columns([2, 1])
        with col_left:
            st.markdown('<div class="card"><h3>Weight History</h3>', unsafe_allow_html=True)
            chart_data = pd.DataFrame({
                'Date': pd.date_range(start='2024-01-01', periods=10, freq='W'),
                'Weight': [data['weight']+i for i in [5, 4, 4.5, 3, 2, 1, 0.5, 0, -0.5, -1]]
            })
            fig = px.line(chart_data, x='Date', y='Weight', template="plotly_white", markers=True)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_right:
            st.markdown('<div class="card"><h3>Daily Mood Check</h3>', unsafe_allow_html=True)
            mood_input = st.text_input("How are you feeling today?")
            if mood_input:
                analysis = call_gemini(f"Analyze the sentiment of this text and give a brief motivational response: {mood_input}")
                st.write(analysis)
            st.markdown('</div>', unsafe_allow_html=True)

    elif nav == "Diet Plan":
        st.markdown("## 🥗 Personalized AI Diet Plan")
        if st.button("Regenerate Plan"):
            with st.spinner("Analyzing nutritional needs..."):
                prompt = f"Create a 7-day diet plan for a {data['age']} year old {data['gender']} weighing {data['weight']}kg. Goal: Reach {data['goal']}kg. Conditions: {data['conditions']}. Allergies: {data['allergies']}. Pregnancy status: {data['pregnant']} (Month {data['month']})."
                st.session_state.diet_plan = call_gemini(prompt)
        
        if 'diet_plan' in st.session_state:
            st.markdown(st.session_state.diet_plan)
        else:
            st.write("Click the button to generate your custom meal plan.")

    elif nav == "Workout Plan":
        st.markdown("## 🏃‍♂️ Custom Workout Schedule")
        if st.button("Generate Exercise Routine"):
            with st.spinner("Designing workouts..."):
                prompt = f"Design a weekly workout plan for a {data['gender']} with a BMI of {data['bmi']}. Activity level: {data['activity']}. Medical conditions: {data['conditions']}. Pregnancy: {data['pregnant']} (Month {data['month']}). Focus on achieving a target weight of {data['goal']}kg."
                st.session_state.workout_plan = call_gemini(prompt)
        
        if 'workout_plan' in st.session_state:
            st.markdown(st.session_state.workout_plan)
        else:
            st.write("Your AI coach is ready to build your routine.")

    elif nav == "Progress":
        st.markdown("## 📈 Progress Tracking")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Monthly Schedule")
            # Simplified Calendar Mockup
            days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            weeks = [st.columns(7) for _ in range(4)]
            for r, week in enumerate(weeks):
                for c, day_col in enumerate(week):
                    day_num = r*7 + c + 1
                    if day_num <= 31:
                        with day_col:
                            status = "✅" if day_num % 3 == 0 else "⭕"
                            st.write(f"**{day_num}**")
                            st.caption(status)
        
        with col2:
            st.subheader("Input Latest Stats")
            st.number_input("Update Weight", value=data['weight'])
            st.text_area("Notes/Feedback", placeholder="How did this month feel?")
            st.button("Save Entry")

    elif nav == "AI Chatbot":
        st.markdown("## 💬 AuraFit Assistant")
        st.caption("Ask anything about fitness, nutrition, or your plan.")
        
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
        
        if prompt := st.chat_input("Ask me something..."):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)
            
            with st.chat_message("assistant"):
                response = call_gemini(prompt, system_instruction=f"You are AuraFit Assistant. Help the user based on their profile: {str(data)}")
                st.write(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})

# --- MAIN APP ROUTING ---
if st.session_state.page == "Home":
    home_page()
elif st.session_state.page == "Login":
    login_page()
elif st.session_state.authenticated:
    if st.session_state.page == "Onboarding":
        onboarding_page()
    else:
        dashboard_page()
else:
    # Fallback to Home if something goes wrong with auth state
    st.session_state.page = "Home"
    st.rerun()
