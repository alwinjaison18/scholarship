// API service functions for connecting to FastAPI backend
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const FALLBACK_API_URL = "http://localhost:3000"; // Next.js API routes as fallback

interface ApiResponse<T> {
  data: T;
  success: boolean;
  message?: string;
}

interface Scholarship {
  id: number;
  title: string;
  provider: string;
  amount: number;
  deadline: string;
  category: string;
  eligibility: string;
  description: string;
  location: string;
  verified: boolean;
  trending: boolean;
  views: number;
  applications: number;
  tags: string[];
  educationLevel: string;
  field: string;
  source_url?: string;
  created_at?: string;
  updated_at?: string;
}

interface SystemStats {
  total_scholarships: number;
  active_scholarships: number;
  verified_scholarships: number;
  total_users: number;
  jobs_today: number;
  running_jobs: number;
  failed_jobs_today: number;
  recent_scholarships: number;
  avg_job_duration: number;
  success_rate: number;
}

interface SystemHealth {
  overall_status: string;
  database: {
    status: boolean;
    response_time_ms: number;
    scholarship_count: number;
    job_count: number;
  };
  celery: {
    status: boolean;
    redis_response_time_ms: number;
    active_workers: number;
    queue_size: number;
  };
  resources: {
    cpu_usage: number;
    memory_usage: number;
    disk_usage: number;
    memory_total_gb: number;
    memory_used_gb: number;
  };
  timestamp: string;
}

interface ScrapingJob {
  id: string;
  source_url: string;
  source_name: string;
  status: "pending" | "running" | "completed" | "failed" | "cancelled";
  job_type: string;
  priority: string;
  items_scraped: number;
  items_validated: number;
  items_saved: number;
  items_rejected: number;
  started_at: string | null;
  completed_at: string | null;
  duration: number | null;
  errors: string[] | null;
  warnings: string[] | null;
  retry_count: number;
  created_at: string;
}

// Generic API call function
async function apiCall<T>(
  endpoint: string,
  options?: RequestInit
): Promise<ApiResponse<T>> {
  try {
    console.log(`Making API call to: ${API_BASE_URL}${endpoint}`);
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      headers: {
        "Content-Type": "application/json",
        ...options?.headers,
      },
      ...options,
    });

    if (!response.ok) {
      throw new Error(
        `HTTP error! status: ${response.status} - ${response.statusText}`
      );
    }

    const data = await response.json();
    return { data, success: true };
  } catch (error) {
    console.error(`API call failed for ${endpoint}:`, error);

    // Try fallback to Next.js API routes
    if (error instanceof TypeError && error.message.includes("fetch")) {
      console.log(`Trying fallback API at: ${FALLBACK_API_URL}${endpoint}`);
      try {
        const fallbackResponse = await fetch(`${FALLBACK_API_URL}${endpoint}`, {
          headers: {
            "Content-Type": "application/json",
            ...options?.headers,
          },
          ...options,
        });

        if (fallbackResponse.ok) {
          const fallbackData = await fallbackResponse.json();
          return {
            data: fallbackData.data || fallbackData,
            success: true,
            message: "Using Next.js API fallback",
          };
        }
      } catch (fallbackError) {
        console.error("Fallback API also failed:", fallbackError);
      }
    }

    return {
      data: {} as T,
      success: false,
      message:
        "Backend server is not running. Please start the FastAPI backend server.",
    };
  }
}

