import { User } from "lucide-react";

interface UserAvatarProps {
  name?: string;
  size?: "sm" | "md" | "lg";
  className?: string;
}

export function UserAvatar({ name = "User", size = "md", className = "" }: UserAvatarProps) {
  const getInitials = (name: string) => {
    return name
      .split(" ")
      .map(word => word.charAt(0))
      .join("")
      .toUpperCase()
      .slice(0, 2);
  };

  const sizeClasses = {
    sm: "w-6 h-6 text-xs",
    md: "w-8 h-8 text-sm",
    lg: "w-10 h-10 text-base"
  };

  return (
    <div className={`rounded-full bg-[#d32f2f] text-white flex items-center justify-center font-medium ${sizeClasses[size]} ${className}`}>
      {name ? getInitials(name) : <User className="w-4 h-4" />}
    </div>
  );
} 