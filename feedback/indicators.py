from utils.drawing_utils import draw_progress_bar,display_stage,display_counter
import cv2

display_counter_poisiton=(40, 160)
display_stage_poisiton=(40, 190)
display_counter_angel_color=(255,255,0)
display_progress_bar_position=(40, 100)


def draw_squat_indicators(frame, counter, angle, stage, msg_hip, msg_depth, msg_general1):
    display_msg_position_hip = (40, 220)    # hip feedback position
    display_msg_position_knee = (40, 250)   # knee feedback position  
    display_msg_position_general = (40, 280) # General feedback position

    # Counter
    display_counter(frame,counter, position=display_counter_poisiton, color=(0, 0, 0),
                    background_color=(192,192,192))

    # Stage
    display_stage(frame, stage,"Stage", position=display_stage_poisiton, color=(0, 0, 0), 
                  background_color=(192,192,192))

    draw_progress_bar(frame, exercise="squat", value=counter, position=display_progress_bar_position, size=(200, 20),
                       color=(163, 245, 184, 1),background_color=(255,255,255))

    # Feedback Messages
    if msg_hip:
        cv2.putText(frame, f"Left Hip: {msg_hip}", display_msg_position_hip, 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2, cv2.LINE_AA)
    
    if msg_depth:
        cv2.putText(frame, f"Right Knee: {msg_depth}", display_msg_position_knee, 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2, cv2.LINE_AA)
    
    if msg_general1 == "Excellent form!":
        cv2.putText(frame, f"Form: {msg_general1}", display_msg_position_general, 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)
    
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
    
    if msg_general!="Excellent form!":
        cv2.putText(frame, f"!! ERROR !!",
                    (300,100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f"Form: {msg_general}", display_msg_position_general, 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2, cv2.LINE_AA)
    else:
        cv2.putText(frame, f"Form: {msg_general}", display_msg_position_general, 
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)


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

    draw_progress_bar(frame, exercise="hammer_curl", value=(counter_right+counter_left)/2,
                       position=display_progress_bar_position, size=(200, 20), color=(163, 245, 184, 1), 
                       background_color=(255,255,255))

