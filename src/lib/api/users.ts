import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import apiClient from "@/lib/api-client";
import { User, UserProfile, Application } from "@/types";

// User API functions
export const userAPI = {
  // Get current user profile
  getCurrentUser: async (): Promise<User> => {
    const response = await apiClient.get("/users/me");
    return response.data;
  },

  // Update user profile
  updateProfile: async (data: Partial<UserProfile>): Promise<User> => {
    const response = await apiClient.put("/users/me", data);
    return response.data;
  },

  // Get user applications
  getUserApplications: async (userId: string): Promise<Application[]> => {
    const response = await apiClient.get(`/users/${userId}/applications`);
    return response.data;
  },

  // Apply for scholarship
  applyForScholarship: async (
    scholarshipId: string,
    data: Record<string, unknown>
  ): Promise<Application> => {
    const response = await apiClient.post(
      `/scholarships/${scholarshipId}/apply`,
      data
    );
    return response.data;
  },

  // Get user bookmarks
  getUserBookmarks: async (): Promise<string[]> => {
    const response = await apiClient.get("/users/me/bookmarks");
    return response.data;
  },

  // Add bookmark
  addBookmark: async (scholarshipId: string): Promise<void> => {
    await apiClient.post(`/users/me/bookmarks/${scholarshipId}`);
  },

  // Remove bookmark
  removeBookmark: async (scholarshipId: string): Promise<void> => {
    await apiClient.delete(`/users/me/bookmarks/${scholarshipId}`);
  },

  // Get user notifications
  getUserNotifications: async () => {
    const response = await apiClient.get("/users/me/notifications");
    return response.data;
  },

  // Mark notification as read
  markNotificationAsRead: async (notificationId: string): Promise<void> => {
    await apiClient.patch(`/users/me/notifications/${notificationId}/read`);
  },

  // Get user dashboard stats
  getUserDashboardStats: async () => {
    const response = await apiClient.get("/users/me/dashboard");
    return response.data;
  },
};

// React Query hooks for users
export const useCurrentUser = () => {
  return useQuery({
    queryKey: ["user", "current"],
    queryFn: userAPI.getCurrentUser,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

export const useUserApplications = (userId: string) => {
  return useQuery({
    queryKey: ["user", userId, "applications"],
    queryFn: () => userAPI.getUserApplications(userId),
    enabled: !!userId,
  });
};

export const useUserBookmarks = () => {
  return useQuery({
    queryKey: ["user", "bookmarks"],
    queryFn: userAPI.getUserBookmarks,
  });
};

export const useUserNotifications = () => {
  return useQuery({
    queryKey: ["user", "notifications"],
    queryFn: userAPI.getUserNotifications,
  });
};

export const useUserDashboardStats = () => {
  return useQuery({
    queryKey: ["user", "dashboard"],
    queryFn: userAPI.getUserDashboardStats,
  });
};

// Mutations
export const useUpdateProfile = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: userAPI.updateProfile,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["user", "current"] });
    },
  });
};

export const useApplyForScholarship = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      scholarshipId,
      data,
    }: {
      scholarshipId: string;
      data: Record<string, unknown>;
    }) => userAPI.applyForScholarship(scholarshipId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["user", "applications"] });
    },
  });
};

export const useAddBookmark = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: userAPI.addBookmark,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["user", "bookmarks"] });
    },
  });
};

export const useRemoveBookmark = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: userAPI.removeBookmark,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["user", "bookmarks"] });
    },
  });
};

export const useMarkNotificationAsRead = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: userAPI.markNotificationAsRead,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["user", "notifications"] });
    },
  });
};
