import { lazy, Suspense, useState } from 'react'
import ImageUpload from './components/ImageUpload'
import SolutionDisplay from './components/SolutionDisplay'
import { uploadFaceImage, solveCube, resetCube, getCubeState } from './api/client'
import './App.css'

const CubeVisualization = lazy(() => import('./components/CubeVisualization'))

const FACES = [
  { id: 0, name: 'UP (White)' },
  { id: 1, name: 'FRONT (Red)' },
  { id: 2, name: 'RIGHT (Blue)' },
  { id: 3, name: 'BACK (Orange)' },
  { id: 4, name: 'LEFT (Green)' },
  { id: 5, name: 'DOWN (Yellow)' },
]

export default function App() {
  const [uploadedFaces, setUploadedFaces] = useState<{ [key: number]: boolean }>({})
  const [loading, setLoading] = useState(false)
  const [solution, setSolution] = useState<string[] | null>(null)
  const [cubeState, setCubeState] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)

  const handleImageUpload = async (faceId: number, file: File) => {
    try {
      setError(null)
      setLoading(true)
      const result = await uploadFaceImage(file, faceId)
      setUploadedFaces((prev) => ({ ...prev, [faceId]: true }))
      console.log(`Face ${result.face_name} uploaded:`, result.colors)
    } catch (err: any) {
      setError(`Failed to upload face ${faceId}: ${err.message}`)
    } finally {
      setLoading(false)
    }
  }

  const handleSolve = async () => {
    try {
      setError(null)
      setLoading(true)
      const result = await solveCube()
      setSolution(result.moves)
      setCubeState(result.cube_state)
    } catch (err: any) {
      setError(`Failed to solve: ${err.message}`)
    } finally {
      setLoading(false)
    }
  }

  const handleReset = async () => {
    try {
      setError(null)
      await resetCube()
      setUploadedFaces({})
      setSolution(null)
      setCubeState(null)
    } catch (err: any) {
      setError(`Failed to reset: ${err.message}`)
    }
  }

  const allFacesUploaded = Object.keys(uploadedFaces).length === 6

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>🎲 Rubik's Cube Solver</h1>
        <p>Upload 6 face images and get the solution instantly</p>
      </header>

      <main className="app-main">
        {error && <div className="error-box">{error}</div>}

        <section className="upload-section">
          <h2>Step 1: Upload Cube Faces</h2>
          <div className="faces-grid">
            {FACES.map((face) => (
              <ImageUpload
                key={face.id}
                faceId={face.id}
                faceName={face.name}
                isUploaded={uploadedFaces[face.id] || false}
                onUpload={handleImageUpload}
                disabled={loading}
              />
            ))}
          </div>
        </section>

        <section className="action-section">
          <h2>Step 2: Solve</h2>
          <button
            onClick={handleSolve}
            disabled={!allFacesUploaded || loading}
            className="solve-btn"
          >
            {loading ? 'Processing...' : 'Solve Cube'}
          </button>
          <button onClick={handleReset} className="reset-btn">
            Reset
          </button>
        </section>

        {solution && <SolutionDisplay moves={solution} cubeState={cubeState} />}
        {cubeState && (
          <Suspense fallback={<div className="visualization-loading">Loading cube view...</div>}>
            <CubeVisualization cubeState={cubeState} />
          </Suspense>
        )}
      </main>

      <footer className="app-footer">
        <p>Powered by CNN + IDA* Algorithm</p>
      </footer>
    </div>
  )
}
