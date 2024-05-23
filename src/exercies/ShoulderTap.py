import mediapipe as mp
from src.ThreadedCamera import ThreadedCamera
from src.exercies.Exercise import Exercise
import time
from src.utils import *

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
mp_pose = mp.solutions.pose

pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
pose_landmark_drawing_spec = mp_drawing.DrawingSpec(thickness=5, circle_radius=2, color=(0, 0, 255))
pose_connection_drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1, color=(0, 255, 0))
PRESENCE_THRESHOLD = 0.5
VISIBILITY_THRESHOLD = 0.5
performedPushUp = False


class ShoulderTap(Exercise):
    def __init__(self):
        pass

    def exercise(self, source):
        threaded_camera = ThreadedCamera(source)
        ang1 = 0
        ang2 = 0
        count = 0
        frames = 0
        performedLeftTap = False
        performedRightTap = False
        while True:

            success, image = threaded_camera.show_frame()
            if not success or image is None:
                continue
            image = cv2.flip(image, 1)
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
                # shoulder - elbow - wrist
                if 11 in idx_to_coordinates and 13 in idx_to_coordinates and 15 in idx_to_coordinates:  # left side of body
                    cv2.line(image, (idx_to_coordinates[11]), (idx_to_coordinates[13]), thickness=6,
                             color=(255, 0, 0))
                    cv2.line(image, (idx_to_coordinates[13]), (idx_to_coordinates[15]), thickness=6,
                             color=(255, 0, 0))
                    ang1 = ang((idx_to_coordinates[11], idx_to_coordinates[13]),
                               (idx_to_coordinates[13], idx_to_coordinates[15]))
                    cv2.putText(image, str(round(ang1, 2)),
                                (idx_to_coordinates[13][0] - 40, idx_to_coordinates[13][1] - 50),
                                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=0.8, color=(0, 255, 0), thickness=3)
                    cv2.circle(image, (idx_to_coordinates[11]), 10, (0, 0, 255), cv2.FILLED)
                    cv2.circle(image, (idx_to_coordinates[11]), 15, (0, 0, 255), 2)
                    cv2.circle(image, (idx_to_coordinates[13]), 10, (0, 0, 255), cv2.FILLED)
                    cv2.circle(image, (idx_to_coordinates[13]), 15, (0, 0, 255), 2)
                    cv2.circle(image, (idx_to_coordinates[15]), 10, (0, 0, 255), cv2.FILLED)
                    cv2.circle(image, (idx_to_coordinates[15]), 15, (0, 0, 255), 2)
                if 12 in idx_to_coordinates and 14 in idx_to_coordinates and 16 in idx_to_coordinates:  # right side of body
                    cv2.line(image, (idx_to_coordinates[12]), (idx_to_coordinates[14]), thickness=6,
                             color=(255, 0, 0))
                    cv2.line(image, (idx_to_coordinates[14]), (idx_to_coordinates[16]), thickness=6,
                             color=(255, 0, 0))
                    ang2 = ang((idx_to_coordinates[12], idx_to_coordinates[14]),
                               (idx_to_coordinates[14], idx_to_coordinates[16]))
                    cv2.putText(image, str(round(ang2, 2)),
                                (idx_to_coordinates[14][0] - 40, idx_to_coordinates[14][1] - 50),
                                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=0.8, color=(0, 255, 0), thickness=3)
                    cv2.circle(image, (idx_to_coordinates[12]), 10, (0, 0, 255), cv2.FILLED)
                    cv2.circle(image, (idx_to_coordinates[12]), 15, (0, 0, 255), 2)
                    cv2.circle(image, (idx_to_coordinates[14]), 10, (0, 0, 255), cv2.FILLED)
                    cv2.circle(image, (idx_to_coordinates[14]), 15, (0, 0, 255), 2)
                    cv2.circle(image, (idx_to_coordinates[16]), 10, (0, 0, 255), cv2.FILLED)
                    cv2.circle(image, (idx_to_coordinates[16]), 15, (0, 0, 255), 2)
            except:
                pass

            try:
                frames += 1
                # cv2.putText(image, str(frames), (1200, 255), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                #             fontScale=1.1, color=(0, 255, 0), thickness=4)
                if frames > 80:
                    if ang1 < 120:
                        performedLeftTap = True
                    if ang1 > 150 and performedLeftTap:
                        count += 1
                        performedLeftTap = False
                    if ang2 < 120:
                        performedRightTap = True
                    if ang2 > 150 and performedRightTap:
                        count += 1
                        performedRightTap = False

                ang1 = 180 - ang1
                c1 = (255, 0, 0)
                if ang1 > 70:
                    c1 = (0, 255, 0)
                else:
                    c1 = (255, 0, 0)
                barLeft = np.interp(ang1, (10, 70), (850, 300))
                perLeft = np.interp(ang1, (10, 50), (0, 100))
                cv2.rectangle(image, (1400, 300), (1460, 850), c1)
                cv2.rectangle(image, (1400, int(barLeft)), (1460, 850), c1, cv2.FILLED)
                cv2.putText(image, f'{int(perLeft)} %', (1400, 255), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=1.1, color=c1, thickness=4)


                ang2 = 180 - ang2
                c2 = (255, 0, 0)
                if ang2 > 70:
                    c2 = (0, 255, 0)
                else:
                    c2 = (255, 0, 0)
                barRight = np.interp(ang2, (10, 70), (850, 300))
                perRight = np.interp(ang2, (10, 50), (0, 100))
                cv2.rectangle(image, (550, 300), (610, 850), c2)
                cv2.rectangle(image, (550, int(barRight)), (610, 850), c2, cv2.FILLED)
                cv2.putText(image, f'{int(perRight)} %', (550, 255), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=1.1, color=c2, thickness=4)

            except:
                pass
            if 0 in idx_to_coordinates:
                cv2.putText(image, "Taps : " + str(round(count)),
                            (idx_to_coordinates[0][0] - 80, idx_to_coordinates[0][1] - 290),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=1.2, color=(0, 0, 255), thickness=4)
            cv2.imshow('Image', rescale_frame(image, percent=150))
            if cv2.waitKey(5) & 0xFF == 27:
                break
        pose.close()
