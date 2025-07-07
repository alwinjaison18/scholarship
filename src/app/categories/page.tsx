"use client";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import Navigation, { PageHeader } from "@/components/navigation";
import { Footer } from "@/components/navigation";
import {
  BookOpen,
  GraduationCap,
  Users,
  Target,
  Award,
  ArrowRight,
  Search,
  Filter,
} from "lucide-react";

const CATEGORIES = [
  {
    id: "merit-based",
    name: "Merit-Based Scholarships",
    description:
      "Scholarships awarded based on academic excellence and achievements",
    icon: Award,
    count: 850,
    color: "bg-indigo-500",
    lightColor: "bg-indigo-50",
    textColor: "text-indigo-600",
  },
  {
    id: "need-based",
    name: "Need-Based Scholarships",
    description:
      "Financial aid for students from economically disadvantaged backgrounds",
    icon: Users,
    count: 650,
    color: "bg-emerald-500",
    lightColor: "bg-emerald-50",
    textColor: "text-emerald-600",
  },
  {
    id: "minority",
    name: "Minority Scholarships",
    description:
      "Support for students from minority communities and underrepresented groups",
    icon: Target,
    count: 400,
    color: "bg-purple-500",
    lightColor: "bg-purple-50",
    textColor: "text-purple-600",
  },
  {
    id: "sports",
    name: "Sports Scholarships",
    description:
      "Recognition and support for outstanding athletic achievements",
    icon: Target,
    count: 200,
    color: "bg-amber-500",
    lightColor: "bg-amber-50",
    textColor: "text-amber-600",
  },
  {
    id: "research",
    name: "Research Scholarships",
    description:
      "Funding for students pursuing research and innovation projects",
    icon: BookOpen,
    count: 300,
    color: "bg-blue-500",
    lightColor: "bg-blue-50",
    textColor: "text-blue-600",
  },
  {
    id: "postgraduate",
    name: "Postgraduate Scholarships",
    description: "Advanced degree funding for masters and doctoral programs",
    icon: GraduationCap,
    count: 500,
    color: "bg-rose-500",
    lightColor: "bg-rose-50",
    textColor: "text-rose-600",
  },
];

export default function CategoriesPage() {
  return (
    <div className="min-h-screen bg-white">
      <Navigation />

      <PageHeader
        title="Scholarship Categories"
        description="Explore scholarships by category to find the perfect opportunity for your educational journey"
      />

      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {CATEGORIES.map((category) => (
              <Card
                key={category.id}
                className="hover:shadow-medium transition-all duration-200 cursor-pointer group"
              >
                <CardHeader className="pb-4">
                  <div className="flex items-center justify-between mb-4">
                    <div
                      className={`w-12 h-12 ${category.color} rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform`}
                    >
                      <category.icon className="w-6 h-6 text-white" />
                    </div>
                    <Badge variant="muted" className="text-xs">
                      {category.count} scholarships
                    </Badge>
                  </div>
                  <CardTitle className="text-title font-semibold text-slate-900 group-hover:text-indigo-600 transition-colors">
                    {category.name}
                  </CardTitle>
                  <CardDescription className="text-slate-600">
                    {category.description}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <Button
                    variant="outline"
                    className="w-full group-hover:bg-indigo-50 group-hover:border-indigo-200 group-hover:text-indigo-700"
                  >
                    View Scholarships
                    <ArrowRight className="w-4 h-4 ml-2" />
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>

          <div className="mt-16 text-center">
            <div className="max-w-3xl mx-auto">
              <h3 className="text-title font-semibold text-slate-900 mb-4">
                Can&apos;t find what you&apos;re looking for?
              </h3>
              <p className="text-slate-600 mb-8">
                Browse all available scholarships or contact our support team
                for personalized assistance.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Button size="lg" className="bg-gradient-primary">
                  <Search className="w-5 h-5 mr-2" />
                  Browse All Scholarships
                </Button>
                <Button size="lg" variant="outline">
                  <Filter className="w-5 h-5 mr-2" />
                  Advanced Search
                </Button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
}
