import cv2
import numpy as np

img = cv2.imread("handwriting1.jpeg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

thresh = cv2.adaptiveThreshold(
    gray, 255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY_INV,
    13, 4
)

contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

output = img.copy()
filtered = 0
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    if 5 < w < 200 and 5 < h < 70:
        cv2.rectangle(output, (x, y), (x+w, y+h), (0, 255, 0), 1)
        filtered += 1

print("Filtered:", filtered)

cv2.namedWindow("Contours", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Contours", 800, 1000)
cv2.imshow("Contours", output)
cv2.waitKey(0)
cv2.destroyAllWindows()
