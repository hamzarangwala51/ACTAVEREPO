# visual_detection.py
# visual_detection.py
import cv2
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
def detect_visual_text(video_path):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    visual_text = ""

    # Loop through video frames
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        # Convert the frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Perform OCR on the grayscale frame
        text = pytesseract.image_to_string(gray_frame)

        # Append the recognized text to the result
        visual_text += text + " "

    cap.release()

    return visual_text.strip()

