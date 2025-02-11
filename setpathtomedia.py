import os

def seleccion(personaje='Albert', verbose=False):
    # What character to use
    clone_to_use = personaje  # "Steve"
    global input_video, presentation_video, goodbye_video, results_path, w_vid, h_vid
    # Path to the media directory containing
    # the avatar image, welcome video and goodbye videos
    path = f"./media/"

    input_video = path + f"{clone_to_use}/image.jpg"
    presentation_video = path + f"{clone_to_use}/presentation.mp4"
    goodbye_video = path + f"{clone_to_use}/goodbye.mp4"
    results_path = path + f"{clone_to_use}/results/result.mp4"
    w_vid = h_vid = "90%"

    if verbose:
        print(w_vid, h_vid, results_path)
        print(clone_to_use)
        if os.path.isfile(input_video):
            print(f"Clone image found: {input_video}")
        else:
            print(f"CLONE IMAGE NOT FOUND: {input_video}")

        if os.path.isfile(presentation_video):
            print(f"Clone video found: {presentation_video}")
        else:
            print(f"CLONE VIDEO NOT FOUND: {presentation_video}")

        if os.path.isfile(goodbye_video):
            print(f"Clone goodbye video found: {goodbye_video}")
        else:
            print(f"CLONE GOODBYE NOT FOUND: {goodbye_video}")

    # Return the paths
    return input_video, presentation_video, goodbye_video, results_path
