"""
Data loading utilities for Rubik's Cube face dataset
"""
import os
import numpy as np
from pathlib import Path
from typing import Tuple, List
from PIL import Image


class CubeDataLoader:
    """Load and preprocess Rubik's Cube face dataset"""
    
    COLOR_MAP = {
        'W': 0, 'white': 0,
        'R': 1, 'red': 1,
        'G': 2, 'green': 2,
        'B': 3, 'blue': 3,
        'O': 4, 'orange': 4,
        'Y': 5, 'yellow': 5
    }
    
    def __init__(self, dataset_path: str):
        """
        Initialize data loader
        
        Args:
            dataset_path: Path to Kaggle Rubik's Cube dataset
        """
        self.dataset_path = dataset_path
        self.image_paths: List[str] = []
        self.labels: List[int] = []
    
    def load_kaggle_dataset(self, img_size: int = 224) -> Tuple[np.ndarray, np.ndarray]:
        """
        Load images from Kaggle dataset structure
        
        Expected structure:
        dataset/
          - color_name/
            - image1.jpg
            - image2.jpg
            - ...
        
        Args:
            img_size: Target image size
            
        Returns:
            (images, labels) arrays
        """
        images = []
        labels = []
        
        for color_name, color_idx in self.COLOR_MAP.items():
            color_dir = os.path.join(self.dataset_path, color_name)
            if not os.path.exists(color_dir):
                continue
            
            for img_file in os.listdir(color_dir):
                if img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    img_path = os.path.join(color_dir, img_file)
                    try:
                        img = Image.open(img_path).convert('RGB')
                        img = img.resize((img_size, img_size), Image.Resampling.LANCZOS)
                        img_array = np.array(img, dtype=np.float32) / 255.0
                        
                        images.append(img_array)
                        labels.append(color_idx)
                    except Exception as e:
                        print(f"Error loading {img_path}: {e}")
        
        return np.array(images), np.array(labels)
    
    def load_sample_dataset(self, num_samples: int = 100, img_size: int = 224) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate synthetic sample dataset for testing
        
        Args:
            num_samples: Number of samples per color
            img_size: Image size
            
        Returns:
            (images, labels) arrays
        """
        images = []
        labels = []
        
        # Define color RGB values
        color_values = {
            0: (255, 255, 255),  # White
            1: (255, 0, 0),      # Red
            2: (0, 255, 0),      # Green
            3: (0, 0, 255),      # Blue
            4: (255, 165, 0),    # Orange
            5: (255, 255, 0),    # Yellow
        }
        
        for color_idx, rgb in color_values.items():
            for _ in range(num_samples):
                # Create random noisy image with dominant color
                img = np.random.randint(0, 256, (img_size, img_size, 3), dtype=np.uint8)
                
                # Set dominant color in center region
                h1, h2 = img_size // 4, 3 * img_size // 4
                w1, w2 = img_size // 4, 3 * img_size // 4
                img[h1:h2, w1:w2] = np.array(rgb, dtype=np.uint8)
                
                # Add some noise
                noise = np.random.normal(0, 10, img.shape)
                img = np.clip(img.astype(float) + noise, 0, 255).astype(np.uint8)
                
                images.append(img.astype(np.float32) / 255.0)
                labels.append(color_idx)
        
        return np.array(images), np.array(labels)
