#styles.py
import streamlit as st
import base64
import os

def apply_custom_theme():
    """
    Reads your local Sarangkot image from your project folder, converts it to base64, 
    and applies it as a fixed background with a white transparency overlay.
    """
    # Using your exact filename from your folder
    image_filename = "sarangkot_20180710001134.jpg"
    
    # Securely read and convert the local image asset
    if os.path.exists(image_filename):
        with open(image_filename, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        bg_image_css = f"data:image/jpg;base64,{encoded_string}"
    else:
        # Fallback background color if the image is missing or named incorrectly
        bg_image_css = ""

    st.markdown(f"""
        <style>
        /* Fixed photographic background using your local Sarangkot image with a 20% white transparency layer */
        .stApp {{
            background-image: linear-gradient(rgba(255, 253, 247, 0.30), rgba(255, 253, 247, 0.30)), 
                              url("{bg_image_css}");
            background-size: cover !important;
            background-position: center !important;
            background-attachment: fixed !important;
        }}
        
        /* Style Titles to stay bold and dark against the mountain background */
        h1{{ 
            color: #1F2937 !important; 
            font-weight: 1000 !important;
        }}
        /* 3. Regular Markdown Headers (like ## Your Top Recommendations) */
        h2 {{
            color: #FFFFF7 !important;
            font-size: 2rem !important;
        }}
        
        /* Make all input labels pure white */
        [data-testid="stWidgetLabel"] p, label p {{
            color: #FFFFFF !important;
            font-weight: 600 !important;
        }}
        /* Make captions/sub-captions pure white */
        .stCaptionContainer p, [data-testid="stCaptionContainer"] p {{
            color: #FFFFFF !important;
            font-weight: 500 !important;
            font-size: 1.1rem !important;
        }}
        /* 1. Make the Button Dark Blue and lock it down securely */
        div.stButton > button {{
            background-color: #1d3557 !important;
            color: white !important;
            border: none !important;
            font-weight: bold !important;
        }}
        div.stButton > button:hover,
        div.stButton > button:active,
        div.stButton > button:focus {{
            background-color: #1d3557 !important;
            color: white !important;
            border: none !important;
        }}
        


        /* 2. Hover State: Turn the button beautiful Forest Green when mouse glides over it */
        div.stButton > button:hover,
        div.stButton > button:active,
        div.stButton > button:focus {{
            background-color: #166534 !important;
            color: white !important;
            border: none !important;
        }}
        
        /* 3. Make the Radio Selection Dots Green */
        div[data-testid="stRadio"] [role="radio"][aria-checked="true"] {{
            accent-color: #166534 !important;
        }}

        
        /* Style the result containers with Left Nepalese Crimson Red border and crisp white background */
        [data-testid="stVerticalBlockBorderWrapper"] {{
            border-left: 5px solid #e63946 !important;
            background-color: rgba(255, 255, 255, 0.9) !important;
            border-radius: 4px;
        }}

        /* ===============================
   MAIN GLASS CONTAINER
   =============================== */

div[data-testid="stVerticalBlockBorderWrapper"]:first-of-type {{
    background: rgba(255, 255, 255, 0.18) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;

    border: 1px solid rgba(255,255,255,0.35) !important;
    border-radius: 20px !important;

    padding: 25px !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.25) !important;
}}
        </style>
    """, unsafe_allow_html=True)

