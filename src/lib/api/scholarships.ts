import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import apiClient from "@/lib/api-client";
import { Scholarship, ScholarshipFilters, PaginatedResponse } from "@/types";

// Scholarship API functions
export const scholarshipAPI = {
  // Get all scholarships with filters and pagination
  getScholarships: async (
    filters: ScholarshipFilters = {},
    page: number = 1,
    limit: number = 10
  ): Promise<PaginatedResponse<Scholarship>> => {
    const params = new URLSearchParams();

    if (filters.search) params.append("search", filters.search);
    if (filters.category) params.append("category", filters.category);
    if (filters.level) params.append("level", filters.level);
    if (filters.state) params.append("state", filters.state);
    if (filters.minAmount)
      params.append("min_amount", filters.minAmount.toString());
    if (filters.maxAmount)
      params.append("max_amount", filters.maxAmount.toString());
    if (filters.deadline) params.append("deadline", filters.deadline);
    if (filters.isVerified !== undefined)
      params.append("is_verified", filters.isVerified.toString());

    params.append("page", page.toString());
    params.append("limit", limit.toString());

    const response = await apiClient.get(`/scholarships?${params.toString()}`);
    return response.data;
  },

  // Get scholarship by ID
  getScholarship: async (id: string): Promise<Scholarship> => {
    const response = await apiClient.get(`/scholarships/${id}`);
    return response.data;
  },

  // Create new scholarship (admin only)
  createScholarship: async (
    data: Partial<Scholarship>
  ): Promise<Scholarship> => {
    const response = await apiClient.post("/scholarships", data);
    return response.data;
  },

  // Update scholarship (admin only)
  updateScholarship: async (
    id: string,
    data: Partial<Scholarship>
  ): Promise<Scholarship> => {
    const response = await apiClient.put(`/scholarships/${id}`, data);
    return response.data;
  },

  // Delete scholarship (admin only)
  deleteScholarship: async (id: string): Promise<void> => {
    await apiClient.delete(`/scholarships/${id}`);
  },

  // Get trending scholarships
  getTrendingScholarships: async (
    limit: number = 10
  ): Promise<Scholarship[]> => {
    const response = await apiClient.get(
      `/scholarships/trending?limit=${limit}`
    );
    return response.data;
  },

  // Get featured scholarships
  getFeaturedScholarships: async (
    limit: number = 10
  ): Promise<Scholarship[]> => {
    const response = await apiClient.get(
      `/scholarships/featured?limit=${limit}`
    );
    return response.data;
  },

  // Get scholarship statistics
  getScholarshipStats: async () => {
    const response = await apiClient.get("/scholarships/stats");
    return response.data;
  },
};

// React Query hooks for scholarships
export const useScholarships = (
  filters: ScholarshipFilters = {},
  page: number = 1,
  limit: number = 10
) => {
  return useQuery({
    queryKey: ["scholarships", filters, page, limit],
    queryFn: () => scholarshipAPI.getScholarships(filters, page, limit),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

export const useScholarship = (id: string) => {
  return useQuery({
    queryKey: ["scholarship", id],
    queryFn: () => scholarshipAPI.getScholarship(id),
    enabled: !!id,
  });
};

export const useTrendingScholarships = (limit: number = 10) => {
  return useQuery({
    queryKey: ["scholarships", "trending", limit],
    queryFn: () => scholarshipAPI.getTrendingScholarships(limit),
    staleTime: 10 * 60 * 1000, // 10 minutes
  });
};

export const useFeaturedScholarships = (limit: number = 10) => {
  return useQuery({
    queryKey: ["scholarships", "featured", limit],
    queryFn: () => scholarshipAPI.getFeaturedScholarships(limit),
    staleTime: 10 * 60 * 1000, // 10 minutes
  });
};

export const useScholarshipStats = () => {
  return useQuery({
    queryKey: ["scholarships", "stats"],
    queryFn: scholarshipAPI.getScholarshipStats,
    staleTime: 30 * 60 * 1000, // 30 minutes
  });
};

// Mutations
export const useCreateScholarship = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: scholarshipAPI.createScholarship,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["scholarships"] });
    },
  });
};

export const useUpdateScholarship = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<Scholarship> }) =>
      scholarshipAPI.updateScholarship(id, data),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ["scholarships"] });
      queryClient.invalidateQueries({ queryKey: ["scholarship", data.id] });
    },
  });
};

export const useDeleteScholarship = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: scholarshipAPI.deleteScholarship,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["scholarships"] });
    },
  });
};
