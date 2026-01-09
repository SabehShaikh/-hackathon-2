"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { CheckCircle2, Zap, Shield, Sparkles, Github, Linkedin } from "lucide-react";
import { ThemeToggle } from "@/components/ThemeToggle";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

export default function LandingPage() {
  const router = useRouter();
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    // Check if user is authenticated
    if (typeof window !== "undefined") {
      const token = document.cookie.includes("auth_token");
      if (token) {
        setIsAuthenticated(true);
        router.push("/dashboard");
      }
    }
  }, [router]);

  if (isAuthenticated) {
    return null; // Will redirect to dashboard
  }

  const features = [
    {
      icon: <Zap className="h-6 w-6" />,
      title: "Lightning Fast",
      description: "Create, update, and manage tasks in milliseconds with our optimized interface.",
    },
    {
      icon: <CheckCircle2 className="h-6 w-6" />,
      title: "Simple & Intuitive",
      description: "Clean, modern design that gets out of your way and lets you focus on what matters.",
    },
    {
      icon: <Shield className="h-6 w-6" />,
      title: "Secure & Private",
      description: "Your data is encrypted and protected with industry-standard security measures.",
    },
    {
      icon: <Sparkles className="h-6 w-6" />,
      title: "Beautiful Design",
      description: "Gorgeous dark mode support and smooth animations that make task management enjoyable.",
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50 dark:from-gray-900 dark:via-gray-900 dark:to-gray-800">
      {/* Navigation */}
      <nav className="border-b border-purple-100 bg-white/80 backdrop-blur-lg dark:border-gray-800 dark:bg-gray-900/80">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-purple-600 to-blue-600">
                <CheckCircle2 className="h-5 w-5 text-white" />
              </div>
              <h1 className="text-xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
                TodoApp
              </h1>
            </div>
            <div className="flex items-center gap-3">
              <ThemeToggle />
              <Link href="/login">
                <Button variant="ghost" size="sm">
                  Sign In
                </Button>
              </Link>
              <Link href="/signup">
                <Button size="sm" className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700">
                  Get Started
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative overflow-hidden px-4 py-20 sm:px-6 sm:py-32 lg:px-8">
        <div className="absolute inset-0 -z-10 bg-[radial-gradient(45rem_50rem_at_top,theme(colors.purple.100),white)] opacity-20 dark:bg-[radial-gradient(45rem_50rem_at_top,theme(colors.purple.900),transparent)]" />

        <div className="mx-auto max-w-4xl text-center">
          <div className="mb-8 inline-flex items-center gap-2 rounded-full border border-purple-200 bg-purple-50 px-4 py-2 text-sm font-medium text-purple-700 dark:border-purple-900 dark:bg-purple-900/30 dark:text-purple-300">
            <Sparkles className="h-4 w-4" />
            Simple. Powerful. Beautiful.
          </div>

          <h1 className="mb-6 text-5xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-6xl lg:text-7xl">
            Organize Your Life,{" "}
            <span className="bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
              One Task at a Time
            </span>
          </h1>

          <p className="mx-auto mb-10 max-w-2xl text-lg leading-8 text-gray-600 dark:text-gray-300">
            Experience the most elegant way to manage your tasks. Clean interface,
            powerful features, and lightning-fast performance.
          </p>

          <div className="flex flex-col items-center justify-center gap-4 sm:flex-row">
            <Link href="/signup">
              <Button size="lg" className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 shadow-lg shadow-purple-500/50 dark:shadow-purple-900/50 px-8 py-6 text-lg">
                Get Started Free
              </Button>
            </Link>
            <Link href="/login">
              <Button variant="outline" size="lg" className="px-8 py-6 text-lg border-2">
                Sign In
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="px-4 py-20 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-7xl">
          <div className="mb-16 text-center">
            <h2 className="mb-4 text-3xl font-bold text-gray-900 dark:text-white sm:text-4xl">
              Everything you need to stay organized
            </h2>
            <p className="mx-auto max-w-2xl text-lg text-gray-600 dark:text-gray-300">
              Powerful features wrapped in a beautiful, intuitive interface
            </p>
          </div>

          <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
            {features.map((feature, index) => (
              <div
                key={index}
                className="group relative overflow-hidden rounded-2xl border border-gray-200 bg-white p-8 shadow-sm transition-all hover:shadow-xl hover:shadow-purple-500/10 dark:border-gray-800 dark:bg-gray-900/50"
              >
                <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-purple-600 to-blue-600 text-white shadow-lg">
                  {feature.icon}
                </div>
                <h3 className="mb-2 text-xl font-semibold text-gray-900 dark:text-white">
                  {feature.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-400">
                  {feature.description}
                </p>
                <div className="absolute inset-0 -z-10 bg-gradient-to-br from-purple-500/0 to-blue-500/0 opacity-0 transition-opacity group-hover:opacity-5" />
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="px-4 py-20 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-4xl">
          <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-purple-600 to-blue-600 px-8 py-16 shadow-2xl sm:px-16">
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,theme(colors.purple.400),transparent)] opacity-40" />
            <div className="relative text-center">
              <h2 className="mb-4 text-3xl font-bold text-white sm:text-4xl">
                Ready to get started?
              </h2>
              <p className="mb-8 text-lg text-purple-100">
                Join thousands of users who have transformed their productivity
              </p>
              <Link href="/signup">
                <Button size="lg" variant="secondary" className="bg-white text-purple-600 hover:bg-gray-100 px-8 py-6 text-lg shadow-xl">
                  Create Your Free Account
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-gray-200 bg-white dark:border-gray-800 dark:bg-gray-900">
        <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
          <div className="flex flex-col items-center gap-4">
            <p className="text-center text-sm text-gray-600 dark:text-gray-400">
              © 2026 TodoApp. Built with Next.js and FastAPI.
            </p>
            <div className="flex items-center gap-3">
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Made by <span className="font-semibold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">Sabeh Shaikh</span>
              </p>
              <div className="flex gap-2">
                <a
                  href="https://github.com/SabehShaikh"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="rounded-lg p-2 text-gray-600 transition-colors hover:bg-gray-100 hover:text-gray-900 dark:text-gray-400 dark:hover:bg-gray-800 dark:hover:text-gray-100"
                  aria-label="GitHub"
                >
                  <Github className="h-5 w-5" />
                </a>
                <a
                  href="https://www.linkedin.com/in/sabeh-shaikh/"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="rounded-lg p-2 text-gray-600 transition-colors hover:bg-gray-100 hover:text-gray-900 dark:text-gray-400 dark:hover:bg-gray-800 dark:hover:text-gray-100"
                  aria-label="LinkedIn"
                >
                  <Linkedin className="h-5 w-5" />
                </a>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