// Scholarship API functions
export const scholarshipApi = {
  // Get all scholarships with optional filters
  getScholarships: async (params?: {
    category?: string;
    search?: string;
    limit?: number;
    offset?: number;
    sort?: string;
  }): Promise<ApiResponse<Scholarship[]>> => {
    const queryString = params
      ? new URLSearchParams(
          Object.entries(params)
            .filter(([, value]) => value !== undefined)
            .map(([key, value]) => [key, String(value)])
        ).toString()
      : "";

    const result = await apiCall<Scholarship[]>(
      `/api/scholarships${queryString ? `?${queryString}` : ""}`
    );

    // Fallback to mock data if backend is not available
    if (
      !result.success &&
      result.message?.includes("Backend server is not running")
    ) {
      console.log("Using mock scholarships data");
      let filteredScholarships = [...MOCK_SCHOLARSHIPS];

      // Apply filters to mock data
      if (params?.category) {
        filteredScholarships = filteredScholarships.filter((scholarship) =>
          scholarship.category
            .toLowerCase()
            .includes(params.category!.toLowerCase())
        );
      }

      if (params?.search) {
        filteredScholarships = filteredScholarships.filter(
          (scholarship) =>
            scholarship.title
              .toLowerCase()
              .includes(params.search!.toLowerCase()) ||
            scholarship.provider
              .toLowerCase()
              .includes(params.search!.toLowerCase())
        );
      }

      return {
        data: filteredScholarships,
        success: true,
        message: "Using mock data - backend not available",
      };
    }

    return result;
  },

  // Get single scholarship by ID
  getScholarship: async (id: number): Promise<ApiResponse<Scholarship>> => {
    return apiCall<Scholarship>(`/api/scholarships/${id}`);
  },

  // Get trending scholarships
  getTrendingScholarships: async (): Promise<ApiResponse<Scholarship[]>> => {
    const result = await apiCall<Scholarship[]>("/api/scholarships/trending");

    // Fallback to mock data if backend is not available
    if (
      !result.success &&
      result.message?.includes("Backend server is not running")
    ) {
      console.log("Using mock trending scholarships data");
      const trendingScholarships = MOCK_SCHOLARSHIPS.filter((s) => s.trending);
      return {
        data: trendingScholarships,
        success: true,
        message: "Using mock data - backend not available",
      };
    }

    return result;
  },

  // Get recent scholarships
  getRecentScholarships: async (
    limit: number = 10
  ): Promise<ApiResponse<Scholarship[]>> => {
    return apiCall<Scholarship[]>(`/api/scholarships/recent?limit=${limit}`);
  },

  // Get scholarships by deadline (upcoming deadlines)
  getUpcomingDeadlines: async (): Promise<ApiResponse<Scholarship[]>> => {
    return apiCall<Scholarship[]>("/api/scholarships/deadlines");
  },
};

// Mock data for development when backend is not available
const MOCK_SCHOLARSHIPS: Scholarship[] = [
  {
    id: 1,
    title: "National Merit Scholarship",
    provider: "Government of India",
    amount: 120000,
    deadline: "2024-03-31",
    category: "Academic Excellence",
    eligibility: "12th pass with 90%+ marks",
    description:
      "Merit-based scholarship for outstanding students pursuing higher education",
    location: "All India",
    verified: true,
    trending: true,
    views: 1250,
    applications: 450,
    tags: ["Merit", "Academic", "Government"],
    educationLevel: "Undergraduate",
    field: "All Fields",
    source_url: "https://www.scholarships.gov.in/merit",
    created_at: "2024-01-01T00:00:00Z",
    updated_at: "2024-01-15T10:30:00Z",
  },
  {
    id: 2,
    title: "SC/ST Scholarship Program",
    provider: "Ministry of Social Justice",
    amount: 80000,
    deadline: "2024-04-15",
    category: "Social Welfare",
    eligibility: "SC/ST students with family income < 2.5 lakhs",
    description:
      "Financial assistance for SC/ST students pursuing higher education",
    location: "All India",
    verified: true,
    trending: true,
    views: 980,
    applications: 320,
    tags: ["SC/ST", "Social Justice", "Government"],
    educationLevel: "Undergraduate",
    field: "All Fields",
    source_url: "https://www.scholarships.gov.in/sc-st",
    created_at: "2024-01-01T00:00:00Z",
    updated_at: "2024-01-15T10:30:00Z",
  },
  {
    id: 3,
    title: "Girls Education Scholarship",
    provider: "Women & Child Development",
    amount: 50000,
    deadline: "2024-05-01",
    category: "Women Empowerment",
    eligibility: "Girl students from economically weaker sections",
    description:
      "Supporting girls' education and empowerment through financial assistance",
    location: "All India",
    verified: true,
    trending: false,
    views: 750,
    applications: 280,
    tags: ["Girls", "Empowerment", "Government"],
    educationLevel: "Undergraduate",
    field: "All Fields",
    source_url: "https://www.scholarships.gov.in/girls",
    created_at: "2024-01-01T00:00:00Z",
    updated_at: "2024-01-15T10:30:00Z",
  },
];

