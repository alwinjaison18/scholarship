"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useSession, signOut } from "next-auth/react";
import {
  Menu,
  X,
  Home,
  BookOpen,
  User,
  Settings,
  Bell,
  LogOut,
  Award,
  Phone,
  Mail,
  MapPin,
  Clock,
  CheckCircle,
  Shield,
  Info,
  Database,
  Globe,
  Zap,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { cn } from "@/lib/utils";

interface NavItem {
  label: string;
  href: string;
  icon: React.ComponentType<{ className?: string }>;
  badge?: number;
  isActive?: boolean;
  children?: NavItem[];
}

const mainNavItems: NavItem[] = [
  { label: "Home", href: "/", icon: Home },
  { label: "Scholarships", href: "/scholarships", icon: BookOpen },
  { label: "About", href: "/about", icon: Info },
  { label: "Contact", href: "/contact", icon: Phone },
];

// Admin navigation items
const adminNavItems: NavItem[] = [
  { label: "Admin Dashboard", href: "/admin", icon: Database },
  { label: "Scraping Jobs", href: "/admin/scraping-jobs", icon: Globe },
  { label: "Test Scraping", href: "/test-scraping", icon: Zap },
];

// const userNavItems: NavItem[] = [
//   { label: "Dashboard", href: "/dashboard", icon: BarChart3 },
//   { label: "My Applications", href: "/applications", icon: Award, badge: 3 },
//   { label: "Bookmarks", href: "/bookmarks", icon: Heart },
//   { label: "Profile", href: "/profile", icon: User },
//   { label: "Notifications", href: "/notifications", icon: Bell, badge: 5 },
//   { label: "Settings", href: "/settings", icon: Settings },
// ];

// const adminNavItems: NavItem[] = [
//   { label: "Admin Dashboard", href: "/admin", icon: Database },
//   { label: "Scholarships", href: "/admin/scholarships", icon: BookOpen },
//   { label: "Users", href: "/admin/users", icon: Users },
//   { label: "Applications", href: "/admin/applications", icon: Award },
//   { label: "Scraping Jobs", href: "/admin/scraping", icon: Globe },
//   { label: "Analytics", href: "/admin/analytics", icon: TrendingUp },
//   { label: "System Health", href: "/admin/health", icon: Zap },
//   { label: "Settings", href: "/admin/settings", icon: Settings },
// ];

// Component for authenticated user menu
function AuthenticatedUserMenu() {
  const { data: session, status } = useSession();

  if (status === "loading") {
    return (
      <div className="w-8 h-8 bg-gray-200 rounded-full animate-pulse"></div>
    );
  }

  if (!session) {
    return (
      <div className="flex items-center space-x-2">
        <Button variant="ghost" size="sm" asChild>
          <Link href="/auth/signin">Sign In</Link>
        </Button>
        <Button variant="default" size="sm" asChild>
          <Link href="/auth/signup">Sign Up</Link>
        </Button>
      </div>
    );
  }

  return (
    <div className="flex items-center space-x-4">
      <Button variant="ghost" size="sm" className="relative" asChild>
        <Link href="/dashboard/notifications">
          <Bell className="w-5 h-5" />
          <Badge className="absolute -top-2 -right-2 w-5 h-5 p-0 flex items-center justify-center text-xs">
            3
          </Badge>
        </Link>
      </Button>

      <div className="flex items-center space-x-2">
        <Avatar className="w-8 h-8">
          <AvatarImage src="" alt={session.user?.name || ""} />
          <AvatarFallback>
            {session.user?.name
              ?.split(" ")
              .map((n) => n[0])
              .join("") || "U"}
          </AvatarFallback>
        </Avatar>

        <div className="flex items-center space-x-2">
          <Button variant="ghost" size="sm" asChild>
            <Link href="/dashboard">Dashboard</Link>
          </Button>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => signOut({ callbackUrl: "/" })}
          >
            <LogOut className="w-4 h-4" />
          </Button>
        </div>
      </div>
    </div>
  );
}

