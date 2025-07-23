import os
import cv2
import numpy as np
import face_recognition
from typing import List, Dict, Any, Tuple, Optional

class ImageRecognition:
    """
    Image recognition system specialized for Alzheimer's patients.
    Provides face detection, object recognition, and memory prompts.
    """
    
    def __init__(self, known_faces_dir='data/images/family_photos'):
        """
        Initialize image recognition system.
        
        Args:
            known_faces_dir: Directory containing known face images
        """
        self.known_faces_dir = known_faces_dir
        self.known_faces = []
        self.known_names = []
        
        # Load known faces if directory exists
        if os.path.exists(known_faces_dir):
            self._load_known_faces()
        else:
            os.makedirs(known_faces_dir, exist_ok=True)
            
        # Settings for Arabic-specific prompts
        self.prompt_templates = {
            'person_recognized': "هذه صورة {name}. {relation}",
            'person_unknown': "هل تتذكر من هذا الشخص في الصورة؟",
            'multiple_people': "هذه صورة تحتوي على {count} أشخاص. هل تتذكرهم؟",
            'place_recognized': "هذه صورة من {place}. هل تتذكر متى كنت هناك؟",
            'object_recognized': "هذا {object}. هل لديك ذكريات متعلقة به؟"
        }
        
    def _load_known_faces(self):
        """Load known faces from directory"""
        self.known_faces = []
        self.known_names = []
        
        # Load each image file
        for filename in os.listdir(self.known_faces_dir):
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                # Extract name from filename (e.g. "ahmed_father.jpg" -> "ahmed")
                name = os.path.splitext(filename)[0].split('_')[0]
                
                # Load image and encode face
                image_path = os.path.join(self.known_faces_dir, filename)
                image = face_recognition.load_image_file(image_path)
                
                # Try to find face encodings
                face_encodings = face_recognition.face_encodings(image)
                if face_encodings:
                    # Use first face found
                    self.known_faces.append(face_encodings[0])
                    self.known_names.append(name)
                    print(f"Loaded known face: {name}")
                else:
                    print(f"No face found in {filename}")
    
    def add_known_face(self, image_path: str, name: str, relation: str = "") -> bool:
        """
        Add a new known face.
        
        Args:
            image_path: Path to image containing face
            name: Name of person
            relation: Relationship to patient (e.g., "son", "wife")
            
        Returns:
            bool: True if face was added, False otherwise
        """
        try:
            # Load image and find faces
            image = face_recognition.load_image_file(image_path)
            face_encodings = face_recognition.face_encodings(image)
            
            if not face_encodings:
                print(f"No face found in {image_path}")
                return False
                
            # Use first face found
            face_encoding = face_encodings[0]
            
            # Add to known faces
            self.known_faces.append(face_encoding)
            self.known_names.append(name)
            
            # Save copy to known faces directory
            relation_suffix = f"_{relation}" if relation else ""
            output_filename = f"{name}{relation_suffix}.jpg"
            output_path = os.path.join(self.known_faces_dir, output_filename)
            
            # Save image
            cv2.imwrite(output_path, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
            
            print(f"Added known face: {name}")
            return True
            
        except Exception as e:
            print(f"Error adding known face: {e}")
            return False
    
    def recognize_faces(self, image_path: str) -> List[Dict[str, Any]]:
        """
        Recognize faces in an image.
        
        Args:
            image_path: Path to image
            
        Returns:
            List of dictionaries with face information
        """
        results = []
        
        try:
            # Load image
            image = face_recognition.load_image_file(image_path)
            
            # Find faces
            face_locations = face_recognition.face_locations(image)
            face_encodings = face_recognition.face_encodings(image, face_locations)
            
            # Process each face
            for face_encoding, face_location in zip(face_encodings, face_locations):
                # Compare with known faces
                matches = face_recognition.compare_faces(self.known_faces, face_encoding, tolerance=0.6)
                name = "Unknown"
                confidence = 0.0
                
                # Use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(self.known_faces, face_encoding)
                if len(face_distances) > 0:
                    best_match_index = np.argmin(face_distances)
                    confidence = 1.0 - face_distances[best_match_index]
                    
                    if matches[best_match_index] and confidence > 0.5:
                        name = self.known_names[best_match_index]
                
                # Extract face location
                top, right, bottom, left = face_location
                
                # Add to results
                results.append({
                    'name': name,
                    'confidence': float(confidence),
                    'location': {'top': top, 'right': right, 'bottom': bottom, 'left': left}
                })
                
            return results
            
        except Exception as e:
            print(f"Error recognizing faces: {e}")
            return []
    
    def analyze_image(self, image_path: str) -> Dict[str, Any]:
        """
        Analyze image for faces, objects, and memory prompts.
        
        Args:
            image_path: Path to image
            
        Returns:
            Dictionary with analysis results
        """
        analysis = {
            'faces': [],
            'objects': [],
            'scene_type': 'unknown',
            'memory_prompts': [],
            'has_known_faces': False
        }
        
        # Recognize faces
        faces = self.recognize_faces(image_path)
        analysis['faces'] = faces
        
        # Check for known faces
        known_faces = [face for face in faces if face['name'] != "Unknown"]
        analysis['has_known_faces'] = len(known_faces) > 0
        
        # Generate memory prompts
        if analysis['has_known_faces']:
            # Create prompts for each known person
            for face in known_faces:
                name = face['name']
                prompt = self.prompt_templates['person_recognized'].format(
                    name=name,
                    relation=self._get_relation(name)
                )
                analysis['memory_prompts'].append(prompt)
        elif len(faces) > 0:
            # Unknown faces
            if len(faces) == 1:
                analysis['memory_prompts'].append(self.prompt_templates['person_unknown'])
            else:
                analysis['memory_prompts'].append(
                    self.prompt_templates['multiple_people'].format(count=len(faces))
                )
        
        # Add general memory prompt
        analysis['memory_prompts'].append("هل تتذكر متى التقطت هذه الصورة؟")
        
        return analysis
    
    def _get_relation(self, name: str) -> str:
        """Get relationship for a person if available"""
        # Look for relation in filename
        for filename in os.listdir(self.known_faces_dir):
            if filename.startswith(f"{name}_"):
                parts = os.path.splitext(filename)[0].split('_')
                if len(parts) > 1:
                    relation = parts[1]
                    # Map English relation to Arabic
                    relation_map = {
                        'father': 'والدك',
                        'mother': 'والدتك',
                        'son': 'ابنك',
                        'daughter': 'ابنتك',
                        'brother': 'أخوك',
                        'sister': 'أختك',
                        'wife': 'زوجتك',
                        'husband': 'زوجك',
                        'friend': 'صديقك',
                        'grandfather': 'جدك',
                        'grandmother': 'جدتك'
                    }
                    return relation_map.get(relation.lower(), relation)
        return ""
    
    def generate_memory_prompt(self, image_path: str) -> str:
        """
        Generate a memory prompt for an image.
        
        Args:
            image_path: Path to image
            
        Returns:
            Memory prompt string
        """
        analysis = self.analyze_image(image_path)
        
        if analysis['memory_prompts']:
            # Return first prompt
            return analysis['memory_prompts'][0]
        else:
            # Generic prompt
            return "هل تتذكر شيئًا عن هذه الصورة؟"
    
    def mark_faces(self, image_path: str, output_path: str) -> bool:
        """
        Create a copy of image with faces marked.
        
        Args:
            image_path: Path to input image
            output_path: Path to save output image
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                print(f"Error loading image: {image_path}")
                return False
            
            # Recognize faces
            faces = self.recognize_faces(image_path)
            
            # Draw rectangles around faces
            for face in faces:
                top = face['location']['top']
                right = face['location']['right']
                bottom = face['location']['bottom']
                left = face['location']['left']
                
                # Draw rectangle
                color = (0, 255, 0) if face['name'] != "Unknown" else (0, 0, 255)
                cv2.rectangle(image, (left, top), (right, bottom), color, 2)
                
                # Draw name
                name = face['name']
                confidence = int(face['confidence'] * 100)
                text = f"{name} ({confidence}%)"
                cv2.putText(image, text, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            
            # Save image
            cv2.imwrite(output_path, image)
            return True
            
        except Exception as e:
            print(f"Error marking faces: {e}")
            return False
    
    def get_known_faces(self) -> List[Dict[str, Any]]:
        """Get list of known faces"""
        known_faces = []
        
        for i, name in enumerate(self.known_names):
            known_faces.append({
                'name': name,
                'relation': self._get_relation(name)
            })
            
        return known_faces

# Example usage
if __name__ == "__main__":
    # Create image recognition system
    recognition = ImageRecognition()
    
    # Test with an image
    test_image = "data/images/family_photos/test.jpg"
    
    if os.path.exists(test_image):
        # Analyze image
        print(f"Analyzing image: {test_image}")
        analysis = recognition.analyze_image(test_image)
        
        # Print results
        print(f"Found {len(analysis['faces'])} faces:")
        for face in analysis['faces']:
            print(f"  {face['name']} ({face['confidence']:.2f})")
            
        print("\nMemory prompts:")
        for prompt in analysis['memory_prompts']:
            print(f"  {prompt}")
            
        # Mark faces
        output_image = "data/images/family_photos/test_marked.jpg"
        recognition.mark_faces(test_image, output_image)
        print(f"Marked faces saved to: {output_image}")
    else:
        print(f"Test image not found: {test_image}")
        print("Add a test image to test the system")
