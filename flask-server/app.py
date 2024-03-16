from flask import Flask, Response
from object_detection_model import ObjectDetection
import cv2

app = Flask(__name__)
detector = ObjectDetection(capture_index=0)

def generate_frames():
    cap = cv2.VideoCapture(0)
    assert cap.isOpened()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        annotated_frame = detector.get_annotated_frame(frame)
        _, buffer = cv2.imencode('.jpg', annotated_frame)
        frame_encoded = buffer.tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_encoded + b'\r\n')
    cap.release()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)