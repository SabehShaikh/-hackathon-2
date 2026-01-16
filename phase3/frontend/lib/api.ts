import type { Task, TaskCreateRequest, TaskUpdateRequest, APIError, ChatRequest, ChatResponse } from "./types";

// PRODUCTION FIX: Hardcoded HTTPS URL to prevent mixed content errors on Vercel
// This ensures the app always uses HTTPS in production, even if env var is missing
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "https://sabehshaikh-hackathon2-todo-backend.hf.space";

// Retry configuration
const MAX_RETRIES = 3;
const INITIAL_BACKOFF = 1000; // 1 second
const MAX_BACKOFF = 10000; // 10 seconds

/**
 * Sleep helper for retry delays
 */
function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Generic API client with authentication, error handling, and retry logic
 */
async function fetchAPI<T>(
  endpoint: string,
  options: RequestInit = {},
  retries: number = MAX_RETRIES
): Promise<T> {
  const token = getAuthToken();

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  let lastError: APIError | null = null;
  let backoff = INITIAL_BACKOFF;

  for (let attempt = 1; attempt <= retries; attempt++) {
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

        // Don't retry on client errors (4xx) except for rate limits
        if (response.status >= 400 && response.status < 500 && response.status !== 429) {
          throw error;
        }

        // Throw for retry
        lastError = error;
        throw error;
      }

      return data as T;
    } catch (error) {
      // If it's already an API error, check if we should retry
      if ((error as APIError).status) {
        const apiError = error as APIError;

        // Don't retry client errors (except rate limits)
        if (apiError.status >= 400 && apiError.status < 500 && apiError.status !== 429) {
          throw apiError;
        }

        lastError = apiError;
      } else {
        // Network or other error
        lastError = {
          message: "Network error. Please check your connection.",
          status: 0,
          details: { originalError: error },
        };
      }

      // If this was the last attempt, throw
      if (attempt === retries) {
        throw lastError;
      }

      // Wait before retry with exponential backoff
      console.log(`[API] Attempt ${attempt} failed, retrying in ${backoff}ms...`);
      await sleep(backoff);
      backoff = Math.min(backoff * 2, MAX_BACKOFF);
    }
  }

  // Should never reach here, but just in case
  throw lastError || {
    message: "Request failed after retries",
    status: 0,
    details: {},
  };
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
 * Also clears conversation_id to prevent "Conversation not found" errors
 * when a different user logs in
 */
export function clearAuthToken(): void {
  if (typeof window === "undefined") return;
  localStorage.removeItem("auth_token");
  localStorage.removeItem("user_email");
  localStorage.removeItem("conversation_id");
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
      method: "PATCH",
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

// ============================================================================
// Phase 3: Chat API
// ============================================================================

/**
 * Chat API endpoints for AI-powered task management
 */
export const chatAPI = {
  /**
   * Send a chat message to the AI agent
   * Uses higher retry count for better reliability
   */
  sendMessage: async (data: ChatRequest): Promise<ChatResponse> => {
    return fetchAPI<ChatResponse>("/api/chat", {
      method: "POST",
      body: JSON.stringify(data),
    }, MAX_RETRIES);
  },
};

/**
 * Get conversation ID from localStorage
 */
export function getConversationId(): number | null {
  if (typeof window === "undefined") return null;
  const id = localStorage.getItem("conversation_id");
  return id ? parseInt(id, 10) : null;
}

/**
 * Set conversation ID in localStorage
 */
export function setConversationId(id: number): void {
  if (typeof window === "undefined") return;
  localStorage.setItem("conversation_id", id.toString());
}

/**
 * Clear conversation ID from localStorage (start new conversation)
 */
export function clearConversationId(): void {
  if (typeof window === "undefined") return;
  localStorage.removeItem("conversation_id");
}
