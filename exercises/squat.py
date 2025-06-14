import cv2
from pose_estimation.angle_calculation import calculate_angle

class Squat:
    def __init__(self):
        self.counter = 0
        self.stage = "Up"
        
        # Add feedback messages dictionary
        self.feedback_messages = {
            'hip_hinge': "",
            'depth': "",
            'general': ""
        }
        
        # Define ideal ranges for squat form
        self.ideal_hip_hinge_range = (45, 90)  # Shoulder-hip-knee angle for proper hip hinge
        self.ideal_squat_depth = 45  # Hip-knee angle for proper depth
        self.minimum_squat_depth = 120  # Minimum acceptable depth

    def calculate_angle(self, hip, knee, ankle):
        return calculate_angle(hip, knee, ankle)
    
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
            
            # Calculate hip hinge angle (shoulder-hip-knee angle)
            hip_hinge_angle_left = calculate_angle(shoulder_left, hip_left, knee_left)
            hip_hinge_angle_right = calculate_angle(shoulder_right, hip_right, knee_right)
            avg_hip_hinge_angle = (hip_hinge_angle_left + hip_hinge_angle_right) / 2
            
            # Hip hinge feedback - checking if trainer is bending from hip
            if self.stage in ["Descent", "Ascent"]:
                if avg_hip_hinge_angle < self.ideal_hip_hinge_range[0]:
                    feedback_msgs['hip_hinge'] = "Lean forward more from hips!"
                elif avg_hip_hinge_angle > self.ideal_hip_hinge_range[1]:
                    feedback_msgs['hip_hinge'] = "Too much forward lean!"
                else:
                    feedback_msgs['hip_hinge'] = "Good hip hinge!"
            
            # Depth feedback - checking how low the trainer is going
            avg_depth_angle = (hip_knee_angle_left + hip_knee_angle_right) / 2
            
            if self.stage == "Descent" or self.stage == "Ascent":
                if avg_depth_angle > self.minimum_squat_depth:
                    feedback_msgs['depth'] = "Go lower! Aim for parallel!"
                elif avg_depth_angle > self.ideal_squat_depth:
                    feedback_msgs['depth'] = "Almost there! A bit deeper!"
                else:
                    feedback_msgs['depth'] = "Great depth!"
            
            # General feedback combining both aspects
            if (self.ideal_hip_hinge_range[0] <= avg_hip_hinge_angle <= self.ideal_hip_hinge_range[1] and
                avg_depth_angle <= self.ideal_squat_depth and 
                self.stage in ["Descent", "Ascent"]):
                feedback_msgs['general'] = "Excellent form!"
            elif self.stage == "Starting Position":
                feedback_msgs['general'] = "Ready to squat!"
            
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

        # Calculate angles (hip-knee-ankle for depth tracking)
        angle_left = self.calculate_angle(hip_left, knee_left, ankle_left)
        angle_right = self.calculate_angle(hip_right, knee_right, ankle_right)
        
        # Analyze form before drawing
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
        cv2.putText(frame, f'Angle Left: {int(angle_left)}', angle_text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        angle_text_position_right = (knee_right[0] + 10, knee_right[1] - 10)
        cv2.putText(frame, f'Angle Right: {int(angle_right)}', angle_text_position_right, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)


        if angle_left <= 42 and self.stage == "Up":
            self.stage = "Down"
            self.counter += 1
        elif angle_left >= 170 and self.stage == "Down":
            self.stage = "Up"
        # # Update exercise stage and counter
        # if angle > 170:
        #     self.stage = "Starting Position"
        # elif 80 < angle < 170 and self.stage == "Starting Position":
        #     self.stage = "Descent"
        # elif angle < 80 and self.stage == "Descent":
        #     self.stage = "Ascent"
        #     self.counter += 1
            
        # Return counter, angle, stage, and feedback messages
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



# import cv2
# from pose_estimation.angle_calculation import calculate_angle

# class Squat:
#     def __init__(self):
#         self.counter = 0
#         self.stage = None

#     def calculate_angle(self, hip, knee, ankle):
#         return calculate_angle(hip, knee, ankle)

#     def track_squat(self, landmarks, frame):
#         # Landmark coordinates
#         hip = [int(landmarks[23].x * frame.shape[1]), int(landmarks[23].y * frame.shape[0])]
#         knee = [int(landmarks[25].x * frame.shape[1]), int(landmarks[25].y * frame.shape[0])]
#         shoulder = [int(landmarks[11].x * frame.shape[1]), int(landmarks[11].y * frame.shape[0])]

#         hip_right = [int(landmarks[24].x * frame.shape[1]), int(landmarks[24].y * frame.shape[0])]
#         knee_right = [int(landmarks[26].x * frame.shape[1]), int(landmarks[26].y * frame.shape[0])]
#         shoulder_right = [int(landmarks[12].x * frame.shape[1]), int(landmarks[12].y * frame.shape[0])]

#         # Calculate angles
#         angle = self.calculate_angle(shoulder, hip, knee)
#         angle_right = self.calculate_angle(shoulder_right, hip_right, knee_right)

#         # Draw lines and circles to highlight key points
#         self.draw_line_with_style(frame, shoulder, hip, (178, 102, 255), 2)
#         self.draw_line_with_style(frame, hip, knee, (178, 102, 255), 2)
#         self.draw_line_with_style(frame, shoulder_right, hip_right, (51, 153, 255), 2)
#         self.draw_line_with_style(frame, hip_right, knee_right, (51, 153, 255), 2)

#         self.draw_circle(frame, shoulder, (178, 102, 255), 8)
#         self.draw_circle(frame, hip, (178, 102, 255), 8)
#         self.draw_circle(frame, knee, (178, 102, 255), 8)
#         self.draw_circle(frame, shoulder_right, (51, 153, 255), 8)
#         self.draw_circle(frame, hip_right, (51, 153, 255), 8)
#         self.draw_circle(frame, knee_right, (51, 153, 255), 8)

#         # Display angles on screen
#         angle_text_position = (knee[0] + 10, knee[1] - 10)
#         cv2.putText(frame, f'Angle Left: {int(angle)}', angle_text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

#         angle_text_position_right = (knee_right[0] + 10, knee_right[1] - 10)
#         cv2.putText(frame, f'Angle Right: {int(angle_right)}', angle_text_position_right, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

#         # Update exercise stage and counter
#         if angle > 170:
#             self.stage = "Starting Position"
#         elif 90 < angle < 170 and self.stage == "Starting Position":
#             self.stage = "Descent"
#         elif angle < 90 and self.stage == "Descent":
#             self.stage = "Ascent"
#             self.counter += 1
#         return self.counter, angle, self.stage

#     def draw_line_with_style(self, frame, start_point, end_point, color, thickness):
#         """Draw a line with specified style."""
#         cv2.line(frame, start_point, end_point, color, thickness, lineType=cv2.LINE_AA)

#     def draw_circle(self, frame, center, color, radius):
#         """Draw a circle with specified style."""
#         cv2.circle(frame, center, radius, color, -1)  # -1 to fill the circle
