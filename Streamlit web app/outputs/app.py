import streamlit as st

st.set_page_config(
    page_title="Football Analysis Hub",
    layout="wide",
    initial_sidebar_state="expanded"
)
import euro_shot_map
import web_app
import main
import AI_app
# Set page configuration

from PIL import Image
# Background GIF & Overlay
st.markdown(
    """
    <style>
    .stApp {
        background: "Gemini_Generated_Image_5pfzxb5pfzxb5pfz.jpg" no-repeat center center fixed;
        background-size: cover;
    }
    .background-overlay {
        background-color: rgba(0, 0, 0, 0.5);
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
    }
    </style>
    <div class="background-overlay"></div>
    """,
    unsafe_allow_html=True
)

# Main Heading Section
with st.container():
    st.title("**⚽ SPECIAL UNIFIED INTERFACE FOR FOOTBALL ANALYSIS(SUI)**")
    st.subheader("Insights | Tactics | Tracking | Strategy")
    st.write("Welcome to the future of football analytics.")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Player Tracking", "Formations & Tactics", "Euro 2024 Shot Maps", "Heatmaps", "AI Predictions", "About"])

# Routing Logic
if page == "Home":
    st.markdown("""
        Welcome to the **Football Analysis Hub** — your all-in-one platform for visualizing and understanding football like never before.

        **Features:**
        - Real-time **Player Tracking**
        - Team **Formations and Tactical Analysis**
        - Tournament-wise **Statistical Insights**
    """)
    img = Image.open("Gemini_Generated_Image_5pfzxb5pfzxb5pfz.jpg")
    resized_img = img.resize((1200, 1000))  # (width, height)
    st.image(resized_img, caption="Football Analysis Hub")

elif page == "Player Tracking":
    main.main()

elif page == "Formations & Tactics":
    web_app.app()

elif page == "Euro 2024 Shot Maps":
    
    euro_shot_map.app()

elif page == "Heatmaps":
    st.write("Heatmaps section coming soon!")  # Placeholder

elif page == "AI Predictions":
    AI_app.main()

elif page == "About":
    st.header("About This Project")
    st.markdown("""
        Created by SUI... Team, this project aims to bridge football with technology.
        Using computer vision, machine learning, and data science — we bring the pitch to your screen in a whole new way.
    """)

# Footer
st.markdown("---")
st.caption("Powered by Streamlit | Developed with passion for football.")
