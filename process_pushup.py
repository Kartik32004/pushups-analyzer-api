# # import cv2
# # import numpy as np
# # import PoseModule as pm

# # # --- Logic copied directly from PushUpCounter.py ---
# # #
# # def update_feedback_and_count(elbow, shoulder, hip, direction, count, form):
# #     """Determines the feedback message and updates the count based on the angles."""
# #     feedback = "Fix Form"
# #     if elbow > 160 and shoulder > 40 and hip > 160:
# #         form = 1
# #     if form == 1:
# #         if elbow <= 90 and hip > 160:
# #             feedback = "Up"
# #             if direction == 0:
# #                 count += 0.5
# #                 direction = 1
# #         elif elbow > 160 and shoulder > 40 and hip > 160:
# #             feedback = "Down"
# #             if direction == 1:
# #                 count += 0.5
# #                 direction = 0
# #         else:
# #             feedback = "Fix Form"
# #     return feedback, count, direction, form

# # #
# # def draw_ui(img, per, bar, count, feedback, form):
# #     """Draws the UI elements on the image (modifies img in-place)."""
# #     if form == 1:
# #         cv2.rectangle(img, (580, 50), (600, 380), (0, 255, 0), 3)
# #         cv2.rectangle(img, (580, int(bar)), (600, 380), (0, 255, 0), cv2.FILLED)
# #         cv2.putText(img, f'{int(per)}%', (565, 430), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

# #     cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
# #     cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
    
# #     cv2.rectangle(img, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
# #     cv2.putText(img, feedback, (500, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)


# # # --- This is the new function our API will call ---
# # # It replaces the 'while' loop from PushUpCounter.py
# # def process_frame(img, detector, count, direction, form):
# #     """
# #     Processes a single frame for pushup analysis.
# #     Takes an image and the current state, returns the processed image and new state.
# #     """
# #     # Set defaults
# #     feedback = "Fix Form"
# #     per, bar = 0, 0 # Default values if no pose
    
# #     # Run the stateful detector methods in order
# #     # 1. Find pose (populates detector.results)
# #     #
# #     img = detector.findPose(img, False) 
    
# #     # 2. Find position (populates detector.lmList)
# #     #
# #     lmList = detector.findPosition(img, False) 

# #     if len(lmList) != 0:
# #         # 3. Find angles (uses detector.lmList)
# #         #
# #         elbow = detector.findAngle(img, 11, 13, 15, draw=False) 
# #         shoulder = detector.findAngle(img, 13, 11, 23, draw=False)
# #         hip = detector.findAngle(img, 11, 23, 25, draw=False)
        
# #         # 4. Run logic
# #         #
# #         per = np.interp(elbow, (90, 160), (0, 100))
# #         bar = np.interp(elbow, (90, 160), (380, 50))
# #         feedback, count, direction, form = update_feedback_and_count(
# #             elbow, shoulder, hip, direction, count, form
# #         )
    
# #     # 5. Always draw the UI on the image
# #     #
# #     draw_ui(img, per, bar, count, feedback, form)
    
# #     # 6. Return the modified image and the new state

# #     return img, count, direction, form


# import cv2
# import numpy as np

# def update_feedback_and_count(elbow, shoulder, hip, direction, count, form):
#     """Determines the feedback message and updates the count based on the angles."""
#     feedback = "Fix Form"
    
#     # Check if proper starting position (arms extended, body straight)
#     if elbow > 160 and shoulder > 40 and hip > 160:
#         form = 1
    
#     if form == 1:
#         # Down position - elbow bent, hip still straight
#         if elbow <= 90 and hip > 160:
#             feedback = "Up"
#             if direction == 0:
#                 count += 0.5
#                 direction = 1
#         # Up position - arms extended, body straight  
#         elif elbow > 160 and shoulder > 40 and hip > 160:
#             feedback = "Down"
#             if direction == 1:
#                 count += 0.5
#                 direction = 0
#         else:
#             feedback = "Fix Form"
    
#     return feedback, count, direction, form

# def draw_ui(img, per, bar, count, feedback, form, elbow_angle=0, shoulder_angle=0, hip_angle=0):
#     """Draws the UI elements on the image (modifies img in-place)."""
#     h, w = img.shape[:2]
    
#     # Progress bar (only when form is correct)
#     if form == 1:
#         # Vertical progress bar on the right side
#         bar_x = w - 40
#         cv2.rectangle(img, (bar_x, 50), (bar_x + 20, 380), (0, 255, 0), 3)
#         cv2.rectangle(img, (bar_x, int(bar)), (bar_x + 20, 380), (0, 255, 0), cv2.FILLED)
        
