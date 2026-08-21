import './SolutionDisplay.css'

interface Props {
  moves: string[]
  cubeState: any
}

export default function SolutionDisplay({ moves, cubeState }: Props) {
  return (
    <section className="solution-section">
      <h2>Solution</h2>
      <div className="solution-container">
        <div className="moves-box">
          <h3>Moves ({moves.length} steps)</h3>
          <div className="moves-display">
            {moves.length > 0 ? (
              <p className="moves-sequence">
                {moves.join(' ')}
              </p>
            ) : (
              <p className="already-solved">✓ Cube is already solved!</p>
            )}
          </div>
          <div className="moves-breakdown">
            {moves.map((move, idx) => (
              <span key={idx} className="move-badge">
                {move}
              </span>
            ))}
          </div>
        </div>

        {cubeState && (
          <div className="cube-state-box">
            <h3>Final Cube State</h3>
            <div className="cube-state-grid">
              {Object.entries(cubeState).map(([face, colors]: [string, any]) => (
                <div key={face} className="face-display">
                  <strong>{face}</strong>
                  <div className="face-grid">
                    {colors && colors.map((row: string[], rowIdx: number) => (
                      <div key={rowIdx} className="face-row">
                        {row.map((color: string, colIdx: number) => (
                          <div
                            key={colIdx}
                            className="color-cell"
                            style={{
                              backgroundColor: getColorHex(color),
                            }}
                            title={color}
                          >
                            {color}
                          </div>
                        ))}
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </section>
  )
}

function getColorHex(letter: string): string {
  const colorMap: { [key: string]: string } = {
    W: '#ffffff', // White
    Y: '#ffff00', // Yellow
    R: '#ff0000', // Red
    O: '#ff8800', // Orange
    G: '#00aa00', // Green
    B: '#0000ff', // Blue
  }
  return colorMap[letter] || '#cccccc'
}
