import cv2
import numpy as np
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

# --- Import your custom modules ---
import PoseModule as pm
from process_pushup import process_frame # Our new logic file

# --- App Initialization (like squat API) ---
app = FastAPI(title="AI Pushup Trainer API")

# --- CORS Middleware (like squat API) ---
#
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# --- Initialize Detector (like squat API) ---
# We create one detector and reuse it for all connections
detector = pm.poseDetector()

@app.get("/")
def root():
    return {"message": "Welcome to the AI Pushup Trainer API"}

# --- WebSocket Endpoint (like squat API) ---
#
@app.websocket("/ws/live_pushup")
async def websocket_live_stream(websocket: WebSocket):
    """
    WebSocket endpoint for live pushup analysis.
    Receives binary JPEG frames, processes them, and sends back the processed frame.
    """
    await websocket.accept()
    
    # --- State variables for this specific user ---
    # Each connection gets its own counter
    count = 0
    direction = 0
    form = 0
    
    try:
        while True:
            # 1. Receive Frame from Client
            #
            data = await websocket.receive_bytes()
            
            # 2. Decode Frame
            #
            nparr = np.frombuffer(data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # 3. Process the Frame using our new function
            processed_img, new_count, new_dir, new_form = process_frame(
                frame, detector, count, direction, form
            )
            
            # 4. Update the state for this user
            count, direction, form = new_count, new_dir, new_form

            # 5. Encode Frame Back to JPEG
            #
            _, buffer = cv2.imencode('.jpg', processed_img)
            
            # 6. Send Processed Frame Back to Client
            #
            await websocket.send_bytes(buffer.tobytes())

    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        print(f"An error occurred: {e}")
        await websocket.close(code=1011)

# --- Run the API (like squat API) ---
#
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)