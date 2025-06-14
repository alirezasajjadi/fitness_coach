# feedback/indicators.py
from utils.drawing_utils import draw_gauge_meter,draw_progress_bar,display_stage,display_counter
import cv2

display_counter_poisiton=(40, 160)
display_stage_poisiton=(40, 190)
display_counter_angel_color=(255,255,0)
display_progress_bar_position=(40, 100)


def draw_squat_indicators(frame, counter, angle, stage, msg_hip, msg_depth, msg_general1):
    display_msg_position_left = (40, 300)    # Left arm feedback position
    display_msg_position_right = (40, 330)   # Right arm feedback position  
    display_msg_position_general = (40, 360) # General feedback position

    # Feedback Messages
    if msg_hip:
        cv2.putText(frame, f"Left Arm: {msg_hip}", display_msg_position_left, 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2, cv2.LINE_AA)
    
    if msg_depth:
        cv2.putText(frame, f"Right Arm: {msg_depth}", display_msg_position_right, 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2, cv2.LINE_AA)
    
    if msg_general1:
        cv2.putText(frame, f"Form: {msg_general1}", display_msg_position_general, 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2, cv2.LINE_AA)

    # Counter
    display_counter(frame,counter, position=display_counter_poisiton, color=(0, 0, 0),
                    background_color=(192,192,192))

    # Stage
    display_stage(frame, stage,"Stage", position=display_stage_poisiton, color=(0, 0, 0), 
                  background_color=(192,192,192))

    draw_progress_bar(frame, exercise="squat", value=counter, position=display_progress_bar_position, size=(200, 20),
                       color=(163, 245, 184, 1),background_color=(255,255,255))

    # draw_gauge_meter(frame, angle=angle, text="Squat Gauge Meter", position=(135, 415), radius=75, color=(0, 0, 255))

def draw_pushup_indicators(frame, counter, angle, stage, msg_left, msg_right, msg_general):
    display_msg_position_left = (40, 220)    # Left arm feedback position
    display_msg_position_right = (40, 250)   # Right arm feedback position  
    display_msg_position_general = (40, 280) # General feedback position

    # Counter
    display_counter(frame,counter, position=display_counter_poisiton, color=(0, 0, 0),
                    background_color=(192,192,192))

    display_stage(frame, stage,"Stage", position=display_stage_poisiton, color=(0, 0, 0),
                  background_color=(192,192,192))
    
    draw_progress_bar(frame, exercise="push_up", value=counter, position=display_progress_bar_position, 
                      size=(200, 20), color=(163, 245, 184, 1),background_color=(255,255,255))
    

    # Feedback Messages
    # if msg_left:
    #     cv2.putText(frame, f"Left Arm: {msg_left}", display_msg_position_left, 
    #                 cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2, cv2.LINE_AA)
    
    # if msg_right:
    #     cv2.putText(frame, f"Right Arm: {msg_right}", display_msg_position_right, 
    #                 cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2, cv2.LINE_AA)
    
    if msg_general!="Excellent form!":
        cv2.putText(frame, f"!! ERROR !!",
                    (300,100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f"Form: {msg_general}", display_msg_position_general, 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2, cv2.LINE_AA)
    else:
        cv2.putText(frame, f"Form: {msg_general}", display_msg_position_general, 
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)


    # text = "Push-u Gauge Meter"
    # draw_gauge_meter(frame, angle=angle,text=text, position=(350,80), radius=50, color=(0, 102, 204))


def draw_hammercurl_indicators(frame, counter_right, counter_left, warning_message_right, warning_message_left, stage_right, stage_left):
    display_counter_poisiton_left_arm = (40, 220)
    display_msg_position_right = (40, 260) 
    display_msg_position_left = (40, 290)

    # Right Arm Indicators
    display_counter(frame, counter_right, position=display_counter_poisiton, color=(0, 0, 0),
                    background_color=(192,192,192))

    display_stage(frame, stage_right, "Right Stage", position=display_stage_poisiton,
                   color=(0, 0, 0), background_color=(192,192,192))
    display_stage(frame, stage_left, "Left Stage", position=display_counter_poisiton_left_arm,
                   color=(0, 0, 0), background_color=(192,192,192))

    if warning_message_left=="Excellent form!" and warning_message_right=="Excellent form!":
        cv2.putText(frame, f"Feedback Right: {warning_message_right}",
            display_msg_position_right, cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, f"Feedback Left: {warning_message_left}",
            display_msg_position_left, cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)

    
    else:
        cv2.putText(frame, f"!! ERROR !!",
                    (300,100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f"Feedback Right: {warning_message_right}",
                    display_msg_position_right, cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f"Feedback Left: {warning_message_left}", 
                    display_msg_position_left, cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2, cv2.LINE_AA)
    # display_stage(frame, warning_message_right, "Right Feedback", position=display_msg_position_right, color=(0, 0, 255), background_color=(192, 192, 192))
    # display_stage(frame, warning_message_left, "Left Feedback", position=display_msg_position_left, color=(0, 0, 255), background_color=(192, 192, 192))

    # Progress Bars
    draw_progress_bar(frame, exercise="hammer_curl", value=(counter_right+counter_left)/2,
                       position=display_progress_bar_position, size=(200, 20), color=(163, 245, 184, 1), 
                       background_color=(255,255,255))

    # text_right = "Right Gauge Meter"
    # text_left = "Left Gauge Meter"

    # # Gauge Meters for Angles
    # draw_gauge_meter(frame, angle=angle_right,text=text_right, position=(1200,80), radius=50, color=(0, 102, 204))
    # draw_gauge_meter(frame, angle=angle_left,text=text_left, position=(1200,240), radius=50, color=(0, 102, 204))


