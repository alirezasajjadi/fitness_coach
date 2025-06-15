import cv2
import time
from pose_estimation.angle_calculation import calculate_angle
import math

import cv2
import time
import math
from pose_estimation.angle_calculation import calculate_angle

class PushUp:
    def __init__(self):
        self.counter = 0
        self.stage = "Up"
        self.angle_threshold_up = 150 
        self.angle_threshold_down = 77  
        self.last_counter_update = time.time()
        
        self.feedback_messages = {
            'left': "",
            'right': "",
            'general': ""
        }
        
        self.ideal_back_angle_range = (160, 180)  

        self.last_stage_change = time.time()

    def analyze_form(self, landmarks, frame, angle_left, angle_right):
        """Analyze push-up form and generate feedback"""
        feedback_msgs = {'left': "", 'right': "", 'general': "Excellent form!"}
        
        try:
            left_shoulder = [int(landmarks[11].x * frame.shape[1]), int(landmarks[11].y * frame.shape[0])]
            right_shoulder = [int(landmarks[12].x * frame.shape[1]), int(landmarks[12].y * frame.shape[0])]
            left_hip = [int(landmarks[23].x * frame.shape[1]), int(landmarks[23].y * frame.shape[0])]
            right_hip = [int(landmarks[24].x * frame.shape[1]), int(landmarks[24].y * frame.shape[0])]
            left_ankle = [int(landmarks[27].x * frame.shape[1]), int(landmarks[27].y * frame.shape[0])]
            right_ankle = [int(landmarks[28].x * frame.shape[1]), int(landmarks[28].y * frame.shape[0])]
            
            back_angle_left = calculate_angle(left_shoulder, left_hip, left_ankle)
            back_angle_right = calculate_angle(right_shoulder, right_hip, right_ankle)
            avg_back_angle = (back_angle_left + back_angle_right) / 2
            
         
            # Back alignment feedback
            if avg_back_angle < self.ideal_back_angle_range[0]:
                feedback_msgs['general'] = "Keep back straight!"

            # if self.stage == "Down" and min(angle_left, angle_right) > self.angle_threshold_down:
                # feedback_msgs['general'] = "Go lower!"

            # # Speed analysis
            # current_time = time.time()
            # if hasattr(self, 'last_stage') and self.last_stage != self.stage:
            #     stage_duration = current_time - self.last_stage_change
            #     if stage_duration < 0.5:  # Too fast
            #         feedback_msgs['general'] = "Slower movement! 🐌"
            #         self.form_violations['too_fast'] += 1
            #     self.last_stage_change = current_time
            #     self.last_stage = self.stage
            
            # Range of motion feedback based on stage
            # if self.stage == "Descent" and min(angle_left, angle_right) > 100:
            #     feedback_msgs['general'] = "Go lower!"
            
            if (self.ideal_back_angle_range[0] <= avg_back_angle <= self.ideal_back_angle_range[1] and
                feedback_msgs['general'] == ""):
                feedback_msgs['general'] = "Excellent form!"
            
            self.feedback_messages = feedback_msgs
            
        except Exception as e:
            self.feedback_messages = {'left': "", 'right': "", 'general': ""}

    def track_push_up(self, landmarks, frame):
        
        shoulder_left = [int(landmarks[11].x * frame.shape[1]), int(landmarks[11].y * frame.shape[0])]
        elbow_left = [int(landmarks[13].x * frame.shape[1]), int(landmarks[13].y * frame.shape[0])]
        wrist_left = [int(landmarks[15].x * frame.shape[1]), int(landmarks[15].y * frame.shape[0])]
        hip_left = [int(landmarks[23].x * frame.shape[1]), int(landmarks[23].y * frame.shape[0])]
        ankle_left = [int(landmarks[27].x * frame.shape[1]), int(landmarks[27].y * frame.shape[0])]

        ankle_right = [int(landmarks[28].x * frame.shape[1]), int(landmarks[28].y * frame.shape[0])]
        hip_right = [int(landmarks[24].x * frame.shape[1]), int(landmarks[24].y * frame.shape[0])]
        shoulder_right = [int(landmarks[12].x * frame.shape[1]), int(landmarks[12].y * frame.shape[0])]
        elbow_right = [int(landmarks[14].x * frame.shape[1]), int(landmarks[14].y * frame.shape[0])]
        wrist_right = [int(landmarks[16].x * frame.shape[1]), int(landmarks[16].y * frame.shape[0])]

        angle_elbow_left = calculate_angle(shoulder_left, elbow_left, wrist_left)
        angle_elbow_right = calculate_angle(shoulder_right, elbow_right, wrist_right)
        angle_hip_left = calculate_angle(shoulder_left, hip_left, ankle_left)
        angle_hip_right = calculate_angle(shoulder_right, hip_right, ankle_right)

        self.analyze_form(landmarks, frame, angle_elbow_left, angle_elbow_right)

        self.draw_line_with_style(frame, shoulder_left, elbow_left, (0, 0, 255), 2)
        self.draw_line_with_style(frame, elbow_left, wrist_left, (0, 0, 255), 2)
        self.draw_line_with_style(frame, shoulder_left, hip_left, (0, 0, 255), 2)
        self.draw_line_with_style(frame, hip_left, ankle_left, (0, 0, 255), 2)

        self.draw_line_with_style(frame, shoulder_right, elbow_right, (102, 0, 0), 2)
        self.draw_line_with_style(frame, elbow_right, wrist_right, (102, 0, 0), 2)
        self.draw_line_with_style(frame, shoulder_right, hip_right, (102, 0, 0), 2)
        self.draw_line_with_style(frame, hip_right, ankle_right, (102, 0, 0), 2)


        self.draw_circle(frame, shoulder_left, (0, 0, 255), 8)
        self.draw_circle(frame, elbow_left, (0, 0, 255), 8)
        self.draw_circle(frame, wrist_left, (0, 0, 255), 8)
        self.draw_circle(frame, hip_left, (0, 0, 255), 8)
        self.draw_circle(frame, ankle_left, (102, 0, 0), 8)

        self.draw_circle(frame, shoulder_right, (102, 0, 0), 8)
        self.draw_circle(frame, elbow_right, (102, 0, 0), 8)
        self.draw_circle(frame, wrist_right, (102, 0, 0), 8)
        self.draw_circle(frame, hip_right, (102, 0, 0), 8)
        self.draw_circle(frame, ankle_right, (102, 0, 0), 8)

        angle_text_position_eblow_left = (elbow_left[0] + 10, elbow_left[1] - 10)
        cv2.putText(frame, f'Angle: {int(angle_elbow_left)}', angle_text_position_eblow_left, 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        angle_text_position_elbow_right = (elbow_right[0] + 10, elbow_right[1] - 10)
        cv2.putText(frame, f'Angle: {int(angle_elbow_right)}', angle_text_position_elbow_right, 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        angle_text_position_hip_left = (hip_left[0] + 10, hip_left[1] - 10)
        cv2.putText(frame, f'Angle: {int(angle_hip_left)}', angle_text_position_hip_left, 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        angle_text_position_hip_right = (hip_right[0] + 10, hip_right[1] - 10)
        cv2.putText(frame, f'Angle: {int(angle_hip_right)}', angle_text_position_hip_right, 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        current_time = time.time()

        if self.feedback_messages['general'] == "Excellent form!":
            if angle_elbow_right >= self.angle_threshold_up:
                self.stage = "Up" 
            elif self.stage == "Up" and angle_elbow_right <= self.angle_threshold_down:
                self.stage = "Down"
                # Increment counter only if enough time has passed since last update
                if current_time - self.last_counter_update > 1:  # 1 second threshold
                    self.counter += 1
                    self.last_counter_update = current_time        

        return (self.counter, angle_elbow_left, self.stage, 
                self.feedback_messages['left'], self.feedback_messages['right'], 
                self.feedback_messages['general'])

    def draw_line_with_style(self, frame, start_point, end_point, color, thickness):
        """Draw a line with specified style."""
        cv2.line(frame, start_point, end_point, color, thickness, lineType=cv2.LINE_AA)

    def draw_circle(self, frame, center, color, radius):
        """Draw a circle with specified style."""
        cv2.circle(frame, center, radius, color, -1)  # -1 to fill the circle