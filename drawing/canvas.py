import cv2
import numpy as np


class Canvas:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.canvas = np.zeros(
            (height, width, 3),
            dtype=np.uint8
        )

        # Current stroke
        self.current_stroke = None

        # All completed strokes
        self.strokes = []

        self.previous_point = None
        self.smoothed_point = None

        # Drawing settings
        self.color = (0, 255, 0)
        self.thickness = 6

        # Eraser size
        self.eraser_size = 35

        # Smoothing
        self.smoothing_factor = 0.50

    # =========================================
    # SMOOTH POINT
    # =========================================

    def smooth_point(self, point):

        if self.smoothed_point is None:

            self.smoothed_point = point

            return point

        old_x, old_y = self.smoothed_point
        new_x, new_y = point

        smooth_x = int(
            old_x * (1 - self.smoothing_factor)
            + new_x * self.smoothing_factor
        )

        smooth_y = int(
            old_y * (1 - self.smoothing_factor)
            + new_y * self.smoothing_factor
        )

        self.smoothed_point = (
            smooth_x,
            smooth_y
        )

        return self.smoothed_point

    # =========================================
    # START DRAWING
    # =========================================

    def start_stroke(self, point, color, thickness):

        self.current_stroke = {
            "color": color,
            "thickness": thickness,
            "points": [point]
        }

    # =========================================
    # DRAW
    # =========================================

    def draw(self, point):

        if point is None:
            return

        point = self.smooth_point(point)

        if self.current_stroke is None:

            self.start_stroke(
                point,
                self.color,
                self.thickness
            )

        else:

            self.current_stroke["points"].append(point)

        if self.previous_point is not None:

            cv2.line(
                self.canvas,
                self.previous_point,
                point,
                self.color,
                self.thickness,
                cv2.LINE_AA
            )

        self.previous_point = point

    # =========================================
    # ERASE
    # =========================================

    def erase(self, point):

        if point is None:
            return

        point = self.smooth_point(point)

        # Start eraser stroke
        if self.current_stroke is None:

            self.start_stroke(
                point,
                (0, 0, 0),
                self.eraser_size
            )

        else:

            self.current_stroke["points"].append(point)

        if self.previous_point is not None:

            cv2.line(
                self.canvas,
                self.previous_point,
                point,
                (0, 0, 0),
                self.eraser_size,
                cv2.LINE_AA
            )

        self.previous_point = point

    # =========================================
    # FINISH CURRENT STROKE
    # =========================================

    def stop_drawing(self):

        if self.current_stroke is not None:

            points = self.current_stroke["points"]

            if len(points) > 0:

                self.strokes.append(
                    self.current_stroke
                )

        self.current_stroke = None
        self.previous_point = None
        self.smoothed_point = None

    # =========================================
    # REDRAW EVERYTHING
    # =========================================

    def redraw(self):

        self.canvas = np.zeros(
            (self.height, self.width, 3),
            dtype=np.uint8
        )

        for stroke in self.strokes:

            points = stroke["points"]
            color = stroke["color"]
            thickness = stroke["thickness"]

            if len(points) == 1:

                cv2.circle(
                    self.canvas,
                    points[0],
                    thickness // 2,
                    color,
                    -1
                )

            else:

                for i in range(1, len(points)):

                    cv2.line(
                        self.canvas,
                        points[i - 1],
                        points[i],
                        color,
                        thickness,
                        cv2.LINE_AA
                    )

    # =========================================
    # UNDO
    # =========================================

    def undo(self):

        # Finish current stroke first
        self.stop_drawing()

        if len(self.strokes) > 0:

            self.strokes.pop()

            self.redraw()

    # =========================================
    # CLEAR
    # =========================================

    def clear(self):

        self.canvas = np.zeros(
            (self.height, self.width, 3),
            dtype=np.uint8
        )

        self.strokes = []

        self.current_stroke = None
        self.previous_point = None
        self.smoothed_point = None

    # =========================================
    # CHANGE COLOR
    # =========================================

    def set_color(self, color):

        self.stop_drawing()

        self.color = color

    # =========================================
    # GET CANVAS
    # =========================================

    def get_canvas(self):

        return self.canvas