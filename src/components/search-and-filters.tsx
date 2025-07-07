"use client";

import React, { useState, useEffect } from "react";
import { Search, X, SlidersHorizontal } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { cn } from "@/lib/utils";

export interface FilterOptions {
  categories: string[];
  levels: string[];
  states: string[];
  amounts: { min: number; max: number }[];
  deadlines: string[];
}

export interface ActiveFilters {
  query: string;
  category: string;
  level: string;
  state: string;
  amountRange: string;
  deadline: string;
  sortBy: string;
}

export interface SearchAndFiltersProps {
  onSearch: (filters: ActiveFilters) => void;
  onFilterChange: (filters: ActiveFilters) => void;
  loading?: boolean;
  resultCount?: number;
  className?: string;
  defaultFilters?: Partial<ActiveFilters>;
  filterOptions?: FilterOptions;
}

const defaultFilterOptions: FilterOptions = {
  categories: [
    "Government",
    "Merit-based",
    "Need-based",
    "SC/ST/OBC",
    "Women",
    "Minority",
    "Disabled",
    "Sports",
    "Arts",
    "Science",
    "Engineering",
    "Medical",
    "MBA",
    "PhD",
  ],
  levels: [
    "School",
    "Higher Secondary",
    "Undergraduate",
    "Postgraduate",
    "PhD",
    "All Levels",
  ],
  states: [
    "All India",
    "Andhra Pradesh",
    "Arunachal Pradesh",
    "Assam",
    "Bihar",
    "Chhattisgarh",
    "Goa",
    "Gujarat",
    "Haryana",
    "Himachal Pradesh",
    "Jharkhand",
    "Karnataka",
    "Kerala",
    "Madhya Pradesh",
    "Maharashtra",
    "Manipur",
    "Meghalaya",
    "Mizoram",
    "Nagaland",
    "Odisha",
    "Punjab",
    "Rajasthan",
    "Sikkim",
    "Tamil Nadu",
    "Telangana",
    "Tripura",
    "Uttar Pradesh",
    "Uttarakhand",
    "West Bengal",
    "Delhi",
    "Jammu and Kashmir",
    "Ladakh",
    "Puducherry",
  ],
  amounts: [
    { min: 0, max: 10000 },
    { min: 10000, max: 25000 },
    { min: 25000, max: 50000 },
    { min: 50000, max: 100000 },
    { min: 100000, max: 999999 },
  ],
  deadlines: [
    "This Week",
    "This Month",
    "Next Month",
    "Next 3 Months",
    "Next 6 Months",
    "No Deadline",
  ],
};

const sortOptions = [
  { value: "relevance", label: "Most Relevant" },
  { value: "deadline", label: "Deadline (Soon)" },
  { value: "amount-high", label: "Amount (High to Low)" },
  { value: "amount-low", label: "Amount (Low to High)" },
  { value: "popularity", label: "Most Popular" },
  { value: "newest", label: "Newest First" },
];

