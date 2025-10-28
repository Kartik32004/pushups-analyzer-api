# # import cv2
# # import numpy as np
# # import uvicorn
# # from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# # from fastapi.middleware.cors import CORSMiddleware

# # # --- Import your custom modules ---
# # import PoseModule as pm
# # from process_pushup import process_frame # Our new logic file

# # # --- App Initialization (like squat API) ---
# # app = FastAPI(title="AI Pushup Trainer API")

# # # --- CORS Middleware (like squat API) ---
# # #
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],  # Allows all origins
# #     allow_credentials=True,
# #     allow_methods=["*"],  # Allows all methods
# #     allow_headers=["*"],  # Allows all headers
# # )

# # # --- Initialize Detector (like squat API) ---
# # # We create one detector and reuse it for all connections
# # detector = pm.poseDetector()

# # @app.get("/")
# # def root():
# #     return {"message": "Welcome to the AI Pushup Trainer API"}

# # # --- WebSocket Endpoint (like squat API) ---
# # #
# # @app.websocket("/ws/live_pushup")
# # async def websocket_live_stream(websocket: WebSocket):
# #     """
# #     WebSocket endpoint for live pushup analysis.
# #     Receives binary JPEG frames, processes them, and sends back the processed frame.
# #     """
# #     await websocket.accept()
    
# #     # --- State variables for this specific user ---
# #     # Each connection gets its own counter
# #     count = 0
# #     direction = 0
# #     form = 0
    
# #     try:
# #         while True:
# #             # 1. Receive Frame from Client
# #             #
# #             data = await websocket.receive_bytes()
            
# #             # 2. Decode Frame
# #             #
# #             nparr = np.frombuffer(data, np.uint8)
# #             frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

# #             # 3. Process the Frame using our new function
# #             processed_img, new_count, new_dir, new_form = process_frame(
# #                 frame, detector, count, direction, form
# #             )
            
# #             # 4. Update the state for this user
# #             count, direction, form = new_count, new_dir, new_form

# #             # 5. Encode Frame Back to JPEG
# #             #
# #             _, buffer = cv2.imencode('.jpg', processed_img)
            
# #             # 6. Send Processed Frame Back to Client
# #             #
# #             await websocket.send_bytes(buffer.tobytes())

# #     except WebSocketDisconnect:
# #         print("WebSocket disconnected")
# #     except Exception as e:
# #         print(f"An error occurred: {e}")
# #         await websocket.close(code=1011)

# # # --- Run the API (like squat API) ---




# import cv2
# import numpy as np
# import uvicorn
# from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# from fastapi.middleware.cors import CORSMiddleware

# # --- Import your custom modules ---
# import PoseModule as pm
# from process_pushup import process_frame

# # --- App Initialization ---
# app = FastAPI(title="AI Pushup Trainer API")

# # --- CORS Middleware ---
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # --- Initialize Detector ---
# detector = pm.poseDetector()

# @app.get("/")
# def root():
#     return {
#         "message": "Welcome to the AI Pushup Trainer API",
#         "status": "online",
#         "endpoints": {
#             "websocket": "/ws/live_pushup"
#         }
#     }

# @app.get("/health")
# def health():
#     return {"status": "healthy"}

# # --- WebSocket Endpoint ---
# @app.websocket("/ws/live_pushup")
# async def websocket_live_stream(websocket: WebSocket):
#     """
#     WebSocket endpoint for live pushup analysis.
#     Receives binary JPEG frames, processes them, and sends back the processed frame.
#     """
#     await websocket.accept()
#     print("✅ Client connected to pushup analyzer")
    
#     # State variables for this specific user
#     count = 0
#     direction = 0
#     form = 0
    
#     try:
#         frame_count = 0
#         while True:
#             # 1. Receive Frame from Client
#             data = await websocket.receive_bytes()
#             frame_count += 1
            
#             if frame_count % 10 == 0:  # Log every 10 frames
#                 print(f"📸 Received frame #{frame_count}, size: {len(data)} bytes")
            
#             # 2. Decode Frame
#             nparr = np.frombuffer(data, np.uint8)
#             frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
#             if frame is None:
#                 print("❌ Failed to decode frame")
#                 continue

#             # 3. Process the Frame
#             try:
#                 processed_img, new_count, new_dir, new_form = process_frame(
#                     frame, detector, count, direction, form
#                 )
                
#                 # 4. Update the state
#                 count, direction, form = new_count, new_dir, new_form
                
#                 if count != new_count:
#                     print(f"💪 Pushup count updated: {count}")

#             except Exception as e:
#                 print(f"❌ Error processing frame: {e}")
#                 processed_img = frame  # Send original frame if processing fails

#             # 5. Encode Frame Back to JPEG
#             success, buffer = cv2.imencode('.jpg', processed_img)
            
#             if not success:
#                 print("❌ Failed to encode processed frame")
#                 continue
            
#             # 6. Send Processed Frame Back to Client
#             await websocket.send_bytes(buffer.tobytes())
            
