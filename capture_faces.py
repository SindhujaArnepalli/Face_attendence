import cv2
import os

# -----------------------------
# INPUT NAME
# -----------------------------
name = input("Enter your name: ").strip().lower()
save_path = os.path.join("known_faces", name)
os.makedirs(save_path, exist_ok=True)

# -----------------------------
# LOAD HAARCASCADE (SAFE PATH)
# -----------------------------
cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(cascade_path)

if face_cascade.empty():
    print("❌ Haarcascade not loaded")
    exit()

# -----------------------------
# OPEN CAMERA (WINDOWS FIX)
# -----------------------------
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("❌ Camera not accessible")
    exit()

count = 0
MAX_IMAGES = 20

print("📸 Press 'C' to capture | 'Q' to quit")

while True:
    ret, frame = cap.read()

    if not ret:
        print("❌ Frame not received")
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face = gray[y:y+h, x:x+w]
        face = cv2.resize(face, (200, 200))

        img_path = os.path.join(save_path, f"{count}.jpg")
        cv2.imwrite(img_path, face)
        count += 1

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, f"Saved: {count}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        if count >= MAX_IMAGES:
            break

    cv2.imshow("Capturing Faces", frame)

    if count >= MAX_IMAGES:
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print(f"✅ Face capture complete for '{name}'")