export function SearchAndFilters({
  onSearch,
  onFilterChange,
  loading = false,
  resultCount = 0,
  className,
  defaultFilters = {},
  filterOptions = defaultFilterOptions,
}: SearchAndFiltersProps) {
  const [isFiltersOpen, setIsFiltersOpen] = useState(false);
  const [filters, setFilters] = useState<ActiveFilters>({
    query: "",
    category: "",
    level: "",
    state: "",
    amountRange: "",
    deadline: "",
    sortBy: "relevance",
    ...defaultFilters,
  });

  const [searchQuery, setSearchQuery] = useState(filters.query);

  useEffect(() => {
    onFilterChange(filters);
  }, [filters, onFilterChange]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    const updatedFilters = { ...filters, query: searchQuery };
    setFilters(updatedFilters);
    onSearch(updatedFilters);
  };

  const handleFilterChange = (key: keyof ActiveFilters, value: string) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
  };

  const clearFilter = (key: keyof ActiveFilters) => {
    setFilters((prev) => ({ ...prev, [key]: "" }));
  };

  const clearAllFilters = () => {
    setFilters({
      query: "",
      category: "",
      level: "",
      state: "",
      amountRange: "",
      deadline: "",
      sortBy: "relevance",
    });
    setSearchQuery("");
  };

  const getActiveFiltersCount = () => {
    return Object.entries(filters).filter(
      ([key, value]) => key !== "query" && key !== "sortBy" && value !== ""
    ).length;
  };

  const getAmountRangeLabel = (value: string) => {
    const range = filterOptions.amounts.find(
      (_, index) => index.toString() === value
    );
    if (!range) return "";
    if (range.max === 999999) return `₹${range.min.toLocaleString()}+`;
    return `₹${range.min.toLocaleString()} - ₹${range.max.toLocaleString()}`;
  };

  const activeFiltersCount = getActiveFiltersCount();

  return (
    <div className={cn("space-y-4", className)}>
      {/* Search Bar */}
      <Card>
        <CardContent className="p-4">
          <form onSubmit={handleSearch} className="flex gap-2">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search scholarships, categories, or eligibility criteria..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10"
              />
            </div>
            <Button type="submit" disabled={loading}>
              {loading ? "Searching..." : "Search"}
            </Button>
            <Button
              type="button"
              variant="outline"
              onClick={() => setIsFiltersOpen(!isFiltersOpen)}
              className="relative"
            >
              <SlidersHorizontal className="h-4 w-4 mr-2" />
              Filters
              {activeFiltersCount > 0 && (
                <Badge
                  variant="secondary"
                  className="absolute -top-2 -right-2 h-5 w-5 p-0 flex items-center justify-center text-xs"
                >
                  {activeFiltersCount}
                </Badge>
              )}
            </Button>
          </form>
        </CardContent>
      </Card>

      {/* Active Filters */}
      {(filters.query || activeFiltersCount > 0) && (
        <div className="flex flex-wrap gap-2 items-center">
          <span className="text-sm text-muted-foreground">Active filters:</span>
          {filters.query && (
            <Badge variant="secondary" className="flex items-center gap-1">
              Search: &quot;{filters.query}&quot;
              <X
                className="h-3 w-3 cursor-pointer"
                onClick={() => {
                  setFilters((prev) => ({ ...prev, query: "" }));
                  setSearchQuery("");
                }}
              />
            </Badge>
          )}
          {filters.category && (
            <Badge variant="secondary" className="flex items-center gap-1">
              Category: {filters.category}
              <X
                className="h-3 w-3 cursor-pointer"
                onClick={() => clearFilter("category")}
              />
            </Badge>
          )}
          {filters.level && (
            <Badge variant="secondary" className="flex items-center gap-1">
              Level: {filters.level}
              <X
                className="h-3 w-3 cursor-pointer"
                onClick={() => clearFilter("level")}
              />
            </Badge>
          )}
          {filters.state && (
            <Badge variant="secondary" className="flex items-center gap-1">
              State: {filters.state}
              <X
                className="h-3 w-3 cursor-pointer"
                onClick={() => clearFilter("state")}
              />
            </Badge>
          )}
          {filters.amountRange && (
            <Badge variant="secondary" className="flex items-center gap-1">
              Amount: {getAmountRangeLabel(filters.amountRange)}
              <X
                className="h-3 w-3 cursor-pointer"
                onClick={() => clearFilter("amountRange")}
              />
            </Badge>
          )}
          {filters.deadline && (
            <Badge variant="secondary" className="flex items-center gap-1">
              Deadline: {filters.deadline}
              <X
                className="h-3 w-3 cursor-pointer"
                onClick={() => clearFilter("deadline")}
              />
            </Badge>
          )}
          {(filters.query || activeFiltersCount > 0) && (
            <Button
              variant="ghost"
              size="sm"
              onClick={clearAllFilters}
              className="h-6 text-xs"
            >
              Clear All
            </Button>
          )}
        </div>
      )}

      {/* Results Count and Sort */}
      <div className="flex justify-between items-center">
        <div className="text-sm text-muted-foreground">
          {resultCount > 0 && (
            <span>
              {resultCount.toLocaleString()} scholarship
              {resultCount !== 1 ? "s" : ""} found
            </span>
          )}
        </div>
        <div className="flex items-center gap-2">
          <span className="text-sm text-muted-foreground">Sort by:</span>
          <Select
            value={filters.sortBy}
            onValueChange={(value) => handleFilterChange("sortBy", value)}
          >
            <SelectTrigger className="w-40">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {sortOptions.map((option) => (
                <SelectItem key={option.value} value={option.value}>
                  {option.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      </div>

      {/* Filters Panel */}
      {isFiltersOpen && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <span>Advanced Filters</span>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setIsFiltersOpen(false)}
              >
                <X className="h-4 w-4" />
              </Button>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div>
                <label className="text-sm font-medium mb-2 block">
                  Category
                </label>
                <Select
                  value={filters.category}
                  onValueChange={(value) =>
                    handleFilterChange("category", value)
                  }
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select category" />
                  </SelectTrigger>
                  <SelectContent>
                    {filterOptions.categories.map((category) => (
                      <SelectItem key={category} value={category}>
                        {category}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div>
                <label className="text-sm font-medium mb-2 block">
                  Education Level
                </label>
                <Select
                  value={filters.level}
                  onValueChange={(value) => handleFilterChange("level", value)}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select level" />
                  </SelectTrigger>
                  <SelectContent>
                    {filterOptions.levels.map((level) => (
                      <SelectItem key={level} value={level}>
                        {level}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div>
                <label className="text-sm font-medium mb-2 block">State</label>
                <Select
                  value={filters.state}
                  onValueChange={(value) => handleFilterChange("state", value)}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select state" />
                  </SelectTrigger>
                  <SelectContent>
                    {filterOptions.states.map((state) => (
                      <SelectItem key={state} value={state}>
                        {state}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div>
                <label className="text-sm font-medium mb-2 block">
                  Amount Range
                </label>
                <Select
                  value={filters.amountRange}
                  onValueChange={(value) =>
                    handleFilterChange("amountRange", value)
                  }
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select amount range" />
                  </SelectTrigger>
                  <SelectContent>
                    {filterOptions.amounts.map((range, index) => (
                      <SelectItem key={index} value={index.toString()}>
                        {range.max === 999999
                          ? `₹${range.min.toLocaleString()}+`
                          : `₹${range.min.toLocaleString()} - ₹${range.max.toLocaleString()}`}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div>
                <label className="text-sm font-medium mb-2 block">
                  Deadline
                </label>
                <Select
                  value={filters.deadline}
                  onValueChange={(value) =>
                    handleFilterChange("deadline", value)
                  }
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select deadline" />
                  </SelectTrigger>
                  <SelectContent>
                    {filterOptions.deadlines.map((deadline) => (
                      <SelectItem key={deadline} value={deadline}>
                        {deadline}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

export default SearchAndFilters;
