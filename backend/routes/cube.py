from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from typing import Optional
from services.image_processor import ImageProcessor
from services.model_inference import ModelInference
from services.cube_solver import CubeSolver

router = APIRouter(prefix="/cube", tags=["cube"])

# Global instances
image_processor = ImageProcessor()
model_inference = ModelInference()
cube_solver = CubeSolver()


@router.post("/upload-face")
async def upload_face(
    image: UploadFile = File(...),
    face_id: int = Form(...)
) -> dict:
    """
    Upload an image for a cube face
    
    Args:
        image: Image file
        face_id: Face index (0-5)
        
    Returns:
        Face colors as 3x3 matrix and metadata
    """
    try:
        if not (0 <= face_id <= 5):
            raise HTTPException(status_code=400, detail="Invalid face_id (must be 0-5)")
        
        # Read file content
        content = await image.read()
        
        # Preprocess image
        img_array = image_processor.preprocess_image(content)
        
        # Extract colors from image
        colors = image_processor.extract_cube_colors(img_array)
        
        # Update cube solver with face
        cube_solver.set_face(face_id, colors)
        
        face_names = ['UP', 'FRONT', 'RIGHT', 'BACK', 'LEFT', 'DOWN']
        
        return {
            'face_id': face_id,
            'face_name': face_names[face_id],
            'colors': colors,
            'success': True
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/solve")
async def solve_cube() -> dict:
    """
    Solve the cube based on uploaded faces
    
    Returns:
        Move sequence and final cube state
    """
    try:
        # Validate cube
        is_valid, msg = cube_solver.is_valid_cube()
        if not is_valid:
            raise HTTPException(status_code=400, detail=f"Invalid cube: {msg}")
        
        # Solve
        moves, success = cube_solver.solve()
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to solve cube")
        
        return {
            'moves': moves,
            'cube_state': cube_solver.get_state(),
            'success': True
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reset")
async def reset_cube() -> dict:
    """Reset cube to initial state"""
    try:
        cube_solver.reset()
        return {'message': 'Cube reset successfully', 'success': True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/state")
async def get_cube_state() -> dict:
    """Get current cube state"""
    try:
        return {
            'cube_state': cube_solver.get_state(),
            'success': True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check() -> dict:
    """Health check endpoint"""
    return {
        'status': 'healthy',
        'model_loaded': model_inference.model_loaded
    }
