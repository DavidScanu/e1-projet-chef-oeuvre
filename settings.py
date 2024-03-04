from pathlib import Path
import sys

# Récupère le chemin absolu du fichier actuel
file_path = Path(__file__).resolve()

# Récupère le répertoire parent du fichier actuel
root_path = file_path.parent

# Ajoutez le chemin racine à la liste sys.path s'il n'y est pas déjà
if root_path not in sys.path:
    sys.path.append(str(root_path))

# Récupère le chemin relatif du répertoire racine par rapport au répertoire de travail actuel
ROOT = root_path.relative_to(Path.cwd())

# Sources
IMAGE = 'Image'
VIDEO = 'Video'
WEBCAM = 'Webcam'
RTSP = 'RTSP'
YOUTUBE = 'YouTube'

SOURCES_LIST = [IMAGE, VIDEO, WEBCAM, RTSP, YOUTUBE]

# Configuration des images
IMAGES_DIR = ROOT / 'images'
DEFAULT_IMAGE = IMAGES_DIR / 'cover-01.jpg'
DEFAULT_DETECT_IMAGE = IMAGES_DIR / 'cover-01-detected.jpg'

# Configuration des vidéos
VIDEO_DIR = ROOT / 'videos'
VIDEO_1_PATH = VIDEO_DIR / 'demo_1.mp4'
VIDEO_2_PATH = VIDEO_DIR / 'video_2.mp4'
VIDEO_3_PATH = VIDEO_DIR / 'video_3.mp4'
VIDEOS_DICT = {
    'video_1': VIDEO_1_PATH,
    'video_2': VIDEO_2_PATH,
    'video_3': VIDEO_3_PATH,
}

# Configuration du modèle
MODEL_DIR = ROOT / 'weights'
DETECTION_MODEL = MODEL_DIR / 'yolov8n.pt'
# Dans le cas de votre modèle personnalisé, commentez la ligne ci-dessus et
# Placez le nom de votre fichier .pt de modèle personnalisé sur la ligne ci-dessous
# DETECTION_MODEL = MODEL_DIR / 'my_detection_model.pt'

SEGMENTATION_MODEL = MODEL_DIR / 'yolov8n-seg.pt'

# Webcam
WEBCAM_PATH = 0
