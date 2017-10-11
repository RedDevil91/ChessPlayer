import cv2
import numpy as np

roi_size = 640
corners = np.float32([[0,          0],
                      [roi_size,   0],
                      [roi_size,   roi_size],
                      [0,          roi_size]])


class NoTableError(BaseException):
    pass


class RegionOfInterest(object):
    padding = 0

    def __init__(self, contour, moment, approx):
        self.contour = contour
        self.moment = moment
        self.approx = np.reshape(approx, (4, 2)).astype(np.float32)

        # sorting corners for perspective transform
        self.corners = np.zeros(self.approx.shape, dtype=np.float32)
        corner_diff = np.diff(self.approx, axis=1)
        corner_sum = np.sum(self.approx, axis=1)
        self.corners[0] = self.approx[np.argmin(corner_sum)]
        self.corners[1] = self.approx[np.argmin(corner_diff)]
        self.corners[2] = self.approx[np.argmax(corner_sum)]
        self.corners[3] = self.approx[np.argmax(corner_diff)]

        # add padding to table
        self.corners[0][0] -= self.padding
        self.corners[0][1] -= self.padding
        self.corners[1][0] += self.padding
        self.corners[1][1] -= self.padding
        self.corners[2][0] += self.padding
        self.corners[2][1] += self.padding
        self.corners[3][0] -= self.padding
        self.corners[3][1] += self.padding
        return


def preprocess_image(input_image):
    gray = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY_INV)
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
        # calculate the area
        contour_area = cv2.contourArea(cont)
        hull_area = cv2.contourArea(cv2.convexHull(cont))
        area_ratio = contour_area / float(hull_area)
        # if the approximation has 4 vertex and the area ratio is greater than 0.9 then
        # we assume that it's a square
        if len(approx) == 4 and area_ratio > 0.9:
            M = cv2.moments(cont)
            roi_img = RegionOfInterest(cont, M, approx)
            # the greatest square will be the sudoku table itself
            break
    else:
        # if there is no square
        raise NoTableError
    return roi_img


if __name__ == '__main__':
    raw_image = cv2.imread('pictures/board_start2.png')
    thresholded = preprocess_image(raw_image)
    roi = get_roi(thresholded)

    # use perspective transformation on the image to get the table only
    pers_matrix = cv2.getPerspectiveTransform(roi.corners, corners)
    table_image = cv2.warpPerspective(raw_image, pers_matrix, (roi_size, roi_size))

    cv2.imshow('table', table_image)

    gray = cv2.cvtColor(table_image, cv2.COLOR_BGR2GRAY)

    for row in range(8):
        for col in range(8):
            row_start = row*80
            row_end = (row+1)*80
            col_start = col*80
            col_end = (col+1)*80
            cv2.imwrite('squares/square_%d_%d.png' % (row, col), gray[row_start:row_end, col_start:col_end])

    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
