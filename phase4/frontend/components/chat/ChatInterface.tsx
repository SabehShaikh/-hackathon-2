"use client";

import { useState, useRef, useEffect, useCallback } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { chatAPI, getConversationId, setConversationId, clearConversationId } from "@/lib/api";
import type { ChatMessage, APIError } from "@/lib/types";
import { toast } from "sonner";
import { Send, RefreshCw, MessageSquare, Loader2, Bot, User, AlertCircle } from "lucide-react";

// Suggestions for new users - showcasing multi-task and flexible NLP
const SUGGESTIONS = [
  { text: "Add buy groceries", description: "Add a task" },
  { text: "Show my tasks", description: "List all tasks" },
  { text: "Add call mom and add pay bills", description: "Add multiple tasks" },
  { text: "Complete the first task", description: "Mark done by position" },
  { text: "Remind me to exercise tomorrow", description: "Natural language" },
];

export function ChatInterface() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setLocalConversationId] = useState<number | null>(null);
  const [errorState, setErrorState] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Load conversation ID from localStorage on mount
  useEffect(() => {
    const savedId = getConversationId();
    if (savedId) {
      setLocalConversationId(savedId);
    }
  }, []);

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Focus input on mount
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleSubmit = useCallback(async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput("");
    setIsLoading(true);
    setErrorState(null);

    // Add user message to UI immediately
    setMessages((prev) => [
      ...prev,
      { role: "user", content: userMessage, timestamp: new Date().toISOString() },
    ]);

    try {
      const response = await chatAPI.sendMessage({
        conversation_id: conversationId ?? undefined,
        message: userMessage,
      });

      // Save conversation ID for persistence
      if (response.conversation_id) {
        setLocalConversationId(response.conversation_id);
        setConversationId(response.conversation_id);
      }

      // Add assistant response
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: response.response, timestamp: new Date().toISOString() },
      ]);
    } catch (error) {
      const apiError = error as APIError;
      console.error("Chat error:", apiError);

      // Handle stale conversation - clear and suggest retry
      if (apiError.status === 404 && conversationId) {
        clearConversationId();
        setLocalConversationId(null);
        // Remove the user message we just added
        setMessages((prev) => prev.slice(0, -1));
        setIsLoading(false);
        toast.info("Starting fresh conversation...");
        // Retry without conversation_id
        setInput(userMessage);
        inputRef.current?.focus();
        return;
      }

      // Determine user-friendly error message
      let errorMessage: string;

      if (apiError.status === 401) {
        errorMessage = "Your session has expired. Please log in again.";
        toast.error("Session expired");
      } else if (apiError.status === 429) {
        errorMessage = "Too many requests. Please wait a moment and try again.";
      } else if (apiError.status === 0) {
        errorMessage = "Unable to connect to the server. Please check your internet connection.";
      } else if (apiError.message) {
        // Use the error message from the server (which is now specific)
        errorMessage = apiError.message;
      } else {
        errorMessage = "Something went wrong. Please try again.";
      }

      // Show error message in chat
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: errorMessage,
          timestamp: new Date().toISOString(),
          isError: true,
        },
      ]);

      setErrorState(errorMessage);
    } finally {
      setIsLoading(false);
      // Re-focus input after response
      inputRef.current?.focus();
    }
  }, [input, isLoading, conversationId]);

  const handleNewConversation = useCallback(() => {
    clearConversationId();
    setLocalConversationId(null);
    setMessages([]);
    setErrorState(null);
    toast.success("Started new conversation");
    inputRef.current?.focus();
  }, []);

  const handleSuggestionClick = useCallback((suggestion: string) => {
    setInput(suggestion);
    inputRef.current?.focus();
  }, []);

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)] bg-white dark:bg-gray-900 rounded-xl shadow-lg border border-purple-100 dark:border-gray-800">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-purple-100 dark:border-gray-800">
        <div className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-purple-600 to-blue-600">
            <MessageSquare className="h-5 w-5 text-white" />
          </div>
          <div>
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white">AI Task Assistant</h2>
            <p className="text-xs text-gray-500 dark:text-gray-400">
              Manage tasks with natural language
            </p>
          </div>
        </div>
        <Button
          variant="outline"
          size="sm"
          onClick={handleNewConversation}
          className="flex items-center gap-2"
        >
          <RefreshCw className="h-4 w-4" />
          New Chat
        </Button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center">
            <div className="flex h-16 w-16 items-center justify-center rounded-full bg-gradient-to-br from-purple-100 to-blue-100 dark:from-purple-900/30 dark:to-blue-900/30 mb-4">
              <Bot className="h-8 w-8 text-purple-600 dark:text-purple-400" />
            </div>
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
              Hi! I&apos;m your task assistant
            </h3>
            <p className="text-sm text-gray-500 dark:text-gray-400 max-w-sm mb-4">
              I can help you add, list, complete, update, and delete tasks using natural language.
              Try these examples:
            </p>
            <div className="flex flex-wrap justify-center gap-2 max-w-md">
              {SUGGESTIONS.map((suggestion, index) => (
                <SuggestionChip
                  key={index}
                  onClick={() => handleSuggestionClick(suggestion.text)}
                  title={suggestion.description}
                >
                  {suggestion.text}
                </SuggestionChip>
              ))}
            </div>
          </div>
        ) : (
          messages.map((message, index) => (
            <ChatBubble key={index} message={message} />
          ))
        )}
        {isLoading && (
          <div className="flex items-start gap-2">
            <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-gray-100 to-gray-200 dark:from-gray-700 dark:to-gray-800">
              <Bot className="h-4 w-4 text-gray-600 dark:text-gray-300" />
            </div>
            <div className="rounded-2xl px-4 py-3 bg-gray-100 dark:bg-gray-800 border-l-2 border-purple-500">
              <div className="flex items-center gap-1">
                <span className="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                <span className="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                <span className="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Error banner */}
      {errorState && (
        <div className="mx-4 mb-2 p-2 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg flex items-center gap-2">
          <AlertCircle className="h-4 w-4 text-red-500" />
          <span className="text-sm text-red-700 dark:text-red-300 flex-1">{errorState}</span>
          <button
            onClick={() => setErrorState(null)}
            className="text-red-500 hover:text-red-700 text-sm"
          >
            Dismiss
          </button>
        </div>
      )}

      {/* Input */}
      <form onSubmit={handleSubmit} className="p-4 border-t border-purple-100 dark:border-gray-800 bg-gray-50/50 dark:bg-gray-800/50">
        <div className="flex gap-2">
          <Input
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type a message... (e.g., 'Add buy milk' or 'Show my tasks')"
            disabled={isLoading}
            className="flex-1 focus:ring-2 focus:ring-purple-500/20 focus:border-purple-500 transition-all"
          />
          <Button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 shadow-lg shadow-purple-500/25 hover:shadow-purple-500/40 transition-all hover:scale-105 active:scale-95"
          >
            {isLoading ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Send className="h-4 w-4" />
            )}
          </Button>
        </div>
        <p className="text-xs text-gray-400 mt-2">
          Tip: Try &quot;Add X and add Y&quot; for multiple tasks, or &quot;Complete the first task&quot;
        </p>
      </form>
    </div>
  );
}

