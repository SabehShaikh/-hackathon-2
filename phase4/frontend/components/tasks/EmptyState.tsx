import { CheckCircle2 } from "lucide-react";

export function EmptyState() {
  return (
    <div className="flex flex-col items-center justify-center py-16 text-center">
      <div className="rounded-full bg-gradient-to-br from-purple-100 to-blue-100 p-6 dark:from-purple-900/30 dark:to-blue-900/30">
        <CheckCircle2 className="h-16 w-16 text-purple-600 dark:text-purple-400" />
      </div>
      <h3 className="mt-6 text-xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
        No tasks yet
      </h3>
      <p className="mt-3 max-w-sm text-sm text-gray-600 dark:text-gray-400">
        Get started by creating your first task. Stay organized and productive!
      </p>
    </div>
  );
}
