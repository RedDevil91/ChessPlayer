import os
import cv2
import numpy as np

from chess_table import ChessTable, TABLE_FIELD_NUM, SQUARE_SIZE
from win_interface import win_screen


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


def preprocess_image(input_image, threshold, algo=cv2.THRESH_BINARY_INV):
    gray = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, threshold, 255, algo)
    return thresh


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


def evaluate_square(square):
    for figure in os.listdir("figures"):
        fig_img = cv2.imread("figures/" + figure)
        fig_img = cv2.cvtColor(fig_img, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(square, fig_img)
        if np.mean(diff) < 1.0:
            res, _ = os.path.splitext(figure)
            return res
    else:
        raise AssertionError


def decide_table_orientation(image):
    topleft_square = image[0:SQUARE_SIZE, 0:SQUARE_SIZE]
    topleft_figure = evaluate_square(topleft_square)
    if topleft_figure.startswith("b_"):
        return 'white'
    return 'black'


def get_table_from_screen(player='white'):
    ratio, screen_img = win_screen()
    thresholded = preprocess_image(screen_img, 220)
    roi = get_roi(thresholded)

    # increment is needed because the table size is 639x639
    table_image = screen_img[roi.corners[0][1]:roi.corners[2][1] + 1, roi.corners[0][0]:roi.corners[2][0] + 1]

    gray = preprocess_image(table_image, 30, algo=cv2.THRESH_BINARY)

    player = decide_table_orientation(gray)

    table = ChessTable(roi.corners[0], ratio)

    for row in range(TABLE_FIELD_NUM):
        for col in range(TABLE_FIELD_NUM):
            row_start = row * SQUARE_SIZE
            row_end = (row + 1) * SQUARE_SIZE
            col_start = col * SQUARE_SIZE
            col_end = (col + 1) * SQUARE_SIZE
            square = gray[row_start:row_end, col_start:col_end]
            figure = evaluate_square(square)
            if player == 'white':
                field_id = (TABLE_FIELD_NUM - row - 1) * TABLE_FIELD_NUM + col
            else:
                field_id = row * TABLE_FIELD_NUM + col
            field = table.setField(field_id, figure)
            field.setCenter(table.top_left, row, col)
    return table


if __name__ == '__main__':
    import time
    from win_interface import Mouse

    start = time.time()
    table = get_table_from_screen()
    print(time.time() - start)
    print(table)
    # TODO: check the difference between the real and the screenshot pixel values
    # mouse = Mouse()
    # from_field = table.getField("e2")
    # from_point = from_field.getCenter()
    # to_field = table.getField("e4")
    # to_point = to_field.getCenter()
    # mouse.click(from_point[0], from_point[1])
    # time.sleep(0.2)
    # mouse.click(to_point[0], to_point[1])
