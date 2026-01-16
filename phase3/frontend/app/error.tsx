"use client";

import { useEffect } from "react";
import { Button } from "@/components/ui/button";
import { AlertCircle } from "lucide-react";

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Log the error to an error reporting service
    console.error("Application error:", error);
  }, [error]);

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gray-50 dark:bg-gray-900 px-4">
      <div className="text-center">
        <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-red-100 dark:bg-red-900/20">
          <AlertCircle className="h-8 w-8 text-red-600 dark:text-red-400" />
        </div>

        <h2 className="mt-6 text-2xl font-semibold text-gray-900 dark:text-white">
          Something went wrong!
        </h2>
        <p className="mt-2 text-gray-600 dark:text-gray-400">
          We encountered an error while processing your request.
        </p>

        {error.message && (
          <p className="mt-2 text-sm text-gray-500 dark:text-gray-500">
            {error.message}
          </p>
        )}

        <div className="mt-8">
          <Button onClick={() => reset()}>Try again</Button>
        </div>
      </div>
    </div>
  );
}
