"use client";

import * as React from "react";
import { cn } from "@/lib/utils";

export interface LoadingSpinnerProps
  extends React.HTMLAttributes<HTMLDivElement> {
  size?: "sm" | "md" | "lg";
  color?: "primary" | "secondary" | "muted";
}

const LoadingSpinner = React.forwardRef<HTMLDivElement, LoadingSpinnerProps>(
  ({ className, size = "md", color = "primary", ...props }, ref) => {
    const sizeClasses = {
      sm: "h-4 w-4",
      md: "h-8 w-8",
      lg: "h-12 w-12",
    };

    const colorClasses = {
      primary: "border-primary",
      secondary: "border-secondary",
      muted: "border-muted-foreground",
    };

    return (
      <div
        ref={ref}
        className={cn(
          "inline-block animate-spin rounded-full border-2 border-solid border-current border-r-transparent motion-reduce:animate-[spin_1.5s_linear_infinite]",
          sizeClasses[size],
          colorClasses[color],
          className
        )}
        role="status"
        aria-label="Loading"
        {...props}
      >
        <span className="sr-only">Loading...</span>
      </div>
    );
  }
);
LoadingSpinner.displayName = "LoadingSpinner";

export { LoadingSpinner };
