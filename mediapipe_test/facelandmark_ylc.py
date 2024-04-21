import cv2 as cv
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

cap = cv.VideoCapture('./video.mp4')
mp_face_mesh = mp.solutions.face_mesh

with mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
) as face_mesh:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            break

        # 竖直方向翻转
        image = cv.flip(image, 0)

        results = face_mesh.process(image)

        # print the face_blendshapes data
        print(type(results))


        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
                )

        cv.imshow("My Video", cv.flip(image, 1))

        if cv.waitKey(100) == ord('q'):
            break

cap.release()
cv.destroyAllWindows()