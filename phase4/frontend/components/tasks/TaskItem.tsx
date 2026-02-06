"use client";

import { useState } from "react";
import { Task } from "@/lib/types";
import { Card, CardContent } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { Button } from "@/components/ui/button";
import { formatDistanceToNow } from "date-fns";
import { useOptimisticToggle } from "@/hooks/useOptimisticToggle";
import { tasksAPI } from "@/lib/api";
import { toast } from "sonner";
import { Pencil, Trash2, CheckCircle2 } from "lucide-react";
import { EditTaskDialog } from "./EditTaskDialog";
import { DeleteConfirmDialog } from "./DeleteConfirmDialog";

interface TaskItemProps {
  task: Task;
}

export function TaskItem({ task }: TaskItemProps) {
  const { value: completed, isPending, toggle } = useOptimisticToggle(task.completed);
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);

  // Format the date
  // Backend returns UTC timestamps without 'Z' suffix, so we need to add it
  // to ensure JavaScript parses them as UTC, not local time
  const createdAtStr = task.createdAt || '';
  const created_at_utc = createdAtStr.endsWith('Z') ? createdAtStr : `${createdAtStr}Z`;

  const formattedDate = createdAtStr
    ? formatDistanceToNow(new Date(created_at_utc), { addSuffix: true })
    : 'Unknown';

  const handleToggle = async () => {
    try {
      await toggle(async () => {
        await tasksAPI.toggleComplete(task.id);
        window.dispatchEvent(new Event("taskUpdated"));
      });
    } catch (error: any) {
      console.error("Toggle task error:", error);
      console.error("Error details:", {
        message: error?.message,
        status: error?.status,
        details: error?.details
      });
      toast.error(error?.message || "Failed to update task");
    }
  };

  return (
    <>
      <Card className={`group transition-all duration-200 hover:shadow-lg hover:shadow-purple-500/10 dark:hover:shadow-purple-900/20 hover:-translate-y-0.5 border-l-4 ${
        completed
          ? "opacity-75 border-l-green-500 dark:border-l-green-600"
          : "border-l-purple-500 dark:border-l-purple-600"
      }`}>
        <CardContent className="flex items-start gap-4 p-6">
          <Checkbox
            checked={completed}
            onCheckedChange={handleToggle}
            disabled={isPending}
            className="mt-1 h-5 w-5 transition-transform hover:scale-110"
          />

          <div className="flex-1 min-w-0">
            <h3
              className={`font-semibold text-lg text-gray-900 dark:text-white transition-colors ${
                completed ? "line-through text-gray-500 dark:text-gray-500" : ""
              }`}
            >
              {task.title}
            </h3>

            {task.description && (
              <p
                className={`mt-2 text-sm text-gray-600 dark:text-gray-400 ${
                  completed ? "line-through" : ""
                }`}
              >
                {task.description}
              </p>
            )}

            <div className="mt-3 flex items-center gap-4 text-xs text-gray-500 dark:text-gray-500">
              <span className="flex items-center gap-1">
                <svg className="h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
                </svg>
                {formattedDate}
              </span>
              {completed && (
                <span className="inline-flex items-center gap-1 rounded-full bg-gradient-to-r from-green-100 to-emerald-100 px-2.5 py-0.5 text-xs font-medium text-green-800 dark:from-green-900 dark:to-emerald-900 dark:text-green-200">
                  <CheckCircle2 className="h-3 w-3" />
                  Completed
                </span>
              )}
            </div>
          </div>

          {/* Mobile: always visible, Desktop: show on hover */}
          <div className="flex gap-1.5 opacity-100 md:opacity-0 transition-opacity md:group-hover:opacity-100">
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setIsEditDialogOpen(true)}
              className="h-9 w-9 transition-all hover:scale-110 hover:bg-purple-50 hover:text-purple-600 dark:hover:bg-purple-950 dark:hover:text-purple-400"
            >
              <Pencil className="h-4 w-4" />
            </Button>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setIsDeleteDialogOpen(true)}
              className="h-9 w-9 text-red-600 transition-all hover:scale-110 hover:bg-red-50 hover:text-red-700 dark:text-red-400 dark:hover:bg-red-950 dark:hover:text-red-300"
            >
              <Trash2 className="h-4 w-4" />
            </Button>
          </div>
        </CardContent>
      </Card>

      <EditTaskDialog
        task={task}
        isOpen={isEditDialogOpen}
        onClose={() => setIsEditDialogOpen(false)}
      />

      <DeleteConfirmDialog
        task={task}
        isOpen={isDeleteDialogOpen}
        onClose={() => setIsDeleteDialogOpen(false)}
      />
    </>
  );
}
