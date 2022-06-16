from random import expovariate


AUTH_ENDPOINT = "alfresco/api/-default-/public/authentication/versions/1"

BASE_ENDPOINT = "alfresco/api/-default-/public/alfresco/versions/1"

AUDIO_PATTERNS = [".wav", ".WAV"]
IMAGE_PATTERNS = [
    ".gif",
    ".GIF",
    ".jpg",
    ".JPG",
    ".jpeg",
    ".JPEG",
    ".tiff",
    ".TIFF",
    ".png",
    ".PNG",
]
VIDEO_PATTERNS = [".mp4","webm"]

FILE_PATTERNS = AUDIO_PATTERNS + VIDEO_PATTERNS + IMAGE_PATTERNS
