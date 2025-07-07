"use client";

import { useState, useMemo } from "react";
import { useScholarships } from "@/hooks/useApi";
import { LoadingSpinner } from "@/components/ui/loading-spinner";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { AlertCircle } from "lucide-react";
import Link from "next/link";
import {
  Search,
  SlidersHorizontal,
  Calendar,
  MapPin,
  GraduationCap,
  IndianRupee,
  Clock,
  Eye,
  Heart,
  Share2,
  ChevronDown,
  ChevronUp,
  CheckCircle,
  ArrowRight,
  BookOpen,
  TrendingUp,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import Navigation from "@/components/navigation";
import {
  cn,
  formatDate,
  getDaysUntilDeadline,
  getDeadlineStatusWithColors,
} from "@/lib/utils";

const CATEGORIES = [
  "All Categories",
  "Engineering",
  "Medical",
  "Arts & Humanities",
  "Science",
  "Commerce",
  "Law",
  "Education",
  "Agriculture",
  "Management",
  "Social Sciences",
  "Other",
];

const SCHOLARSHIP_TYPES = [
  "All Types",
  "Merit Based",
  "Need Based",
  "Minority",
  "Sports",
  "Arts",
  "Research",
  "International",
  "State Government",
  "Central Government",
  "Private",
];

const SORT_OPTIONS = [
  { label: "Most Relevant", value: "relevance" },
  { label: "Application Deadline", value: "deadline" },
  { label: "Amount (High to Low)", value: "amount_desc" },
  { label: "Amount (Low to High)", value: "amount_asc" },
  { label: "Recently Added", value: "newest" },
  { label: "Most Popular", value: "popular" },
];

export default function SearchPage() {
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("All Categories");
  const [selectedType, setSelectedType] = useState("All Types");
  const [sortBy, setSortBy] = useState("relevance");
  const [showFilters, setShowFilters] = useState(false);
  const [savedScholarships, setSavedScholarships] = useState<Set<number>>(
    new Set()
  );

  // Use API hook to fetch scholarships
  const {
    data: scholarshipsResponse,
    isLoading,
    error,
  } = useScholarships({
    category:
      selectedCategory === "All Categories" ? undefined : selectedCategory,
    search: searchTerm || undefined,
    sort: sortBy,
  });

  const scholarships = scholarshipsResponse?.success
    ? scholarshipsResponse.data
    : [];

  // Filter scholarships based on search and filters
  const filteredScholarships = scholarships.filter((scholarship) => {
    const matchesType =
      selectedType === "All Types" ||
      scholarship.category === selectedType ||
      scholarship.tags?.some((tag) =>
        tag.toLowerCase().includes(selectedType.toLowerCase())
      );

    return matchesType;
  });

  // Sort scholarships (API handles most sorting, this is for local refinement)
  const sortedScholarships = [...filteredScholarships].sort((a, b) => {
    switch (sortBy) {
      case "deadline":
        return new Date(a.deadline).getTime() - new Date(b.deadline).getTime();
      case "amount_desc":
        return b.amount - a.amount;
      case "amount_asc":
        return a.amount - b.amount;
      case "popular":
        return (b.views || 0) - (a.views || 0);
      default:
        return 0;
    }
  });

  const handleSaveScholarship = (id: number) => {
    setSavedScholarships((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(id)) {
        newSet.delete(id);
      } else {
        newSet.add(id);
      }
      return newSet;
    });
  };

  const formatAmount = (amount: number) => {
    if (amount >= 100000) {
      return `₹${(amount / 100000).toFixed(1)}L`;
    } else if (amount >= 1000) {
      return `₹${(amount / 1000).toFixed(1)}K`;
    } else {
      return `₹${amount.toLocaleString()}`;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation />

      {/* Loading State */}
      {isLoading && (
        <div className="container mx-auto px-4 py-12">
          <div className="flex items-center justify-center">
            <LoadingSpinner size="lg" />
            <span className="ml-3 text-gray-600">Loading scholarships...</span>
          </div>
        </div>
      )}

      {/* Error State */}
      {error && !isLoading && (
        <div className="container mx-auto px-4 py-12">
          <Alert className="max-w-2xl mx-auto">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>
              Failed to load scholarships. Please try again later.
            </AlertDescription>
          </Alert>
        </div>
      )}

      {/* Content */}
      {!isLoading && !error && (
        <div>
          {/* Header */}
          <div className="bg-white border-b border-gray-200 shadow-sm">
            <div className="container mx-auto px-4 py-6">
              <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
                <div>
                  <h1 className="text-2xl font-bold text-gray-900">
                    Scholarship Search
                  </h1>
                  <p className="text-gray-600 mt-1">
                    Discover {sortedScholarships.length} verified scholarships
                    from trusted sources
                  </p>
                </div>

                {/* Search Bar */}
                <div className="relative flex-1 max-w-2xl">
                  <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
                  <Input
                    placeholder="Search scholarships, providers, or keywords..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-12 pr-4 py-3 text-base border-2 border-gray-200 focus:border-blue-500 rounded-lg"
                  />
                </div>
              </div>
            </div>
          </div>

          <div className="container mx-auto px-4 py-6">
            <div className="flex flex-col lg:flex-row gap-6">
              {/* Filters Sidebar */}
              <div className="lg:w-80">
                <div className="lg:sticky lg:top-6">
                  {/* Mobile Filter Toggle */}
                  <div className="lg:hidden mb-4">
                    <Button
                      variant="outline"
                      onClick={() => setShowFilters(!showFilters)}
                      className="w-full flex items-center justify-between"
                    >
                      <span className="flex items-center gap-2">
                        <SlidersHorizontal className="h-4 w-4" />
                        Filters
                      </span>
                      {showFilters ? (
                        <ChevronUp className="h-4 w-4" />
                      ) : (
                        <ChevronDown className="h-4 w-4" />
                      )}
                    </Button>
                  </div>

                  {/* Filter Panel */}
                  <div
                    className={cn(
                      "space-y-6 lg:block",
                      showFilters ? "block" : "hidden"
                    )}
                  >
                    {/* Category Filter */}
                    <Card>
                      <CardHeader className="pb-3">
                        <CardTitle className="text-sm font-medium text-gray-900">
                          Category
                        </CardTitle>
                      </CardHeader>
                      <CardContent className="pt-0">
                        <div className="space-y-2">
                          {CATEGORIES.map((category) => (
                            <button
                              key={category}
                              onClick={() => setSelectedCategory(category)}
                              className={cn(
                                "w-full text-left px-3 py-2 rounded-md text-sm transition-colors",
                                selectedCategory === category
                                  ? "bg-blue-100 text-blue-700 font-medium"
                                  : "text-gray-600 hover:bg-gray-100"
                              )}
                            >
                              {category}
                            </button>
                          ))}
                        </div>
                      </CardContent>
                    </Card>

                    {/* Type Filter */}
                    <Card>
                      <CardHeader className="pb-3">
                        <CardTitle className="text-sm font-medium text-gray-900">
                          Type
                        </CardTitle>
                      </CardHeader>
                      <CardContent className="pt-0">
                        <div className="space-y-2">
                          {SCHOLARSHIP_TYPES.map((type) => (
                            <button
                              key={type}
                              onClick={() => setSelectedType(type)}
                              className={cn(
                                "w-full text-left px-3 py-2 rounded-md text-sm transition-colors",
                                selectedType === type
                                  ? "bg-blue-100 text-blue-700 font-medium"
                                  : "text-gray-600 hover:bg-gray-100"
                              )}
                            >
                              {type}
                            </button>
                          ))}
                        </div>
                      </CardContent>
                    </Card>
                  </div>
                </div>
              </div>

              {/* Results */}
              <div className="flex-1">
                {/* Sort Options */}
                <div className="flex items-center justify-between mb-6">
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-medium text-gray-900">
                      Sort by:
                    </span>
                    <select
                      value={sortBy}
                      onChange={(e) => setSortBy(e.target.value)}
                      className="text-sm border border-gray-300 rounded-lg px-3 py-2 bg-white"
                    >
                      {SORT_OPTIONS.map((option) => (
                        <option key={option.value} value={option.value}>
                          {option.label}
                        </option>
                      ))}
                    </select>
                  </div>
                  <div className="text-sm text-gray-500">
                    {sortedScholarships.length} results found
                  </div>
                </div>

                {/* No Results */}
                {sortedScholarships.length === 0 && (
                  <div className="text-center py-12">
                    <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                      <BookOpen className="h-8 w-8 text-gray-400" />
                    </div>
                    <h3 className="text-lg font-medium text-gray-900 mb-2">
                      No scholarships found
                    </h3>
                    <p className="text-gray-600 max-w-md mx-auto">
                      Try adjusting your search terms or filters to find more
                      scholarships.
                    </p>
                  </div>
                )}

                {/* Scholarship Cards */}
                <div className="space-y-4">
                  {sortedScholarships.map((scholarship) => (
                    <Card
                      key={scholarship.id}
                      className="hover:shadow-md transition-shadow"
                    >
                      <CardContent className="p-6">
                        <div className="flex items-start justify-between mb-4">
                          <div className="flex-1">
                            <div className="flex items-center gap-2 mb-2">
                              {scholarship.verified && (
                                <CheckCircle className="h-5 w-5 text-green-500" />
                              )}
                              {scholarship.trending && (
                                <TrendingUp className="h-5 w-5 text-orange-500" />
                              )}
                              <Link
                                href={`/scholarships/${scholarship.id}`}
                                className="text-lg font-semibold text-gray-900 hover:text-blue-600 transition-colors"
                              >
                                {scholarship.title}
                              </Link>
                            </div>
                            <p className="text-sm text-gray-600 mb-3">
                              {scholarship.provider}
                            </p>
                            <p className="text-sm text-gray-700 mb-4 line-clamp-2">
                              {scholarship.description}
                            </p>
                          </div>
                          <div className="flex items-center gap-2 ml-4">
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() =>
                                handleSaveScholarship(scholarship.id)
                              }
                            >
                              <Heart
                                className={cn(
                                  "h-4 w-4",
                                  savedScholarships.has(scholarship.id)
                                    ? "fill-red-500 text-red-500"
                                    : "text-gray-400"
                                )}
                              />
                            </Button>
                            <Button variant="ghost" size="sm">
                              <Share2 className="h-4 w-4 text-gray-400" />
                            </Button>
                          </div>
                        </div>

                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-4 text-sm text-gray-600">
                            <div className="flex items-center gap-1">
                              <IndianRupee className="h-4 w-4" />
                              <span className="font-medium">
                                {formatAmount(scholarship.amount)}
                              </span>
                            </div>
                            <div className="flex items-center gap-1">
                              <Calendar className="h-4 w-4" />
                              <span>{formatDate(scholarship.deadline)}</span>
                            </div>
                            <div className="flex items-center gap-1">
                              <MapPin className="h-4 w-4" />
                              <span>{scholarship.location}</span>
                            </div>
                          </div>
                          <div className="flex items-center gap-2">
                            <Badge variant="secondary">
                              {scholarship.category}
                            </Badge>
                            <Link href={`/scholarships/${scholarship.id}`}>
                              <Button size="sm">
                                View Details
                                <ArrowRight className="h-4 w-4 ml-1" />
                              </Button>
                            </Link>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>

                {/* Load More */}
                {sortedScholarships.length > 0 && (
                  <div className="text-center mt-8">
                    <Button variant="outline" size="lg" className="px-8">
                      Load More Scholarships
                    </Button>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
