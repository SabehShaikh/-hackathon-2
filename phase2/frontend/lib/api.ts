import type { Task, TaskCreateRequest, TaskUpdateRequest, APIError } from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Generic API client with authentication and error handling
 */
async function fetchAPI<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getAuthToken();

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers,
    });

    // Handle different response statuses
    if (response.status === 204) {
      return {} as T; // No content
    }

    const data = await response.json();

    if (!response.ok) {
      const error: APIError = {
        message: data.detail || data.message || "An error occurred",
        status: response.status,
        details: data,
      };
      throw error;
    }

    return data as T;
  } catch (error) {
    if ((error as APIError).status) {
      throw error; // Re-throw API errors
    }

    // Network or other errors
    const apiError: APIError = {
      message: "Network error. Please check your connection.",
      status: 0,
      details: { originalError: error },
    };
    throw apiError;
  }
}

/**
 * Get authentication token from localStorage
 */
function getAuthToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("auth_token");
}

/**
 * Set authentication token in localStorage
 */
export function setAuthToken(token: string): void {
  if (typeof window === "undefined") return;
  localStorage.setItem("auth_token", token);
}

/**
 * Remove authentication token from localStorage
 */
export function clearAuthToken(): void {
  if (typeof window === "undefined") return;
  localStorage.removeItem("auth_token");
  localStorage.removeItem("user_email");
}

/**
 * Set user email in localStorage
 */
export function setUserEmail(email: string): void {
  if (typeof window === "undefined") return;
  localStorage.setItem("user_email", email);
}

/**
 * Get user email from localStorage
 */
export function getUserEmail(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("user_email");
}

/**
 * Task API endpoints
 */
export const tasksAPI = {
  /**
   * List all tasks for authenticated user
   */
  list: async (): Promise<Task[]> => {
    return fetchAPI<Task[]>("/api/tasks");
  },

  /**
   * Get a single task by ID
   */
  get: async (id: number): Promise<Task> => {
    return fetchAPI<Task>(`/api/tasks/${id}`);
  },

  /**
   * Create a new task
   */
  create: async (data: TaskCreateRequest): Promise<Task> => {
    return fetchAPI<Task>("/api/tasks", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  /**
   * Update an existing task
   */
  update: async (id: number, data: TaskUpdateRequest): Promise<Task> => {
    return fetchAPI<Task>(`/api/tasks/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    });
  },

  /**
   * Toggle task completion status
   */
  toggleComplete: async (id: number): Promise<Task> => {
    console.log(`[API] Toggling task ${id} completion status`);
    try {
      const result = await fetchAPI<Task>(`/api/tasks/${id}/complete`, {
        method: "PATCH",
      });
      console.log(`[API] Toggle successful:`, result);
      return result;
    } catch (error) {
      console.error(`[API] Toggle failed:`, error);
      throw error;
    }
  },

  /**
   * Delete a task
   */
  delete: async (id: number): Promise<void> => {
    return fetchAPI<void>(`/api/tasks/${id}`, {
      method: "DELETE",
    });
  },
};

/**
 * Health check endpoint (no auth required)
 */
export async function checkHealth(): Promise<{ status: string }> {
  return fetchAPI<{ status: string }>("/api/health");
}
