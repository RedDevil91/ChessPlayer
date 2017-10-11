import os
import cv2
import numpy as np

from win_interface import screenshot


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
    contours, hierarchy = cv2.findContours(input_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

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
    return "No match"


if __name__ == '__main__':
    raw_image = cv2.imread('pictures/screen_00.png')
    thresholded = preprocess_image(raw_image, 220)
    roi = get_roi(thresholded)
    
    # increment is needed because the table size is 639x639
    table_image = raw_image[roi.corners[0][1]:roi.corners[2][1]+1, roi.corners[0][0]:roi.corners[2][0]+1]

    gray = preprocess_image(table_image, 30, algo=cv2.THRESH_BINARY)

    cv2.imshow("table", gray)

    for row in range(8):
        for col in range(8):
            row_start = row*80
            row_end = (row+1)*80
            col_start = col*80
            col_end = (col+1)*80
            square = gray[row_start:row_end, col_start:col_end]
            print evaluate_square(square)
            # cv2.imwrite('squares/square_%d_%d.png' % (row, col), square)

    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
