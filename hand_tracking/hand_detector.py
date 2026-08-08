import cv2
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class HandDetector:

    def __init__(self):

        base_options = python.BaseOptions(
            model_asset_path="hand_landmarker.task"
        )

        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_hands=1,
            min_hand_detection_confidence=0.5,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5
        )

        self.detector = vision.HandLandmarker.create_from_options(options)

    def find_hands(self, frame):

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        # Timestamp is required for VIDEO mode
        timestamp = int(cv2.getTickCount() / cv2.getTickFrequency() * 1000)

        results = self.detector.detect_for_video(
            mp_image,
            timestamp
        )

        # Draw landmarks
        if results.hand_landmarks:

            for hand_landmarks in results.hand_landmarks:

                for landmark in hand_landmarks:

                    h, w, _ = frame.shape

                    x = int(landmark.x * w)
                    y = int(landmark.y * h)

                    cv2.circle(
                        frame,
                        (x, y),
                        4,
                        (0, 255, 0),
                        cv2.FILLED
                    )

        return frame, results

    def get_index_finger(self, results, frame):

        if not results.hand_landmarks:
            return None

        hand = results.hand_landmarks[0]

        # Landmark 8 = index finger tip
        index_tip = hand[8]

        height, width, _ = frame.shape

        x = int(index_tip.x * width)
        y = int(index_tip.y * height)

        return x, y