"use client";
import { useState, useRef, useEffect } from "react";
import { GripVertical } from "lucide-react";

interface ResizablePanelProps {
  children: React.ReactNode;
  minWidth?: number;
  maxWidth?: number;
  defaultWidth?: number;
  onResize?: (width: number) => void;
  className?: string;
}

export function ResizablePanel({
  children,
  minWidth = 320,
  maxWidth = 600,
  defaultWidth = 420,
  onResize,
  className = "",
}: ResizablePanelProps) {
  const [width, setWidth] = useState(defaultWidth);
  const [isDragging, setIsDragging] = useState(false);
  const startX = useRef(0);
  const startWidth = useRef(0);

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (!isDragging) return;
      
      const deltaX = e.clientX - startX.current;
      const newWidth = Math.max(minWidth, Math.min(maxWidth, startWidth.current + deltaX));
      
      setWidth(newWidth);
      onResize?.(newWidth);
    };

    const handleMouseUp = () => {
      setIsDragging(false);
    };

    if (isDragging) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
    }

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isDragging, minWidth, maxWidth, onResize]);

  const handleMouseDown = (e: React.MouseEvent) => {
    setIsDragging(true);
    startX.current = e.clientX;
    startWidth.current = width;
  };

  return (
    <div 
      className={`relative ${className}`}
      style={{ width: `${width}px` }}
    >
      {children}
      <div
        className="absolute right-0 top-0 bottom-0 w-1 bg-zinc-700 hover:bg-[#d32f2f] cursor-col-resize flex items-center justify-center group"
        onMouseDown={handleMouseDown}
      >
        <GripVertical className="w-4 h-4 text-zinc-500 group-hover:text-[#d32f2f] opacity-0 group-hover:opacity-100 transition-opacity" />
      </div>
    </div>
  );
} 