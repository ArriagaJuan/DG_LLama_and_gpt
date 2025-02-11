import utils

def load_input(input_video_path=None):
    
    #print(f"Using {device}")
    frames, fps = utils.load_input_image_or_video(input_video_path)

    return frames,fps

    