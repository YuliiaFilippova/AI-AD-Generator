from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector
import cv2


def detect_scenes(video_path):

    video_manager = VideoManager([video_path])
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector())

    video_manager.start()

    scene_manager.detect_scenes(frame_source=video_manager)

    scene_list = scene_manager.get_scene_list()

    scenes = []

    for start, end in scene_list:
        scenes.append((start.get_seconds(), end.get_seconds()))

    return scenes

def split_by_time(video_path, chunk_duration=8.0):

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps

    scenes = []
    start = 0.0

    while start < duration:
        end = min(start + chunk_duration, duration)
        scenes.append((start, end))
        start = end

    return scenes