import math
import cv2
import numpy as np
from mediapipe.python.solutions.drawing_utils import _normalized_to_pixel_coordinates


def draw_ellipse(
        img, center, axes, angle,
        startAngle, endAngle, color,
        thickness=2, lineType=cv2.LINE_AA, shift=10):
    # uses the shift to accurately get sub-pixel resolution for arc
    # taken from https://stackoverflow.com/a/44892317/5087436
    center = (
        int(round(center[0] * 2 ** shift)),
        int(round(center[1] * 2 ** shift))
    )
    axes = (
        int(round(axes[0] * 2 ** shift)),
        int(round(axes[1] * 2 ** shift))
    )
    return cv2.ellipse(
        img, center, axes, angle,
        startAngle, endAngle, color,
        thickness, lineType, shift)


def convert_arc(pt1, pt2, sagitta):
    # extract point coordinates
    x1, y1 = pt1
    x2, y2 = pt2

    # find normal from midpoint, follow by length sagitta
    n = np.array([y2 - y1, x1 - x2])
    n_dist = np.sqrt(np.sum(n ** 2))

    if np.isclose(n_dist, 0):
        # catch error here, d(pt1, pt2) ~ 0
        print('Error: The distance between pt1 and pt2 is too small.')

    n = n / n_dist
    x3, y3 = (np.array(pt1) + np.array(pt2)) / 2 + sagitta * n

    # calculate the circle from three points
    # see https://math.stackexchange.com/a/1460096/246399
    A = np.array([
        [x1 ** 2 + y1 ** 2, x1, y1, 1],
        [x2 ** 2 + y2 ** 2, x2, y2, 1],
        [x3 ** 2 + y3 ** 2, x3, y3, 1]])
    M11 = np.linalg.det(A[:, (1, 2, 3)])
    M12 = np.linalg.det(A[:, (0, 2, 3)])
    M13 = np.linalg.det(A[:, (0, 1, 3)])
    M14 = np.linalg.det(A[:, (0, 1, 2)])

    if np.isclose(M11, 0):
        # catch error here, the points are collinear (sagitta ~ 0)
        print('Error: The third point is collinear.')

    cx = 0.5 * M12 / M11
    cy = -0.5 * M13 / M11
    radius = np.sqrt(cx ** 2 + cy ** 2 + M14 / M11)

    # calculate angles of pt1 and pt2 from center of circle
    pt1_angle = 180 * np.arctan2(y1 - cy, x1 - cx) / np.pi
    pt2_angle = 180 * np.arctan2(y2 - cy, x2 - cx) / np.pi

    return (cx, cy), radius, pt1_angle, pt2_angle


def dot(vA, vB):
    return vA[0] * vB[0] + vA[1] * vB[1]


def ang(lineA, lineB):
    # Get nicer vector form
    vA = [(lineA[0][0] - lineA[1][0]), (lineA[0][1] - lineA[1][1])]
    vB = [(lineB[0][0] - lineB[1][0]), (lineB[0][1] - lineB[1][1])]
    # Get dot prod
    dot_prod = dot(vA, vB)
    # Get magnitudes
    magA = dot(vA, vA) ** 0.5
    magB = dot(vB, vB) ** 0.5
    # Get cosine value
    cos_ = dot_prod / magA / magB
    # Get angle in radians and then convert to degrees
    angle = math.acos(dot_prod / magB / magA)
    # Basically doing angle <- angle mod 360
    ang_deg = math.degrees(angle) % 360
    ang_deg = 180 - ang_deg

    if ang_deg - 180 >= 0:
        # As in if statement
        return 360 - ang_deg
    else:

        return ang_deg


def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent / 100)
    height = int(frame.shape[0] * percent / 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)


def get_idx_to_coordinates(image, results, VISIBILITY_THRESHOLD=0.5, PRESENCE_THRESHOLD=0.5):
    idx_to_coordinates = {}
    image_rows, image_cols, _ = image.shape
    try:
        for idx, landmark in enumerate(results.pose_landmarks.landmark):
            if ((landmark.HasField('visibility') and
                 landmark.visibility < VISIBILITY_THRESHOLD) or
                    (landmark.HasField('presence') and
                     landmark.presence < PRESENCE_THRESHOLD)):
                continue
            landmark_px = _normalized_to_pixel_coordinates(landmark.x, landmark.y,
                                                           image_cols, image_rows)
            if landmark_px:
                idx_to_coordinates[idx] = landmark_px
    except:
        pass
    return idx_to_coordinates
