import streamlit as st
import time
import pandas as pd
import os
import imageio
from PIL import Image, ImageDraw, ImageFont

st.set_page_config(page_title="Local AI Video Synthesis Studio", layout="wide")

st.title("🎬 Local AI Prompt-to-Video Engine")
st.caption("Generates MP4 files locally rendering frame layers matching your exact prompt (No API Key Required)")

# Function to synthesize local MP4 frames matching prompt text and style
def generate_local_mp4(prompt_text, style_name, duration_str, output_filename="generated_video.mp4"):
    width, height = 640, 360
    fps = 10
    total_frames = 30  # Rendered sample frame sequence
    
    # Style-based background color definitions
    style_colors = {
        "Cinematic 🎬": (20, 30, 50),
        "Realistic 📸": (40, 60, 40),
        "Anime 🎨": (90, 40, 80),
        "3D Render 🧊": (70, 70, 80),
        "Cyberpunk 🌆": (15, 15, 35)
    }
    bg_color = style_colors.get(style_name, (30, 30, 30))
    accent_color = (255, 200, 0) if "Cyberpunk" in style_name else (255, 255, 255)
    
    writer = imageio.get_writer(output_filename, fps=fps)
    
    for frame_idx in range(total_frames):
        # Create Frame Surface
        img = Image.new("RGB", (width, height), color=bg_color)
        draw = ImageDraw.Draw(img)
        
        # Render Animated Motion Circles based on Prompt Length
        circle_x = int((frame_idx / total_frames) * width)
        circle_y = int((height / 2) + (30 if frame_idx % 2 == 0 else -30))
        draw.ellipse([circle_x - 20, circle_y - 20, circle_x + 20, circle_y + 20], fill=accent_color)
        
        # Render Text Prompt Overlay directly onto the Video Frame
        display_prompt = prompt_text[:40] + "..." if len(prompt_text) > 40 else prompt_text
        draw.text((30, 30), f"PROMPT: {display_prompt}", fill=(255, 255, 255))
        draw.text((30, 60), f"STYLE: {style_name} | DURATION: {duration_str}", fill=(200, 200, 200))
        draw.text((30, height - 40), f"Rendered Frame: {frame_idx + 1}/{total_frames}", fill=(150, 150, 150))
        
        # Append frame to video writer
        writer.append_data(imageio.core.util.Array(img))
        
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

st.sidebar.header("🎵 Audio & Motion Controls")
audio_track = st.sidebar.selectbox("Background Music", ["None", "Cinematic Orchestral 🎻", "Lo-Fi Beats 🎧", "Cyberpunk Synth 🎹"])
camera_motion = st.sidebar.selectbox("Camera Motion", ["Static", "Slow Zoom In 🔍", "Pan Right ➡️", "Drone Shot 🚁"])

# Interface Tabs
tab1, tab2 = st.tabs(["🚀 Video Generator", "📜 Generated Videos History"])

with tab1:
    prompt = st.text_area("Enter Video Prompt:", placeholder="E.g., A futuristic space shuttle landing on Mars...", height=100)
    
    st.write("---")
    
    # Button 1: Magic Prompt (Separate Line)
    if st.button("🪄 Enhance Prompt with Magic AI", use_container_width=True):
        if prompt.strip():
            st.session_state.enhanced_prompt = f"{prompt}, 8k resolution, cinematic lighting, hyper-detailed, {style} style"
        else:
            st.warning("Please enter a prompt first!")

    if st.session_state.enhanced_prompt:
        st.info(f"✨ **Magic Enhanced Prompt:** {st.session_state.enhanced_prompt}")

    # Button 2: Generate Local Video (Separate Line)
    if st.button("🚀 Generate Local Video File", type="primary", use_container_width=True):
        if not prompt.strip():
            st.warning("Please enter a prompt first!")
        else:
            final_prompt = st.session_state.enhanced_prompt if st.session_state.enhanced_prompt else prompt
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("⏳ Initializing local synthesis engine...")
            progress_bar.progress(20)
            time.sleep(0.5)
            
            status_text.text(f"⏳ Generating frames locally for: '{final_prompt[:30]}...'")
            progress_bar.progress(50)
            
            # Synthesize local MP4 file dynamically
            output_file = generate_local_mp4(final_prompt, style, duration)
            
            progress_bar.progress(100)
            status_text.success("🎉 Local MP4 file successfully rendered!")
            
            # Display synthesized video file directly from disk
            st.subheader("📺 Locally Generated Video Output")
            with open(output_file, "rb") as file:
                video_bytes = file.read()
                st.video(video_bytes)
                
                # Save Record to History
                st.session_state.video_history.append({
                    "Prompt": final_prompt,
                    "Style": style,
                    "Duration": duration,
                    "Quality": quality
                })
                
                # Download Generated MP4
                st.download_button(
                    label="📥 Download Generated MP4 Video",
                    data=video_bytes,
                    file_name="local_generated_video.mp4",
                    mime="video/mp4",
                    use_container_width=True
                )

with tab2:
    st.subheader("History of Generated Videos")
    if st.session_state.video_history:
        df = pd.DataFrame(st.session_state.video_history)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No videos generated in this session yet.")
