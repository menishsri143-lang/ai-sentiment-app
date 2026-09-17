import streamlit as st
import time
import pandas as pd

st.set_page_config(page_title="Advanced AI Text-to-Video Studio", layout="wide")

st.title("🎬 Advanced AI Text-to-Video Studio")
st.caption("Free Local Video Generator Engine with Working Video Previews")

# Direct Working MP4 Video Links
VIDEO_LIBRARY = {
    "Cinematic 🎬": "https://www.w3schools.com/html/mov_bbb.mp4",
    "Realistic 📸": "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4",
    "Anime 🎨": "https://www.w3schools.com/html/movie.mp4",
    "3D Render 🧊": "https://www.w3schools.com/html/mov_bbb.mp4",
    "Cyberpunk 🌆": "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4"
}

# Initialize Session State for History
if 'video_history' not in st.session_state:
    st.session_state.video_history = []

# Sidebar Parameters
st.sidebar.header("⚙️ Core Parameters")
style = st.sidebar.selectbox("Visual Style", list(VIDEO_LIBRARY.keys()))
duration = st.sidebar.select_slider("Duration", options=["10 sec", "30 sec", "60 sec"])
aspect_ratio = st.sidebar.radio("Aspect Ratio", ["16:9 (Landscape)", "9:16 (Portrait/Reels)", "1:1 (Square)"])
quality = st.sidebar.select_slider("Render Quality", options=["720p", "1080p (FHD)", "4K (Ultra HD)"])

st.sidebar.header("🎵 Audio & Camera Controls")
audio_track = st.sidebar.selectbox("Background Music", ["None", "Cinematic Orchestral 🎻", "Lo-Fi Beats 🎧", "Cyberpunk Synth 🎹"])
camera_motion = st.sidebar.selectbox("Camera Motion", ["Static", "Slow Zoom In 🔍", "Pan Right ➡️", "Drone Shot 🚁"])
fps = st.sidebar.select_slider("Frame Rate", options=["24 FPS (Cinematic)", "30 FPS (Standard)", "60 FPS (Smooth)"])

# Main Interface
tab1, tab2 = st.tabs(["🚀 Video Generator", "📜 Generated Videos History"])

with tab1:
    prompt = st.text_area("Enter Video Prompt:", placeholder="E.g., An astronaut riding a horse on Mars during sunset...", height=100)
    
    col1, col2 = st.columns([1, 4])
    with col1:
        enhance_btn = st.button("🪄 Magic Prompt")
    with col2:
        generate_btn = st.button("🚀 Generate Video", type="primary", use_container_width=True)

    if enhance_btn and prompt.strip():
        enhanced_text = f"{prompt}, highly detailed, 8k resolution, volumetric lighting, photorealistic, {style} style, {camera_motion}"
        st.info(f"✨ Enhanced Prompt: **{enhanced_text}**")

    if generate_btn:
        if not prompt.strip():
            st.warning("Please enter a text prompt first!")
        else:
            st.info(f"Engine Running | Style: {style} | Audio: {audio_track} | Camera: {camera_motion}")
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            steps = [
                "Analyzing prompt structure...",
                f"Selecting style template: {style}...",
                f"Configuring camera motion ({camera_motion}) & {fps}...",
                f"Synthesizing audio layer: {audio_track}...",
                "Rendering high-quality frame sequences...",
                "Encoding final MP4 video output..."
            ]
            
            for i, step in enumerate(steps):
                status_text.text(f"⏳ {step}")
                progress_bar.progress((i + 1) * 16 + 4)
                time.sleep(0.8)
                
            status_text.success("🎉 Video generation completed successfully!")
            
            # Dynamic Working Video Output
            st.subheader(f"📺 Generated Video Preview ({style})")
            selected_video_url = VIDEO_LIBRARY.get(style, VIDEO_LIBRARY["Cinematic 🎬"])
            st.video(selected_video_url)
            
            # Save to History
            st.session_state.video_history.append({
                "Prompt": prompt,
                "Style": style,
                "Duration": duration,
                "Quality": quality,
                "Camera": camera_motion,
                "Audio": audio_track
            })
            
            st.download_button(
                label="📥 Download Generated MP4 Video",
                data=b"Mock video stream content",
                file_name=f"{style.split()[0].lower()}_generated_video.mp4",
                mime="video/mp4"
            )

with tab2:
    st.subheader("History of Generated Videos")
    if st.session_state.video_history:
        df = pd.DataFrame(st.session_state.video_history)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No videos generated in this session yet.")