export default function Navigation() {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const pathname = usePathname();

  const isActive = (href: string) => pathname === href;

  return (
    <nav className="border-b bg-white/95 backdrop-blur supports-[backdrop-filter]:bg-white/60 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center">
            <Link href="/" className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-lg flex items-center justify-center">
                <Award className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
                ShikshaSetu
              </span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:block flex-1">
            <div className="ml-10 flex items-baseline space-x-4">
              {mainNavItems.map((item) => (
                <Link
                  key={item.href}
                  href={item.href}
                  className={cn(
                    "px-3 py-2 rounded-md text-sm font-medium transition-colors",
                    isActive(item.href)
                      ? "bg-indigo-100 text-indigo-700"
                      : "text-slate-700 hover:bg-slate-100 hover:text-slate-900"
                  )}
                >
                  <div className="flex items-center space-x-1">
                    <item.icon className="w-4 h-4" />
                    <span>{item.label}</span>
                    {item.badge && (
                      <Badge variant="destructive" className="ml-1 text-xs">
                        {item.badge}
                      </Badge>
                    )}
                  </div>
                </Link>
              ))}

              {/* Admin Navigation */}
              <div className="border-l border-slate-200 ml-4 pl-4">
                {adminNavItems.map((item) => (
                  <Link
                    key={item.href}
                    href={item.href}
                    className={cn(
                      "px-3 py-2 rounded-md text-sm font-medium transition-colors ml-2",
                      isActive(item.href)
                        ? "bg-emerald-100 text-emerald-700"
                        : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
                    )}
                  >
                    <div className="flex items-center space-x-1">
                      <item.icon className="w-4 h-4" />
                      <span>{item.label}</span>
                    </div>
                  </Link>
                ))}
              </div>
            </div>
          </div>

          {/* User Menu */}
          <div className="hidden md:flex items-center space-x-4">
            <AuthenticatedUserMenu />
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            >
              {isMobileMenuOpen ? (
                <X className="w-6 h-6" />
              ) : (
                <Menu className="w-6 h-6" />
              )}
            </Button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMobileMenuOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-white border-t">
              {/* Mobile Navigation Items */}
              {mainNavItems.map((item) => (
                <Link
                  key={item.href}
                  href={item.href}
                  className={cn(
                    "block px-3 py-2 rounded-md text-base font-medium transition-colors",
                    isActive(item.href)
                      ? "bg-indigo-100 text-indigo-700"
                      : "text-slate-700 hover:bg-slate-100 hover:text-slate-900"
                  )}
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  <div className="flex items-center space-x-2">
                    <item.icon className="w-5 h-5" />
                    <span>{item.label}</span>
                    {item.badge && (
                      <Badge variant="destructive" className="ml-auto text-xs">
                        {item.badge}
                      </Badge>
                    )}
                  </div>
                </Link>
              ))}

              {/* Mobile Admin Navigation */}
              <div className="border-t border-slate-200 pt-2">
                <div className="px-3 py-2 text-sm font-medium text-slate-500">
                  Admin Panel
                </div>
                {adminNavItems.map((item) => (
                  <Link
                    key={item.href}
                    href={item.href}
                    className={cn(
                      "block px-3 py-2 rounded-md text-base font-medium transition-colors",
                      isActive(item.href)
                        ? "bg-emerald-100 text-emerald-700"
                        : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
                    )}
                    onClick={() => setIsMobileMenuOpen(false)}
                  >
                    <div className="flex items-center space-x-2">
                      <item.icon className="w-5 h-5" />
                      <span>{item.label}</span>
                    </div>
                  </Link>
                ))}
              </div>

              {/* Mobile User Menu */}
              <div className="pt-4 pb-3 border-t border-slate-200">
                <div className="flex items-center px-3 mb-3">
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 bg-indigo-500 rounded-full flex items-center justify-center">
                      <User className="w-5 h-5 text-white" />
                    </div>
                  </div>
                  <div className="ml-3">
                    <div className="text-base font-medium text-slate-800">
                      Guest User
                    </div>
                    <div className="text-sm text-slate-500">Not logged in</div>
                  </div>
                </div>
                <div className="space-y-1">
                  <Button variant="outline" className="w-full justify-start">
                    <User className="w-4 h-4 mr-2" />
                    Login
                  </Button>
                  <Button variant="ghost" className="w-full justify-start">
                    <Settings className="w-4 h-4 mr-2" />
                    Settings
                  </Button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}

// Header Component for different pages
export function PageHeader({
  title,
  description,
  action,
  breadcrumb,
}: {
  title: string;
  description?: string;
  action?: React.ReactNode;
  breadcrumb?: { label: string; href?: string }[];
}) {
  return (
    <div className="bg-gradient-to-r from-indigo-50 to-purple-50 border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {breadcrumb && (
          <nav className="flex mb-4" aria-label="Breadcrumb">
            <ol className="flex items-center space-x-2 text-sm">
              {breadcrumb.map((item, index) => (
                <li key={index} className="flex items-center">
                  {index > 0 && <span className="mx-2 text-slate-400">/</span>}
                  {item.href ? (
                    <Link
                      href={item.href}
                      className="text-slate-600 hover:text-indigo-600 transition-colors"
                    >
                      {item.label}
                    </Link>
                  ) : (
                    <span className="text-slate-900 font-medium">
                      {item.label}
                    </span>
                  )}
                </li>
              ))}
            </ol>
          </nav>
        )}

        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-headline font-bold text-slate-900">{title}</h1>
            {description && (
              <p className="mt-2 text-lg text-slate-600">{description}</p>
            )}
          </div>
          {action && (
            <div className="flex items-center space-x-4">{action}</div>
          )}
        </div>
      </div>
    </div>
  );
}

