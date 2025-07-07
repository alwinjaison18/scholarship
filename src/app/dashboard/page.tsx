"use client";

import { useEffect } from "react";
import { useSession } from "next-auth/react";
import { useRouter } from "next/navigation";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import {
  BookOpen,
  Clock,
  User,
  Settings,
  BookmarkIcon,
  Bell,
  Search,
  Activity,
  ArrowRight,
  FileText,
  CheckCircle,
  AlertCircle,
  XCircle,
} from "lucide-react";
import Link from "next/link";
import { cn } from "@/lib/utils";

// Mock data for demonstration
const mockDashboardData = {
  user: {
    name: "Rahul Sharma",
    email: "rahul.sharma@example.com",
    avatar: null,
    joinDate: "2025-01-15",
    location: "Delhi, India",
    education: "B.Tech Computer Science",
    completionRate: 85,
  },
  stats: {
    totalApplications: 12,
    pendingApplications: 4,
    approvedApplications: 3,
    rejectedApplications: 2,
    totalBookmarks: 28,
    profileCompletion: 85,
    scholarshipsViewed: 156,
  },
  recentApplications: [
    {
      id: "1",
      title: "Prime Minister Scholarship Scheme",
      status: "pending",
      appliedDate: "2025-01-20",
      amount: 25000,
      deadline: "2025-02-28",
    },
    {
      id: "2",
      title: "Merit-cum-Means Scholarship",
      status: "approved",
      appliedDate: "2025-01-18",
      amount: 15000,
      deadline: "2025-02-15",
    },
    {
      id: "3",
      title: "State Government Scholarship",
      status: "rejected",
      appliedDate: "2025-01-15",
      amount: 8000,
      deadline: "2025-02-10",
    },
  ],
  recommendedScholarships: [
    {
      id: "1",
      title: "National Scholarship Portal - Post Matric",
      amount: 12000,
      deadline: "2025-03-15",
      category: "Government",
      matchScore: 95,
    },
    {
      id: "2",
      title: "INSPIRE Scholarship Programme",
      amount: 80000,
      deadline: "2025-03-30",
      category: "Science",
      matchScore: 88,
    },
    {
      id: "3",
      title: "Kishore Vaigyanik Protsahan Yojana",
      amount: 7000,
      deadline: "2025-04-15",
      category: "Research",
      matchScore: 82,
    },
  ],
  notifications: [
    {
      id: "1",
      type: "deadline",
      message:
        "Application deadline for Prime Minister Scholarship Scheme is in 7 days",
      time: "2 hours ago",
      isRead: false,
    },
    {
      id: "2",
      type: "approval",
      message:
        "Your Merit-cum-Means Scholarship application has been approved!",
      time: "1 day ago",
      isRead: false,
    },
    {
      id: "3",
      type: "new",
      message: "3 new scholarships matching your profile are available",
      time: "2 days ago",
      isRead: true,
    },
  ],
};

const getStatusColor = (status: string) => {
  switch (status) {
    case "approved":
      return "bg-green-100 text-green-800";
    case "pending":
      return "bg-yellow-100 text-yellow-800";
    case "rejected":
      return "bg-red-100 text-red-800";
    default:
      return "bg-gray-100 text-gray-800";
  }
};

const getStatusIcon = (status: string) => {
  switch (status) {
    case "approved":
      return <CheckCircle className="h-4 w-4" />;
    case "pending":
      return <AlertCircle className="h-4 w-4" />;
    case "rejected":
      return <XCircle className="h-4 w-4" />;
    default:
      return <Clock className="h-4 w-4" />;
  }
};

