import { Droplet } from "lucide-react";
import { Switch } from "@/components/ui/switch";
import { UserAvatar } from "@/components/floodsense/UserAvatar";

export default function Header({ onToggleTheme }: { onToggleTheme?: () => void }) {
  return (
    <header className="flex items-center justify-between w-full px-6 py-4 border-b border-zinc-800 bg-zinc-950">
      <div className="flex items-center gap-2 text-white text-xl font-bold">
        <Droplet className="text-[#d32f2f] w-7 h-7" />
        AnalytIQ GIS
      </div>
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2">
          <span className="text-zinc-400 text-xs">Dark</span>
          <Switch onClick={onToggleTheme} />
        </div>
        <UserAvatar name="John Doe" size="sm" />
      </div>
    </header>
  );
} 