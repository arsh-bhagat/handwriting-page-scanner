import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

img = cv2.imread("handwriting1.jpeg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cropped = gray[100:1500, 50:850]

thresh = cv2.adaptiveThreshold(
    cropped, 255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY,
    11, 4
)
text = pytesseract.image_to_string(thresh, config="--psm 11")
print(text)

x = len(text)
print("total characters recognised: ", x)
cv2.namedWindow("thresh", cv2.WINDOW_NORMAL)
cv2.resizeWindow("thresh", 800, 1000)
cv2.imshow("thresh", thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()