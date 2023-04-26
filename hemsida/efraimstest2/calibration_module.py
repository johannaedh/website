import cv2
import os
from roboflow import Roboflow
import numpy as np
import tempfile
import shutil

def calibrate_cross(video_path):
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Created folder dodge in {temp_dir}")

        # The rest of your code, but replace the hard-coded paths with temp_dir
        video = cv2.VideoCapture(video_path)

        i = 0
        while video.isOpened():
            ret, frame = video.read()
            if not ret:
                break
            cv2.imwrite(os.path.join(temp_dir, 'dodge' + str(i) + '.jpg'), frame)
            i += 1
        frame_rate = int(video.get(cv2.CAP_PROP_FPS))

        video.release()
        cv2.destroyAllWindows()

        rf = Roboflow(api_key="HEfNlI5lkTBazBknN8jz") #  CPkBglSIfMhKhrghnYcq
        project = rf.workspace().project("ball-images")
        model = project.version(2).model

        list_of_images_numbers = list(range(1, i, frame_rate))

        x = []
        y = []
        w = []
        h = []

        for k in list_of_images_numbers:
            prediction = model.predict(temp_dir + "/dodge" + str(k) + '.jpg')
            for result in prediction.json()['predictions']:
                x.append(result['x'])
                y.append(result['y'])
                w.append(result['width'])
                h.append(result['height'])
            if len(x) < 2:
                continue
            if len(y) < 2:
                continue
            if max(abs(x[-2] - x[-1]), abs(y[-2] - y[-1])) < 5:
                print('Calibration for camera done successfully')
                break

        if len(x) == 0:
            return None, None, None
        else:
            cross_position_x = x[-1]
            cross_position_y = y[-1]
            ball_radius = (w[-1] + h[-1]) / 4

            print('x: ' + str(cross_position_x), 'y: ' + str(cross_position_y))
            print('Bollens radie för camera: ' + str(ball_radius))
            return cross_position_x, cross_position_y, ball_radius

# The temporary directory is automatically deleted when exiting the 'with' block.
