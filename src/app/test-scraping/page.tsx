"use client";

import { useState } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { LoadingSpinner } from "@/components/ui/loading-spinner";
import Navigation, { PageHeader } from "@/components/navigation";
import { Footer } from "@/components/navigation";
import {
  RefreshCw,
  CheckCircle,
  XCircle,
  Clock,
  Database,
  AlertCircle,
} from "lucide-react";

interface ScrapingJob {
  job_id: string;
  source: string;
  status: string;
  items_scraped: number;
  items_saved: number;
  items_rejected: number;
  started_at: string | null;
  completed_at: string | null;
  created_at: string;
  errors: string[] | null;
}

export default function TestScrapingPage() {
  const [jobs, setJobs] = useState<ScrapingJob[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const startScraping = async (source: string) => {
    try {
      setLoading(true);
      setError(null);
      setSuccess(null);

      const response = await fetch(`/api/test/test-scraping?source=${source}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setSuccess(
        `Scraping job started for ${source.toUpperCase()}: ${data.job_id}`
      );

      // Refresh jobs list
      await fetchRecentJobs();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to start scraping");
    } finally {
      setLoading(false);
    }
  };

  const fetchRecentJobs = async () => {
    try {
      const response = await fetch("/api/test/recent-jobs");

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setJobs(data);
    } catch (err) {
      console.error("Failed to fetch recent jobs:", err);
    }
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
      default:
        return <AlertCircle className="w-4 h-4 text-gray-500" />;
    }
  };

  return (
    <div className="min-h-screen bg-slate-50">
      <Navigation />
      <PageHeader
        title="Test Scraping"
        description="Test the scholarship scraping functionality"
        action={
          <Button onClick={fetchRecentJobs} variant="outline">
            <RefreshCw className="w-4 h-4 mr-2" />
            Refresh Jobs
          </Button>
        }
      />

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <Alert className="mb-6 border-red-200 bg-red-50">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {success && (
          <Alert className="mb-6 border-emerald-200 bg-emerald-50">
            <CheckCircle className="h-4 w-4" />
            <AlertDescription>{success}</AlertDescription>
          </Alert>
        )}

        {/* Start Scraping Section */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>Start Scraping Job</CardTitle>
            <CardDescription>
              Test the scraping functionality by starting a job for different
              sources
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <Button
                onClick={() => startScraping("nsp")}
                disabled={loading}
                className="h-24 flex-col space-y-2"
                variant="outline"
              >
                {loading ? (
                  <LoadingSpinner />
                ) : (
                  <>
                    <Database className="w-8 h-8" />
                    <span>Test NSP Scraping</span>
                  </>
                )}
              </Button>

              <Button
                onClick={() => startScraping("ugc")}
                disabled={loading}
                className="h-24 flex-col space-y-2"
                variant="outline"
              >
                {loading ? (
                  <LoadingSpinner />
                ) : (
                  <>
                    <Database className="w-8 h-8" />
                    <span>Test UGC Scraping</span>
                  </>
                )}
              </Button>

              <Button
                onClick={() => startScraping("aicte")}
                disabled={loading}
                className="h-24 flex-col space-y-2"
                variant="outline"
              >
                {loading ? (
                  <LoadingSpinner />
                ) : (
                  <>
                    <Database className="w-8 h-8" />
                    <span>Test AICTE Scraping</span>
                  </>
                )}
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Recent Jobs Section */}
        <Card>
          <CardHeader>
            <CardTitle>Recent Jobs</CardTitle>
            <CardDescription>
              View the status of recent scraping jobs
            </CardDescription>
          </CardHeader>
          <CardContent>
            {jobs.length === 0 ? (
              <div className="text-center py-8">
                <Database className="w-12 h-12 text-slate-400 mx-auto mb-4" />
                <p className="text-slate-600">No recent jobs found</p>
                <p className="text-sm text-slate-500 mt-2">
                  Start a scraping job to see it here
                </p>
              </div>
            ) : (
              <div className="space-y-4">
                {jobs.map((job) => (
                  <div
                    key={job.job_id}
                    className="border rounded-lg p-4 bg-white"
                  >
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center space-x-3">
                        {getStatusIcon(job.status)}
                        <div>
                          <div className="font-medium text-sm">
                            {job.source} Scraping Job
                          </div>
                          <div className="text-xs text-slate-500">
                            ID: {job.job_id}
                          </div>
                        </div>
                      </div>
                      {getStatusBadge(job.status)}
                    </div>

                    <div className="grid grid-cols-3 gap-4 mb-3">
                      <div>
                        <div className="text-lg font-semibold text-slate-900">
                          {job.items_scraped}
                        </div>
                        <div className="text-xs text-slate-500">Scraped</div>
                      </div>
                      <div>
                        <div className="text-lg font-semibold text-emerald-600">
                          {job.items_saved}
                        </div>
                        <div className="text-xs text-slate-500">Saved</div>
                      </div>
                      <div>
                        <div className="text-lg font-semibold text-red-600">
                          {job.items_rejected}
                        </div>
                        <div className="text-xs text-slate-500">Rejected</div>
                      </div>
                    </div>

                    <div className="text-xs text-slate-500">
                      Created: {new Date(job.created_at).toLocaleString()}
                      {job.started_at && (
                        <span className="ml-4">
                          Started: {new Date(job.started_at).toLocaleString()}
                        </span>
                      )}
                      {job.completed_at && (
                        <span className="ml-4">
                          Completed:{" "}
                          {new Date(job.completed_at).toLocaleString()}
                        </span>
                      )}
                    </div>

                    {job.errors && job.errors.length > 0 && (
                      <div className="mt-3 p-3 bg-red-50 rounded-md">
                        <div className="text-sm font-medium text-red-800 mb-1">
                          Errors:
                        </div>
                        <div className="text-xs text-red-700">
                          {job.errors.map((error, index) => (
                            <div key={index} className="mb-1">
                              {error}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      <Footer />
    </div>
  );
}
