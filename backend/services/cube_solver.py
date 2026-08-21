from copy import deepcopy
from typing import Dict, List, Tuple
from collections import defaultdict

import kociemba


class CubeSolver:
    """
    Solve Rubik's cube from face color states
    
    Face order (standard):
    - UP (U)     - White
    - DOWN (D)   - Yellow
    - FRONT (F)  - Red
    - BACK (B)   - Orange
    - LEFT (L)   - Green
    - RIGHT (R)  - Blue
    """
    
    def __init__(self):
        # Store uploaded face colors
        # Key: face name (U, D, F, B, L, R)
        # Value: 3x3 grid of color letters
        self.cube_state: Dict[str, List[List[str]]] = {
            'U': [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']],
            'D': [['Y', 'Y', 'Y'], ['Y', 'Y', 'Y'], ['Y', 'Y', 'Y']],
            'F': [['R', 'R', 'R'], ['R', 'R', 'R'], ['R', 'R', 'R']],
            'B': [['O', 'O', 'O'], ['O', 'O', 'O'], ['O', 'O', 'O']],
            'L': [['G', 'G', 'G'], ['G', 'G', 'G'], ['G', 'G', 'G']],
            'R': [['B', 'B', 'B'], ['B', 'B', 'B'], ['B', 'B', 'B']],
        }
        
        # Face order for input (0=U, 1=F, 2=R, 3=B, 4=L, 5=D)
        self.face_names = ['U', 'F', 'R', 'B', 'L', 'D']
        self.face_labels = ['UP (White)', 'FRONT (Red)', 'RIGHT (Blue)', 
                           'BACK (Orange)', 'LEFT (Green)', 'DOWN (Yellow)']
    
    def set_face(self, face_id: int, colors: List[List[str]]) -> bool:
        """
        Set colors for a specific face
        
        Args:
            face_id: Index 0-5 (U, F, R, B, L, D)
            colors: 3x3 grid of color letters
            
        Returns:
            Success status
        """
        if face_id < 0 or face_id >= 6:
            return False
        
        face_name = self.face_names[face_id]
        self.cube_state[face_name] = colors
        return True
    
    def get_face(self, face_id: int) -> List[List[str]]:
        """Get colors for a specific face"""
        if face_id < 0 or face_id >= 6:
            return []
        
        return self.cube_state[self.face_names[face_id]]
    
    def is_valid_cube(self) -> Tuple[bool, str]:
        """
        Validate cube state
        
        Returns:
            (is_valid, error_message)
        """
        # Count each color
        color_count = defaultdict(int)
        for face in self.cube_state.values():
            for row in face:
                for color in row:
                    color_count[color] += 1
        
        # Each color should appear exactly 9 times
        valid_colors = {'W', 'Y', 'R', 'O', 'G', 'B'}
        for color in valid_colors:
            if color_count[color] != 9:
                return False, f"Color {color} appears {color_count[color]} times, expected 9"
        
        # Check for unknown colors
        for color in color_count:
            if color not in valid_colors:
                return False, f"Unknown color: {color}"
        
        return True, "Cube is valid"
    
    def solve(self) -> Tuple[List[str], bool]:
        """
        Solve the cube with Kociemba's native two-phase algorithm.
        
        Returns:
            (list of moves, success)
        """
        is_valid, error_msg = self.is_valid_cube()
        if not is_valid:
            return [], False
        
        if self._is_solved():
            return [], True

        try:
            solution = kociemba.solve(self._to_kociemba_facelets())
        except ValueError:
            return [], False

        return solution.split() if solution else [], True

    def _to_kociemba_facelets(self) -> str:
        """Convert detected sticker colors to Kociemba's URFDLB face order."""
        face_order = "URFDLB"
        color_to_face = {
            self.cube_state[face][1][1]: face
            for face in face_order
        }

        try:
            return "".join(
                color_to_face[color]
                for face in face_order
                for row in self.cube_state[face]
                for color in row
            )
        except KeyError as error:
            raise ValueError(f"Unrecognized sticker color: {error.args[0]}") from error

    def _is_solved(self) -> bool:
        return all(
            color == face[0][0]
            for face in self.cube_state.values()
            for row in face
            for color in row
        )
    
    def reset(self):
        """Reset cube to solved state"""
        self.cube_state = {
            'U': [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']],
            'D': [['Y', 'Y', 'Y'], ['Y', 'Y', 'Y'], ['Y', 'Y', 'Y']],
            'F': [['R', 'R', 'R'], ['R', 'R', 'R'], ['R', 'R', 'R']],
            'B': [['O', 'O', 'O'], ['O', 'O', 'O'], ['O', 'O', 'O']],
            'L': [['G', 'G', 'G'], ['G', 'G', 'G'], ['G', 'G', 'G']],
            'R': [['B', 'B', 'B'], ['B', 'B', 'B'], ['B', 'B', 'B']],
        }
    
    def get_state(self) -> Dict:
        """Get current cube state"""
        return deepcopy(self.cube_state)
