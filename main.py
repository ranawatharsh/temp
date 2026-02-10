import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

# --- CONFIGURATION ---
st.set_page_config(
    page_title="NutriVerse | AI-Powered Health",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- PREMIUM DESIGNER CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&family=Epilogue:wght@400;500;600;700;800;900&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    :root {
        --primary: #FF6B00;
        --primary-dark: #E85D00;
        --secondary: #FF8C42;
        --accent: #FFA500;
        --white: #FFFFFF;
        --black: #000000;
        --dark: #0A0A0A;
        --darker: #050505;
        --gray: #1A1A1A;
        --gray-light: #2A2A2A;
        --success: #FF6B00;
        --card-bg: rgba(255, 255, 255, 0.03);
        --border: rgba(255, 107, 0, 0.15);
    }
    
    /* Hide Streamlit */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    .stApp {
        background: #000000;
        font-family: 'Sora', sans-serif;
        overflow-x: hidden;
    }
    
    /* Animated Background */
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .animated-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(-45deg, #000000, #0A0A0A, #1A0A00, #0A0A0A);
        background-size: 400% 400%;
        animation: gradient-shift 15s ease infinite;
        z-index: -1;
    }
    
    /* Navbar */
    .navbar {
        position: sticky;
        top: 0;
        z-index: 1000;
        background: rgba(0, 0, 0, 0.95);
        backdrop-filter: blur(30px);
        border-bottom: 1px solid rgba(255, 107, 0, 0.2);
        padding: 1.2rem 4rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        animation: slideDown 0.8s ease;
    }
    
    @keyframes slideDown {
        from { transform: translateY(-100%); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .logo-icon {
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, #FF6B00, #FFA500);
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.8rem;
        box-shadow: 0 8px 32px rgba(255, 107, 0, 0.5);
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
    }
    
    .logo-text {
        font-family: 'Epilogue', sans-serif;
        font-size: 1.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FFFFFF, #FF6B00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
    }
    
    .nav-menu {
        display: flex;
        gap: 3rem;
        align-items: center;
    }
    
    .nav-link {
        color: rgba(255, 255, 255, 0.7);
        text-decoration: none;
        font-weight: 500;
        font-size: 0.95rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        padding: 0.5rem 0;
    }
    
    .nav-link::before {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 0;
        height: 2px;
        background: linear-gradient(90deg, var(--primary), var(--secondary));
        transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .nav-link:hover {
        color: white;
    }
    
    .nav-link:hover::before {
        width: 100%;
    }
    
    /* Hero Section */
    .hero {
        position: relative;
        padding: 8rem 4rem 6rem;
        overflow: hidden;
    }
    
    .hero-glow {
        position: absolute;
        width: 600px;
        height: 600px;
        border-radius: 50%;
        filter: blur(120px);
        opacity: 0.2;
        animation: glow-pulse 4s ease-in-out infinite;
    }
    
    .hero-glow-1 {
        top: -200px;
        left: -100px;
        background: var(--primary);
    }
    
    .hero-glow-2 {
        top: 100px;
        right: -100px;
        background: var(--secondary);
    }
    
    @keyframes glow-pulse {
        0%, 100% { opacity: 0.2; transform: scale(1); }
        50% { opacity: 0.3; transform: scale(1.1); }
    }
    
    .hero-grid {
        position: relative;
        display: grid;
        grid-template-columns: 1.2fr 1fr;
        gap: 6rem;
        max-width: 1400px;
        margin: 0 auto;
        align-items: center;
    }
    
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.6rem;
        background: rgba(255, 107, 0, 0.1);
        border: 1px solid rgba(255, 107, 0, 0.4);
        padding: 0.6rem 1.5rem;
        border-radius: 100px;
        font-size: 0.75rem;
        font-weight: 600;
        color: #FF6B00;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
        animation: fadeInUp 0.8s ease 0.2s both;
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .hero-title {
        font-family: 'Epilogue', sans-serif;
        font-size: 4.5rem;
        font-weight: 900;
        line-height: 1.1;
        color: white;
        margin-bottom: 1.5rem;
        animation: fadeInUp 0.8s ease 0.3s both;
    }
    
    .hero-gradient-text {
        background: linear-gradient(135deg, #FF6B00 0%, #FFA500 50%, #FFFFFF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .hero-description {
        font-size: 1.2rem;
        line-height: 1.8;
        color: rgba(255, 255, 255, 0.7);
        margin-bottom: 3rem;
        max-width: 600px;
        animation: fadeInUp 0.8s ease 0.4s both;
    }
    
    .hero-cta {
        display: flex;
        gap: 1.5rem;
        animation: fadeInUp 0.8s ease 0.5s both;
    }
    
    .hero-image-container {
        position: relative;
        animation: fadeInUp 0.8s ease 0.6s both;
    }
    
    .hero-card {
        background: linear-gradient(135deg, rgba(255, 107, 0, 0.1), rgba(255, 165, 0, 0.1));
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 107, 0, 0.2);
        border-radius: 30px;
        padding: 3rem;
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.5);
        transition: transform 0.4s ease;
    }
    
    .hero-card:hover {
        transform: translateY(-10px);
    }
    
    .hero-emojis {
        display: flex;
        justify-content: space-around;
        align-items: center;
        font-size: 5rem;
        animation: float 3s ease-in-out infinite;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary), var(--primary-dark));
        color: white;
        border: none;
        padding: 1.2rem 3rem;
        border-radius: 100px;
        font-weight: 700;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 10px 30px rgba(255, 107, 53, 0.4);
        font-family: 'Sora', sans-serif;
        letter-spacing: 0.5px;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 50%;
        transform: translate(-50%, -50%);
        transition: width 0.6s ease, height 0.6s ease;
    }
    
    .stButton > button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 20px 50px rgba(255, 107, 53, 0.5);
    }
    
    /* Stats Section */
    .stats-section {
        padding: 2rem 4rem;
        margin-top: -3rem;
        position: relative;
        z-index: 10;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 2rem;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    .stat-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 2.5rem 2rem;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    
    .stat-card:hover::before {
        opacity: 0.1;
    }
    
    .stat-card:hover {
        transform: translateY(-10px);
        border-color: rgba(255, 107, 53, 0.4);
        box-shadow: 0 20px 50px rgba(255, 107, 53, 0.2);
    }
    
    .stat-number {
        font-family: 'Epilogue', sans-serif;
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FF6B00, #FFA500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        position: relative;
    }
    
    .stat-label {
        font-size: 0.95rem;
        color: rgba(255, 255, 255, 0.6);
        font-weight: 500;
        letter-spacing: 0.5px;
        position: relative;
    }
    
    /* Features Section */
    .section {
        padding: 8rem 4rem;
        position: relative;
    }
    
    .section-header {
        text-align: center;
        max-width: 700px;
        margin: 0 auto 5rem;
    }
    
    .section-badge {
        display: inline-block;
        background: rgba(255, 107, 0, 0.1);
        border: 1px solid rgba(255, 107, 0, 0.4);
        color: #FF6B00;
        padding: 0.5rem 1.2rem;
        border-radius: 100px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 1.5rem;
    }
    
    .section-title {
        font-family: 'Epilogue', sans-serif;
        font-size: 3rem;
        font-weight: 800;
        color: white;
        margin-bottom: 1.5rem;
        line-height: 1.2;
    }
    
    .section-subtitle {
        font-size: 1.15rem;
        color: rgba(255, 255, 255, 0.6);
        line-height: 1.7;
    }
    
    .features-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 2.5rem;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 3rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, var(--primary), var(--secondary));
        transform: scaleX(0);
        transform-origin: left;
        transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .feature-card:hover::before {
        transform: scaleX(1);
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        border-color: rgba(255, 107, 53, 0.3);
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.4);
    }
    
    .feature-icon {
        width: 70px;
        height: 70px;
        background: linear-gradient(135deg, rgba(255, 107, 0, 0.2), rgba(255, 165, 0, 0.2));
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.2rem;
        margin-bottom: 2rem;
        transition: transform 0.4s ease;
    }
    
    .feature-card:hover .feature-icon {
        transform: scale(1.1) rotate(5deg);
    }
    
    .feature-title {
        font-family: 'Epilogue', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: white;
        margin-bottom: 1rem;
    }
    
    .feature-description {
        color: rgba(255, 255, 255, 0.7);
        line-height: 1.7;
        font-size: 1rem;
    }
    
    /* Auth Pages */
    .auth-container {
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 4rem 2rem;
        position: relative;
    }
    
    .auth-box {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(30px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 30px;
        padding: 4rem 3rem;
        max-width: 550px;
        width: 100%;
        box-shadow: 0 30px 80px rgba(0, 0, 0, 0.4);
    }
    
    .auth-title {
        font-family: 'Epilogue', sans-serif;
        font-size: 2.5rem;
        font-weight: 800;
        text-align: center;
        color: white;
        margin-bottom: 0.8rem;
    }
    
    .auth-subtitle {
        text-align: center;
        color: rgba(255, 255, 255, 0.6);
        margin-bottom: 3rem;
        font-size: 1.05rem;
    }
    
    /* Form Elements */
    .stTextInput label,
    .stNumberInput label,
    .stSelectbox label,
    .stMultiSelect label,
    .stTextArea label,
    .stCheckbox label,
    .stDateInput label {
        color: white !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        margin-bottom: 0.8rem !important;
    }
    
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea textarea,
    .stDateInput > div > div > input {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1.5px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: white !important;
        padding: 1rem 1.2rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        font-family: 'Sora', sans-serif !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stTextArea textarea:focus,
    .stDateInput > div > div > input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.15) !important;
        background: rgba(255, 255, 255, 0.08) !important;
    }
    
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1.5px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
    }
    
    .stSelectbox > div > div:hover,
    .stMultiSelect > div > div:hover {
        border-color: rgba(255, 107, 53, 0.5) !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2.5rem;
        background: transparent;
        border-bottom: 2px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: none;
        color: rgba(255, 255, 255, 0.5);
        font-weight: 600;
        font-size: 1.05rem;
        padding: 1rem 0;
        font-family: 'Sora', sans-serif;
    }
    
    .stTabs [aria-selected="true"] {
        color: var(--primary);
        border-bottom: 3px solid var(--primary);
    }
    
    /* Dashboard */
    .dashboard {
        background: transparent;
        min-height: 100vh;
    }
    
    .dashboard-header {
        background: linear-gradient(135deg, rgba(255, 107, 0, 0.1), rgba(255, 165, 0, 0.1));
        backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(255, 107, 0, 0.2);
        padding: 3rem 4rem;
    }
    
    .profile-row {
        display: flex;
        align-items: center;
        gap: 2rem;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    .profile-avatar {
        width: 90px;
        height: 90px;
        background: linear-gradient(135deg, #FF6B00, #FFA500);
        border-radius: 22px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5rem;
        color: white;
        font-weight: 800;
        box-shadow: 0 10px 30px rgba(255, 107, 0, 0.5);
    }
    
    .profile-info h1 {
        font-family: 'Epilogue', sans-serif;
        font-size: 2.2rem;
        font-weight: 800;
        color: white;
        margin-bottom: 0.5rem;
    }
    
    .profile-info p {
        color: rgba(255, 255, 255, 0.6);
        font-size: 1rem;
    }
    
    /* Dashboard Stats */
    .dashboard-stats-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 2rem;
        padding: 3rem 4rem;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    .dashboard-stat {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 2rem;
        transition: all 0.4s ease;
    }
    
    .dashboard-stat:hover {
        transform: translateY(-5px);
        border-color: rgba(255, 107, 53, 0.3);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
    }
    
    .stat-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
    }
    
    .stat-icon-box {
        width: 50px;
        height: 50px;
        background: rgba(255, 107, 53, 0.15);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
    }
    
    .stat-value {
        font-family: 'Epilogue', sans-serif;
        font-size: 2.2rem;
        font-weight: 800;
        color: white;
        margin-bottom: 0.3rem;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.6);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 500;
    }
    
    /* Content Cards */
    .content-section {
        display: grid;
        grid-template-columns: 2fr 1fr;
        gap: 2.5rem;
        padding: 0 4rem 4rem;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    .content-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 2.5rem;
    }
    
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
    }
    
    .card-title {
        font-family: 'Epilogue', sans-serif;
        font-size: 1.6rem;
        font-weight: 700;
        color: white;
    }
    
    /* AI Chat Card */
    .ai-card {
        background: linear-gradient(135deg, rgba(255, 107, 0, 0.15), rgba(255, 165, 0, 0.15));
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 107, 0, 0.4);
        border-radius: 24px;
        padding: 2.5rem;
    }
    
    .ai-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    .ai-badge {
        background: linear-gradient(135deg, #FF6B00, #FFA500);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 100px;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .ai-title {
        font-family: 'Epilogue', sans-serif;
        font-size: 1.4rem;
        font-weight: 700;
        color: white;
    }
    
    .ai-message {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 1.5rem;
        color: rgba(255, 255, 255, 0.8);
        line-height: 1.7;
        margin-bottom: 1.5rem;
    }
    
    /* Plan Items */
    .plan-item {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .plan-item:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: rgba(255, 107, 53, 0.3);
        transform: translateX(5px);
    }
    
    .plan-time {
        font-size: 0.75rem;
        color: var(--primary);
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
    
    .plan-name {
        font-weight: 600;
        color: white;
        font-size: 1.05rem;
        margin-bottom: 0.4rem;
    }
    
    .plan-details {
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.6);
    }
    
    /* Footer */
    .footer {
        background: rgba(0, 0, 0, 0.95);
        backdrop-filter: blur(20px);
        border-top: 1px solid rgba(255, 107, 0, 0.2);
        padding: 4rem 4rem 2rem;
        margin-top: 6rem;
    }
    
    .footer-grid {
        display: grid;
        grid-template-columns: 2fr 1fr 1fr 1fr;
        gap: 4rem;
        max-width: 1400px;
        margin: 0 auto 3rem;
    }
    
    .footer-section h3 {
        font-family: 'Epilogue', sans-serif;
        font-size: 1.2rem;
        font-weight: 700;
        color: white;
        margin-bottom: 1.5rem;
    }
    
    .footer-section p,
    .footer-section a {
        color: rgba(255, 255, 255, 0.6);
        text-decoration: none;
        display: block;
        margin-bottom: 0.8rem;
        font-size: 0.95rem;
        line-height: 1.7;
        transition: color 0.3s ease;
    }
    
    .footer-section a:hover {
        color: var(--primary);
    }
    
    .footer-bottom {
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        padding-top: 2rem;
        text-align: center;
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.9rem;
    }
    
    /* Slider */
    .stSlider > label {
        color: white !important;
        font-weight: 600 !important;
    }
    
    /* Success Messages */
    .stSuccess {
        background: rgba(6, 214, 160, 0.1) !important;
        border: 1px solid rgba(6, 214, 160, 0.3) !important;
        border-radius: 12px !important;
        color: var(--success) !important;
    }
    
    /* Dataframe */
    .stDataFrame {
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }
    
    /* Checkbox */
    .stCheckbox {
        padding: 0.5rem 0 !important;
    }
    
    /* Spacing */
    .spacer-sm { height: 1.5rem; }
    .spacer-md { height: 3rem; }
    .spacer-lg { height: 5rem; }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if 'page' not in st.session_state:
    st.session_state.page = "Home"
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

# --- NAVBAR ---
def draw_navbar():
    st.markdown("""
    <div class="animated-bg"></div>
    <div class="navbar">
        <div class="logo-container">
            <div class="logo-icon">✨</div>
            <div class="logo-text">NutriVerse</div>
        </div>
        <div class="nav-menu">
            <a href="#"  class="nav-link">Home</a>
            <a href="#" class="nav-link">Features</a>
            <a href="#" class="nav-link">Plans</a>
            <a href="#" class="nav-link">About</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- FOOTER ---
def draw_footer():
    st.markdown("""
    <div class="footer">
        <div class="footer-grid">
            <div class="footer-section">
                <div class="logo-container" style="margin-bottom: 1.5rem;">
                    <div class="logo-icon">✨</div>
                    <div class="logo-text">NutriVerse</div>
                </div>
                <p>Transform your health journey with AI-powered nutrition and fitness plans tailored just for you.</p>
            </div>
            <div class="footer-section">
                <h3>Features</h3>
                <a href="#">AI Meal Plans</a>
                <a href="#">Workout Programs</a>
                <a href="#">Progress Tracking</a>
                <a href="#">AI Coach</a>
            </div>
            <div class="footer-section">
                <h3>Resources</h3>
                <a href="#">Blog</a>
                <a href="#">Recipes</a>
                <a href="#">Success Stories</a>
                <a href="#">Support</a>
            </div>
            <div class="footer-section">
                <h3>Company</h3>
                <a href="#">About Us</a>
                <a href="#">Contact</a>
                <a href="#">Privacy</a>
                <a href="#">Terms</a>
            </div>
        </div>
        <div class="footer-bottom">
            © 2024 NutriVerse. Crafted with 💜 for your wellness journey.
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- HOME PAGE ---
def home_page():
    draw_navbar()
    
    # Hero Section
    st.markdown("""
    <div class="hero">
        <div class="hero-glow hero-glow-1"></div>
        <div class="hero-glow hero-glow-2"></div>
        <div class="hero-grid">
            <div>
                <div class="hero-badge">
                    <span>🏆</span> AI-POWERED HEALTH PLATFORM
                </div>
                <h1 class="hero-title">
                    Transform Your<br>
                    <span class="hero-gradient-text">Health & Fitness</span><br>
                    Journey Today
                </h1>
                <p class="hero-description">
                    Experience personalized nutrition and workout plans powered by advanced AI. 
                    Get custom meal schedules, exercise routines, and 24/7 coaching designed 
                    specifically for your body, goals, and lifestyle.
                </p>
                <div class="hero-cta">
                </div>
            </div>
            <div class="hero-image-container">
                <div class="hero-card">
                    <div class="hero-emojis">
                        <span>🏃</span>
                        <span>🥗</span>
                        <span>💪</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # CTA Buttons
    col1, col2, col3, col4 = st.columns([1, 0.8, 0.8, 1])
    with col2:
        if st.button("🚀 Start Free Trial", key="cta1"):
            st.session_state.page = "Signup"
            st.rerun()
    
    # Stats Section
    st.markdown("""
    <div class="stats-section">
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">120K+</div>
                <div class="stat-label">Happy Users</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">500K+</div>
                <div class="stat-label">Meal Plans</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">98%</div>
                <div class="stat-label">Success Rate</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">24/7</div>
                <div class="stat-label">AI Support</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Features Section
    st.markdown("""
    <div class="section">
        <div class="section-header">
            <div class="section-badge">✨ FEATURES</div>
            <h2 class="section-title">Everything You Need<br>To Reach Your Goals</h2>
            <p class="section-subtitle">
                Powerful AI-driven tools and personalized guidance to transform your health and achieve lasting results
            </p>
        </div>
        <div class="features-grid">
            <div class="feature-card">
                <div class="feature-icon">🤖</div>
                <h3 class="feature-title">AI Meal Planning</h3>
                <p class="feature-description">
                    Personalized nutrition plans based on your age, weight, goals, allergies, and preferences. 
                    Smart meal scheduling for optimal results.
                </p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">💪</div>
                <h3 class="feature-title">Custom Workouts</h3>
                <p class="feature-description">
                    Tailored exercise programs designed for your fitness level and objectives. 
                    From beginner to advanced routines.
                </p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📊</div>
                <h3 class="feature-title">Progress Analytics</h3>
                <p class="feature-description">
                    Track weight, BMI, calories, and achievements with beautiful dashboards. 
                    Visualize your transformation journey.
                </p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🤰</div>
                <h3 class="feature-title">Pregnancy Care</h3>
                <p class="feature-description">
                    Specialized nutrition and safe exercise plans for expecting mothers. 
                    Trimester-specific guidance for mom and baby.
                </p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">💬</div>
                <h3 class="feature-title">AI Coach 24/7</h3>
                <p class="feature-description">
                    Get instant answers about nutrition, workouts, and wellness from our intelligent chatbot. 
                    Always here to help.
                </p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🗓️</div>
                <h3 class="feature-title">Smart Scheduling</h3>
                <p class="feature-description">
                    Organized monthly calendars for meals and workouts. 
                    Never wonder what to eat or how to train.
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    draw_footer()

# --- SIGNUP PAGE ---
def signup_page():
    draw_navbar()
    
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col2:
        st.markdown("""
        <div class="auth-box">
            <h2 class="auth-title">Join NutriVerse</h2>
            <p class="auth-subtitle">Start your transformation journey today</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="spacer-md"></div>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Create Account", "Sign In"])
        
        with tab1:
            st.markdown('<div class="spacer-sm"></div>', unsafe_allow_html=True)
            name = st.text_input("Full Name", placeholder="Enter your full name")
            email = st.text_input("Email Address", placeholder="you@example.com")
            password = st.text_input("Password", type="password", placeholder="Create a strong password")
            
            st.markdown('<div class="spacer-md"></div>', unsafe_allow_html=True)
            
            if st.button("Create Account", use_container_width=True):
                if name and email and password:
                    st.session_state.user_data['name'] = name
                    st.session_state.user_data['email'] = email
                    st.session_state.page = "Profile"
                    st.rerun()
                else:
                    st.error("Please fill all fields")
        
        with tab2:
            st.markdown('<div class="spacer-sm"></div>', unsafe_allow_html=True)
            login_email = st.text_input("Email", placeholder="you@example.com", key="login_email")
            login_pass = st.text_input("Password", type="password", placeholder="Your password", key="login_pass")
            
            st.markdown('<div class="spacer-md"></div>', unsafe_allow_html=True)
            
            if st.button("Sign In", use_container_width=True):
                if login_email and login_pass:
                    st.session_state.user_data['name'] = "Demo User"
                    st.session_state.page = "Dashboard"
                    st.rerun()
        
        st.markdown('<div class="spacer-sm"></div>', unsafe_allow_html=True)
        if st.button("← Back to Home", use_container_width=True):
            st.session_state.page = "Home"
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- PROFILE SETUP ---
def profile_page():
    draw_navbar()
    
    st.markdown('<div class="spacer-md"></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([0.15, 2, 0.15])
    
    with col2:
        st.markdown("""
        <div class="auth-box">
            <h2 class="auth-title">Build Your Profile</h2>
            <p class="auth-subtitle">Help us create your personalized health plan</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="spacer-md"></div>', unsafe_allow_html=True)
        
        with st.form("profile_form"):
            st.markdown("### 📋 Basic Information")
            c1, c2 = st.columns(2)
            
            with c1:
                age = st.number_input("Age", min_value=13, max_value=100, value=25)
                height = st.number_input("Height (cm)", min_value=100, max_value=250, value=170)
                weight = st.number_input("Current Weight (kg)", min_value=30.0, max_value=300.0, value=70.0)
            
            with c2:
                gender = st.selectbox("Gender", ["Male", "Female", "Non-binary", "Other"])
                goal_weight = st.number_input("Goal Weight (kg)", min_value=30.0, max_value=300.0, value=65.0)
                activity = st.selectbox("Activity Level", ["Sedentary", "Light", "Moderate", "Very Active", "Athlete"])
            
            st.markdown('<div class="spacer-sm"></div>', unsafe_allow_html=True)
            
            st.markdown("### 🎯 Health Goals")
            goal = st.selectbox("Primary Goal", ["Weight Loss", "Muscle Gain", "Maintenance", "Athletic Performance", "General Health"])
            timeline = st.selectbox("Timeline", ["1 Month", "3 Months", "6 Months", "1 Year"])
            
            st.markdown('<div class="spacer-sm"></div>', unsafe_allow_html=True)
            
            st.markdown("### 🏥 Health Details")
            c3, c4 = st.columns(2)
            
            with c3:
                is_pregnant = st.checkbox("I am pregnant")
                if is_pregnant:
                    pregnancy_month = st.slider("Pregnancy Month", 1, 9, 3)
                else:
                    pregnancy_month = None
                
                diseases = st.multiselect("Medical Conditions", 
                    ["None", "Diabetes", "Hypertension", "PCOS", "Thyroid", "Heart Disease"])
            
            with c4:
                allergies = st.multiselect("Food Allergies", 
                    ["None", "Peanuts", "Tree Nuts", "Dairy", "Eggs", "Shellfish", "Soy", "Gluten"])
                
                dietary = st.multiselect("Diet Preferences", 
                    ["No Restrictions", "Vegetarian", "Vegan", "Keto", "Paleo", "Halal"])
            
            st.markdown('<div class="spacer-lg"></div>', unsafe_allow_html=True)
            
            if st.form_submit_button("✨ Generate My Plan", use_container_width=True):
                height_m = height / 100
                bmi = weight / (height_m ** 2)
                
                st.session_state.user_data.update({
                    'age': age, 'height': height, 'weight': weight, 'gender': gender,
                    'goal_weight': goal_weight, 'bmi': round(bmi, 1), 'activity': activity,
                    'goal': goal, 'timeline': timeline, 'is_pregnant': is_pregnant,
                    'pregnancy_month': pregnancy_month, 'diseases': diseases,
                    'allergies': allergies, 'dietary': dietary
                })
                
                st.session_state.page = "Dashboard"
                st.rerun()

# --- DASHBOARD ---
def dashboard_page():
    draw_navbar()
    
    data = st.session_state.user_data
    name = data.get('name', 'User').split()[0]
    weight = data.get('weight', 70)
    goal_weight = data.get('goal_weight', 65)
    bmi = data.get('bmi', 22.5)
    
    # Header
    st.markdown(f"""
    <div class="dashboard">
        <div class="dashboard-header">
            <div class="profile-row">
                <div class="profile-avatar">{name[0].upper()}</div>
                <div class="profile-info">
                    <h1>Welcome back, {name}! 👋</h1>
                    <p>Your personalized health dashboard • {datetime.now().strftime('%B %d, %Y')}</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats
    st.markdown(f"""
    <div class="dashboard-stats-grid">
        <div class="dashboard-stat">
            <div class="stat-top">
                <div class="stat-icon-box">⚖️</div>
            </div>
            <div class="stat-value">{weight} kg</div>
            <div class="stat-label">Current Weight</div>
        </div>
        <div class="dashboard-stat">
            <div class="stat-top">
                <div class="stat-icon-box">🎯</div>
            </div>
            <div class="stat-value">{goal_weight} kg</div>
            <div class="stat-label">Goal Weight</div>
        </div>
        <div class="dashboard-stat">
            <div class="stat-top">
                <div class="stat-icon-box">📊</div>
            </div>
            <div class="stat-value">{bmi}</div>
            <div class="stat-label">BMI Index</div>
        </div>
        <div class="dashboard-stat">
            <div class="stat-top">
                <div class="stat-icon-box">🔥</div>
            </div>
            <div class="stat-value">14 Days</div>
            <div class="stat-label">Active Streak</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Content
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    
    # Left Column
    st.markdown('<div>', unsafe_allow_html=True)
    
    # Weight Chart
    st.markdown("""
    <div class="content-card">
        <div class="card-header">
            <h3 class="card-title">📈 Weight Progress</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    dates = [(datetime.now() - timedelta(days=x)).strftime('%b %d') for x in range(29, -1, -1)]
    weights = [weight + 2 - (0.06 * i) + np.random.normal(0, 0.12) for i in range(30)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, y=weights, mode='lines+markers', name='Weight',
        line=dict(color='#FF6B00', width=3),
        marker=dict(size=6, color='#FF6B00'),
        fill='tozeroy', fillcolor='rgba(255, 107, 0, 0.1)'
    ))
    fig.add_trace(go.Scatter(
        x=[dates[0], dates[-1]], y=[goal_weight, goal_weight],
        mode='lines', name='Goal', line=dict(color='#FFFFFF', width=2, dash='dot')
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='rgba(255,255,255,0.7)'),
        xaxis=dict(showgrid=False, showline=True, linecolor='rgba(255,255,255,0.1)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', title='Weight (kg)'),
        hovermode='x unified', margin=dict(l=0, r=0, t=10, b=0), height=300,
        showlegend=True, legend=dict(orientation="h", y=1.02, x=1, xanchor="right")
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Diet Plan
    st.markdown("""
    <div class="content-card">
        <div class="card-header">
            <h3 class="card-title">🍽️ Today's Meal Plan</h3>
        </div>
        <div class="plan-item">
            <div class="plan-time">7:00 AM • BREAKFAST</div>
            <div class="plan-name">Protein Oatmeal Bowl</div>
            <div class="plan-details">380 cal • 50g carbs • 18g protein • 9g fat</div>
        </div>
        <div class="plan-item">
            <div class="plan-time">10:30 AM • SNACK</div>
            <div class="plan-name">Greek Yogurt & Berries</div>
            <div class="plan-details">220 cal • 18g carbs • 16g protein • 8g fat</div>
        </div>
        <div class="plan-item">
            <div class="plan-time">1:00 PM • LUNCH</div>
            <div class="plan-name">Grilled Chicken Bowl</div>
            <div class="plan-details">480 cal • 38g carbs • 42g protein • 16g fat</div>
        </div>
        <div class="plan-item">
            <div class="plan-time">4:00 PM • SNACK</div>
            <div class="plan-name">Apple & Almond Butter</div>
            <div class="plan-details">190 cal • 24g carbs • 6g protein • 9g fat</div>
        </div>
        <div class="plan-item">
            <div class="plan-time">7:30 PM • DINNER</div>
            <div class="plan-name">Salmon & Quinoa</div>
            <div class="plan-details">540 cal • 48g carbs • 38g protein • 22g fat</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Workout Plan
    st.markdown("""
    <div class="content-card">
        <div class="card-header">
            <h3 class="card-title">💪 Today's Workout</h3>
        </div>
        <div class="plan-item">
            <div class="plan-time">WARM UP • 5 MIN</div>
            <div class="plan-name">Dynamic Mobility</div>
            <div class="plan-details">Leg swings, arm circles, hip rotations</div>
        </div>
        <div class="plan-item">
            <div class="plan-time">CARDIO • 25 MIN</div>
            <div class="plan-name">Interval Running</div>
            <div class="plan-details">Moderate pace • Burns ~250 calories</div>
        </div>
        <div class="plan-item">
            <div class="plan-time">STRENGTH • 30 MIN</div>
            <div class="plan-name">Full Body Circuit</div>
            <div class="plan-details">Squats, Push-ups, Planks, Rows • 3 sets</div>
        </div>
        <div class="plan-item">
            <div class="plan-time">COOL DOWN • 5 MIN</div>
            <div class="plan-name">Stretching</div>
            <div class="plan-details">Focus on all major muscle groups</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Right Column
    st.markdown('<div>', unsafe_allow_html=True)
    
    # AI Chat
    st.markdown("""
    <div class="ai-card">
        <div class="ai-header">
            <div class="ai-badge">AI COACH</div>
            <h3 class="ai-title">Ask Anything</h3>
        </div>
        <div class="ai-message">
            👋 Hi! I'm your AI nutrition coach. Ask me about meal substitutions, workout tips, or any health questions!
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    question = st.text_input("Your question...", placeholder="e.g., Can I replace chicken with fish?", label_visibility="collapsed")
    if st.button("Send", use_container_width=True):
        if question:
            st.success("✅ Great question! Based on your profile...")
    
    st.markdown('<div class="spacer-md"></div>', unsafe_allow_html=True)
    
    # Weekly Stats
    st.markdown("""
    <div class="content-card">
        <h3 class="card-title">📊 Weekly Summary</h3>
    </div>
    """, unsafe_allow_html=True)
    
    summary = pd.DataFrame({
        'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        'Calories': [1820, 1950, 1780, 1900, 1850, 2100, 1920],
        'Workout': ['✅', '✅', '❌', '✅', '✅', '✅', '✅']
    })
    st.dataframe(summary, use_container_width=True, hide_index=True)
    
    st.markdown('<div class="spacer-md"></div>', unsafe_allow_html=True)
    
    # Feedback
    st.markdown("""
    <div class="content-card">
        <h3 class="card-title">💬 Daily Check-in</h3>
        <p style="color: rgba(255,255,255,0.6); margin: 1rem 0;">How are you feeling?</p>
    </div>
    """, unsafe_allow_html=True)
    
    mood = st.select_slider("", options=["😫 Tired", "😐 Okay", "😊 Good", "🤩 Great", "🔥 Amazing"], value="😊 Good", label_visibility="collapsed")
    notes = st.text_area("Notes", placeholder="Share your progress...", label_visibility="collapsed")
    
    if st.button("Submit Feedback", use_container_width=True):
        st.success("✅ Thank you! Feedback recorded.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    draw_footer()

# --- ROUTER ---
if st.session_state.page == "Home":
    home_page()
elif st.session_state.page == "Signup":
    signup_page()
elif st.session_state.page == "Profile":
    profile_page()
elif st.session_state.page == "Dashboard":
    dashboard_page()
