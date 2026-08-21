export interface CubeState {
  U: string[][];
  D: string[][];
  F: string[][];
  B: string[][];
  L: string[][];
  R: string[][];
}

export interface InferenceResult {
  face: string;
  colors: string[][];
}

export interface SolutionResponse {
  moves: string[];
  cube_state: CubeState;
}

export interface UploadResponse {
  face_id: number;
  face_name: string;
  colors: string[][];
  next_face?: string;
}
