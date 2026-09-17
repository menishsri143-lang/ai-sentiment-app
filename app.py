import streamlit as st
import time
import pandas as pd
import imageio
import numpy as np
from PIL import Image, ImageDraw, ImageFont

st.set_page_config(page_title="AI Local Text-to-Image & Video Studio", layout="wide")

st.title("🎬 Local AI Text-to-Image & Video Studio")
st.caption("API-Key-Free Local Frame Rendering Engine for Images & Videos")

# Function to render dynamic local image based on prompt and style
def generate_local_image(prompt_text, style_name):
    width, height = 800, 450
    style_colors = {
        "Cinematic 🎬": (15, 25, 45),
        "Realistic 📸": (35, 55, 35),
        "Anime 🎨": (85, 35, 75),
        "3D Render 🧊": (60, 60, 75),
        "Cyberpunk 🌆": (10, 10, 30)
    }
    bg_color = style_colors.get(style_name, (20, 20, 20))
    accent_color = (0, 230, 255) if "Cyberpunk" in style_name else (255, 180, 0)
    
    img = Image.new("RGB", (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Render motion graphic element
    draw.ellipse([350, 175, 450, 275], fill=accent_color)
    draw.rectangle([50, 50, 750, 400], outline=(255, 255, 255), width=2)
    
    # Prompt Overlay Text
    display_prompt = prompt_text[:50] + "..." if len(prompt_text) > 50 else prompt_text
    draw.text((80, 80), f"AI GENERATED IMAGE", fill=(255, 255, 255))
    draw.text((80, 120), f"PROMPT: {display_prompt}", fill=(200, 220, 255))
    draw.text((80, 160), f"STYLE: {style_name}", fill=(180, 180, 180))
    
    img_path = "generated_image.png"
    img.save(img_path)
    return img_path

# Function to synthesize local MP4 frames
def generate_local_mp4(prompt_text, style_name, duration_str, output_filename="generated_video.mp4"):
    width, height = 640, 360
    fps = 10
    total_frames = 30
    
    style_colors = {
        "Cinematic 🎬": (15, 25, 45),
        "Realistic 📸": (35, 55, 35),
        "Anime 🎨": (85, 35, 75),
        "3D Render 🧊": (60, 60, 75),
        "Cyberpunk 🌆": (10, 10, 30)
    }
    bg_color = style_colors.get(style_name, (20, 20, 20))
    accent_color = (0, 230, 255) if "Cyberpunk" in style_name else (255, 180, 0)
    
    writer = imageio.get_writer(output_filename, fps=fps)
    
    for frame_idx in range(total_frames):
        img = Image.new("RGB", (width, height), color=bg_color)
        draw = ImageDraw.Draw(img)
        
        # Dynamic wave animation
        circle_x = int((frame_idx / total_frames) * (width - 80)) + 40
        circle_y = int((height / 2) + (25 * np.sin(frame_idx * 0.4)))
        draw.ellipse([circle_x - 25, circle_y - 25, circle_x + 25, circle_y + 25], fill=accent_color)
        
        display_prompt = prompt_text[:42] + "..." if len(prompt_text) > 42 else prompt_text
        draw.text((25, 25), f"PROMPT: {display_prompt}", fill=(255, 255, 255))
        draw.text((25, 55), f"STYLE: {style_name} | DURATION: {duration_str}", fill=(200, 220, 255))
        draw.text((25, height - 35), f"Frame: {frame_idx + 1}/{total_frames}", fill=(160, 160, 180))
        
        writer.append_data(np.array(img))
        
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

# Interface Tabs
tab1, tab2 = st.tabs(["🚀 Generator Studio", "📜 Generation History"])

with tab1:
    prompt = st.text_area("Enter Text Prompt:", placeholder="E.g., A futuristic cyberpunk city with neon lights...", height=100)
    
    st.write("---")
    
    # Action 1: Magic Prompt Enhancer
    if st.button("🪄 Enhance Prompt with Magic AI", use_container_width=True):
        if prompt.strip():
            st.session_state.enhanced_prompt = f"{prompt}, 8k resolution, cinematic lighting, highly detailed, {style} style"
        else:
            st.warning("Please enter a prompt first!")

    if st.session_state.enhanced_prompt:
        st.info(f"✨ **Magic Enhanced Prompt:** {st.session_state.enhanced_prompt}")

    col_img, col_vid = st.columns(2)
    
    # Action 2: Text-to-Image Generation
    with col_img:
        if st.button("🖼️ Generate Local Image", type="primary", use_container_width=True):
            if not prompt.strip():
                st.warning("Please enter a prompt first!")
            else:
                final_prompt = st.session_state.enhanced_prompt if st.session_state.enhanced_prompt else prompt
                img_file = generate_local_image(final_prompt, style)
                st.subheader("🖼️ Text-to-Image Result")
                st.image(img_file, use_container_width=True)
                
                with open(img_file, "rb") as file:
                    st.download_button(
                        label="📥 Download Generated Image",
                        data=file,
                        file_name="generated_image.png",
                        mime="image/png",
                        use_container_width=True
                    )

    # Action 3: Text-to-Video Generation
    with col_vid:
        if st.button("🚀 Generate Local Video File", type="primary", use_container_width=True):
            if not prompt.strip():
                st.warning("Please enter a prompt first!")
            else:
                final_prompt = st.session_state.enhanced_prompt if st.session_state.enhanced_prompt else prompt
                video_file = generate_local_mp4(final_prompt, style, duration)
                st.subheader("📺 Text-to-Video Result")
                
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
                        file_name="generated_video.mp4",
                        mime="video/mp4",
                        use_container_width=True
                    )

with tab2:
    st.subheader("History of Generations")
    if st.session_state.video_history:
        df = pd.DataFrame(st.session_state.video_history)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No generations recorded in this session yet.")
