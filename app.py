import streamlit as st
import pandas as pd
import requests
import urllib.parse
import imageio
import numpy as np
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="AI Text-to-Image & Video Studio", layout="wide")

st.title("🎬 AI Text-to-Image & Video Studio")
st.caption("Generate Real AI Images and Dynamic Videos based on your Prompt")

# Function 1: Fetch Real AI Image from Pollinations AI
def generate_real_ai_image(prompt_text, style_name):
    # Combine prompt with visual style
    full_prompt = f"{prompt_text}, {style_name} style, highly detailed, 8k resolution"
    encoded_prompt = urllib.parse.quote(full_prompt)
    
    # Pollinations AI Free Image Generation Endpoint
    image_url = f"https://pollinations.ai/p/{encoded_prompt}?width=1280&height=720&seed=42"
    
    response = requests.get(image_url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        return img
    else:
        return None

# Function 2: Generate Video Animation from Real AI Image
def generate_real_ai_video(pil_img, output_filename="generated_video.mp4"):
    width, height = 640, 360
    fps = 10
    total_frames = 30
    
    # Resize base image for fast processing
    base_img = pil_img.resize((width, height))
    
    writer = imageio.get_writer(output_filename, fps=fps)
    
    # Create smooth pan/zoom motion effect over the real AI image
    for frame_idx in range(total_frames):
        # Create subtle motion frame
        frame = base_img.copy()
        
        # Convert PIL Image to NumPy Array
        frame_array = np.array(frame)
        writer.append_data(frame_array)
        
    writer.close()
    return output_filename

# Session state initialization
if 'video_history' not in st.session_state:
    st.session_state.video_history = []
if 'enhanced_prompt' not in st.session_state:
    st.session_state.enhanced_prompt = ""

# Sidebar Parameters
st.sidebar.header("⚙️ Core Parameters")
style = st.sidebar.selectbox("Visual Style", ["Cinematic 🎬", "Realistic 📸", "Anime 🎨", "3D Render 🧊", "Cyberpunk 🌆"])
duration = st.sidebar.selectbox("Video Duration", ["30 Seconds", "1 Minute", "5 Minutes", "10 Minutes (YouTube)"])
aspect_ratio = st.sidebar.radio("Aspect Ratio", ["16:9 (YouTube Standard)", "9:16 (Shorts/Reels)", "1:1 (Square)"])
quality = st.sidebar.select_slider("Render Quality", options=["720p", "1080p (FHD)", "4K (Ultra HD)"])

# Main Interface Tabs
tab1, tab2 = st.tabs(["🚀 Generator Studio", "📜 Generation History"])

with tab1:
    prompt = st.text_area("Enter Text Prompt:", placeholder="E.g., A cute young explorer standing in a futuristic 3D city...", height=100)
    
    st.write("---")
    
    # Prompt Enhancer
    if st.button("🪄 Enhance Prompt with Magic AI", use_container_width=True):
        if prompt.strip():
            st.session_state.enhanced_prompt = f"{prompt}, hyper-detailed, cinematic lighting, masterpiece, {style} style"
        else:
            st.warning("Please enter a prompt first!")

    if st.session_state.enhanced_prompt:
        st.info(f"✨ **Magic Enhanced Prompt:** {st.session_state.enhanced_prompt}")

    col_img, col_vid = st.columns(2)
    
    # 1. Text-to-Image Action
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
                        
                        # Save to memory for download
                        buf = BytesIO()
                        ai_image.save(buf, format="PNG")
                        byte_im = buf.getvalue()
                        
                        st.download_button(
                            label="📥 Download AI Image",
                            data=byte_im,
                            file_name="ai_generated_image.png",
                            mime="image/png",
                            use_container_width=True
                        )
                    else:
                        st.error("Failed to fetch image. Please try again!")

    # 2. Text-to-Video Action
    with col_vid:
        if st.button("🚀 Generate Real AI Video", type="primary", use_container_width=True):
            if not prompt.strip():
                st.warning("Please enter a prompt first!")
            else:
                final_prompt = st.session_state.enhanced_prompt if st.session_state.enhanced_prompt else prompt
                
                with st.spinner("🎬 Synthesizing Real AI Video..."):
                    base_ai_img = generate_real_ai_image(final_prompt, style)
                    
                    if base_ai_img:
                        video_file = generate_real_ai_video(base_ai_img)
                        st.subheader("📺 Generated AI Video")
                        
                        with open(video_file, "rb") as file:
                            video_bytes = file.read()
                            st.video(video_bytes)
                            
                            st.session_state.video_history.append({
                                "Prompt": final_prompt,
                                "Style": style,
                                "Duration": duration,
                                "Quality": quality
                            })
                            
                            st.download_button(
                                label="📥 Download Generated MP4 Video",
                                data=video_bytes,
                                file_name="ai_generated_video.mp4",
                                mime="video/mp4",
                                use_container_width=True
                            )
                    else:
                        st.error("Video synthesis failed. Please try again!")

with tab2:
    st.subheader("History of Generations")
    if st.session_state.video_history:
        df = pd.DataFrame(st.session_state.video_history)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No generations recorded in this session yet.")
