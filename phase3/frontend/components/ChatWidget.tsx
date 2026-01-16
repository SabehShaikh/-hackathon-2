"use client";

import { useRouter } from "next/navigation";
import { MessageCircle, Sparkles } from "lucide-react";

export function ChatWidget() {
  const router = useRouter();

  return (
    <button
      onClick={() => router.push("/chat")}
      className="fixed bottom-6 right-6 z-50 flex items-center gap-2 px-5 py-4 bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-full shadow-2xl shadow-purple-500/30 hover:shadow-purple-500/50 hover:scale-105 transition-all duration-300 group"
      aria-label="Open AI Chat"
    >
      <div className="relative">
        <MessageCircle className="h-6 w-6" />
        <Sparkles className="absolute -top-1 -right-1 h-3 w-3 text-yellow-300 animate-pulse" />
      </div>
      <span className="font-semibold hidden sm:inline">AI Chat</span>

      {/* Tooltip for mobile */}
      <div className="absolute bottom-full right-0 mb-2 px-3 py-1.5 bg-gray-900 text-white text-sm rounded-lg opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
        Manage tasks with AI
        <div className="absolute top-full right-4 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-gray-900" />
      </div>
    </button>
  );
}
