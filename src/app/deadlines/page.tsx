"use client";

import { useState } from "react";
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
  Calendar,
  Clock,
  AlertCircle,
  CheckCircle,
  ArrowRight,
  IndianRupee,
  BookOpen,
} from "lucide-react";

const UPCOMING_DEADLINES = [
  {
    id: 1,
    title: "Prime Minister's Special Scholarship Scheme",
    provider: "All India Council for Technical Education (AICTE)",
    amount: 125000,
    deadline: "2025-01-15",
    daysLeft: 10,
    category: "Need Based",
    urgency: "high",
  },
  {
    id: 2,
    title: "National Scholarship Portal - Merit Scholarship",
    provider: "Ministry of Education, Government of India",
    amount: 12000,
    deadline: "2025-03-31",
    daysLeft: 85,
    category: "Merit Based",
    urgency: "medium",
  },
  {
    id: 3,
    title: "INSPIRE Scholarship for Higher Education",
    provider: "Department of Science and Technology",
    amount: 80000,
    deadline: "2025-04-30",
    daysLeft: 115,
    category: "Research",
    urgency: "low",
  },
  {
    id: 4,
    title: "Minority Scholarship Scheme",
    provider: "Ministry of Minority Affairs",
    amount: 25000,
    deadline: "2025-02-28",
    daysLeft: 54,
    category: "Minority",
    urgency: "medium",
  },
  {
    id: 5,
    title: "Sports Scholarship Program",
    provider: "Sports Authority of India",
    amount: 50000,
    deadline: "2025-01-31",
    daysLeft: 26,
    category: "Sports",
    urgency: "high",
  },
];

export default function DeadlinesPage() {
  const [filter, setFilter] = useState<"all" | "high" | "medium" | "low">(
    "all"
  );

  const formatAmount = (amount: number) => {
    if (amount >= 100000) {
      return `₹${(amount / 100000).toFixed(1)}L`;
    } else if (amount >= 1000) {
      return `₹${(amount / 1000).toFixed(1)}K`;
    } else {
      return `₹${amount.toLocaleString()}`;
    }
  };

  const getUrgencyColor = (urgency: string) => {
    switch (urgency) {
      case "high":
        return "bg-red-500";
      case "medium":
        return "bg-amber-500";
      case "low":
        return "bg-emerald-500";
      default:
        return "bg-slate-500";
    }
  };

  const getUrgencyBadge = (urgency: string) => {
    switch (urgency) {
      case "high":
        return (
          <Badge variant="destructive" className="text-xs">
            High Priority
          </Badge>
        );
      case "medium":
        return (
          <Badge variant="warning" className="text-xs">
            Medium Priority
          </Badge>
        );
      case "low":
        return (
          <Badge variant="success" className="text-xs">
            Low Priority
          </Badge>
        );
      default:
        return (
          <Badge variant="muted" className="text-xs">
            Unknown
          </Badge>
        );
    }
  };

  const filteredDeadlines =
    filter === "all"
      ? UPCOMING_DEADLINES
      : UPCOMING_DEADLINES.filter((d) => d.urgency === filter);

  return (
    <div className="min-h-screen bg-white">
      <Navigation />

      <PageHeader
        title="Upcoming Deadlines"
        description="Stay on top of important scholarship application deadlines"
      />

      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Filter Buttons */}
          <div className="flex flex-wrap gap-4 mb-8">
            <Button
              variant={filter === "all" ? "default" : "outline"}
              onClick={() => setFilter("all")}
              size="sm"
            >
              All Deadlines
            </Button>
            <Button
              variant={filter === "high" ? "default" : "outline"}
              onClick={() => setFilter("high")}
              size="sm"
            >
              <AlertCircle className="w-4 h-4 mr-2" />
              High Priority
            </Button>
            <Button
              variant={filter === "medium" ? "default" : "outline"}
              onClick={() => setFilter("medium")}
              size="sm"
            >
              <Clock className="w-4 h-4 mr-2" />
              Medium Priority
            </Button>
            <Button
              variant={filter === "low" ? "default" : "outline"}
              onClick={() => setFilter("low")}
              size="sm"
            >
              <CheckCircle className="w-4 h-4 mr-2" />
              Low Priority
            </Button>
          </div>

          {/* Deadlines List */}
          <div className="space-y-6">
            {filteredDeadlines.map((scholarship) => (
              <Card
                key={scholarship.id}
                className="hover:shadow-medium transition-shadow"
              >
                <CardHeader className="pb-4">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <div
                          className={`w-3 h-3 rounded-full ${getUrgencyColor(
                            scholarship.urgency
                          )}`}
                        />
                        <CardTitle className="text-lg font-semibold text-slate-900">
                          {scholarship.title}
                        </CardTitle>
                      </div>
                      <CardDescription className="text-slate-600">
                        {scholarship.provider}
                      </CardDescription>
                    </div>
                    <div className="flex flex-col items-end gap-2">
                      {getUrgencyBadge(scholarship.urgency)}
                      <Badge variant="secondary" className="text-xs">
                        {scholarship.category}
                      </Badge>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
                    <div className="flex items-center space-x-2">
                      <IndianRupee className="w-4 h-4 text-emerald-600" />
                      <span className="text-sm font-semibold text-emerald-600">
                        {formatAmount(scholarship.amount)}
                      </span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Calendar className="w-4 h-4 text-slate-500" />
                      <span className="text-sm text-slate-600">
                        {scholarship.deadline}
                      </span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Clock className="w-4 h-4 text-amber-500" />
                      <span className="text-sm text-amber-600 font-medium">
                        {scholarship.daysLeft} days left
                      </span>
                    </div>
                    <div className="flex justify-end">
                      <Button size="sm" className="bg-gradient-primary">
                        <BookOpen className="w-4 h-4 mr-2" />
                        View Details
                        <ArrowRight className="w-4 h-4 ml-2" />
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {filteredDeadlines.length === 0 && (
            <div className="text-center py-12">
              <Clock className="w-16 h-16 text-slate-400 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-slate-900 mb-2">
                No deadlines found
              </h3>
              <p className="text-slate-600">
                No scholarships match your current filter. Try adjusting your
                selection.
              </p>
            </div>
          )}
        </div>
      </section>

      <Footer />
    </div>
  );
}