#         # Percentage text below bar
#         cv2.putText(img, f'{int(per)}%', (bar_x - 15, 430), 
#                     cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

#     # Pushup counter (bottom left)
#     cv2.rectangle(img, (10, h - 100), (110, h - 10), (0, 255, 0), cv2.FILLED)
#     cv2.putText(img, str(int(count)), (25, h - 40), 
#                 cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
    
#     # Feedback text (top center)
#     feedback_color = (0, 255, 0) if form == 1 else (0, 0, 255)
#     text_size = cv2.getTextSize(feedback, cv2.FONT_HERSHEY_PLAIN, 3, 3)[0]
#     text_x = (w - text_size[0]) // 2
    
#     # Background for feedback text
#     cv2.rectangle(img, (text_x - 10, 10), (text_x + text_size[0] + 10, 60), 
#                   (255, 255, 255), cv2.FILLED)
#     cv2.putText(img, feedback, (text_x, 50), 
#                 cv2.FONT_HERSHEY_PLAIN, 3, feedback_color, 3)
    
#     # Show angles (top left) - for debugging
#     angle_text_y = 30
#     cv2.putText(img, f'Elbow: {int(elbow_angle)}', (10, angle_text_y), 
#                 cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2)
#     cv2.putText(img, f'Shoulder: {int(shoulder_angle)}', (10, angle_text_y + 30), 
#                 cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2)
#     cv2.putText(img, f'Hip: {int(hip_angle)}', (10, angle_text_y + 60), 
#                 cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2)

# def process_frame(img, detector, count, direction, form):
#     """
#     Processes a single frame for pushup analysis.
#     Takes an image and the current state, returns the processed image and new state.
#     """
#     # Set defaults
#     feedback = "Fix Form"
#     per, bar = 0, 0
#     elbow_angle = 0
#     shoulder_angle = 0
#     hip_angle = 0
    
#     # Ensure image is valid
#     if img is None or img.size == 0:
#         print("⚠️ Invalid image received")
#         # Return a black frame with error message
#         error_img = np.zeros((480, 640, 3), dtype=np.uint8)
#         cv2.putText(error_img, "Invalid Frame", (200, 240), 
#                     cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
#         return error_img, count, direction, form
    
#     try:
#         # 1. Find pose (populates detector.results)
#         # Draw=True to show skeleton on image
#         img = detector.findPose(img, draw=True)
        
#         # 2. Find position (populates detector.lmList)
#         lmList = detector.findPosition(img, draw=False)

#         if len(lmList) != 0:
#             # 3. Find angles with drawing enabled to visualize joints
#             # Elbow angle: shoulder(11) - elbow(13) - wrist(15)
#             elbow_angle = detector.findAngle(img, 11, 13, 15, draw=True)
#             # Shoulder angle: elbow(13) - shoulder(11) - hip(23)
#             shoulder_angle = detector.findAngle(img, 13, 11, 23, draw=True)
#             # Hip angle: shoulder(11) - hip(23) - knee(25)
#             hip_angle = detector.findAngle(img, 11, 23, 25, draw=True)
            
#             # 4. Calculate progress percentage
#             per = np.interp(elbow_angle, (90, 160), (0, 100))
#             bar = np.interp(elbow_angle, (90, 160), (380, 50))
            
#             # 5. Run logic to update count and feedback
#             feedback, count, direction, form = update_feedback_and_count(
#                 elbow_angle, shoulder_angle, hip_angle, direction, count, form
#             )
#         else:
#             feedback = "Move into frame"
    
#     except Exception as e:
#         print(f"❌ Error in process_frame: {e}")
#         import traceback
#         traceback.print_exc()
#         feedback = "Error processing"
    
#     # 6. Always draw the UI on the image
#     draw_ui(img, per, bar, count, feedback, form, elbow_angle, shoulder_angle, hip_angle)
    
#     # 7. Return the modified image and the new state
#     return img, count, direction, form





import cv2
import numpy as np
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_feedback_and_count(elbow, shoulder, hip, direction, count, form):
    """Determines the feedback message and updates the count based on the angles."""
    feedback = "Fix Form"
    
    # Check if proper starting position (arms extended, body straight)
    if elbow > 160 and shoulder > 40 and hip > 160:
        form = 1
    
    if form == 1:
        # Down position - elbow bent, hip still straight
        if elbow <= 90 and hip > 160:
            feedback = "Up"
            if direction == 0:
                count += 0.5
                direction = 1
        # Up position - arms extended, body straight  
        elif elbow > 160 and shoulder > 40 and hip > 160:
            feedback = "Down"
            if direction == 1:
                count += 0.5
                direction = 0
        else:
            feedback = "Fix Form"
    
    return feedback, count, direction, form

