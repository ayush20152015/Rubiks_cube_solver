"""
Tests for cube solving logic
"""
from services.cube_solver import CubeSolver


def test_cube_initialization():
    """Test cube initializes correctly"""
    cube = CubeSolver()
    assert cube is not None
    assert len(cube.face_names) == 6


def test_cube_reset():
    """Test cube reset"""
    cube = CubeSolver()
    original_state = cube.get_state()
    
    # Modify state
    cube.cube_state['U'] = [['R', 'R', 'R'], ['R', 'R', 'R'], ['R', 'R', 'R']]
    
    # Reset
    cube.reset()
    reset_state = cube.get_state()
    
    # Should be back to original
    assert reset_state['U'][0][0] == original_state['U'][0][0]


def test_cube_validation():
    """Test cube validation"""
    cube = CubeSolver()
    is_valid, msg = cube.is_valid_cube()
    assert is_valid is True


def test_invalid_cube():
    """Test invalid cube detection"""
    cube = CubeSolver()
    # Add extra red sticker
    cube.cube_state['U'][0][0] = 'R'
    
    is_valid, msg = cube.is_valid_cube()
    assert is_valid is False
    assert 'appears' in msg.lower()


def test_set_face():
    """Test setting face colors"""
    cube = CubeSolver()
    colors = [['W', 'R', 'G'], ['B', 'O', 'Y'], ['W', 'R', 'G']]
    
    result = cube.set_face(0, colors)
    assert result is True
    assert cube.get_face(0) == colors


def test_invalid_face_id():
    """Test invalid face ID handling"""
    cube = CubeSolver()
    colors = [['W'] * 3 for _ in range(3)]
    
    result = cube.set_face(10, colors)
    assert result is False


def test_solved_cube_needs_no_moves():
    cube = CubeSolver()

    moves, success = cube.solve()

    assert success is True
    assert moves == []
