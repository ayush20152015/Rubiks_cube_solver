"""
Model inference utilities
"""
import numpy as np
import tensorflow as tf
from typing import Tuple


class CubeInference:
    """Load and run inference with trained model"""
    
    def __init__(self, model_path: str):
        """
        Initialize inference
        
        Args:
            model_path: Path to saved model
        """
        self.model = tf.keras.models.load_model(model_path)
        self.color_names = ['W', 'R', 'G', 'B', 'O', 'Y']
    
    def predict_color(self, image: np.ndarray) -> Tuple[str, float]:
        """
        Predict color from image
        
        Args:
            image: Image array (224, 224, 3)
            
        Returns:
            (color letter, confidence)
        """
        # Add batch dimension if needed
        if len(image.shape) == 3:
            image = np.expand_dims(image, axis=0)
        
        # Make prediction
        predictions = self.model.predict(image, verbose=0)
        class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][class_idx])
        
        color = self.color_names[class_idx]
        return color, confidence
    
    def predict_face(self, face_image: np.ndarray) -> Tuple[list, float]:
        """
        Predict 3x3 grid of colors from full face image
        
        Args:
            face_image: Full face image (must be preprocessed)
            
        Returns:
            (3x3 color grid, mean confidence)
        """
        # Divide into 3x3 grid
        h, w = face_image.shape[:2]
        cell_h, cell_w = h // 3, w // 3
        
        colors = []
        confidences = []
        
        for i in range(3):
            row = []
            for j in range(3):
                y1, y2 = i * cell_h, (i + 1) * cell_h
                x1, x2 = j * cell_w, (j + 1) * cell_w
                cell = face_image[y1:y2, x1:x2]
                
                color, conf = self.predict_color(cell)
                row.append(color)
                confidences.append(conf)
            
            colors.append(row)
        
        mean_confidence = np.mean(confidences)
        return colors, mean_confidence
