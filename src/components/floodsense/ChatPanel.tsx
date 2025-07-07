import { useRef, useEffect } from "react";
import { Card } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Send, Trash2, Copy, Reply } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkBreaks from "remark-breaks";
import remarkGfm from "remark-gfm";
import { UserAvatar } from "@/components/floodsense/UserAvatar";

export type Message = {
  id: string;
  type: "user" | "bot";
  content: string;
  source?: "ChromaDB" | "GIS" | "LLM";
  loading?: boolean;
  timestamp?: Date;
};

export function ChatPanel({
  messages,
  input,
  onInputChange,
  onSend,
  onClear,
  loadingId,
}: {
  messages: Message[];
  input: string;
  onInputChange: (v: string) => void;
  onSend: () => void;
  onClear: () => void;
  loadingId?: string;
}) {
  const scrollRef = useRef<HTMLDivElement>(null);
  
  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages]);

  const handleCopy = (content: string) => {
    navigator.clipboard.writeText(content);
  };

  const handleReply = (content: string) => {
    onInputChange(content);
  };

  const getSourceColor = (source: string) => {
    switch (source) {
      case "GIS": return "bg-blue-500/20 text-blue-300 border-blue-500/30";
      case "ChromaDB": return "bg-purple-500/20 text-purple-300 border-purple-500/30";
      case "LLM": return "bg-green-500/20 text-green-300 border-green-500/30";
      default: return "bg-zinc-500/20 text-zinc-300 border-zinc-500/30";
    }
  };

  return (
    <Card className="flex flex-col h-full bg-zinc-900/50 backdrop-blur-sm border-zinc-800/50 rounded-xl">
      <ScrollArea className="flex-1 p-4 space-y-4 overflow-y-auto" ref={scrollRef}>
        {messages.map((msg) => (
          <div key={msg.id} className={`flex items-start gap-3 mb-6 ${msg.type === "user" ? "justify-end" : "justify-start"}`}>
            {msg.type === "bot" && (
              <UserAvatar name="FloodSense" size="sm" className="mt-1 flex-shrink-0" />
            )}
            <div className={`group max-w-[80%] px-4 py-3 rounded-2xl text-sm shadow-lg backdrop-blur-md border ${
              msg.type === "user" 
                ? "bg-[#d32f2f]/90 text-white border-[#d32f2f]/30" 
                : "bg-zinc-800/80 text-zinc-100 border-zinc-700/50"
            }`}>
              {/* <ReactMarkdown
                remarkPlugins={[remarkGfm, remarkBreaks]}
                components={{
                  a: ({ href, children }) => (
                    <a
                      href={href}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="underline text-blue-400"
                    >
                      {children}
                    </a>
                  ),
                  h1: ({ children }) => <h1 className="text-xl font-bold mb-2">{children}</h1>,
                  h2: ({ children }) => <h2 className="text-lg font-semibold mb-1">{children}</h2>,
                  p: ({ children }) => <p className="mb-2">{children}</p>,
                }}
              >
                {msg.content}
              </ReactMarkdown> */}
              <ReactMarkdown
                remarkPlugins={[remarkGfm, remarkBreaks]}
                components={{
                  a: ({ href, children }) => (
                    <a href={href} target="_blank" rel="noopener noreferrer" className="underline text-blue-400">
                      {children}
                    </a>
                  ),
                  h1: ({ children }) => <h1 className="text-xl font-bold mb-2">{children}</h1>,
                  h2: ({ children }) => <h2 className="text-lg font-semibold mb-1">{children}</h2>,
                  p: ({ children }) => <p className="mb-2">{children}</p>,
                  ul: ({ children }) => <ul className="list-disc list-inside text-zinc-300 ml-4">{children}</ul>,
                  li: ({ children }) => <li className="mb-1">{children}</li>,
                  blockquote: ({ children }) => (
                    <blockquote className="border-l-4 border-yellow-400 pl-4 text-yellow-300 bg-yellow-400/10 py-2 my-2 rounded">
                      {children}
                    </blockquote>
                  )
                }}
              >
                {msg.content}
              </ReactMarkdown>


              {msg.loading && <span className="ml-2 animate-pulse text-zinc-400">...</span>}
              <div className="mt-2 flex items-center justify-between">
                {msg.source && (
                  <span className={`px-2 py-1 rounded-full text-xs font-medium border ${getSourceColor(msg.source)}`}>
                    {msg.source}
                  </span>
                )}
                <div className="flex items-center gap-2">
                  <span className="text-xs text-zinc-400">
                    {msg.timestamp ? msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : '12:30'}
                  </span>
                  <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                    <Button
                      size="sm"
                      variant="ghost"
                      className="h-6 w-6 p-0 text-zinc-400 hover:text-zinc-200 hover:bg-zinc-700/50"
                      onClick={() => handleCopy(msg.content)}
                    >
                      <Copy className="w-3 h-3" />
                    </Button>
                    <Button
                      size="sm"
                      variant="ghost"
                      className="h-6 w-6 p-0 text-zinc-400 hover:text-zinc-200 hover:bg-zinc-700/50"
                      onClick={() => handleReply(msg.content)}
                    >
                      <Reply className="w-3 h-3" />
                    </Button>
                  </div>
                </div>
              </div>
            </div>
            {msg.type === "user" && (
              <UserAvatar name="John Doe" size="sm" className="mt-1 flex-shrink-0" />
            )}
          </div>
        ))}
      </ScrollArea>
      <form
        className="flex items-center gap-2 p-4 border-t border-zinc-800/50 bg-zinc-950/80 backdrop-blur-sm rounded-b-xl"
        onSubmit={(e) => {
          e.preventDefault();
          onSend();
        }}
      >
        <Input
          className="flex-1 bg-zinc-800/80 text-zinc-100 border-zinc-700/50 backdrop-blur-sm rounded-xl"
          placeholder="Ask about flood risk..."
          value={input}
          onChange={(e) => onInputChange(e.target.value)}
        />
        <Button type="submit" size="icon" className="bg-[#d32f2f] hover:bg-[#b71c1c] text-white rounded-xl">
          <Send className="w-5 h-5" />
        </Button>
        <Button type="button" size="icon" variant="ghost" onClick={onClear} className="rounded-xl">
          <Trash2 className="w-5 h-5 text-zinc-400" />
        </Button>
      </form>
    </Card>
  );
} 