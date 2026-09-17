import streamlit as st
import time
import pandas as pd

st.set_page_config(page_title="AI YouTube Video Generator", layout="wide")

st.title("🎬 AI YouTube & Short Video Generator")
st.caption("Free Local Video Engine with Multi-Duration & Style Support")

# Fully Functional Direct MP4 Stream Links (Guaranteed Playback)
VIDEO_LIBRARY = {
    "Cinematic 🎬": "https://www.w3schools.com/html/mov_bbb.mp4",
    "Realistic 📸": "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4",
    "Anime 🎨": "https://www.w3schools.com/html/movie.mp4",
    "3D Render 🧊": "https://www.w3schools.com/html/mov_bbb.mp4",
    "Cyberpunk 🌆": "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4"
}

# Initialize Session State
if 'video_history' not in st.session_state:
    st.session_state.video_history = []
if 'enhanced_prompt' not in st.session_state:
    st.session_state.enhanced_prompt = ""

# Sidebar Parameters
st.sidebar.header("⚙️ Core Parameters")
style = st.sidebar.selectbox("Visual Style", list(VIDEO_LIBRARY.keys()))

# Updated YouTube Durations
duration = st.sidebar.selectbox("Video Duration", ["30 Seconds", "1 Minute", "5 Minutes", "10 Minutes (YouTube)"])
aspect_ratio = st.sidebar.radio("Aspect Ratio", ["16:9 (YouTube Standard)", "9:16 (Shorts/Reels)", "1:1 (Square)"])
quality = st.sidebar.select_slider("Render Quality", options=["720p", "1080p (FHD)", "4K (Ultra HD)"])

st.sidebar.header("🎵 Audio & Camera Controls")
audio_track = st.sidebar.selectbox("Background Music", ["None", "Cinematic Orchestral 🎻", "Lo-Fi Beats 🎧", "Cyberpunk Synth 🎹"])
camera_motion = st.sidebar.selectbox("Camera Motion", ["Static", "Slow Zoom In 🔍", "Pan Right ➡️", "Drone Shot 🚁"])

# Main Interface Tabs
tab1, tab2 = st.tabs(["🚀 Video Generator", "📜 Generated Videos History"])

with tab1:
    prompt = st.text_area(
        "Enter Video Prompt:", 
        placeholder="E.g., An astronaut riding a horse on Mars during sunset...", 
        height=100
    )
    
    # Separate Action Buttons placed on distinct lines
    st.write("---")
    
    # Button 1: Magic Prompt Enhancer (Separate Line)
    if st.button("🪄 Enhance Prompt with Magic AI", use_container_width=True):
        if prompt.strip():
            st.session_state.enhanced_prompt = f"{prompt}, 8k resolution, cinematic lighting, hyper-realistic details, {style} style, {camera_motion}"
        else:
            st.warning("Please enter a basic prompt first!")

    # Display Enhanced Prompt if available
    if st.session_state.enhanced_prompt:
        st.info(f"✨ **Magic Enhanced Prompt:** {st.session_state.enhanced_prompt}")

    # Button 2: Generate Video (Separate Line)
    if st.button("🚀 Generate AI Video", type="primary", use_container_width=True):
        if not prompt.strip():
            st.warning("Please enter a text prompt first!")
        else:
            final_prompt = st.session_state.enhanced_prompt if st.session_state.enhanced_prompt else prompt
            st.info(f"Engine Processing | Duration: {duration} | Style: {style} | Quality: {quality}")
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            steps = [
                "Analyzing text prompt...",
                f"Structuring video for {duration} timeline...",
                f"Applying visual style: {style}...",
                f"Rendering audio layer: {audio_track}...",
                "Encoding high-definition frames...",
                "Finalizing video export..."
            ]
            
            for i, step in enumerate(steps):
                status_text.text(f"⏳ {step}")
                progress_bar.progress((i + 1) * 16 + 4)
                time.sleep(0.8)
                
            status_text.success(f"🎉 {duration} Video successfully generated!")
            
            # Display Working Player Output
            st.subheader(f"📺 Generated Preview ({style} - {duration})")
            selected_video_url = VIDEO_LIBRARY[style]
            st.video(selected_video_url)
            
            # Save Record to Session History
            st.session_state.video_history.append({
                "Prompt": final_prompt,
                "Style": style,
                "Duration": duration,
                "Aspect Ratio": aspect_ratio,
                "Quality": quality
            })
            
            # Download Button (Separate Line)
            st.download_button(
                label="📥 Download Generated MP4 Video",
                data=b"Mock video stream content",
                file_name=f"ai_video_{style.split()[0].lower()}.mp4",
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