const MOCK_SCRAPING_JOBS: ScrapingJob[] = [
  {
    id: "job_1",
    source_url: "https://www.scholarships.gov.in/",
    source_name: "National Scholarship Portal",
    status: "running",
    job_type: "full_scrape",
    priority: "high",
    items_scraped: 245,
    items_validated: 230,
    items_saved: 225,
    items_rejected: 5,
    started_at: "2024-01-15T10:30:00Z",
    completed_at: null,
    duration: null,
    errors: null,
    warnings: ["Some duplicate entries found"],
    retry_count: 0,
    created_at: "2024-01-15T10:30:00Z",
  },
  {
    id: "job_2",
    source_url: "https://www.ugc.ac.in/scholarships/",
    source_name: "UGC Scholarships",
    status: "completed",
    job_type: "update_scrape",
    priority: "medium",
    items_scraped: 156,
    items_validated: 156,
    items_saved: 150,
    items_rejected: 6,
    started_at: "2024-01-15T09:00:00Z",
    completed_at: "2024-01-15T09:45:00Z",
    duration: 45,
    errors: null,
    warnings: null,
    retry_count: 0,
    created_at: "2024-01-15T09:00:00Z",
  },
  {
    id: "job_3",
    source_url: "https://www.aicte-india.org/schemes/",
    source_name: "AICTE Schemes",
    status: "failed",
    job_type: "full_scrape",
    priority: "low",
    items_scraped: 0,
    items_validated: 0,
    items_saved: 0,
    items_rejected: 0,
    started_at: "2024-01-15T08:00:00Z",
    completed_at: "2024-01-15T08:05:00Z",
    duration: 5,
    errors: ["Connection timeout", "Invalid response format"],
    warnings: null,
    retry_count: 2,
    created_at: "2024-01-15T08:00:00Z",
  },
];

const MOCK_SYSTEM_STATS: SystemStats = {
  total_scholarships: 2456,
  active_scholarships: 1890,
  verified_scholarships: 1634,
  total_users: 12450,
  jobs_today: 8,
  running_jobs: 2,
  failed_jobs_today: 1,
  recent_scholarships: 45,
  avg_job_duration: 28.5,
  success_rate: 94.2,
};

const MOCK_SYSTEM_HEALTH: SystemHealth = {
  overall_status: "healthy",
  database: {
    status: true,
    response_time_ms: 45,
    scholarship_count: 2456,
    job_count: 156,
  },
  celery: {
    status: true,
    redis_response_time_ms: 12,
    active_workers: 3,
    queue_size: 5,
  },
  resources: {
    cpu_usage: 45.2,
    memory_usage: 68.8,
    disk_usage: 23.4,
    memory_total_gb: 16.0,
    memory_used_gb: 11.0,
  },
  timestamp: new Date().toISOString(),
};

