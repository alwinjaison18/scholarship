"use client";

import React from "react";
import Link from "next/link";
import { ArrowRight, Search, Award, Users, BookOpen } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

export interface HeroSectionProps {
  title: string;
  subtitle: string;
  description?: string;
  showSearch?: boolean;
  showStats?: boolean;
  ctaText?: string;
  ctaLink?: string;
  backgroundVariant?: "default" | "gradient" | "pattern";
  className?: string;
  onSearch?: (query: string) => void;
  stats?: {
    scholarships: string;
    students: string;
    amount: string;
    successRate: string;
  };
}

const defaultStats = {
  scholarships: "4,500+",
  students: "25,000+",
  amount: "₹50 Cr+",
  successRate: "78%",
};

export function HeroSection({
  title,
  subtitle,
  description,
  showSearch = false,
  showStats = false,
  ctaText = "Get Started",
  ctaLink = "/scholarships",
  backgroundVariant = "default",
  className,
  onSearch,
  stats = defaultStats,
}: HeroSectionProps) {
  const [searchQuery, setSearchQuery] = React.useState("");

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (onSearch) {
      onSearch(searchQuery);
    } else {
      // Default search behavior
      window.location.href = `/scholarships?q=${encodeURIComponent(
        searchQuery
      )}`;
    }
  };

  const getBackgroundClasses = () => {
    switch (backgroundVariant) {
      case "gradient":
        return "bg-gradient-to-br from-indigo-50 via-blue-50 to-purple-50";
      case "pattern":
        return "bg-gradient-to-br from-emerald-50 via-teal-50 to-cyan-50";
      default:
        return "bg-gradient-to-br from-slate-50 via-gray-50 to-zinc-50";
    }
  };

  return (
    <section
      className={cn(
        "relative overflow-hidden",
        getBackgroundClasses(),
        className
      )}
    >
      {/* Background Pattern */}
      <div className="absolute inset-0 bg-grid-pattern opacity-5" />

      {/* Floating Elements */}
      <div className="absolute top-20 left-10 w-20 h-20 bg-indigo-200 rounded-full opacity-20 animate-pulse" />
      <div
        className="absolute top-40 right-20 w-16 h-16 bg-emerald-200 rounded-full opacity-20 animate-pulse"
        style={{ animationDelay: "1s" }}
      />
      <div
        className="absolute bottom-20 left-20 w-12 h-12 bg-purple-200 rounded-full opacity-20 animate-pulse"
        style={{ animationDelay: "2s" }}
      />

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 lg:py-24">
        <div className="text-center">
          {/* Main Title */}
          <h1 className="text-display font-extrabold text-slate-900 mb-6 leading-tight">
            {title}
            <span className="block text-gradient-primary">{subtitle}</span>
          </h1>

          {/* Description */}
          {description && (
            <p className="text-subtitle text-slate-600 max-w-3xl mx-auto mb-8 leading-relaxed">
              {description}
            </p>
          )}

          {/* Search Bar */}
          {showSearch && (
            <div className="max-w-2xl mx-auto mb-8">
              <form onSubmit={handleSearch} className="relative">
                <div className="relative">
                  <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-slate-400" />
                  <Input
                    type="text"
                    placeholder="Search scholarships, categories, or eligibility criteria..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="pl-12 pr-32 py-4 text-lg border-2 border-slate-200 focus:border-indigo-500 rounded-full shadow-medium"
                  />
                  <Button
                    type="submit"
                    size="lg"
                    className="absolute right-2 top-1/2 transform -translate-y-1/2 rounded-full bg-gradient-primary hover:opacity-90 shadow-primary"
                  >
                    Search
                    <ArrowRight className="ml-2 h-5 w-5" />
                  </Button>
                </div>
              </form>
            </div>
          )}

          {/* CTA Button */}
          {!showSearch && (
            <div className="flex flex-col sm:flex-row gap-4 justify-center mb-8">
              <Link href={ctaLink}>
                <Button
                  size="lg"
                  className="bg-gradient-primary hover:opacity-90 text-lg px-8 py-6 rounded-full"
                >
                  {ctaText}
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
              <Link href="/about">
                <Button
                  size="lg"
                  variant="outline"
                  className="text-lg px-8 py-6 rounded-full border-2"
                >
                  Learn More
                </Button>
              </Link>
            </div>
          )}

          {/* Trust Indicators */}
          <div className="flex flex-wrap justify-center gap-4 mb-8">
            <Badge variant="secondary" className="px-4 py-2 text-sm">
              <Award className="h-4 w-4 mr-2" />
              Verified Scholarships
            </Badge>
            <Badge variant="secondary" className="px-4 py-2 text-sm">
              <Users className="h-4 w-4 mr-2" />
              Trusted by 25,000+ Students
            </Badge>
            <Badge variant="secondary" className="px-4 py-2 text-sm">
              <BookOpen className="h-4 w-4 mr-2" />
              Real-time Updates
            </Badge>
          </div>

          {/* Stats */}
          {showStats && (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto">
              <Card className="border-0 shadow-medium bg-white/80 backdrop-blur-sm">
                <CardContent className="p-6 text-center">
                  <div className="text-3xl font-bold text-indigo-600 mb-2">
                    {stats.scholarships}
                  </div>
                  <div className="text-sm text-slate-600">
                    Total Scholarships
                  </div>
                </CardContent>
              </Card>
              <Card className="border-0 shadow-medium bg-white/80 backdrop-blur-sm">
                <CardContent className="p-6 text-center">
                  <div className="text-3xl font-bold text-emerald-600 mb-2">
                    {stats.students}
                  </div>
                  <div className="text-sm text-slate-600">Active Students</div>
                </CardContent>
              </Card>
              <Card className="border-0 shadow-medium bg-white/80 backdrop-blur-sm">
                <CardContent className="p-6 text-center">
                  <div className="text-3xl font-bold text-purple-600 mb-2">
                    {stats.amount}
                  </div>
                  <div className="text-sm text-slate-600">
                    Amount Distributed
                  </div>
                </CardContent>
              </Card>
              <Card className="border-0 shadow-medium bg-white/80 backdrop-blur-sm">
                <CardContent className="p-6 text-center">
                  <div className="text-3xl font-bold text-blue-600 mb-2">
                    {stats.successRate}
                  </div>
                  <div className="text-sm text-slate-600">Success Rate</div>
                </CardContent>
              </Card>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}

export default HeroSection;
