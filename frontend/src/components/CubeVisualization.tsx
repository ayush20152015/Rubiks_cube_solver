import { OrbitControls } from '@react-three/drei'
import { Canvas } from '@react-three/fiber'
import { useMemo } from 'react'
import type { CubeState } from '../types'
import './CubeVisualization.css'

interface Props {
  cubeState: CubeState
}

const COLORS: Record<string, string> = {
  W: '#f8fafc',
  Y: '#facc15',
  R: '#ef4444',
  O: '#f97316',
  G: '#22c55e',
  B: '#2563eb',
}

function stickerColor(face: string[][], row: number, column: number) {
  return COLORS[face[row]?.[column] ?? ''] ?? '#111827'
}

function Cubies({ cubeState }: Props) {
  const cubies = useMemo(() => {
    return Array.from({ length: 27 }, (_, index) => {
      const x = (index % 3) - 1
      const y = 1 - Math.floor(index / 9)
      const z = 1 - Math.floor((index % 9) / 3)
      const row = 1 - y
      const column = x + 1
      const depthRow = 1 - z
      const depthColumn = z + 1

      return {
        key: `${x}-${y}-${z}`,
        position: [x * 1.05, y * 1.05, z * 1.05] as [number, number, number],
        colors: [
          x === 1 ? stickerColor(cubeState.R, row, depthRow) : '#111827',
          x === -1 ? stickerColor(cubeState.L, row, depthColumn) : '#111827',
          y === 1 ? stickerColor(cubeState.U, depthRow, column) : '#111827',
          y === -1 ? stickerColor(cubeState.D, depthColumn, column) : '#111827',
          z === 1 ? stickerColor(cubeState.F, row, column) : '#111827',
          z === -1 ? stickerColor(cubeState.B, row, 2 - column) : '#111827',
        ],
      }
    })
  }, [cubeState])

  return cubies.map((cubie) => (
    <mesh key={cubie.key} position={cubie.position} castShadow receiveShadow>
      <boxGeometry args={[0.96, 0.96, 0.96]} />
      {cubie.colors.map((color, index) => (
        <meshStandardMaterial key={index} attach={`material-${index}`} color={color} roughness={0.42} />
      ))}
    </mesh>
  ))
}

export default function CubeVisualization({ cubeState }: Props) {
  return (
    <section className="cube-visualization" aria-label="Interactive three dimensional cube">
      <h3>Cube State</h3>
      <div className="cube-canvas">
        <Canvas camera={{ position: [5, 4, 6], fov: 42 }} shadows>
          <color attach="background" args={['#e8f0ee']} />
          <ambientLight intensity={1.5} />
          <directionalLight position={[5, 7, 4]} intensity={2.2} castShadow />
          <Cubies cubeState={cubeState} />
          <OrbitControls enablePan={false} minDistance={5} maxDistance={9} />
        </Canvas>
      </div>
    </section>
  )
}