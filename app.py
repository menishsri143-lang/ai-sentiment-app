# Function 2: Generate Video Animation with Dynamic Duration Support
def generate_real_ai_video(pil_img, duration_str, output_filename="generated_video.mp4"):
    width, height = 640, 360
    fps = 10
    
    # Selected duration based frame calculation
    duration_map = {
        "30 Seconds": 10,       # 10 Seconds Playback
        "1 Minute": 15,         # 15 Seconds Playback
        "5 Minutes": 20,        # 20 Seconds Playback
        "10 Minutes (YouTube)": 30 # 30 Seconds Playback (Prevents Cloud Crash)
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
