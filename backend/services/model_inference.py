import numpy as np
from typing import Optional
import os
from config import settings


class ModelInference:
    """Handle CNN model loading and inference"""
    
    def __init__(self):
        self.model = None
        self.model_loaded = False
        self._load_model()
    
    def _load_model(self):
        """Load pre-trained CNN model"""
        try:
            # For MVP, we can use a placeholder or a pre-trained model
            # In production, you'd load a TensorFlow saved model here
            if os.path.exists(settings.CNN_MODEL_PATH):
                # Load model
                import tensorflow as tf
                self.model = tf.keras.models.load_model(settings.CNN_MODEL_PATH)
                self.model_loaded = True
            else:
                # Use MobileNetV2 as base model for color classification
                import tensorflow as tf
                self.model = tf.keras.applications.MobileNetV2(
                    input_shape=(settings.IMAGE_SIZE, settings.IMAGE_SIZE, 3),
                    include_top=True,
                    weights='imagenet'
                )
                self.model_loaded = True
        except Exception as e:
            print(f"Warning: Could not load CNN model: {e}")
            self.model_loaded = False
    
    def infer(self, image_array: np.ndarray) -> dict:
        """
        Run inference on image array
        
        Args:
            image_array: Preprocessed image array
            
        Returns:
            Inference result with predictions
        """
        if not self.model_loaded:
            return {'error': 'Model not loaded'}
        
        try:
            # Run prediction
            predictions = self.model.predict(image_array, verbose=0)
            
            return {
                'predictions': predictions.tolist(),
                'success': True
            }
        except Exception as e:
            return {'error': str(e), 'success': False}
    
    def get_color_from_image(self, image_array: np.ndarray) -> Optional[str]:
        """
        Simplified color detection from image
        In production, this would be replaced with proper color classification
        
        Args:
            image_array: Preprocessed image array
            
        Returns:
            Detected color as letter (W, R, G, B, O, Y)
        """
        # Convert back to 0-255 range
        img = ((image_array[0] + 1.0) * 127.5).astype(np.uint8)
        
        # Use simple color detection based on pixel statistics
        # This is a placeholder - real implementation would use CNN
        r_mean = np.mean(img[:, :, 0])
        g_mean = np.mean(img[:, :, 1])
        b_mean = np.mean(img[:, :, 2])
        
        # Simple heuristic
        if r_mean > 200 and g_mean > 200 and b_mean > 200:
            return 'W'  # White
        elif r_mean > 150 and g_mean < 100 and b_mean < 100:
            return 'R'  # Red
        elif r_mean < 100 and g_mean > 150 and b_mean < 100:
            return 'G'  # Green
        elif r_mean < 100 and g_mean < 100 and b_mean > 150:
            return 'B'  # Blue
        elif r_mean > 200 and g_mean > 100 and b_mean < 100:
            return 'Y'  # Yellow
        elif r_mean > 200 and g_mean > 100 and b_mean < 100:
            return 'O'  # Orange
        else:
            return 'W'  # Default to white
