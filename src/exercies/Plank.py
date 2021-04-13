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


class Plank(Exercise):
    def __init__(self):
        pass

    def exercise(self, source):
        threaded_camera = ThreadedCamera(source)
        eang1 = 0
        plankTimer = None
        plankDuration = 0
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
                # shoulder - back - ankle
                if 11 in idx_to_coordinates and 23 in idx_to_coordinates and 27 in idx_to_coordinates:  # left side of body
                    cv2.line(image, (idx_to_coordinates[11]), (idx_to_coordinates[23]), thickness=6,
                             color=(255, 0, 0))
                    cv2.line(image, (idx_to_coordinates[23]), (idx_to_coordinates[27]), thickness=6,
                             color=(255, 0, 0))
                    eang1 = ang((idx_to_coordinates[11], idx_to_coordinates[23]),
                                (idx_to_coordinates[23], idx_to_coordinates[27]))
                    cv2.putText(image, str(round(eang1, 2)),
                                (idx_to_coordinates[23][0] - 40, idx_to_coordinates[23][1] - 50),
                                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=0.8, color=(0, 255, 0), thickness=3)
                    cv2.circle(image, (idx_to_coordinates[11]), 10, (0, 0, 255), cv2.FILLED)
                    cv2.circle(image, (idx_to_coordinates[11]), 15, (0, 0, 255), 2)
                    cv2.circle(image, (idx_to_coordinates[23]), 10, (0, 0, 255), cv2.FILLED)
                    cv2.circle(image, (idx_to_coordinates[23]), 15, (0, 0, 255), 2)
                    cv2.circle(image, (idx_to_coordinates[27]), 10, (0, 0, 255), cv2.FILLED)
                    cv2.circle(image, (idx_to_coordinates[27]), 15, (0, 0, 255), 2)
            except:
                pass

            try:

                if eang1 > 170:
                    if plankTimer == None:
                        plankTimer = time.time()
                    plankDuration += time.time() - plankTimer
                    plankTimer = time.time()
                else:
                    plankTimer = None
                bar = np.interp(eang1, (120, 170), (850, 300))
                per = np.interp(eang1, (120, 170), (0, 100))
                cv2.rectangle(image, (200, 300), (260, 850), (0, 255, 0))
                cv2.rectangle(image, (200, int(bar)), (260, 850), (0, 255, 0), cv2.FILLED)
                cv2.putText(image, f'{int(per)} %', (200, 255), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=1.1, color=(0, 255, 0), thickness=4)

            except:
                pass
            if 0 in idx_to_coordinates:
                cv2.putText(image, "Plank Timer : " + str(round(plankDuration)) + " sec",
                            (idx_to_coordinates[0][0] - 60, idx_to_coordinates[0][1] - 240),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=0.9, color=(0, 255, 0), thickness=4)
            cv2.imshow('Image', rescale_frame(image, percent=150))
            if cv2.waitKey(5) & 0xFF == 27:
                break
        pose.close()
