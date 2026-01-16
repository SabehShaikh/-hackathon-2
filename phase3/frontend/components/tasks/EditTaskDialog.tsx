"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { toast } from "sonner";
import { tasksAPI } from "@/lib/api";
import { Task } from "@/lib/types";

interface EditTaskDialogProps {
  task: Task;
  isOpen: boolean;
  onClose: () => void;
}

export function EditTaskDialog({ task, isOpen, onClose }: EditTaskDialogProps) {
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description || "");
  const [isLoading, setIsLoading] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});

  const MAX_TITLE_LENGTH = 200;
  const MAX_DESCRIPTION_LENGTH = 1000;

  const titleRemaining = MAX_TITLE_LENGTH - title.length;
  const descriptionRemaining = MAX_DESCRIPTION_LENGTH - description.length;

  // Reset form when task changes
  useEffect(() => {
    setTitle(task.title);
    setDescription(task.description || "");
    setErrors({});
  }, [task]);

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    // Title validation
    if (!title.trim()) {
      newErrors.title = "Title is required";
    } else if (title.length < 1 || title.length > MAX_TITLE_LENGTH) {
      newErrors.title = `Title must be between 1 and ${MAX_TITLE_LENGTH} characters`;
    }

    // Description validation (optional)
    if (description && description.length > MAX_DESCRIPTION_LENGTH) {
      newErrors.description = `Description must be ${MAX_DESCRIPTION_LENGTH} characters or less`;
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setIsLoading(true);

    try {
      await tasksAPI.update(task.id, {
        title: title.trim(),
        description: description.trim() || undefined,
      });

      toast.success("Task updated!");
      onClose();

      // Notify TaskList to refresh
      window.dispatchEvent(new Event("taskUpdated"));
    } catch (error: any) {
      console.error("Update task error:", error);

      if (error.status === 401) {
        toast.error("Please log in to update tasks");
      } else if (error.status === 404) {
        toast.error("Task not found");
      } else if (error.status === 422) {
        toast.error("Invalid task data");
      } else {
        toast.error("Failed to update task. Please try again.");
      }

      // Keep form values on error so user doesn't lose changes
    } finally {
      setIsLoading(false);
    }
  };

  const handleCancel = () => {
    if (!isLoading) {
      // Reset to original values on cancel
      setTitle(task.title);
      setDescription(task.description || "");
      setErrors({});
      onClose();
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[525px]">
        <DialogHeader>
          <DialogTitle>Edit Task</DialogTitle>
          <DialogDescription>
            Update your task details below.
          </DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <Label htmlFor="edit-title">Title *</Label>
              <span
                className={`text-xs ${
                  titleRemaining < 20
                    ? "text-red-500"
                    : "text-gray-500 dark:text-gray-400"
                }`}
              >
                {titleRemaining} characters remaining
              </span>
            </div>
            <Input
              id="edit-title"
              placeholder="Enter task title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              disabled={isLoading}
              maxLength={MAX_TITLE_LENGTH}
              className={errors.title ? "border-red-500" : ""}
            />
            {errors.title && (
              <p className="text-sm text-red-500">{errors.title}</p>
            )}
          </div>

          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <Label htmlFor="edit-description">Description</Label>
              <span
                className={`text-xs ${
                  descriptionRemaining < 100
                    ? "text-red-500"
                    : "text-gray-500 dark:text-gray-400"
                }`}
              >
                {descriptionRemaining} characters remaining
              </span>
            </div>
            <Textarea
              id="edit-description"
              placeholder="Enter task description (optional)"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              disabled={isLoading}
              maxLength={MAX_DESCRIPTION_LENGTH}
              rows={4}
              className={errors.description ? "border-red-500" : ""}
            />
            {errors.description && (
              <p className="text-sm text-red-500">{errors.description}</p>
            )}
          </div>

          <div className="flex justify-end gap-3">
            <Button
              type="button"
              variant="outline"
              onClick={handleCancel}
              disabled={isLoading}
            >
              Cancel
            </Button>
            <Button type="submit" disabled={isLoading} className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700">
              {isLoading ? "Saving..." : "Save Changes"}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}
