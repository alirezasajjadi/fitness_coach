import cv2
import numpy as np
from pose_estimation.angle_calculation import calculate_angle

class HammerCurl:
    def __init__(self):
        self.counter_right = 0
        self.counter_left = 0
        self.stage_right = "Down"
        self.stage_left = "Down"

        self.angle_threshold = 30  # threshold for hip-shoulder-elbow misalignment
        self.angle_threshold_up = 45 
        self.angle_threshold_down = 155

    def track_hammer_curl(self, landmarks, frame):
        shoulder_right = [int(landmarks[11].x * frame.shape[1]), int(landmarks[11].y * frame.shape[0])]
        elbow_right = [int(landmarks[13].x * frame.shape[1]), int(landmarks[13].y * frame.shape[0])]
        hip_right = [int(landmarks[23].x * frame.shape[1]), int(landmarks[23].y * frame.shape[0])]
        wrist_right = [int(landmarks[15].x * frame.shape[1]), int(landmarks[15].y * frame.shape[0])]

        shoulder_left = [int(landmarks[12].x * frame.shape[1]), int(landmarks[12].y * frame.shape[0])]
        elbow_left = [int(landmarks[14].x * frame.shape[1]), int(landmarks[14].y * frame.shape[0])]
        hip_left = [int(landmarks[24].x * frame.shape[1]), int(landmarks[24].y * frame.shape[0])]
        wrist_left = [int(landmarks[16].x * frame.shape[1]), int(landmarks[16].y * frame.shape[0])]

        angle_right_counter = calculate_angle(shoulder_right, elbow_right, wrist_right)
        angle_left_counter = calculate_angle(shoulder_left, elbow_left, wrist_left)

        angle_shoulder_right = calculate_angle(elbow_right, shoulder_right, hip_right)
        angle_shoulder_left = calculate_angle(elbow_left, shoulder_left, hip_left)

        self.draw_line_with_style(frame, shoulder_left, elbow_left, (255, 0, 0), 4)
        self.draw_line_with_style(frame, elbow_left, wrist_left, (255, 0, 0), 4)
        self.draw_line_with_style(frame, shoulder_left, hip_left, (255, 0, 0), 4)

        self.draw_line_with_style(frame, shoulder_right, elbow_right, (255, 0, 0), 4)
        self.draw_line_with_style(frame, elbow_right, wrist_right, (255, 0, 0), 4)
        self.draw_line_with_style(frame, shoulder_right, hip_right, (255, 0, 0), 4)

        # highlight key points
        self.draw_circle(frame, shoulder_left, (0, 255, 0), 8)
        self.draw_circle(frame, elbow_left, (0, 255, 0), 8)
        self.draw_circle(frame, wrist_left, (0, 255, 0), 8)
        self.draw_circle(frame, hip_left, (0, 255, 0), 8)

        self.draw_circle(frame, shoulder_right, (0, 255, 0), 8)
        self.draw_circle(frame, elbow_right, (0, 255, 0), 8)
        self.draw_circle(frame, wrist_right, (0, 255, 0), 8)
        self.draw_circle(frame, hip_right, (0, 255, 0), 8)

        angle_text_position_left = (elbow_left[0] + 10, elbow_left[1] - 10)
        cv2.putText(frame, f'Angle: {int(angle_left_counter)}', angle_text_position_left, cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                     (0, 0, 0), 2)

        angle_text_position_right = (elbow_right[0] + 10, elbow_right[1] - 10)
        cv2.putText(frame, f'Angle: {int(angle_right_counter)}', angle_text_position_right, cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 0, 0), 2)

        angle_text_position_shoulder_left = (shoulder_left[0] + 10, shoulder_left[1] - 10)
        cv2.putText(frame, f'Angle: {int(angle_shoulder_left)}', angle_text_position_shoulder_left, cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 0, 0), 2)
        
        angle_text_position_shoulder_right = (shoulder_right[0] + 10, shoulder_right[1] - 10)
        cv2.putText(frame, f'Angle: {int(angle_shoulder_right)}', angle_text_position_shoulder_right, cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 0, 0), 2)
        
        warning_message_right = None
        warning_message_left = None

        # Check for misalignment based on elbow-shoulder-hip angle
        if abs(angle_shoulder_right) > self.angle_threshold:
            warning_message_right = f"Keep elbow closer to body. Angle: {angle_shoulder_right:.2f}"
        if abs(angle_shoulder_left) > self.angle_threshold:
            warning_message_left = f"Keep elbow closer to body. Angle: {angle_shoulder_left:.2f}"

        if  warning_message_right==None:
            if self.stage_right == "Down" and angle_right_counter <= self.angle_threshold_up:
                self.stage_right = "Up"
                self.counter_right +=1
            elif angle_right_counter >= self.angle_threshold_down:
                self.stage_right = "Down"

        if  warning_message_left==None:
            if self.stage_left == "Down" and angle_left_counter <= self.angle_threshold_up:
                self.stage_left = "Up"
                self.counter_left +=1
            elif angle_left_counter >= self.angle_threshold_down:
                self.stage_left = "Down"

        if warning_message_left==None:
            warning_message_left = "Excellent form!"
        if warning_message_right==None:
            warning_message_right = "Excellent form!"
        
        return self.counter_right, self.counter_left, warning_message_right, warning_message_left, self.stage_right, self.stage_left

    def draw_line_with_style(self, frame, start_point, end_point, color, thickness):
        cv2.line(frame, start_point, end_point, color, thickness, lineType=cv2.LINE_AA)

    def draw_circle(self, frame, center, color, radius):
        cv2.circle(frame, center, radius, color, -1) 