def draw_ui(img, per, bar, count, feedback, form, elbow_angle=0, shoulder_angle=0, hip_angle=0):
    """Draws the UI elements on the image (modifies img in-place)."""
    try:
        h, w = img.shape[:2]
        
        # Progress bar (only when form is correct)
        if form == 1:
            bar_x = w - 40
            cv2.rectangle(img, (bar_x, 50), (bar_x + 20, 380), (0, 255, 0), 3)
            cv2.rectangle(img, (bar_x, int(bar)), (bar_x + 20, 380), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, f'{int(per)}%', (bar_x - 15, 430), 
                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

        # Pushup counter (bottom left)
        cv2.rectangle(img, (10, h - 100), (110, h - 10), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (25, h - 40), 
                    cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
        
        # Feedback text (top center)
        feedback_color = (0, 255, 0) if form == 1 else (0, 0, 255)
        text_size = cv2.getTextSize(feedback, cv2.FONT_HERSHEY_PLAIN, 3, 3)[0]
        text_x = (w - text_size[0]) // 2
        
        # Background for feedback text
        cv2.rectangle(img, (text_x - 10, 10), (text_x + text_size[0] + 10, 60), 
                      (255, 255, 255), cv2.FILLED)
        cv2.putText(img, feedback, (text_x, 50), 
                    cv2.FONT_HERSHEY_PLAIN, 3, feedback_color, 3)
        
        # Show angles (top left)
        angle_text_y = 30
        cv2.putText(img, f'Elbow: {int(elbow_angle)}', (10, angle_text_y), 
                    cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2)
        cv2.putText(img, f'Shoulder: {int(shoulder_angle)}', (10, angle_text_y + 30), 
                    cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2)
        cv2.putText(img, f'Hip: {int(hip_angle)}', (10, angle_text_y + 60), 
                    cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2)
    except Exception as e:
        logger.error(f"Error drawing UI: {e}")

def process_frame(img, detector, count, direction, form):
    """
    Processes a single frame for pushup analysis.
    Takes an image and the current state, returns the processed image and new state.
    
    CRITICAL: Always returns a valid image, even if processing fails.
    """
    # Set defaults
    feedback = "Move into frame"
    per, bar = 0, 0
    elbow_angle = 0
    shoulder_angle = 0
    hip_angle = 0
    
    # Validate input image
    if img is None or img.size == 0:
        logger.error("⚠️ Invalid/empty image received")
        error_img = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(error_img, "Invalid Frame", (200, 240), 
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
        return error_img, count, direction, form
    
    try:
        # Make a copy to avoid modifying original
        img_copy = img.copy()
        
        # 1. Find pose (populates detector.results)
        img_copy = detector.findPose(img_copy, draw=True)
        
        # 2. Find position (populates detector.lmList)
        lmList = detector.findPosition(img_copy, draw=False)

        if len(lmList) != 0:
            try:
                # 3. Find angles with drawing enabled to visualize joints
                elbow_angle = detector.findAngle(img_copy, 11, 13, 15, draw=True)
                shoulder_angle = detector.findAngle(img_copy, 13, 11, 23, draw=True)
                hip_angle = detector.findAngle(img_copy, 11, 23, 25, draw=True)
                
                # 4. Calculate progress percentage
                per = np.interp(elbow_angle, (90, 160), (0, 100))
                bar = np.interp(elbow_angle, (90, 160), (380, 50))
                
                # 5. Run logic to update count and feedback
                feedback, count, direction, form = update_feedback_and_count(
                    elbow_angle, shoulder_angle, hip_angle, direction, count, form
                )
                
                logger.debug(f"✓ Processed: count={count}, feedback={feedback}")
            except Exception as angle_error:
                logger.error(f"Error calculating angles: {angle_error}")
                feedback = "Error detecting pose"
        else:
            feedback = "Move into frame"
            logger.debug("No pose detected in frame")
    
    except Exception as e:
        logger.error(f"❌ Critical error in process_frame: {e}")
        import traceback
        traceback.print_exc()
        feedback = "Processing error"
        # Return original image with error message
        try:
            cv2.putText(img, "Error", (50, 50), 
                        cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
            return img, count, direction, form
        except:
            # Last resort: return black frame with error
            error_img = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(error_img, "Error", (200, 240), 
                        cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
            return error_img, count, direction, form
    
    # 6. Always draw the UI on the image (with error handling)
    draw_ui(img_copy, per, bar, count, feedback, form, elbow_angle, shoulder_angle, hip_angle)
    
    # 7. Return the modified image and the new state
    return img_copy, count, direction, form
