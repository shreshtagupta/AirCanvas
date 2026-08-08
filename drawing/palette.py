import cv2


class ColorPalette:

    def __init__(self):

        # OpenCV uses BGR
        self.colors = [
            ("GREEN", (0, 255, 0)),
            ("RED", (0, 0, 255)),
            ("BLUE", (255, 0, 0)),
            ("YELLOW", (0, 255, 255)),
            ("PURPLE", (255, 0, 255)),
            ("WHITE", (255, 255, 255)),
            ("ORANGE", (0, 165, 255)),
            ("PINK", (203, 192, 255))
        ]

        self.selected_index = 0

        # Palette position
        self.start_x = 20
        self.start_y = 100

        # Size of each color box
        self.box_size = 45
        self.gap = 10

    def get_selected_color(self):

        return self.colors[self.selected_index][1]

    def get_selected_name(self):

        return self.colors[self.selected_index][0]

    def draw(self, frame):

        x = self.start_x

        for i, (name, color) in enumerate(self.colors):

            # Highlight selected color
            if i == self.selected_index:

                cv2.rectangle(
                    frame,
                    (
                        x - 4,
                        self.start_y - 4
                    ),
                    (
                        x + self.box_size + 4,
                        self.start_y + self.box_size + 4
                    ),
                    (255, 255, 255),
                    2
                )

            # Color box
            cv2.rectangle(
                frame,
                (
                    x,
                    self.start_y
                ),
                (
                    x + self.box_size,
                    self.start_y + self.box_size
                ),
                color,
                -1
            )

            # Move to next box
            x += self.box_size + self.gap

        # Current color text
        cv2.putText(
            frame,
            "COLOR: " + self.get_selected_name(),
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            self.get_selected_color(),
            2
        )

    def select_color(self, mouse_x, mouse_y):

        x = self.start_x

        for i in range(len(self.colors)):

            if (
                x <= mouse_x <= x + self.box_size
                and
                self.start_y <= mouse_y <= self.start_y + self.box_size
            ):

                self.selected_index = i

                return self.get_selected_color()

            x += self.box_size + self.gap

        return None