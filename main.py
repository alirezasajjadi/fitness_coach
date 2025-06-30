import cv2
import numpy as np
from pose_estimation.estimation import PoseEstimator
from exercises.squat import Squat
from exercises.hammer_curl import HammerCurl
from exercises.push_up import PushUp
from feedback.layout import layout_indicators
from feedback.information import get_exercise_info
from utils.draw_text_with_background import draw_text_with_background

def main():
    # video_path = r"C:\Users\yakupzengin\Fitness-Trainer\data\squat.mp4"
    # video_path = r"C:\Users\yakupzengin\Fitness-Trainer\data\push_up.mp4"
    video_path = "/home/alireza/Documents/university/project/pose estimation/gith/data/pushup/pushupcrt1.mp4"

    # exercise_type = "hammer_curl"
    exercise_type = "push_up"
    # exercise_type = "squat"
# 20 5

    cap = cv2.VideoCapture(video_path)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FPS, 30)

    pose_estimator = PoseEstimator()

    # fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30
    # frame_delay = int(1000 / fps)

    if exercise_type == "hammer_curl":
        exercise = HammerCurl()
    elif exercise_type == "squat":
        exercise = Squat()
    elif exercise_type == "push_up":
        exercise = PushUp()
    else:
        print("Invalid exercise type.")
        return

    exercise_info = get_exercise_info(exercise_type)

    window_name = f"{exercise_type.replace('_', ' ').title()} Tracker"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 1280, 720)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output_file = "output.mp4"
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # frame = cv2.flip(frame, 1)

        results = pose_estimator.estimate_pose(frame, exercise_type)

        if results.pose_landmarks:
            if exercise_type == "squat":
                counter, angle, stage, msg_hip, msg_depth, msg_general1 = exercise.track_squat(results.pose_landmarks.landmark, frame)
                layout_indicators(frame, exercise_type, (counter, angle, stage, msg_hip, msg_depth, msg_general1))
            elif exercise_type == "hammer_curl":
                (counter_right, counter_left,
                 warning_message_right, warning_message_left, stage_right, stage_left) = exercise.track_hammer_curl(
                    results.pose_landmarks.landmark, frame)
                layout_indicators(frame, exercise_type,
                                  (counter_right, counter_left,
                                   warning_message_right, warning_message_left, stage_right, stage_left))
            elif exercise_type == "push_up":
                counter, angle, stage, msg_right, msg_left, msg_general = exercise.track_push_up(results.pose_landmarks.landmark, frame)
                layout_indicators(frame, exercise_type, (counter, angle, stage, msg_right, msg_left, msg_general))


        draw_text_with_background(frame, f"Exercise: {exercise_info.get('name', 'N/A')}", (40, 50),
                                  cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255,), (118, 29, 14, 0.79), 1)


        out.write(frame)

        cv2.imshow(window_name, frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
