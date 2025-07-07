"use client";

import Link from "next/link";
import { useTrendingScholarships } from "@/hooks/useApi";
import { LoadingSpinner } from "@/components/ui/loading-spinner";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import Navigation from "@/components/navigation";
import { Footer } from "@/components/navigation";
import {
  Award,
  Users,
  Target,
  TrendingUp,
  CheckCircle,
  ArrowRight,
  BookOpen,
  Calendar,
  IndianRupee,
  Star,
  Shield,
  Clock,
  Globe,
} from "lucide-react";
// Utils are defined locally in the component

// Statistics data
const STATS = [
  { label: "Active Scholarships", value: "2,500+", icon: Award },
  { label: "Students Helped", value: "50,000+", icon: Users },
  { label: "Success Rate", value: "85%", icon: Target },
  { label: "Amount Distributed", value: "₹250 Cr+", icon: TrendingUp },
];

// Features data
const FEATURES = [
  {
    icon: Shield,
    title: "Verified Scholarships",
    description:
      "All scholarships are verified from trusted government and private sources.",
  },
  {
    icon: BookOpen,
    title: "Easy Application",
    description:
      "Streamlined application process with step-by-step guidance and support.",
  },
  {
    icon: Clock,
    title: "Real-time Updates",
    description:
      "Get instant notifications about new scholarships and deadline reminders.",
  },
  {
    icon: Globe,
    title: "All India Coverage",
    description:
      "Scholarships from central, state governments, and private organizations.",
  },
];

