// Type definitions for Todo Frontend Application

export interface User {
  id: string;
  email: string;
  createdAt: string;
}

export interface Task {
  id: number;
  user_id: string;
  title: string;
  description: string | null;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export interface Session {
  user: User;
  token: string;
  expiresAt: string;
}

export interface APIError {
  message: string;
  status: number;
  details?: Record<string, unknown>;
}

// Request/Response Models
export interface TaskCreateRequest {
  title: string;
  description?: string;
}

export interface TaskUpdateRequest {
  title?: string;
  description?: string;
}

export interface SignupRequest {
  email: string;
  password: string;
  confirmPassword: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface AuthResponse {
  user: User;
  token: string;
  expiresAt: string;
}

export interface TaskListResponse {
  tasks: Task[];
}

export interface HealthResponse {
  status: string;
  timestamp?: string;
}
