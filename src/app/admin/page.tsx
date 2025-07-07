"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useSession } from "next-auth/react";
import { useSystemStats, useSystemHealth } from "@/hooks/useApi";
import { LoadingSpinner } from "@/components/ui/loading-spinner";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import Navigation, { PageHeader } from "@/components/navigation";
import { Footer } from "@/components/navigation";
import {
  Database,
  Activity,
  Users,
  Award,
  CheckCircle,
  AlertCircle,
  XCircle,
  TrendingUp,
  Server,
  RefreshCw,
  Play,
  BarChart3,
  FileText,
} from "lucide-react";

export default function AdminDashboard() {
  const router = useRouter();
  const { data: session, status } = useSession();
  const [refreshing, setRefreshing] = useState(false);

  // Use API hooks to fetch data
  const { data: statsResponse, isLoading: statsLoading } = useSystemStats();
  const { data: healthResponse, isLoading: healthLoading } = useSystemHealth();

  const stats = statsResponse?.success ? statsResponse.data : null;
  const health = healthResponse?.success ? healthResponse.data : null;
  const loading = statsLoading || healthLoading;

  // Handle authentication - this must be called before any early returns
  useEffect(() => {
    if (status === "loading") return;

    if (!session) {
      console.log("No session, redirecting to signin");
      router.push("/auth/signin?callbackUrl=/admin");
      return;
    }

    if (session.user.role !== "admin") {
      console.log("User is not admin, redirecting to dashboard");
      router.push("/dashboard");
      return;
    }

    console.log("Admin authenticated successfully");
  }, [session, status, router]);

  // Show loading spinner while checking authentication
  if (status === "loading") {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  // If not authenticated or not admin, don't render anything (will redirect)
  if (!session || session.user.role !== "admin") {
    return null;
  }

  const handleRefresh = async () => {
    setRefreshing(true);
    // Simulate API call
    setTimeout(() => {
      setRefreshing(false);
    }, 1000);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "healthy":
        return "bg-emerald-500";
      case "warning":
        return "bg-yellow-500";
      case "unhealthy":
        return "bg-red-500";
      default:
        return "bg-gray-500";
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "healthy":
        return <CheckCircle className="w-4 h-4 text-emerald-600" />;
      case "warning":
        return <AlertCircle className="w-4 h-4 text-yellow-600" />;
      case "unhealthy":
        return <XCircle className="w-4 h-4 text-red-600" />;
      default:
        return <AlertCircle className="w-4 h-4 text-gray-600" />;
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50">
        <Navigation />
        <div className="flex items-center justify-center min-h-[60vh]">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <Navigation />
      <PageHeader
        title="Admin Dashboard"
        description="Monitor system health and manage scraping operations"
        action={
          <Button onClick={handleRefresh} disabled={refreshing}>
            <RefreshCw
              className={`w-4 h-4 mr-2 ${refreshing ? "animate-spin" : ""}`}
            />
            Refresh
          </Button>
        }
      />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Admin Navigation */}
        <div className="mb-8">
          <div className="bg-white rounded-lg border shadow-sm p-6">
            <h2 className="text-lg font-semibold text-slate-900 mb-4">
              Admin Tools
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <Button
                variant="outline"
                className="justify-start h-auto p-4"
                asChild
              >
                <a href="/admin/scraping-jobs">
                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                      <Database className="w-5 h-5 text-blue-600" />
                    </div>
                    <div className="text-left">
                      <div className="font-medium">Scraping Jobs</div>
                      <div className="text-sm text-slate-500">
                        Monitor and manage scraping jobs
                      </div>
                    </div>
                  </div>
                </a>
              </Button>

              <Button
                variant="outline"
                className="justify-start h-auto p-4"
                asChild
              >
                <a href="/test-scraping">
                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                      <Play className="w-5 h-5 text-green-600" />
                    </div>
                    <div className="text-left">
                      <div className="font-medium">Test Scraping</div>
                      <div className="text-sm text-slate-500">
                        Test and debug scraping operations
                      </div>
                    </div>
                  </div>
                </a>
              </Button>

              <Button
                variant="outline"
                className="justify-start h-auto p-4"
                asChild
              >
                <a href="/admin">
                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
                      <BarChart3 className="w-5 h-5 text-purple-600" />
                    </div>
                    <div className="text-left">
                      <div className="font-medium">Analytics</div>
                      <div className="text-sm text-slate-500">
                        View system analytics and reports
                      </div>
                    </div>
                  </div>
                </a>
              </Button>
            </div>
          </div>
        </div>

        {/* System Status */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-slate-900">
              System Status
            </h2>
            <div className="flex items-center space-x-2">
              <div
                className={`w-3 h-3 rounded-full ${getStatusColor(
                  health?.overall_status || "unknown"
                )}`}
              ></div>
              <span className="text-sm text-slate-600 capitalize">
                {health?.overall_status || "Unknown"}
              </span>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Database</CardTitle>
                {health?.database &&
                  getStatusIcon(
                    health.database.status ? "healthy" : "unhealthy"
                  )}
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {health?.database?.response_time_ms?.toFixed(1) || "N/A"}ms
                </div>
                <p className="text-xs text-slate-600">Response time</p>
                <div className="mt-2 text-xs text-slate-500">
                  {health?.database?.scholarship_count || 0} scholarships
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  Celery Workers
                </CardTitle>
                {health?.celery &&
                  getStatusIcon(health.celery.status ? "healthy" : "unhealthy")}
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {health?.celery?.active_workers || 0}
                </div>
                <p className="text-xs text-slate-600">Active workers</p>
                <div className="mt-2 text-xs text-slate-500">
                  {health?.celery?.queue_size || 0} jobs in queue
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  System Resources
                </CardTitle>
                <Server className="w-4 h-4 text-slate-600" />
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-slate-600">CPU</span>
                    <span className="text-sm font-medium">
                      {health?.resources?.cpu_usage?.toFixed(1) || 0}%
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-slate-600">Memory</span>
                    <span className="text-sm font-medium">
                      {health?.resources?.memory_usage?.toFixed(1) || 0}%
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-slate-600">Disk</span>
                    <span className="text-sm font-medium">
                      {health?.resources?.disk_usage?.toFixed(1) || 0}%
                    </span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Statistics */}
        <div className="mb-8">
          <h2 className="text-lg font-semibold text-slate-900 mb-4">
            System Statistics
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  Total Scholarships
                </CardTitle>
                <Award className="w-4 h-4 text-slate-600" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {stats?.total_scholarships?.toLocaleString() || 0}
                </div>
                <p className="text-xs text-slate-600">
                  {stats?.verified_scholarships || 0} verified
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  Total Users
                </CardTitle>
                <Users className="w-4 h-4 text-slate-600" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {stats?.total_users?.toLocaleString() || 0}
                </div>
                <p className="text-xs text-slate-600">Registered users</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  Jobs Today
                </CardTitle>
                <Activity className="w-4 h-4 text-slate-600" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {stats?.jobs_today || 0}
                </div>
                <p className="text-xs text-slate-600">
                  {stats?.running_jobs || 0} running,{" "}
                  {stats?.failed_jobs_today || 0} failed
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  Success Rate
                </CardTitle>
                <TrendingUp className="w-4 h-4 text-slate-600" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {stats?.success_rate?.toFixed(1) || 0}%
                </div>
                <p className="text-xs text-slate-600">Last 30 days</p>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Quick Actions */}
        <div>
          <h2 className="text-lg font-semibold text-slate-900 mb-4">
            Quick Actions
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <Button
              className="h-20 flex-col space-y-2"
              variant="outline"
              asChild
            >
              <a href="/admin/scraping-jobs">
                <Database className="w-6 h-6" />
                <span>Scraping Jobs</span>
              </a>
            </Button>

            <Button
              className="h-20 flex-col space-y-2"
              variant="outline"
              asChild
            >
              <a href="/admin/scholarships">
                <Award className="w-6 h-6" />
                <span>Manage Scholarships</span>
              </a>
            </Button>

            <Button
              className="h-20 flex-col space-y-2"
              variant="outline"
              asChild
            >
              <a href="/admin/users">
                <Users className="w-6 h-6" />
                <span>User Management</span>
              </a>
            </Button>

            <Button
              className="h-20 flex-col space-y-2"
              variant="outline"
              asChild
            >
              <a href="/admin/logs">
                <FileText className="w-6 h-6" />
                <span>System Logs</span>
              </a>
            </Button>
          </div>
        </div>
      </div>

      <Footer />
    </div>
  );
}