export default function HomePage() {
  const stats = STATS;

  // Use API hook to fetch trending scholarships
  const { data: trendingResponse, isLoading: trendingLoading } =
    useTrendingScholarships();
  const trendingScholarships = trendingResponse?.success
    ? trendingResponse.data.slice(0, 3)
    : [];

  const formatAmount = (amount: number) => {
    if (amount >= 100000) {
      return `₹${(amount / 100000).toFixed(1)}L`;
    } else if (amount >= 1000) {
      return `₹${(amount / 1000).toFixed(1)}K`;
    } else {
      return `₹${amount.toLocaleString()}`;
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-IN", {
      year: "numeric",
      month: "short",
      day: "numeric",
    });
  };

  const getDaysUntilDeadline = (deadline: string) => {
    const now = new Date();
    const deadlineDate = new Date(deadline);
    const diffTime = deadlineDate.getTime() - now.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays;
  };

  return (
    <div className="min-h-screen bg-white">
      <Navigation />

      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-slate-50 via-gray-50 to-zinc-50 pt-16 pb-20">
        <div className="absolute inset-0 bg-grid-pattern opacity-5"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <div className="flex justify-center items-center mb-6">
              <div className="flex items-center space-x-2">
                <Award className="w-8 h-8 text-indigo-600" />
                <Badge
                  variant="secondary"
                  className="bg-indigo-100 text-indigo-800"
                >
                  India&apos;s #1 Scholarship Portal
                </Badge>
              </div>
            </div>

            <h1 className="text-display font-extrabold text-slate-900 mb-6 leading-tight">
              Find Your Perfect
              <span className="block text-gradient-primary">Scholarship</span>
            </h1>

            <p className="text-subtitle text-slate-600 mb-8 max-w-3xl mx-auto">
              Discover thousands of verified scholarships from trusted sources.
              Apply with confidence and secure your educational future.
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button
                size="lg"
                className="bg-gradient-primary shadow-primary px-8"
                asChild
              >
                <Link href="/scholarships">
                  <BookOpen className="w-5 h-5 mr-2" />
                  Browse Scholarships
                </Link>
              </Button>
              <Button
                size="lg"
                variant="outline"
                className="border-slate-200 text-slate-700 hover:bg-slate-50 px-8"
                asChild
              >
                <Link href="/auth/signup">
                  <Users className="w-5 h-5 mr-2" />
                  Create Account
                </Link>
              </Button>{" "}
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <div key={index} className="text-center">
                <div className="flex justify-center mb-4">
                  <div className="w-12 h-12 bg-gradient-to-r from-indigo-100 to-purple-100 rounded-lg flex items-center justify-center">
                    <stat.icon className="w-6 h-6 text-indigo-600" />
                  </div>
                </div>
                <div className="text-2xl md:text-3xl font-bold text-slate-900 mb-2">
                  {stat.value}
                </div>
                <div className="text-sm text-slate-600">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Featured Scholarships */}
      <section className="py-16 bg-slate-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-headline font-bold text-slate-900 mb-4">
              Featured Scholarships
            </h2>
            <p className="text-subtitle text-slate-600">
              Discover the most popular and high-value scholarships available
              right now
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {trendingLoading ? (
              <div className="col-span-full flex justify-center py-8">
                <LoadingSpinner size="lg" />
              </div>
            ) : (
              trendingScholarships.map((scholarship) => (
                <Card
                  key={scholarship.id}
                  className="hover:shadow-medium transition-shadow duration-300"
                >
                  <CardHeader className="pb-4">
                    <div className="flex items-center justify-between mb-2">
                      <Badge variant="secondary" className="text-xs">
                        {scholarship.category}
                      </Badge>
                      <div className="flex items-center space-x-1">
                        {scholarship.verified && (
                          <Badge variant="success" className="text-xs">
                            <CheckCircle className="w-3 h-3 mr-1" />
                            Verified
                          </Badge>
                        )}
                        {scholarship.trending && (
                          <Badge variant="info" className="text-xs">
                            <TrendingUp className="w-3 h-3 mr-1" />
                            Trending
                          </Badge>
                        )}
                      </div>
                    </div>
                    <CardTitle className="text-lg font-semibold line-clamp-2">
                      {scholarship.title}
                    </CardTitle>
                    <CardDescription className="text-sm text-slate-600">
                      {scholarship.provider}
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-slate-700 mb-4 line-clamp-2">
                      {scholarship.description}
                    </p>

                    <div className="grid grid-cols-2 gap-4 mb-4">
                      <div className="flex items-center space-x-2">
                        <IndianRupee className="w-4 h-4 text-emerald-600" />
                        <span className="text-sm font-semibold text-emerald-600">
                          {formatAmount(scholarship.amount)}
                        </span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Calendar className="w-4 h-4 text-slate-500" />
                        <span className="text-sm text-slate-600">
                          {formatDate(scholarship.deadline)}
                        </span>
                      </div>
                    </div>

                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-1">
                        <Clock className="w-4 h-4 text-amber-500" />
                        <span className="text-sm text-amber-600 font-medium">
                          {getDaysUntilDeadline(scholarship.deadline)} days left
                        </span>
                      </div>
                      <Link href={`/scholarships/${scholarship.id}`}>
                        <Button size="sm" className="bg-gradient-primary">
                          Apply Now
                          <ArrowRight className="w-4 h-4 ml-1" />
                        </Button>
                      </Link>
                    </div>
                  </CardContent>
                </Card>
              ))
            )}
          </div>

          <div className="text-center mt-12">
            <Button
              size="lg"
              variant="outline"
              className="border-indigo-200 text-indigo-700 hover:bg-indigo-50"
              asChild
            >
              <Link href="/scholarships">
                View All Scholarships
                <ArrowRight className="w-5 h-5 ml-2" />
              </Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-slate-900 mb-4">
              Why Choose ShikshaSetu?
            </h2>
            <p className="text-lg text-slate-600">
              Your trusted partner in finding and applying for scholarships
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {FEATURES.map((feature, index) => (
              <div key={index} className="text-center">
                <div className="flex justify-center mb-4">
                  <div className="w-16 h-16 bg-gradient-to-r from-indigo-100 to-purple-100 rounded-2xl flex items-center justify-center">
                    <feature.icon className="w-8 h-8 text-indigo-600" />
                  </div>
                </div>
                <h3 className="text-xl font-semibold text-slate-900 mb-2">
                  {feature.title}
                </h3>
                <p className="text-slate-600 text-sm leading-relaxed">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-gradient-to-r from-indigo-600 to-purple-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <Star className="w-12 h-12 text-white mx-auto mb-6" />
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
            Start Your Scholarship Journey Today
          </h2>
          <p className="text-xl text-indigo-100 mb-8 max-w-2xl mx-auto">
            Join thousands of students who have successfully secured
            scholarships through ShikshaSetu
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button
              size="lg"
              variant="secondary"
              className="bg-white text-indigo-600 hover:bg-indigo-50 px-8"
              asChild
            >
              <Link href="/auth/signup">
                Get Started Free
                <ArrowRight className="w-5 h-5 ml-2" />
              </Link>
            </Button>
            <Button
              size="lg"
              variant="outline"
              className="border-white text-white hover:bg-white hover:text-indigo-600 px-8"
              asChild
            >
              <Link href="/scholarships">Browse Scholarships</Link>
            </Button>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
}
