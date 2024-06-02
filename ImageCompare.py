import cv2
import face_recognition


class ImageCompare:
    def __init__(self, img1, img2):
        self.img1 = img1
        self.img2 = img2

    def is_face_match(self):
        """Checks if the face in the input image matches the face in the target image."""
        input_face_encodings = self.get_face_encodings(self.img1)
        target_face_encodings = self.get_face_encodings(self.img2)

        if not input_face_encodings or not target_face_encodings:
            return False  # No faces found in one of the images

        for input_face_encoding in input_face_encodings:
            if self.compare_faces(target_face_encodings, input_face_encoding):
                return True

        return False

    def get_face_encodings(self, image):
        """Returns the face encodings for the faces in the image."""
        face_locations = face_recognition.face_locations(image)
        return face_recognition.face_encodings(image, face_locations)

    def compare_faces(self, known_face_encodings, face_encoding_to_check):
        """Compares a list of face encodings against a candidate encoding to see if they match."""
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding_to_check)
        return True in matches