// Footer Component
export function Footer() {
  return (
    <footer className="bg-slate-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* About */}
          <div>
            <div className="flex items-center space-x-2 mb-4">
              <div className="w-8 h-8 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-lg flex items-center justify-center">
                <Award className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold">ShikshaSetu</span>
            </div>
            <p className="text-slate-400 text-sm">
              India&apos;s most trusted scholarship portal connecting students
              with authentic scholarship opportunities from verified sources.
            </p>
            <div className="flex items-center space-x-4 mt-4">
              <Badge variant="success" className="text-xs">
                <CheckCircle className="w-3 h-3 mr-1" />
                Verified
              </Badge>
              <Badge variant="info" className="text-xs">
                <Shield className="w-3 h-3 mr-1" />
                Secure
              </Badge>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-sm font-semibold uppercase tracking-wider mb-4">
              Quick Links
            </h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link
                  href="/scholarships"
                  className="text-slate-400 hover:text-white transition-colors"
                >
                  Browse Scholarships
                </Link>
              </li>
              <li>
                <Link
                  href="/scholarships?filter=categories"
                  className="text-slate-400 hover:text-white transition-colors"
                >
                  Categories
                </Link>
              </li>
              <li>
                <Link
                  href="/scholarships?filter=deadlines"
                  className="text-slate-400 hover:text-white transition-colors"
                >
                  Upcoming Deadlines
                </Link>
              </li>
              <li>
                <Link
                  href="/about#success-stories"
                  className="text-slate-400 hover:text-white transition-colors"
                >
                  Success Stories
                </Link>
              </li>
              <li>
                <Link
                  href="/how-to-apply"
                  className="text-slate-400 hover:text-white transition-colors"
                >
                  How to Apply
                </Link>
              </li>
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h3 className="text-sm font-semibold uppercase tracking-wider mb-4">
              Resources
            </h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link
                  href="/help"
                  className="text-slate-400 hover:text-white transition-colors"
                >
                  Help Center
                </Link>
              </li>
              <li>
                <Link
                  href="/faq"
                  className="text-slate-400 hover:text-white transition-colors"
                >
                  FAQ
                </Link>
              </li>
              <li>
                <Link
                  href="/guides"
                  className="text-slate-400 hover:text-white transition-colors"
                >
                  Application Guides
                </Link>
              </li>
              <li>
                <Link
                  href="/blog"
                  className="text-slate-400 hover:text-white transition-colors"
                >
                  Blog
                </Link>
              </li>
              <li>
                <Link
                  href="/api"
                  className="text-slate-400 hover:text-white transition-colors"
                >
                  API
                </Link>
              </li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h3 className="text-sm font-semibold uppercase tracking-wider mb-4">
              Contact
            </h3>
            <div className="space-y-2 text-sm">
              <div className="flex items-center space-x-2 text-slate-400">
                <Mail className="w-4 h-4" />
                <span>support@shikhasetu.com</span>
              </div>
              <div className="flex items-center space-x-2 text-slate-400">
                <Phone className="w-4 h-4" />
                <span>+91 80-4000-5000</span>
              </div>
              <div className="flex items-center space-x-2 text-slate-400">
                <MapPin className="w-4 h-4" />
                <span>Bangalore, India</span>
              </div>
              <div className="flex items-center space-x-2 text-slate-400">
                <Clock className="w-4 h-4" />
                <span>24/7 Support</span>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-slate-800 flex items-center justify-between">
          <div className="text-sm text-slate-400">
            © 2025 ShikshaSetu. All rights reserved.
          </div>
          <div className="flex space-x-6 text-sm">
            <Link
              href="/privacy"
              className="text-slate-400 hover:text-white transition-colors"
            >
              Privacy Policy
            </Link>
            <Link
              href="/terms"
              className="text-slate-400 hover:text-white transition-colors"
            >
              Terms of Service
            </Link>
            <Link
              href="/cookies"
              className="text-slate-400 hover:text-white transition-colors"
            >
              Cookie Policy
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
}

// Status indicator component
export function StatusIndicator({
  status,
}: {
  status: "online" | "offline" | "maintenance";
}) {
  const statusConfig = {
    online: { color: "bg-green-500", text: "All systems operational" },
    offline: { color: "bg-red-500", text: "System offline" },
    maintenance: { color: "bg-yellow-500", text: "Scheduled maintenance" },
  };

  const config = statusConfig[status];

  return (
    <div className="flex items-center space-x-2 text-sm">
      <div className={`w-2 h-2 rounded-full ${config.color}`} />
      <span className="text-slate-600">{config.text}</span>
    </div>
  );
}
