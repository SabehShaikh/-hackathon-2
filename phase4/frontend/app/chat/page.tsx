"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Navbar } from "@/components/Navbar";
import { ChatInterface } from "@/components/chat/ChatInterface";
import { getUserEmail } from "@/lib/api";

export default function ChatPage() {
  const router = useRouter();
  const [userEmail, setUserEmail] = useState<string>("");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check authentication
    const token = localStorage.getItem("auth_token");
    const email = getUserEmail();

    if (!token) {
      router.push("/login");
      return;
    }

    setUserEmail(email || "");
    setIsLoading(false);
  }, [router]);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50 dark:from-gray-900 dark:via-gray-900 dark:to-gray-800 flex items-center justify-center">
        <div className="animate-pulse flex flex-col items-center gap-2">
          <div className="h-8 w-8 rounded-full bg-purple-200 dark:bg-purple-800" />
          <div className="h-4 w-24 rounded bg-purple-200 dark:bg-purple-800" />
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50 dark:from-gray-900 dark:via-gray-900 dark:to-gray-800">
      <Navbar userEmail={userEmail} />
      <main className="mx-auto max-w-4xl px-4 py-6">
        <ChatInterface />
      </main>
    </div>
  );
}
