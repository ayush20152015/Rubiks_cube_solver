import cv2
import numpy as np
from PIL import Image
from io import BytesIO
from typing import Tuple
from config import settings


class ImageProcessor:
    """Process and preprocess cube face images"""
    
    @staticmethod
    def preprocess_image(file_content: bytes) -> np.ndarray:
        """
        Preprocess image for CNN inference
        
        Args:
            file_content: Raw image bytes
            
        Returns:
            Preprocessed image as numpy array
        """
        # Load image from bytes
        image = Image.open(BytesIO(file_content))
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize to model input size
        image = image.resize((settings.IMAGE_SIZE, settings.IMAGE_SIZE), Image.Resampling.LANCZOS)
        
        # Convert to numpy array
        img_array = np.array(image, dtype=np.float32)
        
        # Normalize to [-1, 1]
        img_array = img_array / 127.5 - 1.0
        
        return np.expand_dims(img_array, axis=0)  # Add batch dimension
    
    @staticmethod
    def extract_cube_colors(image_array: np.ndarray) -> list[list[str]]:
        """
        Extract 3x3 grid of colors from preprocessed image.
        This is a simplified version - a full version would use
        advanced image processing or the CNN model output directly.
        
        Args:
            image_array: Preprocessed image array
            
        Returns:
            3x3 grid of color letters (W, R, G, B, O, Y)
        """
        # Convert back to uint8 for processing
        img = ((image_array[0] + 1.0) * 127.5).astype(np.uint8)
        
        # Convert to HSV for better color detection
        img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        
        # Divide into 3x3 grid
        h, w = img_hsv.shape[:2]
        grid_h, grid_w = h // 3, w // 3
        
        colors = []
        color_map = {
            'red': 'R',
            'white': 'W',
            'yellow': 'Y',
            'blue': 'B',
            'green': 'G',
            'orange': 'O'
        }
        
        for i in range(3):
            row = []
            for j in range(3):
                # Extract cell
                y1, y2 = i * grid_h, (i + 1) * grid_h
                x1, x2 = j * grid_w, (j + 1) * grid_w
                cell = img_hsv[y1:y2, x1:x2]
                
                # Get dominant color (simplified - use mean HSV)
                mean_hue = np.mean(cell[:, :, 0])
                detected_color = ImageProcessor._hue_to_color(mean_hue)
                row.append(detected_color)
            
            colors.append(row)
        
        return colors
    
    @staticmethod
    def _hue_to_color(hue: float) -> str:
        """
        Convert HSV hue value to color letter
        
        Args:
            hue: HSV hue value (0-180 in OpenCV)
            
        Returns:
            Color letter (W, R, G, B, O, Y)
        """
        # OpenCV HSV ranges for different colors
        if hue < 10 or hue > 170:
            return 'R'  # Red
        elif 10 <= hue < 25:
            return 'O'  # Orange
        elif 25 <= hue < 40:
            return 'Y'  # Yellow
        elif 40 <= hue < 80:
            return 'G'  # Green
        elif 80 <= hue < 130:
            return 'B'  # Blue
        else:
            return 'W'  # White (or grayish)
