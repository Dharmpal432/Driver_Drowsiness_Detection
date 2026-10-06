import cv2
import time
import threading
import winsound

# -----------------------------
# Load face and eye detectors
# -----------------------------
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_eye.xml"
)

# -----------------------------
# Start camera
# -----------------------------
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Camera could not be opened")
    exit()

print("Drowsiness Detection Started")
print("Press Q to close")

# -----------------------------
# Drowsiness settings
# -----------------------------
closed_count = 0

# Number of consecutive frames
# without detected eyes before alert
ALERT_THRESHOLD = 15

alert_active = False
last_beep_time = 0

# -----------------------------
# Non-blocking beep
# -----------------------------
def play_alert():
    winsound.Beep(1500, 500)


# -----------------------------
# Main loop
# -----------------------------
while True:

    ret, frame = camera.read()

    if not ret:
        print("Could not read camera")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect face
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(50, 50)
    )

    # Default status
    status = "NORMAL"

    for (x, y, w, h) in faces:

        # Draw face rectangle
        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        # Region containing the face
        face_gray = gray[y:y + h, x:x + w]
        face_color = frame[y:y + h, x:x + w]

        # Detect eyes
        eyes = eye_cascade.detectMultiScale(
            face_gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(20, 20)
        )

        # Draw eye rectangles
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(
                face_color,
                (ex, ey),
                (ex + ew, ey + eh),
                (255, 0, 0),
                2
            )

        # -----------------------------
        # Drowsiness decision
        # -----------------------------

        if len(eyes) == 0:

            closed_count += 1

        else:

            closed_count = 0
            alert_active = False

        # Show eye count
        cv2.putText(
            frame,
            f"Eyes: {len(eyes)}",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        # Show counter
        cv2.putText(
            frame,
            f"Closed Count: {closed_count}",
            (20, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        # -----------------------------
        # Drowsiness alert
        # -----------------------------

        if closed_count >= ALERT_THRESHOLD:

            status = "DROWSY"

            # Trigger beep only once when alert starts
            current_time = time.time()

            if not alert_active:
                alert_active = True

                threading.Thread(
                    target=play_alert,
                    daemon=True
                ).start()

                last_beep_time = current_time

            # Repeat beep every 2 seconds
            elif current_time - last_beep_time >= 2:

                threading.Thread(
                    target=play_alert,
                    daemon=True
                ).start()

                last_beep_time = current_time

    # -----------------------------
    # Display status
    # -----------------------------

    if status == "DROWSY":

        cv2.putText(
            frame,
            "DROWSINESS ALERT!",
            (20, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (0, 0, 255),
            3
        )

    else:

        cv2.putText(
            frame,
            "STATUS: NORMAL",
            (20, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 255, 0),
            2
        )

    # Show camera
    cv2.imshow("Driver Drowsiness Detection", frame)

    # Press Q to exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# -----------------------------
# Cleanup
# -----------------------------
camera.release()
cv2.destroyAllWindows()

print("Drowsiness Detection Stopped")