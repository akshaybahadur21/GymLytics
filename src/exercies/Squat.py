import mediapipe as mp

from src.ThreadedCamera import ThreadedCamera
from src.exercies.Exercise import Exercise
from src.utils import *

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
pose_landmark_drawing_spec = mp_drawing.DrawingSpec(thickness=5, circle_radius=2, color=(0, 0, 255))
pose_connection_drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1, color=(0, 255, 0))
PRESENCE_THRESHOLD = 0.5
VISIBILITY_THRESHOLD = 0.5
performedSquat = False


class Squat(Exercise):
    def __init__(self):
        pass

    def exercise(self, source):
        threaded_camera = ThreadedCamera(source)
        scount = 0
        while True:
            success, image = threaded_camera.show_frame()
            if not success or image is None:
                continue
            image = cv2.flip(image, 1)
            image_orig = cv2.flip(image, 1)
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                landmark_drawing_spec=pose_landmark_drawing_spec,
                connection_drawing_spec=pose_connection_drawing_spec)

            idx_to_coordinates = get_idx_to_coordinates(image, results)

            try:
                # knee angle
                # cv2.line(image, (idx_to_coordinates[24]), (idx_to_coordinates[26]), thickness=4, color=(0, 0, 255))
                # cv2.line(image, (idx_to_coordinates[26]), (idx_to_coordinates[28]), thickness=4, color=(0, 0, 255))
                # cv2.line(image, (idx_to_coordinates[23]), (idx_to_coordinates[25]), thickness=4, color=(255, 0, 0))
                # cv2.line(image, (idx_to_coordinates[25]), (idx_to_coordinates[27]), thickness=4, color=(255, 0, 0))
                l1 = np.linspace(idx_to_coordinates[24], idx_to_coordinates[26], 100)
                l2 = np.linspace(idx_to_coordinates[26], idx_to_coordinates[28], 100)
                cv2.line(image, (int(l1[99][0]), int(l1[99][1])), (int(l1[69][0]), int(l1[69][1])), thickness=4,
                         color=(0, 0, 255))
                cv2.line(image, (int(l2[0][0]), int(l2[0][1])), (int(l2[30][0]), int(l2[30][1])), thickness=4,
                         color=(0, 0, 255))
                ang1 = ang((idx_to_coordinates[24], idx_to_coordinates[26]),
                           (idx_to_coordinates[26], idx_to_coordinates[28]))
                cv2.putText(image, str(round(ang1, 2)), (idx_to_coordinates[26]),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=0.6, color=(0, 255, 0), thickness=2)
                center, radius, start_angle, end_angle = convert_arc(l1[90], l2[10], sagitta=15)
                axes = (radius, radius)
                draw_ellipse(image, center, axes, -1, start_angle, end_angle, 255)

                l1 = np.linspace(idx_to_coordinates[23], idx_to_coordinates[25], 100)
                l2 = np.linspace(idx_to_coordinates[25], idx_to_coordinates[27], 100)
                cv2.line(image, (int(l1[99][0]), int(l1[99][1])), (int(l1[69][0]), int(l1[69][1])), thickness=4,
                         color=(0, 0, 255))
                cv2.line(image, (int(l2[0][0]), int(l2[0][1])), (int(l2[30][0]), int(l2[30][1])), thickness=4,
                         color=(0, 0, 255))
                ang2 = ang((idx_to_coordinates[23], idx_to_coordinates[25]),
                           (idx_to_coordinates[25], idx_to_coordinates[27]))
                cv2.putText(image, str(round(ang2, 2)), (idx_to_coordinates[25]),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=0.6, color=(0, 255, 0), thickness=2)
                center, radius, start_angle, end_angle = convert_arc(l1[90], l2[10], sagitta=15)
                axes = (radius, radius)
                draw_ellipse(image, center, axes, -1, start_angle, end_angle, 255)
            except:
                pass

            try:
                # elbow
                # cv2.line(image, (idx_to_coordinates[12]), (idx_to_coordinates[14]), thickness=4, color=(255, 0, 255))
                # cv2.line(image, (idx_to_coordinates[14]), (idx_to_coordinates[16]), thickness=4, color=(255, 0, 255))
                # cv2.line(image, (idx_to_coordinates[11]), (idx_to_coordinates[13]), thickness=4, color=(255, 255, 0))
                # cv2.line(image, (idx_to_coordinates[13]), (idx_to_coordinates[15]), thickness=4, color=(255, 255, 0))
                l1 = np.linspace(idx_to_coordinates[12], idx_to_coordinates[14], 100)
                l2 = np.linspace(idx_to_coordinates[14], idx_to_coordinates[16], 100)
                cv2.line(image, (int(l1[99][0]), int(l1[99][1])), (int(l1[69][0]), int(l1[69][1])), thickness=4,
                         color=(0, 0, 255))
                cv2.line(image, (int(l2[0][0]), int(l2[0][1])), (int(l2[30][0]), int(l2[30][1])), thickness=4,
                         color=(0, 0, 255))
                eang1 = ang((idx_to_coordinates[12], idx_to_coordinates[14]),
                            (idx_to_coordinates[14], idx_to_coordinates[16]))
                cv2.putText(image, str(round(eang1, 2)), (idx_to_coordinates[14]),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=0.6, color=(0, 255, 0), thickness=2)
                center, radius, start_angle, end_angle = convert_arc(l1[80], l2[20], sagitta=15)
                axes = (radius, radius)
                draw_ellipse(image, center, axes, -1, start_angle, end_angle, 255)

                l1 = np.linspace(idx_to_coordinates[11], idx_to_coordinates[13], 100)
                l2 = np.linspace(idx_to_coordinates[13], idx_to_coordinates[15], 100)
                cv2.line(image, (int(l1[99][0]), int(l1[99][1])), (int(l1[69][0]), int(l1[69][1])), thickness=4,
                         color=(0, 0, 255))
                cv2.line(image, (int(l2[0][0]), int(l2[0][1])), (int(l2[30][0]), int(l2[30][1])), thickness=4,
                         color=(0, 0, 255))
                eang2 = ang((idx_to_coordinates[11], idx_to_coordinates[13]),
                            (idx_to_coordinates[13], idx_to_coordinates[15]))
                cv2.putText(image, str(round(eang2, 2)), (idx_to_coordinates[13]),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=0.6, color=(0, 255, 0), thickness=2)
                center, radius, start_angle, end_angle = convert_arc(l1[80], l2[20], sagitta=15)
                axes = (radius, radius)
                draw_ellipse(image, center, axes, -1, start_angle, end_angle, 255)
            except:
                pass

            try:
                # Back
                # cv2.line(image, (idx_to_coordinates[12]), (idx_to_coordinates[24]), thickness=4, color=(255, 0, 255))
                # cv2.line(image, (idx_to_coordinates[24]), (idx_to_coordinates[26]), thickness=4, color=(255, 0, 255))
                # cv2.line(image, (idx_to_coordinates[11]), (idx_to_coordinates[23]), thickness=4, color=(255, 255, 0))
                # cv2.line(image, (idx_to_coordinates[23]), (idx_to_coordinates[25]), thickness=4, color=(255, 255, 0))
                if 12 in idx_to_coordinates and 24 in idx_to_coordinates and 26 in idx_to_coordinates:
                    l1 = np.linspace(idx_to_coordinates[12], idx_to_coordinates[24], 100)
                    l2 = np.linspace(idx_to_coordinates[24], idx_to_coordinates[26], 100)
                    cv2.line(image, (int(l1[99][0]), int(l1[99][1])), (int(l1[69][0]), int(l1[69][1])), thickness=4,
                             color=(0, 0, 255))
                    cv2.line(image, (int(l2[0][0]), int(l2[0][1])), (int(l2[30][0]), int(l2[30][1])), thickness=4,
                             color=(0, 0, 255))
                    bang1 = ang((idx_to_coordinates[12], idx_to_coordinates[24]),
                                (idx_to_coordinates[24], idx_to_coordinates[26]))
                    cv2.putText(image, str(round(bang1, 2)), (idx_to_coordinates[24]),
                                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=0.6, color=(0, 255, 0), thickness=2)
                    center, radius, start_angle, end_angle = convert_arc(l1[90], l2[10], sagitta=15)
                    axes = (radius, radius)
                    draw_ellipse(image, center, axes, -1, start_angle, end_angle, 255)

                else:
                    l1 = np.linspace(idx_to_coordinates[11], idx_to_coordinates[23], 100)
                    l2 = np.linspace(idx_to_coordinates[23], idx_to_coordinates[25], 100)
                    cv2.line(image, (int(l1[99][0]), int(l1[99][1])), (int(l1[69][0]), int(l1[69][1])), thickness=4,
                             color=(0, 0, 255))
                    cv2.line(image, (int(l2[0][0]), int(l2[0][1])), (int(l2[30][0]), int(l2[30][1])), thickness=4,
                             color=(0, 0, 255))
                    bang2 = ang((idx_to_coordinates[11], idx_to_coordinates[23]),
                                (idx_to_coordinates[23], idx_to_coordinates[25]))
                    cv2.putText(image, str(round(bang2, 2)), (idx_to_coordinates[23]),
                                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=0.6, color=(0, 255, 0), thickness=2)
                    center, radius, start_angle, end_angle = convert_arc(l1[90], l2[10], sagitta=15)
                    axes = (radius, radius)
                    draw_ellipse(image, center, axes, -1, start_angle, end_angle, 255)
            except:
                pass

            try:
                # Count Number of squats
                if 24 in idx_to_coordinates:
                    hip_coord = idx_to_coordinates[24]
                else:
                    hip_coord = idx_to_coordinates[23]

                if 26 in idx_to_coordinates:
                    knee_coord = idx_to_coordinates[26]
                else:
                    knee_coord = idx_to_coordinates[25]

                if abs(hip_coord[1] - knee_coord[1]) < 35:
                    performedSquat = True
                if abs(hip_coord[1] - knee_coord[1]) > 35 and performedSquat:
                    scount += 1
                    performedSquat = False

            except:
                pass
            if 0 in idx_to_coordinates:
                cv2.putText(image, "Count : " + str(scount),
                            (idx_to_coordinates[0][0] - 30, idx_to_coordinates[0][1] - 80),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=0.9, color=(0, 0, 0), thickness=2)
            cv2.imshow('Image', rescale_frame(image, percent=100))
            if cv2.waitKey(5) & 0xFF == 27:
                break
        pose.close()
