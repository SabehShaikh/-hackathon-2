import { useState, useEffect } from "react";

export function useOptimisticToggle(initialValue: boolean) {
  const [value, setValue] = useState(initialValue);
  const [isPending, setIsPending] = useState(false);

  // Sync with prop changes when not pending
  useEffect(() => {
    if (!isPending) {
      setValue(initialValue);
    }
  }, [initialValue, isPending]);

  const toggle = async (onToggle: () => Promise<void>) => {
    // Store original value for rollback
    const originalValue = value;

    // Optimistically update UI immediately
    setValue(!value);
    setIsPending(true);

    try {
      // Call the actual API
      await onToggle();
      // Success - keep the new value
    } catch (error) {
      // Rollback on error
      setValue(originalValue);
      throw error;
    } finally {
      setIsPending(false);
    }
  };

  return { value, isPending, toggle };
}
