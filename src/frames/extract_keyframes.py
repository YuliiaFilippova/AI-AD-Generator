import os
import cv2


def extract_keyframes(video_path, scenes, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    #os.makedirs("data/frames", exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    scene_frames = []

    for i, (start, end) in enumerate(scenes):

        frames = []

        duration = end - start

        # adaptive number of frames
        num_frames = min(5, max(3, int(duration / 2)))
        #num_frames = int(duration)

        # evenly spaced timestamps
        timestamps = [
            start + (duration * k) / (num_frames - 1)
            for k in range(num_frames)
        ]

        # avoid exact end frame (can cause read issues)
        timestamps[-1] = max(start, timestamps[-1] - 0.1)

        # optional: remove near-duplicate timestamps
        timestamps = list(dict.fromkeys([round(t, 2) for t in timestamps]))

        for j, t in enumerate(timestamps):

            cap.set(cv2.CAP_PROP_POS_FRAMES, int(t * fps))

            ret, frame = cap.read()

            if ret:
                path = os.path.join(output_dir, f"scene_{i}_frame_{j}.jpg")
                cv2.imwrite(path, frame)
                frames.append(path)

        scene_frames.append(frames)

    cap.release()

    return scene_frames
