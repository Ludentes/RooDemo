import React from "react";
import { Button } from "@/components/ui/button";
import { useUIStore } from "@/store";

interface NavItemProps {
  icon: string;
  label: string;
  active?: boolean;
  onClick?: () => void;
}

function NavItem({ icon, label, active = false, onClick }: NavItemProps) {
  return (
    <Button
      variant={active ? "default" : "ghost"}
      className="w-full justify-start"
      onClick={onClick}
    >
      <span className="mr-2">{icon}</span>
      {label}
    </Button>
  );
}

export function Sidebar() {
  const { sidebarOpen } = useUIStore();
  
  if (!sidebarOpen) {
    return null;
  }
  
  return (
    <aside className="w-64 border-r border-border bg-card p-4">
      <nav className="flex flex-col gap-2">
        <NavItem icon="📊" label="Dashboard" active />
        <NavItem icon="🗳️" label="Elections" />
        <NavItem icon="🏢" label="Constituencies" />
        <NavItem icon="📝" label="Transactions" />
        <NavItem icon="🔔" label="Alerts" />
        <NavItem icon="📁" label="Files" />
        <NavItem icon="📈" label="Reports" />
      </nav>
    </aside>
  );
}