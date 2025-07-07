import { NextResponse } from "next/server";

export async function GET() {
  // Mock trending scholarships data
  const mockTrendingScholarships = [
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
  ];

  return NextResponse.json({
    data: mockTrendingScholarships,
    success: true,
    message: "Mock trending scholarships data",
  });
}
