# Handwriting Page Scanner

Detects and highlights word-level regions in a scanned or photographed handwritten notebook page using OpenCV.



---

## What it does

Takes a photo of a handwritten page as input and draws green bounding boxes around every detected word region. Works well on messy, real-world handwriting — not just clean samples.

---

## Setup

```bash
pip install opencv-python numpy
```

---

## Usage

1. Clone the repo
2. Change the image path in `contour_detection.py` to your own file
3. Run:

```bash
python contour_detection.py
```

The script opens a resizable window showing the detected regions. Press any key to close.

---

## Code Walkthrough

```python
img = cv2.imread(r"path\to\image.jpg")
```
Loads the image as a NumPy array — a 3D grid of numbers (height × width × 3 color channels).

```python
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
```
Converts to grayscale — one number per pixel instead of three. Required before thresholding.

```python
thresh = cv2.adaptiveThreshold(
    gray, 255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY_INV,
    13, 4
)
```
Converts grayscale to pure black and white. `THRESH_BINARY_INV` inverts the output so ink is white and paper is black — required for contour detection. `ADAPTIVE` means the threshold is calculated block by block across the image, which handles uneven lighting and ink bleed-through from the back of the page much better than a single global threshold.

- `13` — block size: how many surrounding pixels to consider when deciding if a pixel is ink or paper. Must be odd. Higher = smoother but may miss detail.
- `4` — constant: subtracted from the calculated threshold. Higher = thinner ink. Lower = bolder ink.

```python
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
```
Finds all connected white regions (ink blobs) in the binary image. `RETR_EXTERNAL` returns only outermost contours, ignoring holes inside letters like `o` or `e`.

```python
x, y, w, h = cv2.boundingRect(cnt)
if 5 < w < 200 and 5 < h < 70:
```
Gets the bounding box for each contour and filters by size — removes tiny noise dots (too small) and large blobs like the page border (too large). These values were tuned to match the actual letter sizes in the scanned image.

```python
cv2.rectangle(output, (x, y), (x+w, y+h), (0, 255, 0), 1)
```
Draws a green rectangle on a copy of the original image. `(0, 255, 0)` is green in BGR. `1` is the line thickness.

---

## Tuning Parameters

If detection is off on your image, these are the values to adjust:

| Parameter | Location | Effect |
|-----------|----------|--------|
| `13` (block size) | `adaptiveThreshold` | Higher = smoother, lower = more detail |
| `4` (constant) | `adaptiveThreshold` | Higher = thinner ink, lower = bolder |
| `5 < w < 200` | filter | Adjust for your letter width in pixels |
| `5 < h < 70` | filter | Adjust for your letter height in pixels |

To find the right filter values for your image, print all contour sizes before filtering:

```python
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    print(f"w={w}, h={h}")
```
![Sample Output](output_sample.png)
---

## Known Limitations

- Ruled lines on notebook paper sometimes get detected — can be filtered with `w < 3 * h`
- Letters that touch each other may get grouped into one box
- Very light ink or heavy bleed-through may need threshold tuning

---

## Dependencies

- Python 3.x
- OpenCV (`cv2`)
- NumPy
