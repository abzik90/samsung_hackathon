import cv2
import mediapipe as mp
import pyautogui

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

if __name__ == "__main__":
    # Initialize MediaPipe Hand module
    hands = mp.solutions.hands.Hands()
    cap = cv2.VideoCapture(0)
    screen_width, screen_height = pyautogui.size()
    while cap.isOpened():
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        if not ret:
            break

        # Extract hand landmarks
        landmarks = extract_hand_landmarks(frame)

        # Draw landmarks on the frame
        if landmarks:
            x, y = landmarks[8] # get the index finger's landmark only
            print(x,y)
            frame_height, frame_width, _ = frame.shape
            
            absolute_x = int(x * frame_width)
            absolute_y = int(y * frame_height)

            cv2.circle(frame, (absolute_x, absolute_y), 10, (255, 0, 0))

            index_x = int(screen_width/frame_width * absolute_x) 
            index_y = int(screen_height/frame_height * absolute_y)
            print(index_x, index_y)
            pyautogui.moveTo(index_x, index_y) 

        # Display the frame
        cv2.imshow('Hand Landmarks', frame)

        # Exit when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture and close windows
    cap.release()
    cv2.destroyAllWindows()