// Admin API functions
export const adminApi = {
  // Get system statistics
  getSystemStats: async (): Promise<ApiResponse<SystemStats>> => {
    const result = await apiCall<SystemStats>("/api/admin/stats");

    // Fallback to mock data if backend is not available
    if (
      !result.success &&
      result.message?.includes("Backend server is not running")
    ) {
      console.log("Using mock system stats data");
      return {
        data: MOCK_SYSTEM_STATS,
        success: true,
        message: "Using mock data - backend not available",
      };
    }

    return result;
  },

  // Get system health
  getSystemHealth: async (): Promise<ApiResponse<SystemHealth>> => {
    const result = await apiCall<SystemHealth>("/api/admin/health");

    // Fallback to mock data if backend is not available
    if (
      !result.success &&
      result.message?.includes("Backend server is not running")
    ) {
      console.log("Using mock system health data");
      return {
        data: MOCK_SYSTEM_HEALTH,
        success: true,
        message: "Using mock data - backend not available",
      };
    }

    return result;
  },

  // Get scraping jobs
  getScrapingJobs: async (params?: {
    status?: string;
    source?: string;
    limit?: number;
    offset?: number;
  }): Promise<ApiResponse<ScrapingJob[]>> => {
    const queryString = params
      ? new URLSearchParams(
          Object.entries(params)
            .filter(([, value]) => value !== undefined)
            .map(([key, value]) => [key, String(value)])
        ).toString()
      : "";

    const result = await apiCall<ScrapingJob[]>(
      `/api/admin/scraping-jobs${queryString ? `?${queryString}` : ""}`
    );

    // Fallback to mock data if backend is not available
    if (
      !result.success &&
      result.message?.includes("Backend server is not running")
    ) {
      console.log("Using mock scraping jobs data");
      let filteredJobs = [...MOCK_SCRAPING_JOBS];

      // Apply filters to mock data
      if (params?.status && params.status !== "all") {
        filteredJobs = filteredJobs.filter(
          (job) => job.status === params.status
        );
      }

      return {
        data: filteredJobs,
        success: true,
        message: "Using mock data - backend not available",
      };
    }

    return result;
  },

  // Start a new scraping job
  startScrapingJob: async (
    sourceUrl: string
  ): Promise<ApiResponse<{ job_id: string }>> => {
    return apiCall<{ job_id: string }>("/api/admin/scraping-jobs", {
      method: "POST",
      body: JSON.stringify({ source_url: sourceUrl }),
    });
  },

  // Stop a scraping job
  stopScrapingJob: async (
    jobId: string
  ): Promise<ApiResponse<{ message: string }>> => {
    return apiCall<{ message: string }>(
      `/api/admin/scraping-jobs/${jobId}/stop`,
      {
        method: "POST",
      }
    );
  },

  // Retry a failed scraping job
  retryScrapingJob: async (
    jobId: string
  ): Promise<ApiResponse<{ message: string }>> => {
    return apiCall<{ message: string }>(
      `/api/admin/scraping-jobs/${jobId}/retry`,
      {
        method: "POST",
      }
    );
  },
};

// Test scraping API functions
export const testScrapingApi = {
  // Start test scraping
  startTestScraping: async (
    sourceUrl: string
  ): Promise<ApiResponse<{ job_id: string; message: string }>> => {
    const result = await apiCall<{ job_id: string; message: string }>(
      "/api/test-scraping/start",
      {
        method: "POST",
        body: JSON.stringify({ source_url: sourceUrl }),
      }
    );

    // Fallback behavior if backend is not available
    if (
      !result.success &&
      result.message?.includes("Backend server is not running")
    ) {
      console.log("Mock test scraping started");
      return {
        data: {
          job_id: `test_job_${Date.now()}`,
          message: "Test scraping started (mock mode - backend not available)",
        },
        success: true,
        message: "Using mock response - backend not available",
      };
    }

    return result;
  },

  // Get test scraping status
  getTestScrapingStatus: async (
    jobId: string
  ): Promise<ApiResponse<ScrapingJob>> => {
    const result = await apiCall<ScrapingJob>(
      `/api/test-scraping/status/${jobId}`
    );

    // Fallback behavior if backend is not available
    if (
      !result.success &&
      result.message?.includes("Backend server is not running")
    ) {
      console.log("Using mock test scraping status");
      return {
        data: {
          ...MOCK_SCRAPING_JOBS[0],
          id: jobId,
          status: "running",
        },
        success: true,
        message: "Using mock data - backend not available",
      };
    }

    return result;
  },

  // Get all test scraping jobs
  getTestScrapingJobs: async (): Promise<ApiResponse<ScrapingJob[]>> => {
    const result = await apiCall<ScrapingJob[]>("/api/test-scraping/jobs");

    // Fallback behavior if backend is not available
    if (
      !result.success &&
      result.message?.includes("Backend server is not running")
    ) {
      console.log("Using mock test scraping jobs");
      return {
        data: MOCK_SCRAPING_JOBS.map((job) => ({
          ...job,
          id: `test_${job.id}`,
        })),
        success: true,
        message: "Using mock data - backend not available",
      };
    }

    return result;
  },
};

// Export types for use in components
export type { Scholarship, SystemStats, SystemHealth, ScrapingJob };
