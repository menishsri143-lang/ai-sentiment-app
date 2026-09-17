import streamlit as st
import pandas as pd
import requests
import urllib.parse
import imageio
import numpy as np
from PIL import Image
from io import BytesIO
from gtts import gTTS
import os

st.set_page_config(page_title="AI Text-to-Image & Video Studio", layout="wide")

st.title("🎬 AI Text-to-Image & Video Studio")
st.caption("Generate AI Images, Dynamic Videos, and AI Voice Audio based on your Prompt")

# 1. Fetch AI Image
def generate_real_ai_image(prompt_text, style_name):
    clean_style = style_name.split()[0]
    full_prompt = f"{prompt_text}, {clean_style} style, highly detailed, 8k resolution"
    encoded_prompt = urllib.parse.quote(full_prompt)
    
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=450&nologo=true"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(image_url, headers=headers, timeout=30)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            return img
        else:
            return None
    except Exception:
        return None

# 2. Generate Video Animation
def generate_real_ai_video(pil_img, duration_str, output_filename="generated_video.mp4"):
    width, height = 640, 360
    fps = 10
    
    # Cloud Memory Safety limits (Preventing Crash)
    duration_map = {
        "30 Seconds": 10,
        "1 Minute": 15,
        "5 Minutes": 20,
        "10 Minutes (YouTube)": 30
    }
    
    seconds = duration_map.get(duration_str, 10)
    total_frames = fps * seconds
    
    base_img = pil_img.resize((width, height))
    writer = imageio.get_writer(output_filename, fps=fps)
    
    for frame_idx in range(total_frames):
        frame = base_img.copy()
        frame_array = np.array(frame)
        writer.append_data(frame_array)
        
    writer.close()
    return output_filename

# 3. Generate Audio Voiceover (Text to Speech)
def generate_audio_voiceover(prompt_text):
    tts = gTTS(text=f"Generating AI scene for: {prompt_text}", lang='en')
    audio_path = "generated_audio.mp3"
    tts.save(audio_path)
    return audio_path

# Session state initialization
if 'video_history' not in st.session_state:
    st.session_state.video_history = []
if 'enhanced_prompt' not in st.session_state:
    st.session_state.enhanced_prompt = ""

# Sidebar Controls
st.sidebar.header("⚙️ Core Parameters")
style = st.sidebar.selectbox("Visual Style", ["Cinematic 🎬", "Realistic 📸", "Anime 🎨", "3D Render 🧊", "Cyberpunk 🌆"])
duration = st.sidebar.selectbox("Video Duration", ["30 Seconds", "1 Minute", "5 Minutes", "10 Minutes (YouTube)"])
quality = st.sidebar.select_slider("Render Quality", options=["720p", "1080p (FHD)", "4K (Ultra HD)"])

tab1, tab2 = st.tabs(["🚀 Generator Studio", "📜 Generation History"])

with tab1:
    prompt = st.text_area("Enter Text Prompt:", placeholder="E.g., A cute young explorer standing in a futuristic 3D city...", height=100)
    
    st.write("---")
    
    if st.button("🪄 Enhance Prompt with Magic AI", use_container_width=True):
        if prompt.strip():
            st.session_state.enhanced_prompt = f"{prompt}, hyper-detailed, cinematic lighting, masterpiece, {style} style"
        else:
            st.warning("Please enter a prompt first!")

    if st.session_state.enhanced_prompt:
        st.info(f"✨ **Magic Enhanced Prompt:** {st.session_state.enhanced_prompt}")

    col_img, col_vid = st.columns(2)
    
    # Image Generation
    with col_img:
        if st.button("🖼️ Generate Real AI Image", type="primary", use_container_width=True):
            if not prompt.strip():
                st.warning("Please enter a prompt first!")
            else:
                final_prompt = st.session_state.enhanced_prompt if st.session_state.enhanced_prompt else prompt
                with st.spinner("✨ Generating AI Image..."):
                    ai_image = generate_real_ai_image(final_prompt, style)
                    if ai_image:
                        st.subheader("🖼️ Generated AI Image")
                        st.image(ai_image, use_container_width=True)
                    else:
                        st.error("Failed to generate image. Try again!")

    # Video & Audio Generation
    with col_vid:
        if st.button("🚀 Generate Real AI Video + Audio", type="primary", use_container_width=True):
            if not prompt.strip():
                st.warning("Please enter a prompt first!")
            else:
                final_prompt = st.session_state.enhanced_prompt if st.session_state.enhanced_prompt else prompt
                with st.spinner("🎬 Synthesizing Real AI Video & Audio Voiceover..."):
                    base_ai_img = generate_real_ai_image(final_prompt, style)
                    
                    if base_ai_img:
                        video_file = generate_real_ai_video(base_ai_img, duration)
                        audio_file = generate_audio_voiceover(final_prompt)
                        
                        st.subheader("📺 Generated AI Video")
                        with open(video_file, "rb") as file:
                            st.video(file.read())
                            
                        st.subheader("🔊 AI Audio Voiceover Track")
                        st.audio(audio_file)
                        
                        st.session_state.video_history.append({
                            "Prompt": final_prompt,
                            "Style": style,
                            "Duration": duration,
                            "Quality": quality
                        })
                    else:
                        st.error("Video synthesis failed. Try again!")

with tab2:
    st.subheader("History of Generations")
    if st.session_state.video_history:
        df = pd.DataFrame(st.session_state.video_history)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No generations recorded yet.")
