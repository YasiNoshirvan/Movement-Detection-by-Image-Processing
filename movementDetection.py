import numpy as np
import cv2 as cv
from pathlib import Path


def rescale_frame(frame, percent=40):
    width = int(frame.shape[1] * percent / 100)
    height = int(frame.shape[0] * percent / 100)
    dim = (width, height)
    return cv.resize(frame, dim, interpolation=cv.INTER_AREA)


video_path = Path(__file__).resolve().parent / 'videos' / 'street_camera.mp4'
cap = cv.VideoCapture(str(video_path))

if not cap.isOpened():
    raise FileNotFoundError(f'Cannot open video: {video_path}')

ret, frame1 = cap.read()
if not ret:
    cap.release()
    raise ValueError('Could not read the first frame.')

# Save output video
output_path = Path(__file__).resolve().parent / 'movement_detection_output.mp4'

fps = cap.get(cv.CAP_PROP_FPS)
if fps <= 0:
    fps = 30

first_resized = rescale_frame(frame1, 40)
height, width = first_resized.shape[:2]

fourcc = cv.VideoWriter_fourcc(*'mp4v')
video_writer = cv.VideoWriter(str(output_path), fourcc, fps, (width, height))

if not video_writer.isOpened():
    cap.release()
    raise RuntimeError('Could not create output video.')

min_area = 150  # Ignore small moving areas (noise)

while True:
    ret, frame2 = cap.read()
    if not ret:
        break

    resized_frame1 = rescale_frame(frame1, 40)
    resized_frame2 = rescale_frame(frame2, 40)

    frame_diff = cv.absdiff(resized_frame1, resized_frame2)
    frame_diff_gr = cv.cvtColor(frame_diff, cv.COLOR_BGR2GRAY)
    blurred_frame = cv.GaussianBlur(frame_diff_gr, (5, 5), 0)
    _, mask = cv.threshold(blurred_frame, 15, 255, cv.THRESH_BINARY)

    # Connect nearby white areas and make moving objects easier to detect
    kernel = np.ones((3, 3), np.uint8)
    mask = cv.dilate(mask, kernel, iterations=2)

    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    moving_regions = 0
    for contour in contours:
        if cv.contourArea(contour) < min_area:
            continue

        x, y, w, h = cv.boundingRect(contour)
        cv.rectangle(resized_frame1, (x, y), (x + w, y + h), (0, 0, 255), 2)
        moving_regions += 1

    cv.putText(resized_frame1, f'Moving regions: {moving_regions}',
               (10, 25), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Save only the Movement Detection video
    video_writer.write(resized_frame1)

    cv.imshow('Movement Detection', rescale_frame(resized_frame1, 40))
    cv.imshow('Motion Mask', rescale_frame(mask, 40))

    frame1 = frame2  # Compare the next frame with the current one

    if cv.waitKey(25) & 0xFF == 27:  # ESC
        break

cap.release()
video_writer.release()
cv.destroyAllWindows()

print(f'Video saved successfully: {output_path}')