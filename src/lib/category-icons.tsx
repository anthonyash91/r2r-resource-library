import Link from "next/link";
import {
  Home,
  Briefcase,
  Utensils,
  HeartPulse,
  Brain,
  Shield,
  Bus,
  GraduationCap,
  DollarSign,
  Scale,
  IdCard,
  Users,
  Medal,
  Accessibility,
  Handshake,
  Phone,
  Search,
  type LucideIcon,
} from "lucide-react";

const iconMap: Record<string, LucideIcon> = {
  home: Home,
  briefcase: Briefcase,
  utensils: Utensils,
  "heart-pulse": HeartPulse,
  brain: Brain,
  shield: Shield,
  bus: Bus,
  "graduation-cap": GraduationCap,
  "dollar-sign": DollarSign,
  scale: Scale,
  "id-card": IdCard,
  users: Users,
  medal: Medal,
  accessibility: Accessibility,
  handshake: Handshake,
  phone: Phone,
  search: Search,
};

export function CategoryIcon({ icon, className }: { icon: string | null; className?: string }) {
  const Icon = icon ? iconMap[icon] ?? Search : Search;
  return <Icon className={className} aria-hidden="true" />;
}

export function getCategoryIcon(icon: string | null): LucideIcon {
  return icon ? iconMap[icon] ?? Search : Search;
}
