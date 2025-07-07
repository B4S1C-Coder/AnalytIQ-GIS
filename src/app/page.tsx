"use client";
import dynamic from "next/dynamic";
import { useState } from "react";
import Header from "@/components/floodsense/Header";
import { Sidebar } from "@/components/floodsense/Sidebar";
import { ChatPanel, Message } from "@/components/floodsense/ChatPanel";
import { QueryMetadata } from "@/components/floodsense/QueryMetadata";
import { ResizablePanel } from "@/components/floodsense/ResizablePanel";

const MapPanel = dynamic(() => import("@/components/floodsense/MapPanel").then(m => m.MapPanel), { 
  ssr: false,
  loading: () => (
    <div className="flex-1 h-full min-h-0 bg-zinc-900 rounded-lg flex items-center justify-center">
      <div className="text-zinc-400">Loading map...</div>
    </div>
  )
});

const initialMessages: Message[] = [
  { id: "1", type: "user", content: "Will my house flood?", timestamp: new Date(Date.now() - 300000) },
  { id: "2", type: "bot", content: "## 🌧️ Flood Risk Alert\n\nThere is a **73% chance** that your home may experience flooding.\n\n ⚠️ **Recommended Actions:**\n- Move valuables and important documents to higher ground.\n - Stay updated via local news or flood alerts.\n - Prepare an emergency bag with essentials.\n - Avoid low-lying areas during heavy rainfall.\n - Flood Control Room: `1916`, NDRF: `97110-77372`\n \nStay safe! 🙏"
, source: "GIS", timestamp: new Date(Date.now() - 240000) },
];

export default function Home() {
  const [messages, setMessages] = useState<Message[]>(initialMessages);
  const [input, setInput] = useState("");
  const [location, setLocation] = useState<{ lat: number; lng: number; label?: string }>({ lat: 19.0544, lng: 72.8402, label: "Bandra Home" });
  const [floodZones] = useState<any>({
    "type": "FeatureCollection",
    "features": [
      {
        "type": "Feature",
        "geometry": {
          "type": "Polygon",
          "coordinates": [
            [
              [72.835, 19.05],
              [72.845, 19.05],
              [72.845, 19.06],
              [72.835, 19.06],
              [72.835, 19.05]
            ]
          ]
        },
        "properties": { "risk": 0.73 }
      }
    ]
  });
  const [meta] = useState({ location: "Bandra, Mumbai", time: "2025-07-05 12:30", probability: 73 });

  return (
    <div className="flex flex-col min-h-screen bg-zinc-950">
      <Header />
      <div className="flex flex-1 min-h-0">
        <Sidebar />
        <main className="flex flex-1 min-h-0">
          <ResizablePanel 
            minWidth={320} 
            maxWidth={600} 
            defaultWidth={420}
            className="flex flex-col h-full border-r border-zinc-800 bg-zinc-950"
          >
            <div className="p-4 border-b border-zinc-800">
              <QueryMetadata {...meta} />
            </div>
            <div className="flex-1 min-h-0">
              <ChatPanel
                messages={messages}
                input={input}
                onInputChange={setInput}
                onSend={() => {}}
                onClear={() => setMessages([])}
              />
            </div>
          </ResizablePanel>
          <section className="flex-1 h-full min-h-0 bg-zinc-900">
            <MapPanel location={location} floodZones={floodZones} />
          </section>
        </main>
      </div>
    </div>
  );
}
