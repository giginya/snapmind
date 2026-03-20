import pytesseract
import cv2
from PIL import Image

# ------------------------------------------------------------
# PURPOSE:
# Improve image BEFORE OCR for better accuracy
# ------------------------------------------------------------


def preprocess_image(image_path):

    # Load image
    img = cv2.imread(image_path)

    # Convert to grayscale (removes color noise)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Convert to black/white (important for OCR clarity)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    return thresh


# ------------------------------------------------------------
# PURPOSE:
# Extract text from image
# ------------------------------------------------------------

def extract_text(image_path):

    try:
        processed = preprocess_image(image_path)

        # Convert to PIL for Tesseract
        pil_img = Image.fromarray(processed)

        text = pytesseract.image_to_string(pil_img)

        return text

    except Exception as e:
        print("OCR Error:", e)
        return ""
