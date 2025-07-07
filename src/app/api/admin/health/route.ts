import { NextResponse } from "next/server";

export async function GET() {
  // Mock system health data
  const mockHealth = {
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

  return NextResponse.json({
    data: mockHealth,
    success: true,
    message: "Mock system health data",
  });
}
