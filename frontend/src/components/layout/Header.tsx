import React from "react";
import { Button } from "@/components/ui/button";
import { useUIStore } from "@/store";

export function Header() {
  const { toggleSidebar } = useUIStore();
  
  return (
    <header className="sticky top-0 z-10 border-b border-border bg-card px-6 py-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="icon" onClick={toggleSidebar}>
            <span className="text-xl">☰</span>
          </Button>
          <h1 className="text-xl font-semibold">Election Monitoring System</h1>
        </div>
        <div className="flex items-center gap-4">
          <Button variant="outline" size="sm">
            Help
          </Button>
          <Button variant="outline" size="sm">
            Settings
          </Button>
          <Button variant="outline" size="sm">
            Profile
          </Button>
        </div>
      </div>
    </header>
  );
}