interface ChatMessageExtended extends ChatMessage {
  isError?: boolean;
}

function ChatBubble({ message }: { message: ChatMessageExtended }) {
  const isUser = message.role === "user";
  const isError = message.isError;

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`flex items-start gap-2 max-w-[80%] ${
          isUser ? "flex-row-reverse" : "flex-row"
        }`}
      >
        <div
          className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-full ${
            isUser
              ? "bg-gradient-to-br from-purple-600 to-blue-600"
              : isError
              ? "bg-gradient-to-br from-red-100 to-red-200 dark:from-red-900 dark:to-red-800"
              : "bg-gradient-to-br from-gray-100 to-gray-200 dark:from-gray-700 dark:to-gray-800"
          }`}
        >
          {isUser ? (
            <User className="h-4 w-4 text-white" />
          ) : isError ? (
            <AlertCircle className="h-4 w-4 text-red-600 dark:text-red-300" />
          ) : (
            <Bot className="h-4 w-4 text-gray-600 dark:text-gray-300" />
          )}
        </div>
        <div
          className={`rounded-2xl px-4 py-2 shadow-sm ${
            isUser
              ? "bg-gradient-to-r from-purple-600 to-blue-600 text-white shadow-purple-500/20"
              : isError
              ? "bg-red-50 dark:bg-red-900/30 text-red-700 dark:text-red-300 border border-red-200 dark:border-red-800"
              : "bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-white border-l-2 border-purple-500"
          }`}
        >
          <p className="text-sm whitespace-pre-wrap">{message.content}</p>
        </div>
      </div>
    </div>
  );
}

function SuggestionChip({
  children,
  onClick,
  title,
}: {
  children: React.ReactNode;
  onClick: () => void;
  title?: string;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      title={title}
      className="px-3 py-1.5 text-sm rounded-full bg-purple-50 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 hover:bg-purple-100 dark:hover:bg-purple-900/50 transition-colors"
    >
      {children}
    </button>
  );
}
