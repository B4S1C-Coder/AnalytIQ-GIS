import { MapPin, Clock, Percent } from "lucide-react";

export function QueryMetadata({
  location,
  time,
  probability,
}: {
  location?: string;
  time?: string;
  probability?: number;
}) {
  return (
    <div className="flex gap-4 items-center bg-zinc-900 rounded-lg px-4 py-2 text-zinc-200 text-xs shadow border border-zinc-800">
      {location && (
        <span className="flex items-center gap-1"><MapPin className="w-4 h-4 text-[#d32f2f]" /> {location}</span>
      )}
      {time && (
        <span className="flex items-center gap-1"><Clock className="w-4 h-4 text-zinc-400" /> {time}</span>
      )}
      {probability !== undefined && (
        <span className="flex items-center gap-1"><Percent className="w-4 h-4 text-zinc-400" /> {probability}%</span>
      )}
    </div>
  );
} 