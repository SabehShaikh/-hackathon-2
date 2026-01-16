"use client";

import { useRouter, usePathname } from "next/navigation";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { clearAuthToken } from "@/lib/api";
import { toast } from "sonner";
import { LogOut, MessageSquare, LayoutDashboard } from "lucide-react";
import { ThemeToggle } from "@/components/ThemeToggle";

interface NavbarProps {
  userEmail?: string;
}

export function Navbar({ userEmail }: NavbarProps) {
  const router = useRouter();
  const pathname = usePathname();

  const isOnChat = pathname === "/chat";
  const isOnDashboard = pathname === "/dashboard";

  const handleLogout = () => {
    // Clear auth token
    clearAuthToken();
    document.cookie = "auth_token=; path=/; max-age=0";

    toast.success("Logged out successfully");
    router.push("/login");
  };

  return (
    <nav className="border-b border-purple-100 bg-white/80 backdrop-blur-lg dark:border-gray-800 dark:bg-gray-900/80">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 justify-between items-center">
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-purple-600 to-blue-600">
              <svg className="h-5 w-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
            </div>
            <h1 className="text-xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
              TodoApp
            </h1>
          </div>

          <div className="flex items-center gap-3">
            {/* Navigation Links */}
            <div className="flex items-center gap-1">
              <Link href="/dashboard">
                <Button
                  variant={isOnDashboard ? "default" : "ghost"}
                  size="sm"
                  className={`flex items-center gap-2 ${
                    isOnDashboard
                      ? "bg-gradient-to-r from-purple-600 to-blue-600 text-white"
                      : "text-gray-600 dark:text-gray-300"
                  }`}
                >
                  <LayoutDashboard className="h-4 w-4" />
                  <span className="hidden sm:inline">Dashboard</span>
                </Button>
              </Link>
              <Link href="/chat">
                <Button
                  variant={isOnChat ? "default" : "ghost"}
                  size="sm"
                  className={`flex items-center gap-2 ${
                    isOnChat
                      ? "bg-gradient-to-r from-purple-600 to-blue-600 text-white"
                      : "text-gray-600 dark:text-gray-300"
                  }`}
                >
                  <MessageSquare className="h-4 w-4" />
                  <span className="hidden sm:inline">AI Chat</span>
                </Button>
              </Link>
            </div>

            {userEmail && (
              <span className="hidden md:inline-flex items-center gap-2 rounded-full bg-purple-50 px-3 py-1.5 text-sm font-medium text-purple-700 dark:bg-purple-900/30 dark:text-purple-300">
                <svg className="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" />
                </svg>
                {userEmail}
              </span>
            )}
            <ThemeToggle />
            <Button
              variant="outline"
              size="sm"
              onClick={handleLogout}
              className="flex items-center gap-2 border-2 hover:bg-red-50 hover:border-red-200 hover:text-red-600 dark:hover:bg-red-950 dark:hover:border-red-800 dark:hover:text-red-400 transition-all"
            >
              <LogOut className="h-4 w-4" />
              <span className="hidden sm:inline">Logout</span>
            </Button>
          </div>
        </div>
      </div>
    </nav>
  );
}