export default function Dashboard() {
  const { data: session, status } = useSession();
  const router = useRouter();

  useEffect(() => {
    if (status === "loading") return; // Still loading

    if (status === "unauthenticated") {
      router.push("/auth/signin");
      return;
    }

    // If user is admin, redirect to admin panel
    if (session?.user?.role === "admin") {
      router.push("/admin");
      return;
    }
  }, [status, router, session]);

  if (status === "loading") {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!session) {
    return null;
  }

  const {
    user,
    stats,
    recentApplications,
    recommendedScholarships,
    notifications,
  } = mockDashboardData;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <Link href="/" className="flex items-center space-x-2">
                <BookOpen className="h-8 w-8 text-blue-600" />
                <span className="text-xl font-bold text-gray-900">
                  ShikshaSetu
                </span>
              </Link>
            </div>
            <div className="flex items-center space-x-4">
              <Button variant="outline" size="sm" asChild>
                <Link href="/scholarships">
                  <Search className="h-4 w-4 mr-2" />
                  Browse Scholarships
                </Link>
              </Button>
              <div className="relative">
                <Button variant="ghost" size="sm">
                  <Bell className="h-4 w-4" />
                  {notifications.filter((n) => !n.isRead).length > 0 && (
                    <span className="absolute -top-1 -right-1 h-2 w-2 bg-red-500 rounded-full"></span>
                  )}
                </Button>
              </div>
              <Avatar>
                <AvatarImage src={user.avatar || ""} alt={user.name} />
                <AvatarFallback>
                  {user.name
                    .split(" ")
                    .map((n) => n[0])
                    .join("")}
                </AvatarFallback>
              </Avatar>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Welcome back, {user.name.split(" ")[0]}!
          </h1>
          <p className="text-gray-600 mt-1">
            Here&apos;s your scholarship journey overview
          </p>
        </div>

        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Total Applications
              </CardTitle>
              <FileText className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {stats.totalApplications}
              </div>
              <p className="text-xs text-muted-foreground">
                +2 from last month
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Pending Applications
              </CardTitle>
              <Clock className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {stats.pendingApplications}
              </div>
              <p className="text-xs text-muted-foreground">Awaiting review</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Approved</CardTitle>
              <CheckCircle className="h-4 w-4 text-green-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-600">
                {stats.approvedApplications}
              </div>
              <p className="text-xs text-muted-foreground">Congratulations!</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Bookmarked</CardTitle>
              <BookmarkIcon className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.totalBookmarks}</div>
              <p className="text-xs text-muted-foreground">Saved for later</p>
            </CardContent>
          </Card>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Recent Applications */}
          <div className="lg:col-span-2">
            <Card>
              <CardHeader>
                <CardTitle>Recent Applications</CardTitle>
                <CardDescription>
                  Your latest scholarship applications
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {recentApplications.map((application) => (
                    <div
                      key={application.id}
                      className="flex items-center justify-between p-4 border rounded-lg"
                    >
                      <div className="flex items-center space-x-4">
                        <div className="flex-shrink-0">
                          {getStatusIcon(application.status)}
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium text-gray-900 truncate">
                            {application.title}
                          </p>
                          <p className="text-xs text-gray-500">
                            Applied on{" "}
                            {new Date(
                              application.appliedDate
                            ).toLocaleDateString()}
                          </p>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Badge
                          className={cn(
                            "capitalize",
                            getStatusColor(application.status)
                          )}
                        >
                          {application.status}
                        </Badge>
                        <span className="text-sm font-medium text-gray-900">
                          ₹{application.amount.toLocaleString()}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
                <div className="mt-6">
                  <Button variant="outline" className="w-full" asChild>
                    <Link href="/dashboard/applications">
                      View All Applications
                      <ArrowRight className="ml-2 h-4 w-4" />
                    </Link>
                  </Button>
                </div>
              </CardContent>
            </Card>

            {/* Recommended Scholarships */}
            <Card className="mt-8">
              <CardHeader>
                <CardTitle>Recommended for You</CardTitle>
                <CardDescription>
                  Scholarships matching your profile
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {recommendedScholarships.map((scholarship) => (
                    <div
                      key={scholarship.id}
                      className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 transition-colors"
                    >
                      <div className="flex-1">
                        <div className="flex items-center space-x-2">
                          <p className="text-sm font-medium text-gray-900">
                            {scholarship.title}
                          </p>
                          <Badge variant="secondary">
                            {scholarship.matchScore}% match
                          </Badge>
                        </div>
                        <div className="flex items-center space-x-4 mt-2">
                          <span className="text-sm text-gray-500">
                            ₹{scholarship.amount.toLocaleString()}
                          </span>
                          <span className="text-sm text-gray-500">
                            Due:{" "}
                            {new Date(
                              scholarship.deadline
                            ).toLocaleDateString()}
                          </span>
                          <Badge variant="outline">
                            {scholarship.category}
                          </Badge>
                        </div>
                      </div>
                      <Button size="sm" asChild>
                        <Link href={`/scholarships/${scholarship.id}`}>
                          Apply
                        </Link>
                      </Button>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Profile Completion */}
            <Card>
              <CardHeader>
                <CardTitle>Profile Completion</CardTitle>
                <CardDescription>
                  Complete your profile to get better recommendations
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Progress</span>
                    <span className="text-sm text-muted-foreground">
                      {stats.profileCompletion}%
                    </span>
                  </div>
                  <Progress value={stats.profileCompletion} className="h-2" />
                  <Button
                    variant="outline"
                    size="sm"
                    className="w-full"
                    asChild
                  >
                    <Link href="/dashboard/profile">
                      <User className="mr-2 h-4 w-4" />
                      Complete Profile
                    </Link>
                  </Button>
                </div>
              </CardContent>
            </Card>

            {/* Notifications */}
            <Card>
              <CardHeader>
                <CardTitle>Recent Notifications</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {notifications.slice(0, 3).map((notification) => (
                    <div
                      key={notification.id}
                      className={cn(
                        "p-3 rounded-lg border text-sm",
                        notification.isRead
                          ? "bg-white"
                          : "bg-blue-50 border-blue-200"
                      )}
                    >
                      <p className="text-gray-900">{notification.message}</p>
                      <p className="text-xs text-gray-500 mt-1">
                        {notification.time}
                      </p>
                    </div>
                  ))}
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  className="w-full mt-4"
                  asChild
                >
                  <Link href="/dashboard/notifications">View All</Link>
                </Button>
              </CardContent>
            </Card>

            {/* Quick Actions */}
            <Card>
              <CardHeader>
                <CardTitle>Quick Actions</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 gap-2">
                  <Button variant="outline" size="sm" asChild>
                    <Link href="/scholarships">
                      <Search className="mr-2 h-4 w-4" />
                      Browse
                    </Link>
                  </Button>
                  <Button variant="outline" size="sm" asChild>
                    <Link href="/dashboard/bookmarks">
                      <BookmarkIcon className="mr-2 h-4 w-4" />
                      Bookmarks
                    </Link>
                  </Button>
                  <Button variant="outline" size="sm" asChild>
                    <Link href="/dashboard/profile">
                      <Settings className="mr-2 h-4 w-4" />
                      Settings
                    </Link>
                  </Button>
                  <Button variant="outline" size="sm" asChild>
                    <Link href="/dashboard/help">
                      <Activity className="mr-2 h-4 w-4" />
                      Help
                    </Link>
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
