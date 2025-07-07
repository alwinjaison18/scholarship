import { NextResponse } from "next/server";

export async function GET() {
  // Mock system stats data
  const mockStats = {
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

  return NextResponse.json({
    data: mockStats,
    success: true,
    message: "Mock admin stats data",
  });
}
