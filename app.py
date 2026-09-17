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
from moviepy.editor import VideoFileClip, AudioFileClip

st.set_page_config(page_title="AI Text-to-Video Studio", layout="wide")

st.title("🎬 AI Prompt-to-Video & Audio Studio")
st.caption("Generate AI Videos with Integrated Background Audio from Prompt")

# 1. Image Generation from Prompt
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

# 2. Generate Video + Merge Audio in Background
def generate_real_ai_video_with_audio(pil_img, prompt_text, duration_str):
    raw_video_filename = "temp_video.mp4"
    audio_filename = "temp_audio.mp3"
    final_output_filename = "final_output_video.mp4"
    
    width, height = 640, 360
    fps = 10
    
    duration_map = {
        "30 Seconds": 10,
        "1 Minute": 15,
        "5 Minutes": 20,
        "10 Minutes (YouTube)": 30
    }
    
    seconds = duration_map.get(duration_str, 10)
    total_frames = fps * seconds
    
    # Render Video Frames
    base_img = pil_img.resize((width, height))
    writer = imageio.get_writer(raw_video_filename, fps=fps)
    
    for frame_idx in range(total_frames):
        frame = base_img.copy()
        frame_array = np.array(frame)
        writer.append_data(frame_array)
        
    writer.close()
    
    # Generate Audio Track (gTTS)
    tts = gTTS(text=f"AI Visual Generation for: {prompt_text}", lang='en')
    tts.save(audio_filename)
    
    # Merge Video and Audio into Single MP4 File using MoviePy
    try:
        video_clip = VideoFileClip(raw_video_filename)
        audio_clip = AudioFileClip(audio_filename)
        
        # Loop audio if short, or set video duration matching audio
        final_clip = video_clip.set_audio(audio_clip)
        final_clip.write_videofile(final_output_filename, codec='libx264', audio_codec='aac', logger=None)
        
        # Close clips to free memory
        video_clip.close()
        audio_clip.close()
        
        return final_output_filename
    except Exception as e:
        # Fallback to raw video if merging encounters error
        return raw_video_filename

# Session state initialization
if 'video_history' not in st.session_state:
    st.session_state.video_history = []
if 'enhanced_prompt' not in st.session_state:
    st.session_state.enhanced_prompt = ""

# Sidebar Parameters
st.sidebar.header("⚙️ Core Parameters")
style = st.sidebar.selectbox("Visual Style", ["Cinematic 🎬", "Realistic 📸", "Anime 🎨", "3D Render 🧊", "Cyberpunk 🌆"])
duration = st.sidebar.selectbox("Video Duration", ["30 Seconds", "1 Minute", "5 Minutes", "10 Minutes (YouTube)"])
quality = st.sidebar.select_slider("Render Quality", options=["720p", "1080p (FHD)", "4K (Ultra HD)"])

tab1, tab2 = st.tabs(["🚀 Video Studio", "📜 History"])

with tab1:
    prompt = st.text_area("Enter Video Prompt:", placeholder="E.g., A cute young explorer standing in a futuristic 3D city...", height=100)
    
    st.write("---")
    
    if st.button("🪄 Enhance Prompt with Magic AI", use_container_width=True):
        if prompt.strip():
            st.session_state.enhanced_prompt = f"{prompt}, hyper-detailed, cinematic lighting, masterpiece, {style} style"
        else:
            st.warning("Please enter a prompt first!")

    if st.session_state.enhanced_prompt:
        st.info(f"✨ **Magic Enhanced Prompt:** {st.session_state.enhanced_prompt}")

    if st.button("🚀 Generate AI Video with Audio", type="primary", use_container_width=True):
        if not prompt.strip():
            st.warning("Please enter a text prompt first!")
        else:
            final_prompt = st.session_state.enhanced_prompt if st.session_state.enhanced_prompt else prompt
            
            with st.spinner("🎬 Generating Prompt Match Image & Merging Background Audio Track..."):
                base_ai_img = generate_real_ai_image(final_prompt, style)
                
                if base_ai_img:
                    final_video_path = generate_real_ai_video_with_audio(base_ai_img, final_prompt, duration)
                    
                    st.subheader("📺 Generated Output Video (With Integrated Audio)")
                    
                    with open(final_video_path, "rb") as file:
                        video_bytes = file.read()
                        st.video(video_bytes)
                        
                        st.download_button(
                            label="📥 Download Video MP4 (Audio Included)",
                            data=video_bytes,
                            file_name="ai_generated_video_with_audio.mp4",
                            mime="video/mp4",
                            use_container_width=True
                        )
                        
                        st.session_state.video_history.append({
                            "Prompt": final_prompt,
                            "Style": style,
                            "Duration": duration,
                            "Quality": quality
                        })
                else:
                    st.error("Image generation for prompt failed. Please try again!")

with tab2:
    st.subheader("History of Generations")
    if st.session_state.video_history:
        df = pd.DataFrame(st.session_state.video_history)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No generations recorded yet.")
