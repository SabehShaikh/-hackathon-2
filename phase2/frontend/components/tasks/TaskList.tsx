"use client";

import { useEffect, useState } from "react";
import { Task } from "@/lib/types";
import { TaskItem } from "./TaskItem";
import { EmptyState } from "./EmptyState";
import { Loader2, AlertCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { tasksAPI } from "@/lib/api";

function LoadingSkeleton() {
  return (
    <div className="space-y-4">
      {[1, 2, 3].map((i) => (
        <div
          key={i}
          className="h-24 animate-pulse rounded-lg bg-gradient-to-r from-gray-200 to-gray-300 dark:from-gray-800 dark:to-gray-700"
        />
      ))}
    </div>
  );
}

function ErrorState({ onRetry }: { onRetry?: () => void }) {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center">
      <div className="rounded-full bg-gradient-to-br from-red-100 to-red-200 p-6 dark:from-red-900/30 dark:to-red-800/30">
        <AlertCircle className="h-12 w-12 text-red-600 dark:text-red-400" />
      </div>
      <h3 className="mt-4 text-lg font-semibold text-gray-900 dark:text-white">
        Failed to load tasks
      </h3>
      <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
        There was an error loading your tasks. Please try again.
      </p>
      {onRetry && (
        <Button
          onClick={onRetry}
          variant="outline"
          className="mt-4 border-2 hover:bg-purple-50 hover:border-purple-200 dark:hover:bg-purple-950"
        >
          Retry
        </Button>
      )}
    </div>
  );
}

export function TaskList() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(false);

  const fetchTasks = async () => {
    setIsLoading(true);
    setError(false);

    try {
      const data = await tasksAPI.list();
      setTasks(data);
    } catch (err) {
      console.error("Error fetching tasks:", err);
      setError(true);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();

    // Listen for task updates from other components
    const handleTaskUpdate = () => {
      fetchTasks();
    };

    window.addEventListener("taskUpdated", handleTaskUpdate);
    return () => {
      window.removeEventListener("taskUpdated", handleTaskUpdate);
    };
  }, []);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="h-8 w-8 animate-spin text-purple-600 dark:text-purple-400" />
      </div>
    );
  }

  if (error) {
    return <ErrorState onRetry={fetchTasks} />;
  }

  if (tasks.length === 0) {
    return <EmptyState />;
  }

  return (
    <div className="grid gap-4 sm:grid-cols-1 lg:grid-cols-2">
      {tasks.map((task) => (
        <TaskItem key={task.id} task={task} />
      ))}
    </div>
  );
}