#             if frame_count % 10 == 0:
#                 print(f"✅ Sent processed frame #{frame_count}")

#     except WebSocketDisconnect:
#         print("👋 Client disconnected normally")
#     except Exception as e:
#         print(f"❌ Error occurred: {e}")
#         import traceback
#         traceback.print_exc()
#         await websocket.close(code=1011)  # Internal error

# # --- Run the API ---
# if __name__ == "__main__":
#     print("🚀 Starting Pushup Analyzer API...")
#     print("📡 WebSocket endpoint: ws://localhost:8000/ws/live_pushup")
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)






import cv2
import numpy as np
import uvicorn
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

# Import your custom modules
import PoseModule as pm
from process_pushup import process_frame

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# App Initialization
app = FastAPI(title="AI Pushup Trainer API")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Detector (shared across connections)
detector = pm.poseDetector()
logger.info("✓ Pose detector initialized")

@app.get("/")
def root():
    return {
        "message": "Welcome to the AI Pushup Trainer API",
        "status": "online",
        "endpoints": {
            "websocket": "/ws/live_pushup",
            "health": "/health"
        }
    }

@app.get("/health")
def health():
    return {"status": "healthy", "detector": "ready"}

@app.websocket("/ws/live_pushup")
async def websocket_live_stream(websocket: WebSocket):
    """
    WebSocket endpoint for live pushup analysis.
    Receives binary JPEG frames, processes them, and sends back the processed frame.
    """
    client_id = id(websocket)
    logger.info(f"📥 Client {client_id} attempting to connect")
    
    await websocket.accept()
    logger.info(f"✅ Client {client_id} connected successfully")
    
    # State variables for this specific user
    count = 0
    direction = 0
    form = 0
    frame_count = 0
    error_count = 0
    max_errors = 10  # Disconnect after 10 consecutive errors
    
    try:
        while True:
            # 1. Receive Frame from Client
            try:
                data = await websocket.receive_bytes()
                frame_count += 1
                
                if frame_count % 30 == 0:  # Log every 30 frames (~3 seconds at 10fps)
                    logger.info(f"📸 Client {client_id}: Processed {frame_count} frames (count={count})")
                
            except Exception as recv_error:
                logger.error(f"❌ Client {client_id}: Error receiving data: {recv_error}")
                break
            
            # 2. Decode Frame
            try:
                nparr = np.frombuffer(data, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                
                if frame is None or frame.size == 0:
                    logger.warning(f"⚠️ Client {client_id}: Failed to decode frame #{frame_count}")
                    error_count += 1
                    if error_count >= max_errors:
                        logger.error(f"❌ Client {client_id}: Too many decode errors, closing connection")
                        break
                    continue
                
                # Reset error count on successful decode
                error_count = 0
                
            except Exception as decode_error:
                logger.error(f"❌ Client {client_id}: Decode error: {decode_error}")
                error_count += 1
                if error_count >= max_errors:
                    break
                continue

            # 3. Process the Frame
            try:
                processed_img, new_count, new_dir, new_form = process_frame(
                    frame, detector, count, direction, form
                )
                
                # 4. Update the state
                if new_count != count:
                    logger.info(f"💪 Client {client_id}: Pushup count updated: {count} → {new_count}")
                
                count, direction, form = new_count, new_dir, new_form

            except Exception as process_error:
                logger.error(f"❌ Client {client_id}: Processing error: {process_error}")
                # Send original frame with error message on it
                processed_img = frame.copy()
                cv2.putText(processed_img, "Processing Error", (50, 50), 
                           cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

            # 5. Encode Frame Back to JPEG
            try:
                success, buffer = cv2.imencode('.jpg', processed_img, [cv2.IMWRITE_JPEG_QUALITY, 80])
                
                if not success:
                    logger.error(f"❌ Client {client_id}: Failed to encode frame #{frame_count}")
                    continue
                
            except Exception as encode_error:
                logger.error(f"❌ Client {client_id}: Encode error: {encode_error}")
                continue
            
            # 6. Send Processed Frame Back to Client
            try:
                await websocket.send_bytes(buffer.tobytes())
                
            except Exception as send_error:
                logger.error(f"❌ Client {client_id}: Error sending frame: {send_error}")
                break

    except WebSocketDisconnect:
        logger.info(f"👋 Client {client_id} disconnected normally (frames: {frame_count}, reps: {count})")
    except Exception as e:
        logger.error(f"❌ Client {client_id}: Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        try:
            await websocket.close(code=1011, reason="Internal server error")
        except:
            pass
    finally:
        logger.info(f"🔌 Client {client_id} session ended. Stats: {frame_count} frames, {count} reps")

# Run the API
if __name__ == "__main__":
    logger.info("🚀 Starting Pushup Analyzer API...")
    logger.info("📡 WebSocket endpoint: ws://localhost:8000/ws/live_pushup")
    logger.info("🌐 HTTP endpoint: http://localhost:8000")
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )
