"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { toast } from "sonner";
import { tasksAPI } from "@/lib/api";
import { Task } from "@/lib/types";
import { AlertTriangle } from "lucide-react";

interface DeleteConfirmDialogProps {
  task: Task;
  isOpen: boolean;
  onClose: () => void;
}

export function DeleteConfirmDialog({
  task,
  isOpen,
  onClose,
}: DeleteConfirmDialogProps) {
  const [isLoading, setIsLoading] = useState(false);

  const handleDelete = async () => {
    setIsLoading(true);

    try {
      await tasksAPI.delete(task.id);
      toast.success("Task deleted");
      onClose();

      // Notify TaskList to refresh
      window.dispatchEvent(new Event("taskUpdated"));
    } catch (error: any) {
      console.error("Delete task error:", error);

      if (error.status === 401) {
        toast.error("Please log in to delete tasks");
      } else if (error.status === 404) {
        toast.error("Task not found");
      } else {
        toast.error("Failed to delete task. Please try again.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleCancel = () => {
    if (!isLoading) {
      onClose();
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Escape" && !isLoading) {
      onClose();
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[425px]" onKeyDown={handleKeyDown}>
        <DialogHeader>
          <div className="flex items-center gap-3">
            <div className="rounded-full bg-red-100 p-2 dark:bg-red-900/20">
              <AlertTriangle className="h-5 w-5 text-red-600 dark:text-red-400" />
            </div>
            <DialogTitle>Delete Task</DialogTitle>
          </div>
          <DialogDescription className="pt-3">
            Are you sure you want to delete <strong>"{task.title}"</strong>?
            This action cannot be undone.
          </DialogDescription>
        </DialogHeader>

        <DialogFooter className="gap-2 sm:gap-0">
          <Button
            type="button"
            variant="outline"
            onClick={handleCancel}
            disabled={isLoading}
          >
            Cancel
          </Button>
          <Button
            type="button"
            variant="destructive"
            onClick={handleDelete}
            disabled={isLoading}
          >
            {isLoading ? "Deleting..." : "Delete Task"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
