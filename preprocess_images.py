import os
import cv2
import numpy as np

from chess_table import ChessTable, TABLE_FIELD_NUM, SQUARE_SIZE
from win_interface import Screen, Mouse


class NoTableError(BaseException):
    pass


class RegionOfInterest(object):

    def __init__(self, contour, moment, approx):
        self.contour = contour
        self.moment = moment
        self.approx = np.reshape(approx, (4, 2)).astype(np.float32)

        # sorting corners for perspective transform
        self.corners = np.zeros(self.approx.shape, dtype=np.uint32)
        corner_diff = np.diff(self.approx, axis=1)
        corner_sum = np.sum(self.approx, axis=1)
        self.corners[0] = self.approx[np.argmin(corner_sum)]
        self.corners[1] = self.approx[np.argmin(corner_diff)]
        self.corners[2] = self.approx[np.argmax(corner_sum)]
        self.corners[3] = self.approx[np.argmax(corner_diff)]
        return

    def checkIfSquare(self):
        width = self.corners[2][0] - self.corners[0][0]
        height = self.corners[2][1] - self.corners[0][1]
        return width == height


class GameEngine(object):
    def __init__(self):
        self.mouse = Mouse()
        self.table = None
        return

    def newGame(self):
        table_roi, table_image = self.get_table_from_screen()

        player = self.decide_table_orientation(table_image)
        self.table = ChessTable(table_roi.corners[0], player)
        self.setFields(table_image)
        return

    def setFields(self, table_image):
        fields = []
        for row in range(TABLE_FIELD_NUM):
            for col in range(TABLE_FIELD_NUM):
                row_start = row * SQUARE_SIZE
                row_end = (row + 1) * SQUARE_SIZE
                col_start = col * SQUARE_SIZE
                col_end = (col + 1) * SQUARE_SIZE
                square = table_image[row_start:row_end, col_start:col_end]
                figure = self.evaluate_square(square)
                translation_vector = np.array([(col_start + col_end) / 2, (row_start + row_end) / 2])
                fields.append((figure, translation_vector))
        self.table.setFields(fields)
        return

    def moveFigure(self, from_pos, to_pos):
        from_field = self.table.getField(from_pos)
        from_point = from_field.getCenter()
        to_field = self.table.getField(to_pos)
        to_point = to_field.getCenter()
        self.mouse.click(from_point[0], from_point[1])
        time.sleep(1)
        self.mouse.click(to_point[0], to_point[1])
        time.sleep(1)
        return

    @classmethod
    def get_table_from_screen(cls):
        screen_img = Screen.shot()
        thresholded = cls.preprocess_image(screen_img, 220)
        table_roi = cls.get_roi(thresholded)

        # increment is needed because the table size is 639x639
        table_image = screen_img[table_roi.corners[0][1]:table_roi.corners[2][1] + 1, table_roi.corners[0][0]:table_roi.corners[2][0] + 1]
        table_image = cls.preprocess_image(table_image, 30, algo=cv2.THRESH_BINARY)
        return table_roi, table_image

    @classmethod
    def decide_table_orientation(cls, image):
        topleft_square = image[0:SQUARE_SIZE, 0:SQUARE_SIZE]
        topleft_figure = cls.evaluate_square(topleft_square)
        if topleft_figure.startswith("b_"):
            return 'white'
        return 'black'

    @staticmethod
    def get_roi(input_image):
        # find contours on the preprocessed input image
        _, contours, hierarchy = cv2.findContours(input_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # sort the contours by the area
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        for cont in contours:
            # calculate the perimeter and approximate the contour with a polygon
            perim = cv2.arcLength(cont, True)
            approx = cv2.approxPolyDP(cont, 0.04 * perim, True)
            # we are searching for a square
            if len(approx) != 4:
                continue
            # if the approximation has 4 vertex and the area ratio is greater than 0.9 then
            # we assume that it's a square
            M = cv2.moments(cont)
            roi_img = RegionOfInterest(cont, M, approx)
            if roi_img.checkIfSquare():
                # the greatest square will be the chess table itself
                break
        else:
            # if there is no square
            raise NoTableError
        return roi_img

    @staticmethod
    def evaluate_square(square):
        for figure in os.listdir("figures"):
            fig_img = cv2.imread("figures/" + figure)
            fig_img = cv2.cvtColor(fig_img, cv2.COLOR_BGR2GRAY)
            diff = cv2.absdiff(square, fig_img)
            if np.mean(diff) < 1.0:
                res, _ = os.path.splitext(figure)
                return res
        else:
            raise AssertionError("Couldn't find figure!")

    @staticmethod
    def preprocess_image(input_image, threshold, algo=cv2.THRESH_BINARY_INV):
        gray = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, threshold, 255, algo)
        return thresh


if __name__ == '__main__':
    import time

    engine = GameEngine()
    engine.newGame()
    if engine.table.player == "black":
        engine.moveFigure("d7", "d5")
        engine.moveFigure("g8", "f6")
    else:
        engine.moveFigure("e2", "e4")
        engine.moveFigure("b1", "c3")
