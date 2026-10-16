import streamlit as st
import os
from PIL import Image

# --- 1. Page Configuration ---
st.set_page_config(page_title="🎂 Happy Birthday Surprise! 🎉", page_icon="💝", layout="centered")

# --- 2. Custom CSS Web Animations ---
# This styles the webpage, adds a glowing background loop, and handles image zoom animations.
st.markdown("""
    <style>
    /* Animated Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #121214, #1a1a2e, #2d142c);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Pulsing Glowing Header Text */
    @keyframes titleGlow {
        0% { color: #ff79c6; text-shadow: 0 0 15px rgba(255, 121, 198, 0.6); transform: scale(1); }
        50% { color: #8be9fd; text-shadow: 0 0 30px rgba(139, 233, 253, 0.9); transform: scale(1.02); }
        100% { color: #ff79c6; text-shadow: 0 0 15px rgba(255, 121, 198, 0.6); transform: scale(1); }
    }
    
    .birthday-header {
        font-size: 3.5rem !important;
        font-weight: bold;
        text-align: center;
        animation: titleGlow 4s infinite ease-in-out;
        margin-bottom: 5px;
    }
    
    /* Interactive Glowing Hover Effect for Pictures */
    div[data-testid="stImage"] {
        border: 3px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.4s ease, border-color 0.4s;
    }
    
    div[data-testid="stImage"]:hover {
        transform: scale(1.06) translateY(-8px) rotate(1deg);
        box-shadow: 0 15px 35px rgba(255, 121, 198, 0.5);
        border-color: #ff79c6;
    }

    /* Aesthetic UI Dividers */
    .neon-divider {
        height: 3px;
        background: linear-gradient(90deg, transparent, #ff79c6, #8be9fd, transparent);
        margin: 35px 0;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. Run Confetti & Balloon Animations Natively ---
st.balloons()  # Floats virtual balloons across the screen automatically on load

# --- 4. Main Animated Header ---
st.markdown('<div class="birthday-header">🎉 HAPPY BIRTHDAY! 🎉</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.3rem; color: #f8f8f2; opacity: 0.8;'>Here's to celebrating your special day with your favorite memories! ✨</p>", unsafe_allow_html=True)

# --- 5. Optional Audio / Music Widget ---
st.markdown("### 🎵 Turn Up The Birthday Music")
uploaded_music = st.file_uploader(
    "Choose a music file (MP3, WAV, or OGG):",
    type=["mp3", "wav", "ogg"],
    key="birthday_music",
)
music_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "birthday.mp3")
if uploaded_music is not None:
    st.audio(uploaded_music, format=uploaded_music.type, loop=True)
elif os.path.isfile(music_path):
    with open(music_path, "rb") as music_file:
        st.audio(music_file.read(), format="audio/mp3", loop=True)
else:
    st.info("Upload your music file above, or add an MP3 named birthday.mp3 to the app folder.")
st.caption("Press Play to start the music. Browsers block audio autoplay.")

st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)

# --- 6. Picture Uploading Engine ---
st.markdown("### 📸 Add Photos to the Birthday Wall")
st.write("Drag and drop your favorite pictures below to watch them slide into the animated gallery!")

# Set up local folder directory to hold your uploaded image items
PHOTO_FOLDER = "saved_birthday_memories"
if not os.path.exists(PHOTO_FOLDER):
    os.makedirs(PHOTO_FOLDER)

uploaded_images = st.file_uploader(
    "Choose picture files (PNG, JPG, JPEG):", 
    type=["png", "jpg", "jpeg"], 
    accept_multiple_files=True
)

# Process and save images into your Python project workspace
if uploaded_images:
    for file in uploaded_images:
        save_path = os.path.join(PHOTO_FOLDER, file.name)
        if not os.path.exists(save_path):
            with open(save_path, "wb") as f:
                f.write(file.getbuffer())
    st.toast("Pictures updated safely! Watch the board change below. 😍", icon="🎉")

st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)

# --- 7. Displaying the Animated Picture Grid Layout ---
st.markdown("### 🖼️ The Memory Album Wall")

# Gather all saved image elements currently residing in your storage folder
photo_list = [img for img in os.listdir(PHOTO_FOLDER) if img.lower().endswith(('.png', '.jpg', '.jpeg'))]

if photo_list:
    st.write(f"💡 *Tip: Hover your mouse cursor over the **{len(photo_list)}** photo cards to see them float and glow!*")
    
    # Split pictures dynamically across a clean 2-column gallery dashboard
    columns = st.columns(2)
    for index, image_name in enumerate(sorted(photo_list)):
        image_path = os.path.join(PHOTO_FOLDER, image_name)
        loaded_image = Image.open(image_path)
        
        # Clean title captions by stripping out extensions
        clean_caption = os.path.splitext(image_name)[0].replace("_", " ").title()
        
        with columns[index % 2]:
            st.image(loaded_image, caption=f"✨ {clean_caption}", use_container_width=True)
else:
    st.info("The photo album is currently empty. Drop some birthday picture files into the uploader area above to populate the screen! 🎈")

# --- 8. Re-trigger Animation Button ---
st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)
if st.button("🎆 Re-launch Celebration Rockets!"):
    st.snow()  # Triggers a secondary falling star particle aesthetic
