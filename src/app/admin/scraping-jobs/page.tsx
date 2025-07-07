"use client";

import { useState } from "react";
import { useScrapingJobs } from "@/hooks/useApi";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { LoadingSpinner } from "@/components/ui/loading-spinner";
import Navigation, { PageHeader } from "@/components/navigation";
import { Footer } from "@/components/navigation";
import { Alert, AlertDescription } from "@/components/ui/alert";
import {
  Square,
  RefreshCw,
  Clock,
  CheckCircle,
  XCircle,
  AlertCircle,
  Database,
  Search,
  Eye,
  RotateCcw,
} from "lucide-react";

export default function ScrapingJobsPage() {
  const [filters, setFilters] = useState({
    status: "all",
    source: "all",
    search: "",
  });

  // Use API hooks to fetch and manage scraping jobs
  const {
    data: jobsResponse,
    isLoading: loading,
    error: jobsError,
  } = useScrapingJobs({
    status: filters.status !== "all" ? filters.status : undefined,
    source: filters.source !== "all" ? filters.source : undefined,
  });

  const jobs = jobsResponse?.success ? jobsResponse.data : [];
  const errorMessage =
    jobsError?.message ||
    (jobsResponse?.success === false ? jobsResponse.message : null);

  // Simple handler functions (API integration can be added later)
  const handleRefresh = () => {
    // This will be handled by React Query's refetch
  };

  const startNewJob = (sourceUrl: string, sourceName: string) => {
    console.log(`Starting job for ${sourceName}: ${sourceUrl}`);
    // TODO: Implement with API mutation
  };

  const cancelJob = (jobId: string) => {
    console.log(`Cancelling job: ${jobId}`);
    // TODO: Implement with API mutation
  };

  const retryJob = (jobId: string) => {
    console.log(`Retrying job: ${jobId}`);
    // TODO: Implement with API mutation
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "pending":
        return <Badge variant="secondary">Pending</Badge>;
      case "running":
        return <Badge className="bg-blue-100 text-blue-800">Running</Badge>;
      case "completed":
        return (
          <Badge className="bg-emerald-100 text-emerald-800">Completed</Badge>
        );
      case "failed":
        return <Badge variant="destructive">Failed</Badge>;
      case "cancelled":
        return <Badge variant="secondary">Cancelled</Badge>;
      default:
        return <Badge variant="secondary">{status}</Badge>;
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "pending":
        return <Clock className="w-4 h-4 text-gray-500" />;
      case "running":
        return <RefreshCw className="w-4 h-4 text-blue-500 animate-spin" />;
      case "completed":
        return <CheckCircle className="w-4 h-4 text-emerald-500" />;
      case "failed":
        return <XCircle className="w-4 h-4 text-red-500" />;
      case "cancelled":
        return <Square className="w-4 h-4 text-gray-500" />;
      default:
        return <AlertCircle className="w-4 h-4 text-gray-500" />;
    }
  };

  const formatDuration = (seconds: number | null) => {
    if (!seconds) return "N/A";

    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;

    if (minutes > 0) {
      return `${minutes}m ${remainingSeconds}s`;
    }
    return `${remainingSeconds}s`;
  };

  const filteredJobs = jobs.filter((job) => {
    if (
      filters.search &&
      !job.source_name.toLowerCase().includes(filters.search.toLowerCase())
    ) {
      return false;
    }
    if (
      filters.status &&
      filters.status !== "all" &&
      job.status !== filters.status
    ) {
      return false;
    }
    if (
      filters.source &&
      filters.source !== "all" &&
      job.source_name !== filters.source
    ) {
      return false;
    }
    return true;
  });

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50">
        <Navigation />
        <div className="flex items-center justify-center min-h-[60vh]">
          <LoadingSpinner />
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <Navigation />
      <PageHeader
        title="Scraping Jobs"
        description="Monitor and manage scholarship scraping operations"
        action={
          <div className="flex space-x-2">
            <Button
              onClick={handleRefresh}
              variant="outline"
              disabled={loading}
            >
              <RefreshCw
                className={`w-4 h-4 mr-2 ${loading ? "animate-spin" : ""}`}
              />
              Refresh
            </Button>
          </div>
        }
      />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {errorMessage && (
          <Alert className="mb-6 border-red-200 bg-red-50">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{errorMessage}</AlertDescription>
          </Alert>
        )}

        {/* Development Alert */}
        {errorMessage &&
          errorMessage.includes("Backend server is not running") && (
            <Alert className="mb-6 border-amber-200 bg-amber-50">
              <AlertDescription className="text-amber-800">
                <strong>Development Mode:</strong> Backend server is not
                running. Displaying mock data for development purposes. To see
                live data, start the FastAPI backend server at
                http://localhost:8000.
              </AlertDescription>
            </Alert>
          )}

        {/* Quick Start Section */}
        <div className="mb-8">
          <h2 className="text-lg font-semibold text-slate-900 mb-4">
            Quick Start
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Button
              onClick={() => startNewJob("https://scholarships.gov.in/", "NSP")}
              className="h-20 flex-col space-y-2"
              variant="outline"
            >
              <Database className="w-6 h-6" />
              <span>Scrape NSP</span>
            </Button>

            <Button
              onClick={() => startNewJob("https://www.ugc.ac.in/", "UGC")}
              className="h-20 flex-col space-y-2"
              variant="outline"
            >
              <Database className="w-6 h-6" />
              <span>Scrape UGC</span>
            </Button>

            <Button
              onClick={() =>
                startNewJob("https://www.aicte-india.org/", "AICTE")
              }
              className="h-20 flex-col space-y-2"
              variant="outline"
            >
              <Database className="w-6 h-6" />
              <span>Scrape AICTE</span>
            </Button>
          </div>
        </div>

        {/* Filters */}
        <div className="mb-6">
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 w-4 h-4" />
              <Input
                placeholder="Search jobs..."
                value={filters.search}
                onChange={(e) =>
                  setFilters((prev) => ({ ...prev, search: e.target.value }))
                }
                className="pl-10"
              />
            </div>

            <Select
              value={filters.status}
              onValueChange={(value: string) =>
                setFilters((prev) => ({ ...prev, status: value }))
              }
            >
              <SelectTrigger className="w-48">
                <SelectValue placeholder="Filter by status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Status</SelectItem>
                <SelectItem value="pending">Pending</SelectItem>
                <SelectItem value="running">Running</SelectItem>
                <SelectItem value="completed">Completed</SelectItem>
                <SelectItem value="failed">Failed</SelectItem>
                <SelectItem value="cancelled">Cancelled</SelectItem>
              </SelectContent>
            </Select>

            <Select
              value={filters.source}
              onValueChange={(value: string) =>
                setFilters((prev) => ({ ...prev, source: value }))
              }
            >
              <SelectTrigger className="w-48">
                <SelectValue placeholder="Filter by source" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Sources</SelectItem>
                <SelectItem value="NSP">NSP</SelectItem>
                <SelectItem value="UGC">UGC</SelectItem>
                <SelectItem value="AICTE">AICTE</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>

        {/* Jobs List */}
        <div className="space-y-4">
          {filteredJobs.length === 0 ? (
            <Card>
              <CardContent className="flex items-center justify-center py-12">
                <div className="text-center">
                  <Database className="w-12 h-12 text-slate-400 mx-auto mb-4" />
                  <p className="text-slate-600">No scraping jobs found</p>
                  <p className="text-sm text-slate-500 mt-2">
                    Start a new scraping job to see it here
                  </p>
                </div>
              </CardContent>
            </Card>
          ) : (
            filteredJobs.map((job) => (
              <Card key={job.id}>
                <CardHeader className="pb-3">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      {getStatusIcon(job.status)}
                      <div>
                        <CardTitle className="text-sm font-medium">
                          {job.source_name} - {job.source_url}
                        </CardTitle>
                        <CardDescription className="text-xs">
                          ID: {job.id}
                        </CardDescription>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      {getStatusBadge(job.status)}
                      <Badge variant="outline" className="text-xs">
                        {job.job_type}
                      </Badge>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                    <div>
                      <div className="text-sm font-medium text-slate-900">
                        {job.items_scraped}
                      </div>
                      <div className="text-xs text-slate-500">Scraped</div>
                    </div>
                    <div>
                      <div className="text-sm font-medium text-slate-900">
                        {job.items_saved}
                      </div>
                      <div className="text-xs text-slate-500">Saved</div>
                    </div>
                    <div>
                      <div className="text-sm font-medium text-slate-900">
                        {job.items_rejected}
                      </div>
                      <div className="text-xs text-slate-500">Rejected</div>
                    </div>
                    <div>
                      <div className="text-sm font-medium text-slate-900">
                        {formatDuration(job.duration)}
                      </div>
                      <div className="text-xs text-slate-500">Duration</div>
                    </div>
                  </div>

                  <div className="flex items-center justify-between">
                    <div className="text-xs text-slate-500">
                      Started:{" "}
                      {job.started_at
                        ? new Date(job.started_at).toLocaleString()
                        : "Not started"}
                      {job.completed_at && (
                        <span className="ml-4">
                          Completed:{" "}
                          {new Date(job.completed_at).toLocaleString()}
                        </span>
                      )}
                    </div>

                    <div className="flex space-x-2">
                      <Button size="sm" variant="outline" asChild>
                        <a href={`/admin/scraping-jobs/${job.id}`}>
                          <Eye className="w-4 h-4 mr-1" />
                          View
                        </a>
                      </Button>

                      {job.status === "running" && (
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => cancelJob(job.id)}
                        >
                          <Square className="w-4 h-4 mr-1" />
                          Cancel
                        </Button>
                      )}

                      {job.status === "failed" && (
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => retryJob(job.id)}
                        >
                          <RotateCcw className="w-4 h-4 mr-1" />
                          Retry
                        </Button>
                      )}
                    </div>
                  </div>

                  {job.errors && job.errors.length > 0 && (
                    <div className="mt-4 p-3 bg-red-50 rounded-md">
                      <div className="text-sm font-medium text-red-800 mb-1">
                        Errors ({job.errors.length})
                      </div>
                      <div className="text-xs text-red-700">
                        {job.errors.slice(0, 2).map((error, index) => (
                          <div key={index} className="mb-1">
                            {error}
                          </div>
                        ))}
                        {job.errors.length > 2 && (
                          <div className="text-red-600">
                            +{job.errors.length - 2} more errors
                          </div>
                        )}
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>
            ))
          )}
        </div>
      </div>

      <Footer />
    </div>
  );
}
