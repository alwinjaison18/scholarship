// React Query hooks for data fetching
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { scholarshipApi, adminApi, testScrapingApi } from "@/lib/api";

// Query Keys
export const queryKeys = {
  scholarships: ["scholarships"] as const,
  scholarship: (id: number) => ["scholarships", id] as const,
  trendingScholarships: ["scholarships", "trending"] as const,
  recentScholarships: ["scholarships", "recent"] as const,
  upcomingDeadlines: ["scholarships", "deadlines"] as const,
  systemStats: ["admin", "stats"] as const,
  systemHealth: ["admin", "health"] as const,
  scrapingJobs: ["admin", "scraping-jobs"] as const,
  testScrapingJobs: ["test-scraping", "jobs"] as const,
};

// Scholarship Hooks
export const useScholarships = (params?: {
  category?: string;
  search?: string;
  limit?: number;
  offset?: number;
  sort?: string;
}) => {
  return useQuery({
    queryKey: [...queryKeys.scholarships, params],
    queryFn: () => scholarshipApi.getScholarships(params),
    staleTime: 5 * 60 * 1000, // 5 minutes
    retry: 3,
  });
};

export const useScholarship = (id: number) => {
  return useQuery({
    queryKey: queryKeys.scholarship(id),
    queryFn: () => scholarshipApi.getScholarship(id),
    staleTime: 10 * 60 * 1000, // 10 minutes
    retry: 3,
    enabled: !!id,
  });
};

export const useTrendingScholarships = () => {
  return useQuery({
    queryKey: queryKeys.trendingScholarships,
    queryFn: scholarshipApi.getTrendingScholarships,
    staleTime: 15 * 60 * 1000, // 15 minutes
    retry: 3,
  });
};

export const useRecentScholarships = (limit: number = 10) => {
  return useQuery({
    queryKey: [...queryKeys.recentScholarships, limit],
    queryFn: () => scholarshipApi.getRecentScholarships(limit),
    staleTime: 5 * 60 * 1000, // 5 minutes
    retry: 3,
  });
};

export const useUpcomingDeadlines = () => {
  return useQuery({
    queryKey: queryKeys.upcomingDeadlines,
    queryFn: scholarshipApi.getUpcomingDeadlines,
    staleTime: 30 * 60 * 1000, // 30 minutes
    retry: 3,
  });
};

// Admin Hooks
export const useSystemStats = () => {
  return useQuery({
    queryKey: queryKeys.systemStats,
    queryFn: adminApi.getSystemStats,
    staleTime: 30 * 1000, // 30 seconds
    refetchInterval: 60 * 1000, // Refetch every minute
    retry: 3,
  });
};

export const useSystemHealth = () => {
  return useQuery({
    queryKey: queryKeys.systemHealth,
    queryFn: adminApi.getSystemHealth,
    staleTime: 15 * 1000, // 15 seconds
    refetchInterval: 30 * 1000, // Refetch every 30 seconds
    retry: 3,
  });
};

export const useScrapingJobs = (params?: {
  status?: string;
  source?: string;
  limit?: number;
  offset?: number;
}) => {
  return useQuery({
    queryKey: [...queryKeys.scrapingJobs, params],
    queryFn: () => adminApi.getScrapingJobs(params),
    staleTime: 30 * 1000, // 30 seconds
    refetchInterval: 60 * 1000, // Refetch every minute
    retry: 3,
  });
};

// Test Scraping Hooks
export const useTestScrapingJobs = () => {
  return useQuery({
    queryKey: queryKeys.testScrapingJobs,
    queryFn: testScrapingApi.getTestScrapingJobs,
    staleTime: 30 * 1000, // 30 seconds
    refetchInterval: 5 * 1000, // Refetch every 5 seconds for real-time updates
    retry: 3,
  });
};

// Mutation Hooks
export const useStartScrapingJob = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (sourceUrl: string) => adminApi.startScrapingJob(sourceUrl),
    onSuccess: () => {
      // Invalidate and refetch scraping jobs
      queryClient.invalidateQueries({ queryKey: queryKeys.scrapingJobs });
      queryClient.invalidateQueries({ queryKey: queryKeys.systemStats });
    },
  });
};

export const useStopScrapingJob = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (jobId: string) => adminApi.stopScrapingJob(jobId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.scrapingJobs });
      queryClient.invalidateQueries({ queryKey: queryKeys.systemStats });
    },
  });
};

export const useRetryScrapingJob = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (jobId: string) => adminApi.retryScrapingJob(jobId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.scrapingJobs });
      queryClient.invalidateQueries({ queryKey: queryKeys.systemStats });
    },
  });
};

export const useStartTestScraping = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (sourceUrl: string) =>
      testScrapingApi.startTestScraping(sourceUrl),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.testScrapingJobs });
    },
  });
};

// Helper hook for real-time updates
export const useRealTimeUpdates = () => {
  const queryClient = useQueryClient();

  const refreshAll = () => {
    queryClient.invalidateQueries({ queryKey: queryKeys.scholarships });
    queryClient.invalidateQueries({ queryKey: queryKeys.systemStats });
    queryClient.invalidateQueries({ queryKey: queryKeys.systemHealth });
    queryClient.invalidateQueries({ queryKey: queryKeys.scrapingJobs });
    queryClient.invalidateQueries({ queryKey: queryKeys.testScrapingJobs });
  };

  const refreshScholarships = () => {
    queryClient.invalidateQueries({ queryKey: queryKeys.scholarships });
    queryClient.invalidateQueries({ queryKey: queryKeys.trendingScholarships });
    queryClient.invalidateQueries({ queryKey: queryKeys.recentScholarships });
    queryClient.invalidateQueries({ queryKey: queryKeys.upcomingDeadlines });
  };

  const refreshAdmin = () => {
    queryClient.invalidateQueries({ queryKey: queryKeys.systemStats });
    queryClient.invalidateQueries({ queryKey: queryKeys.systemHealth });
    queryClient.invalidateQueries({ queryKey: queryKeys.scrapingJobs });
  };

  return {
    refreshAll,
    refreshScholarships,
    refreshAdmin,
  };
};
