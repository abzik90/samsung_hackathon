import cv2
import mediapipe as mp
import pyautogui

CLICK_DISTANCE = 10
DRAG_DISTANCE = 70
INDEX_RAISED_DISTANCE = 40

# Function to extract hand landmarks
def extract_hand_landmarks(image):
    # Convert the image to RGB format
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Process the image with MediaPipe
    results = hands.process(image_rgb)
    # List to store landmark positions
    landmark_positions = []
    # Check if hand landmarks are detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            landmark_positions.extend([(landmark.x, landmark.y) for landmark in hand_landmarks.landmark])

    return landmark_positions
def drawCircle(landmarks, index, frame):
    x, y = landmarks[index] # get the index finger's landmark only
    frame_height, frame_width, _ = frame.shape
    
    absolute_x = int(x * frame_width)
    absolute_y = int(y * frame_height)

    cv2.circle(frame, (absolute_x, absolute_y), 10, (255, 0, 0))

    return int(screen_width/frame_width * absolute_x), int(screen_height/frame_height * absolute_y)


if __name__ == "__main__":
    # Initialize MediaPipe Hand module
    hands = mp.solutions.hands.Hands(min_detection_confidence=0.6, min_tracking_confidence=0.6, max_num_hands=1)
    cap = cv2.VideoCapture(0)
    screen_width, screen_height = pyautogui.size()

    while cap.isOpened():
        ret, frame = cap.read()
        # frame = cv2.flip(frame, 1)
        if not ret:
            break

        # Extract hand landmarks
        landmarks = extract_hand_landmarks(frame)

        # Draw landmarks on the frame
        if landmarks:
            index_coordinates = drawCircle(landmarks, 8, frame)
            thumb_coordinates = drawCircle(landmarks, 4, frame)
            height_dif = abs(index_coordinates[1] - thumb_coordinates[1])
            if height_dif < CLICK_DISTANCE:
                pyautogui.click()
                pyautogui.mouseDown(button = "left")
            elif height_dif < DRAG_DISTANCE:
                pyautogui.moveTo(index_coordinates, duration=0.04)
                pyautogui.mouseUp(button = "left", x = index_coordinates[0], y = index_coordinates[1])

        # Display the frame
        cv2.imshow('Hand Landmarks', frame)

        # Exit when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture and close windows
    cap.release()
    cv2.destroyAllWindows()
