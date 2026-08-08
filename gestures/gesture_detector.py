import math


class GestureDetector:

    def __init__(self):
        self.current_gesture = "NO HAND"
        self.candidate_gesture = None
        self.candidate_count = 0

        # Number of frames needed before changing gesture
        self.required_frames = 2

    def distance(self, p1, p2):

        return math.sqrt(
            (p1.x - p2.x) ** 2 +
            (p1.y - p2.y) ** 2
        )

    def detect_raw_gesture(self, results):

        if not results.hand_landmarks:
            return "NO HAND"

        hand = results.hand_landmarks[0]

        # =====================================
        # PINCH DETECTION
        # =====================================

        thumb_tip = hand[4]
        index_tip = hand[8]

        # Distance between thumb and index fingertip
        pinch_distance = self.distance(
            thumb_tip,
            index_tip
        )

        # Size of palm
        palm_size = self.distance(
            hand[0],      # wrist
            hand[9]       # middle finger base
        )

        # Avoid division by zero
        if palm_size > 0:

            pinch_ratio = pinch_distance / palm_size

        else:

            pinch_ratio = 999

        # -------------------------------------
        # PINCH
        # -------------------------------------

        if pinch_ratio < 0.45:
            return "ERASER"

        # =====================================
        # FINGER DETECTION
        # =====================================

        wrist = hand[0]

        index_extended = (
            self.distance(hand[8], wrist)
            >
            self.distance(hand[6], wrist) * 1.15
        )

        middle_extended = (
            self.distance(hand[12], wrist)
            >
            self.distance(hand[10], wrist) * 1.15
        )

        ring_extended = (
            self.distance(hand[16], wrist)
            >
            self.distance(hand[14], wrist) * 1.15
        )

        pinky_extended = (
            self.distance(hand[20], wrist)
            >
            self.distance(hand[18], wrist) * 1.15
        )

        fingers = [
            index_extended,
            middle_extended,
            ring_extended,
            pinky_extended
        ]

        count = sum(fingers)

        # =====================================
        # GESTURES
        # =====================================

        if index_extended and count == 1:
            return "DRAW"

        if count == 4:
            return "OPEN"

        if count == 0:
            return "FIST"

        return "OTHER"

    def get_gesture(self, results):

        detected = self.detect_raw_gesture(results)

        # Same gesture
        if detected == self.current_gesture:

            self.candidate_gesture = None
            self.candidate_count = 0

            return self.current_gesture

        # New gesture
        if detected != self.candidate_gesture:

            self.candidate_gesture = detected
            self.candidate_count = 1

        else:

            self.candidate_count += 1

        # Accept new gesture
        if self.candidate_count >= self.required_frames:

            self.current_gesture = self.candidate_gesture

            self.candidate_gesture = None
            self.candidate_count = 0

        return self.current_gesture