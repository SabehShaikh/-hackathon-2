"use client";

import { useEffect, useState } from "react";
import { Task } from "@/lib/types";
import { TaskItem } from "./TaskItem";
import { EmptyState } from "./EmptyState";
import { Loader2, AlertCircle, ListTodo, CheckCircle2, Clock } from "lucide-react";
import { Button } from "@/components/ui/button";
import { tasksAPI } from "@/lib/api";

type FilterTab = "all" | "pending" | "completed";

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

interface TabButtonProps {
  active: boolean;
  onClick: () => void;
  icon: React.ReactNode;
  label: string;
  count: number;
}

function TabButton({ active, onClick, icon, label, count }: TabButtonProps) {
  return (
    <button
      onClick={onClick}
      className={`flex items-center gap-2 px-4 py-2.5 rounded-xl font-medium transition-all duration-200 ${
        active
          ? "bg-gradient-to-r from-purple-600 to-blue-600 text-white shadow-lg shadow-purple-500/25"
          : "bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700 border border-gray-200 dark:border-gray-700"
      }`}
    >
      {icon}
      <span>{label}</span>
      <span
        className={`ml-1 px-2 py-0.5 rounded-full text-xs font-bold ${
          active
            ? "bg-white/20 text-white"
            : "bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400"
        }`}
      >
        {count}
      </span>
    </button>
  );
}

export function TaskList() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(false);
  const [activeTab, setActiveTab] = useState<FilterTab>("all");

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

  // Calculate counts
  const totalCount = tasks.length;
  const completedCount = tasks.filter((t) => t.completed).length;
  const pendingCount = tasks.filter((t) => !t.completed).length;

  // Filter tasks based on active tab
  const filteredTasks = tasks.filter((task) => {
    if (activeTab === "pending") return !task.completed;
    if (activeTab === "completed") return task.completed;
    return true; // "all"
  });

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

  return (
    <div className="space-y-6">
      {/* Filter Tabs */}
      <div className="flex flex-wrap gap-3">
        <TabButton
          active={activeTab === "all"}
          onClick={() => setActiveTab("all")}
          icon={<ListTodo className="h-4 w-4" />}
          label="All"
          count={totalCount}
        />
        <TabButton
          active={activeTab === "pending"}
          onClick={() => setActiveTab("pending")}
          icon={<Clock className="h-4 w-4" />}
          label="Pending"
          count={pendingCount}
        />
        <TabButton
          active={activeTab === "completed"}
          onClick={() => setActiveTab("completed")}
          icon={<CheckCircle2 className="h-4 w-4" />}
          label="Completed"
          count={completedCount}
        />
      </div>

      {/* Task Stats Summary */}
      <div className="flex flex-wrap gap-4 text-sm">
        <div className="flex items-center gap-2 px-3 py-1.5 bg-purple-50 dark:bg-purple-900/20 rounded-lg">
          <span className="text-purple-600 dark:text-purple-400 font-medium">Total:</span>
          <span className="font-bold text-purple-700 dark:text-purple-300">{totalCount}</span>
        </div>
        <div className="flex items-center gap-2 px-3 py-1.5 bg-green-50 dark:bg-green-900/20 rounded-lg">
          <span className="text-green-600 dark:text-green-400 font-medium">Completed:</span>
          <span className="font-bold text-green-700 dark:text-green-300">{completedCount}</span>
        </div>
        <div className="flex items-center gap-2 px-3 py-1.5 bg-orange-50 dark:bg-orange-900/20 rounded-lg">
          <span className="text-orange-600 dark:text-orange-400 font-medium">Pending:</span>
          <span className="font-bold text-orange-700 dark:text-orange-300">{pendingCount}</span>
        </div>
      </div>

      {/* Task List */}
      {filteredTasks.length === 0 ? (
        <EmptyState />
      ) : (
        <div className="grid gap-4 sm:grid-cols-1 lg:grid-cols-2">
          {filteredTasks.map((task) => (
            <TaskItem key={task.id} task={task} />
          ))}
        </div>
      )}
    </div>
  );
}
