"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Menu,
  X,
  Home,
  BookOpen,
  User,
  LogOut,
  Award,
  Phone,
  Info,
  Database,
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

// Simple authentication state (for development)
const useAuth = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState<{
    name?: string;
    email?: string;
    role?: string;
  } | null>(null);

  return {
    isAuthenticated,
    user,
    signIn: () => setIsAuthenticated(true),
    signOut: () => {
      setIsAuthenticated(false);
      setUser(null);
    },
  };
};

// Component for authenticated user menu
function AuthenticatedUserMenu() {
  const { isAuthenticated, user, signOut } = useAuth();

  if (!isAuthenticated) {
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
      <div className="flex items-center space-x-2">
        <Avatar className="w-8 h-8">
          <AvatarImage src="" alt={user?.name || "User"} />
          <AvatarFallback>
            {user?.name
              ?.split(" ")
              .map((n: string) => n[0])
              .join("") || "U"}
          </AvatarFallback>
        </Avatar>

        <div className="flex items-center space-x-2">
          <Button variant="ghost" size="sm" asChild>
            <Link href="/dashboard">Dashboard</Link>
          </Button>
          <Button variant="ghost" size="sm" onClick={signOut}>
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
              <div className="border-t border-slate-200 pt-2 mt-2">
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
              <div className="border-t border-slate-200 pt-4 pb-3 mt-4">
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

                <div className="px-3 space-y-1">
                  <Button
                    variant="ghost"
                    size="sm"
                    className="w-full justify-start"
                    asChild
                  >
                    <Link href="/auth/signin">Sign In</Link>
                  </Button>
                  <Button
                    variant="default"
                    size="sm"
                    className="w-full justify-start"
                    asChild
                  >
                    <Link href="/auth/signup">Sign Up</Link>
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

// Page header component
export function PageHeader({
  title,
  description,
  action,
}: {
  title: string;
  description?: string;
  action?: React.ReactNode;
}) {
  return (
    <div className="bg-gradient-to-r from-indigo-50 to-purple-50 border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="py-8 md:py-12">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl md:text-3xl font-bold text-slate-900 mb-2">
                {title}
              </h1>
              {description && (
                <p className="text-slate-600 text-lg">{description}</p>
              )}
            </div>
            {action && <div>{action}</div>}
          </div>
        </div>
      </div>
    </div>
  );
}

// Footer component
export function Footer() {
  return (
    <footer className="bg-slate-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid md:grid-cols-4 gap-8">
          <div>
            <div className="flex items-center space-x-2 mb-4">
              <div className="w-8 h-8 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-lg flex items-center justify-center">
                <Award className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold">ShikshaSetu</span>
            </div>
            <p className="text-slate-400">
              India&apos;s premier scholarship portal connecting students with
              opportunities.
            </p>
          </div>

          <div>
            <h3 className="font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2 text-slate-400">
              <li>
                <Link href="/scholarships" className="hover:text-white">
                  Browse Scholarships
                </Link>
              </li>
              <li>
                <Link href="/about" className="hover:text-white">
                  About Us
                </Link>
              </li>
              <li>
                <Link href="/contact" className="hover:text-white">
                  Contact
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="font-semibold mb-4">Support</h3>
            <ul className="space-y-2 text-slate-400">
              <li>
                <Link href="/help" className="hover:text-white">
                  Help Center
                </Link>
              </li>
              <li>
                <Link href="/privacy" className="hover:text-white">
                  Privacy Policy
                </Link>
              </li>
              <li>
                <Link href="/terms" className="hover:text-white">
                  Terms of Service
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="font-semibold mb-4">Admin</h3>
            <ul className="space-y-2 text-slate-400">
              <li>
                <Link href="/admin" className="hover:text-white">
                  Admin Dashboard
                </Link>
              </li>
              <li>
                <Link href="/admin/scraping-jobs" className="hover:text-white">
                  Scraping Jobs
                </Link>
              </li>
              <li>
                <Link href="/test-scraping" className="hover:text-white">
                  Test Scraping
                </Link>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-slate-800 mt-12 pt-8 text-center text-slate-400">
          <p>&copy; 2025 ShikshaSetu. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}
