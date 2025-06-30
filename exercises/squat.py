import cv2
from pose_estimation.angle_calculation import calculate_angle

class Squat:
    def __init__(self):
        self.counter = 0
        self.stage = "Up"
        
        self.feedback_messages = {
            'hip_hinge': "",
            'depth': "",
            'general': ""
        }
        
        self.ideal_hip_hinge_range = 55  # Shoulder-hip-knee angle for proper hip hinge
        
        self.angle_threshold_up = 165
        self.angle_threshold_down = 90  
    
    def analyze_form(self, landmarks, frame, hip_knee_angle_left, hip_knee_angle_right):
        """Analyze squat form and generate feedback"""
        feedback_msgs = {'hip_hinge': "", 'depth': "", 'general': ""}
        
        try:
            # Get landmark positions for hip hinge analysis
            shoulder_left = [int(landmarks[11].x * frame.shape[1]), int(landmarks[11].y * frame.shape[0])]
            shoulder_right = [int(landmarks[12].x * frame.shape[1]), int(landmarks[12].y * frame.shape[0])]
            hip_left = [int(landmarks[23].x * frame.shape[1]), int(landmarks[23].y * frame.shape[0])]
            hip_right = [int(landmarks[24].x * frame.shape[1]), int(landmarks[24].y * frame.shape[0])]
            knee_left = [int(landmarks[25].x * frame.shape[1]), int(landmarks[25].y * frame.shape[0])]
            knee_right = [int(landmarks[26].x * frame.shape[1]), int(landmarks[26].y * frame.shape[0])]
            
            hip_angle_left = calculate_angle(shoulder_left, hip_left, knee_left)
            hip_angle_right = calculate_angle(shoulder_right, hip_right, knee_right)
            avg_hip_angle = (hip_angle_left + hip_angle_right) / 2
            
            if avg_hip_angle < self.ideal_hip_hinge_range:
                feedback_msgs['hip_hinge'] = "Too much forward lean!"
            
            # Depth feedback - checking how low the trainer is going
            avg_depth_angle = (hip_knee_angle_left + hip_knee_angle_right) / 2
            
            if feedback_msgs["hip_hinge"] == "" and feedback_msgs["depth"] == "":
                feedback_msgs['general'] = "Excellent form!"
            
            self.feedback_messages = feedback_msgs
            
        except Exception as e:
            self.feedback_messages = {'hip_hinge': "", 'depth': "", 'general': ""}

    def track_squat(self, landmarks, frame):
        # Landmark coordinates
        hip_left = [int(landmarks[23].x * frame.shape[1]), int(landmarks[23].y * frame.shape[0])]
        knee_left = [int(landmarks[25].x * frame.shape[1]), int(landmarks[25].y * frame.shape[0])]
        shoulder_left = [int(landmarks[11].x * frame.shape[1]), int(landmarks[11].y * frame.shape[0])]
        ankle_left = [int(landmarks[27].x * frame.shape[1]), int(landmarks[27].y * frame.shape[0])]

        hip_right = [int(landmarks[24].x * frame.shape[1]), int(landmarks[24].y * frame.shape[0])]
        knee_right = [int(landmarks[26].x * frame.shape[1]), int(landmarks[26].y * frame.shape[0])]
        shoulder_right = [int(landmarks[12].x * frame.shape[1]), int(landmarks[12].y * frame.shape[0])]
        ankle_right = [int(landmarks[28].x * frame.shape[1]), int(landmarks[28].y * frame.shape[0])]

        angle_left = calculate_angle(hip_left, knee_left, ankle_left)
        angle_right = calculate_angle(hip_right, knee_right, ankle_right)
        hip_angle_left = calculate_angle(shoulder_left, hip_left, knee_left)
        hip_angle_right = calculate_angle(shoulder_right, hip_right, knee_right)

        avg_depth_angle = (angle_left + angle_right) / 2

        self.analyze_form(landmarks, frame, angle_left, angle_right)

        # Draw lines and circles to highlight key points
        self.draw_line_with_style(frame, shoulder_left, hip_left, (178, 102, 255), 2)
        self.draw_line_with_style(frame, hip_left, knee_left, (178, 102, 255), 2)
        self.draw_line_with_style(frame, knee_left, ankle_left, (178, 102, 255), 2)
        self.draw_line_with_style(frame, shoulder_right, hip_right, (51, 153, 255), 2)
        self.draw_line_with_style(frame, hip_right, knee_right, (51, 153, 255), 2)
        self.draw_line_with_style(frame, knee_right, ankle_right, (51, 153, 255), 2)

        self.draw_circle(frame, shoulder_left, (178, 102, 255), 8)
        self.draw_circle(frame, hip_left, (178, 102, 255), 8)
        self.draw_circle(frame, knee_left, (178, 102, 255), 8)
        self.draw_circle(frame, ankle_left, (178, 102, 255), 8)
        self.draw_circle(frame, shoulder_right, (51, 153, 255), 8)
        self.draw_circle(frame, hip_right, (51, 153, 255), 8)
        self.draw_circle(frame, knee_right, (51, 153, 255), 8)
        self.draw_circle(frame, ankle_right, (51, 153, 255), 8)

        # Display angles on screen
        angle_text_position = (knee_left[0] + 10, knee_left[1] - 10)
        cv2.putText(frame, f'Angle: {int(angle_left)}', angle_text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        angle_text_position_right = (knee_right[0] + 10, knee_right[1] - 10)
        cv2.putText(frame, f'Angle: {int(angle_right)}', angle_text_position_right, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        angle_text_position = (hip_left[0] + 10, hip_left[1] - 10)
        cv2.putText(frame, f'Angle: {int(hip_angle_left)}', angle_text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        angle_text_position_right = (hip_right[0] + 10, hip_right[1] - 10)
        cv2.putText(frame, f'Angle: {int(hip_angle_right)}', angle_text_position_right, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        if self.feedback_messages["general"] == "Excellent form!":
            if angle_left <= self.angle_threshold_down and self.stage == "Up":
                self.stage = "Down"
                self.counter += 1
            elif angle_left >= self.angle_threshold_up and self.stage == "Down":
                self.stage = "Up"

            
        return (self.counter, angle_left, self.stage,
                self.feedback_messages['hip_hinge'], 
                self.feedback_messages['depth'],
                self.feedback_messages['general'])

    def draw_line_with_style(self, frame, start_point, end_point, color, thickness):
        """Draw a line with specified style."""
        cv2.line(frame, start_point, end_point, color, thickness, lineType=cv2.LINE_AA)

    def draw_circle(self, frame, center, color, radius):
        """Draw a circle with specified style."""
        cv2.circle(frame, center, radius, color, -1)  # -1 to fill the circle