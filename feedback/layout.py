
from feedback.indicators import draw_squat_indicators, draw_pushup_indicators, draw_hammercurl_indicators

def layout_indicators(frame, exercise_type, exercise_data):
    if exercise_type == "squat":
        counter, angle, stage, msg_hip, msg_depth, msg_general1 = exercise_data
        draw_squat_indicators(frame, counter, angle, stage, msg_hip, msg_depth, msg_general1)
    elif exercise_type == "push_up":
        counter, angle, stage, msg_right, msg_left, msg_general = exercise_data
        draw_pushup_indicators(frame, counter, angle, stage, msg_right, msg_left, msg_general)
    elif exercise_type == "hammer_curl":
        (counter_right, counter_left,
         warning_message_right, warning_message_left, stage_right,stage_left) = exercise_data
        draw_hammercurl_indicators(frame, counter_right, counter_left, warning_message_right, warning_message_left, stage_right,stage_left)

