import { Bug, History } from "lucide-react";

export function Sidebar() {
  const conversationHistory = [
    { id: "1", title: "Flood Risk Assessment", date: "2025-07-05" },
    { id: "2", title: "Property Safety Check", date: "2025-07-04" },
    { id: "3", title: "Emergency Planning", date: "2025-07-03" },
  ];

  return (
    <aside className="flex flex-col bg-zinc-950 border-r border-zinc-800 h-full w-64">
      <div className="p-4 border-b border-zinc-800">
        <h3 className="text-zinc-200 font-medium mb-3">Tools</h3>
        <div className="flex flex-col gap-2">
          <button className="flex items-center gap-2 text-zinc-400 hover:text-[#d32f2f] p-2 rounded-lg hover:bg-zinc-800/50 transition-colors">
            <Bug className="w-4 h-4" />
            <span className="text-sm">Debug</span>
          </button>
        </div>
      </div>
      
      <div className="flex-1 p-4">
        <div className="flex items-center gap-2 text-zinc-200 font-medium mb-3">
          <History className="w-4 h-4" />
          <span className="text-sm">History</span>
        </div>
        <div className="space-y-2">
          {conversationHistory.map((conv) => (
            <button
              key={conv.id}
              className="w-full text-left p-2 rounded-lg hover:bg-zinc-800/50 transition-colors group"
            >
              <div className="text-zinc-300 text-sm font-medium group-hover:text-white">
                {conv.title}
              </div>
              <div className="text-zinc-500 text-xs">
                {conv.date}
              </div>
            </button>
          ))}
        </div>
      </div>
    </aside>
  );
} 