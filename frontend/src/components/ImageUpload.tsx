import { useRef, useState } from 'react'
import './ImageUpload.css'

interface Props {
  faceId: number
  faceName: string
  isUploaded: boolean
  onUpload: (faceId: number, file: File) => void
  disabled: boolean
}

export default function ImageUpload({
  faceId,
  faceName,
  isUploaded,
  onUpload,
  disabled,
}: Props) {
  const inputRef = useRef<HTMLInputElement>(null)
  const [preview, setPreview] = useState<string | null>(null)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      const reader = new FileReader()
      reader.onload = (event) => {
        setPreview(event.target?.result as string)
      }
      reader.readAsDataURL(file)
      onUpload(faceId, file)
    }
  }

  return (
    <div className={`image-upload ${isUploaded ? 'uploaded' : ''}`}>
      <input
        ref={inputRef}
        type="file"
        accept="image/*"
        onChange={handleChange}
        disabled={disabled}
        hidden
      />
      <div
        className="upload-area"
        onClick={() => inputRef.current?.click()}
        style={{ cursor: disabled ? 'not-allowed' : 'pointer' }}
      >
        {preview ? (
          <img src={preview} alt={faceName} className="preview-img" />
        ) : (
          <div className="placeholder">
            <span className="icon">📷</span>
            <p>{faceName}</p>
            <small>Click to upload</small>
          </div>
        )}
        {isUploaded && <div className="checkmark">✓</div>}
      </div>
    </div>
  )
}
