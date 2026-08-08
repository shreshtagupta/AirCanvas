import cv2
import ctypes

from hand_tracking.hand_detector import HandDetector
from drawing.canvas import Canvas
from drawing.palette import ColorPalette
from gestures.gesture_detector import GestureDetector


def get_screen_size():

    user32 = ctypes.windll.user32

    width = user32.GetSystemMetrics(0)
    height = user32.GetSystemMetrics(1)

    return width, height


def main():

    # =========================================
    # SCREEN
    # =========================================

    SCREEN_WIDTH, SCREEN_HEIGHT = get_screen_size()

    print(
        "Screen resolution:",
        SCREEN_WIDTH,
        "x",
        SCREEN_HEIGHT
    )

    # =========================================
    # INTERNAL AIR BOARD
    # =========================================

    BOARD_WIDTH = 1280
    BOARD_HEIGHT = 720

    # =========================================
    # CAMERA
    # =========================================

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():

        print("ERROR: Could not open webcam.")
        return

    # =========================================
    # OBJECTS
    # =========================================

    detector = HandDetector()

    canvas = Canvas(
        BOARD_WIDTH,
        BOARD_HEIGHT
    )

    gesture_detector = GestureDetector()

    palette = ColorPalette()

    # =========================================
    # MOUSE CALLBACK
    # =========================================

    def mouse_callback(event, x, y, flags, param):

        if event == cv2.EVENT_LBUTTONDOWN:

            # Convert screen coordinates
            # to board coordinates

            board_x = int(
                x * BOARD_WIDTH / SCREEN_WIDTH
            )

            board_y = int(
                y * BOARD_HEIGHT / SCREEN_HEIGHT
            )

            selected_color = palette.select_color(
                board_x,
                board_y
            )

            if selected_color is not None:

                canvas.set_color(
                    selected_color
                )

                print(
                    "Selected:",
                    palette.get_selected_name()
                )

    # =========================================
    # WINDOW
    # =========================================

    WINDOW_NAME = "AIR CANVAS"

    cv2.namedWindow(
        WINDOW_NAME,
        cv2.WINDOW_NORMAL
    )

    # Make window the size of the screen
    cv2.resizeWindow(
        WINDOW_NAME,
        SCREEN_WIDTH,
        SCREEN_HEIGHT
    )

    cv2.moveWindow(
        WINDOW_NAME,
        0,
        0
    )

    cv2.setMouseCallback(
        WINDOW_NAME,
        mouse_callback
    )

    # =========================================
    # START
    # =========================================

    print()
    print("================================")
    print("          AIR CANVAS")
    print("================================")
    print()
    print(
        "Board:",
        BOARD_WIDTH,
        "x",
        BOARD_HEIGHT
    )
    print(
        "Screen:",
        SCREEN_WIDTH,
        "x",
        SCREEN_HEIGHT
    )
    print()
    print("INDEX FINGER = DRAW")
    print("PINCH = ERASER")
    print()
    print("Click palette = Change color")
    print("Z = UNDO")
    print("C = CLEAR")
    print("ESC = EXIT")
    print()

    # =========================================
    # MAIN LOOP
    # =========================================

    while True:

        # -------------------------------------
        # CAMERA FRAME
        # -------------------------------------

        success, frame = cap.read()

        if not success:

            print(
                "ERROR: Could not read camera."
            )

            break

        # -------------------------------------
        # MIRROR
        # -------------------------------------

        frame = cv2.flip(
            frame,
            1
        )

        # -------------------------------------
        # RESIZE CAMERA TO BOARD
        # -------------------------------------

        frame = cv2.resize(
            frame,
            (
                BOARD_WIDTH,
                BOARD_HEIGHT
            )
        )

        # -------------------------------------
        # HAND DETECTION
        # -------------------------------------

        frame, results = detector.find_hands(
            frame
        )

        # -------------------------------------
        # GESTURE
        # -------------------------------------

        gesture = gesture_detector.get_gesture(
            results
        )

        # -------------------------------------
        # INDEX FINGER
        # -------------------------------------

        index_position = detector.get_index_finger(
            results,
            frame
        )

        # =====================================
        # DRAW
        # =====================================

        if (
            gesture == "DRAW"
            and index_position is not None
        ):

            x, y = index_position

            canvas.draw(
                (x, y)
            )

            cv2.circle(
                frame,
                (x, y),
                10,
                (0, 255, 0),
                -1
            )

        # =====================================
        # ERASER
        # =====================================

        elif (
            gesture == "ERASER"
            and index_position is not None
        ):

            x, y = index_position

            canvas.erase(
                (x, y)
            )

            cv2.circle(
                frame,
                (x, y),
                canvas.eraser_size // 2,
                (255, 255, 255),
                3
            )

            cv2.putText(
                frame,
                "ERASING",
                (20, 110),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2
            )

        # =====================================
        # STOP DRAWING
        # =====================================

        else:

            canvas.stop_drawing()

        # =====================================
        # GET DRAWING
        # =====================================

        drawing = canvas.get_canvas()

        # =====================================
        # COMBINE
        # =====================================

        output = cv2.addWeighted(
            frame,
            0.7,
            drawing,
            1.0,
            0
        )

        # =====================================
        # PALETTE
        # =====================================

        palette.draw(
            output
        )

        # =====================================
        # GESTURE TEXT
        # =====================================

        cv2.putText(
            output,
            "GESTURE: " + gesture,
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        # =====================================
        # INSTRUCTIONS
        # =====================================

        cv2.putText(
            output,
            "Click palette | Z Undo | C Clear | ESC Exit",
            (20, BOARD_HEIGHT - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            2
        )

        # =====================================
        # SCALE BOARD TO SCREEN
        # =====================================

        display = cv2.resize(
            output,
            (
                SCREEN_WIDTH,
                SCREEN_HEIGHT
            ),
            interpolation=cv2.INTER_LINEAR
        )

        # =====================================
        # SHOW
        # =====================================

        cv2.imshow(
            WINDOW_NAME,
            display
        )

        # =====================================
        # KEYBOARD
        # =====================================

        key = cv2.waitKey(1) & 0xFF

        if key == 27:

            break

        elif key == ord("z"):

            canvas.undo()

            print("Undo")

        elif key == ord("c"):

            canvas.clear()

            print("Canvas cleared")

    # =========================================
    # CLEANUP
    # =========================================

    cap.release()

    cv2.destroyAllWindows()


if __name__ == "__main__":

    main()