import cv2
import numpy as np
import PoseModule as pm

# --- Logic copied directly from PushUpCounter.py ---
#
def update_feedback_and_count(elbow, shoulder, hip, direction, count, form):
    """Determines the feedback message and updates the count based on the angles."""
    feedback = "Fix Form"
    if elbow > 160 and shoulder > 40 and hip > 160:
        form = 1
    if form == 1:
        if elbow <= 90 and hip > 160:
            feedback = "Up"
            if direction == 0:
                count += 0.5
                direction = 1
        elif elbow > 160 and shoulder > 40 and hip > 160:
            feedback = "Down"
            if direction == 1:
                count += 0.5
                direction = 0
        else:
            feedback = "Fix Form"
    return feedback, count, direction, form

#
def draw_ui(img, per, bar, count, feedback, form):
    """Draws the UI elements on the image (modifies img in-place)."""
    if form == 1:
        cv2.rectangle(img, (580, 50), (600, 380), (0, 255, 0), 3)
        cv2.rectangle(img, (580, int(bar)), (600, 380), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f'{int(per)}%', (565, 430), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

    cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
    
    cv2.rectangle(img, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
    cv2.putText(img, feedback, (500, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)


# --- This is the new function our API will call ---
# It replaces the 'while' loop from PushUpCounter.py
def process_frame(img, detector, count, direction, form):
    """
    Processes a single frame for pushup analysis.
    Takes an image and the current state, returns the processed image and new state.
    """
    # Set defaults
    feedback = "Fix Form"
    per, bar = 0, 0 # Default values if no pose
    
    # Run the stateful detector methods in order
    # 1. Find pose (populates detector.results)
    #
    img = detector.findPose(img, False) 
    
    # 2. Find position (populates detector.lmList)
    #
    lmList = detector.findPosition(img, False) 

    if len(lmList) != 0:
        # 3. Find angles (uses detector.lmList)
        #
        elbow = detector.findAngle(img, 11, 13, 15, draw=False) 
        shoulder = detector.findAngle(img, 13, 11, 23, draw=False)
        hip = detector.findAngle(img, 11, 23, 25, draw=False)
        
        # 4. Run logic
        #
        per = np.interp(elbow, (90, 160), (0, 100))
        bar = np.interp(elbow, (90, 160), (380, 50))
        feedback, count, direction, form = update_feedback_and_count(
            elbow, shoulder, hip, direction, count, form
        )
    
    # 5. Always draw the UI on the image
    #
    draw_ui(img, per, bar, count, feedback, form)
    
    # 6. Return the modified image and the new state
    return img, count, direction, form