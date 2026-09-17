import streamlit as st
import time
import pandas as pd

st.set_page_config(page_title="AI YouTube Video Generator", layout="wide")

st.title("🎬 Smart AI Prompt-Matched Video Generator")
st.caption("100% Free Local Video Engine with Dynamic Keyword Matching")

# Working direct video streams mapped to specific prompt keywords
KEYWORD_VIDEOS = {
    "car": "https://www.w3schools.com/html/mov_bbb.mp4",
    "nature": "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4",
    "flower": "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4",
    "cat": "https://www.w3schools.com/html/movie.mp4",
    "dog": "https://www.w3schools.com/html/movie.mp4",
    "space": "https://www.w3schools.com/html/mov_bbb.mp4",
    "city": "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4",
    "default": "https://www.w3schools.com/html/mov_bbb.mp4"
}

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

st.sidebar.header("🎵 Audio Controls")
audio_track = st.sidebar.selectbox("Background Music", ["None", "Cinematic Orchestral 🎻", "Lo-Fi Beats 🎧", "Cyberpunk Synth 🎹"])

tab1, tab2 = st.tabs(["🚀 Video Generator", "📜 Generated Videos History"])

with tab1:
    prompt = st.text_area("Enter Video Prompt:", placeholder="Try entering keywords like 'flower', 'cat', 'car', 'nature', 'city'...", height=100)
    
    st.write("---")
    
    if st.button("🪄 Enhance Prompt with Magic AI", use_container_width=True):
        if prompt.strip():
            st.session_state.enhanced_prompt = f"{prompt}, 8k resolution, cinematic lighting, hyper-realistic details, {style} style"
        else:
            st.warning("Please enter a basic prompt first!")

    if st.session_state.enhanced_prompt:
        st.info(f"✨ **Magic Enhanced Prompt:** {st.session_state.enhanced_prompt}")

    if st.button("🚀 Generate AI Video", type="primary", use_container_width=True):
        if not prompt.strip():
            st.warning("Please enter a text prompt first!")
        else:
            final_prompt = st.session_state.enhanced_prompt if st.session_state.enhanced_prompt else prompt
            st.info(f"Engine Processing | Duration: {duration} | Quality: {quality}")
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            steps = [
                "Analyzing text prompt keywords...",
                f"Structuring video for {duration} timeline...",
                f"Applying visual style: {style}...",
                "Encoding high-definition frames...",
                "Finalizing video export..."
            ]
            
            for i, step in enumerate(steps):
                status_text.text(f"⏳ {step}")
                progress_bar.progress((i + 1) * 20)
                time.sleep(0.6)
                
            status_text.success("🎉 Video matched and generated successfully!")
            
            # Prompt-based Video Matching Logic
            selected_url = KEYWORD_VIDEOS["default"]
            for keyword in KEYWORD_VIDEOS:
                if keyword in prompt.lower():
                    selected_url = KEYWORD_VIDEOS[keyword]
                    break
            
            st.subheader(f"📺 Generated Video Preview")
            st.video(selected_url)
            
            st.session_state.video_history.append({
                "Prompt": final_prompt,
                "Style": style,
                "Duration": duration,
                "Quality": quality
            })
            
            st.download_button(
                label="📥 Download Generated MP4 Video",
                data=b"Mock video stream content",
                file_name="generated_ai_video.mp4",
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
