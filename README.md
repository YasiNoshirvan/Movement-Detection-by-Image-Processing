### 🎥 Movement Detection by Image Processing

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white) ![OpenCV](https://img.shields.io/badge/OpenCV-Video%20Processing-5C3EE8?logo=opencv&logoColor=white)

A small computer vision project that highlights **moving regions in a video** using classical image processing techniques. It compares consecutive frames, removes some noise, and draws bounding boxes around areas where motion is detected.

The processed video is saved as an MP4, making it easy to review the output without running the script.

## ✨ What it does

- Detects changes between consecutive video frames.
- Uses grayscale conversion, Gaussian blur, and thresholding to create a motion mask.
- Applies dilation and contour filtering to reduce small noisy detections.
- Draws red bounding boxes and displays the number of detected **moving regions**.
- Saves the annotated output video; the mask is only shown during execution.

## 🎬 Example output

**[▶ View the processed video](movement_detection_output.mp4)**

## 📂 Files

```text
├── movementDetection.py
├── street_camera.mp4
└── movement_detection_output.mp4
```

## ⚙️ Run locally

```bash
git clone https://github.com/YasiNoshirvan/Movement-Detection-by-Image-Processing.git
cd Movement-Detection-by-Image-Processing
pip install opencv-python numpy
```

**One path adjustment:** The video is currently stored at the repository root, while the Python script looks for it inside `videos/`. In `movementDetection.py`, change the video path to:

```python
video_path = Path(__file__).resolve().parent / 'street_camera.mp4'
```

Then run:

```bash
python movementDetection.py
```

Press **Esc** to stop. The program writes `movement_detection_output.mp4` to the project folder.

## 📝 Limitations

This is a **motion-region detector**, not an object tracker or a vehicle-counting system. One object can produce multiple regions, and shadows or camera motion may also trigger detections. The contour-area threshold can be adjusted for different videos.

---

*Built as a practical OpenCV learning project focused on video processing and motion analysis.*
