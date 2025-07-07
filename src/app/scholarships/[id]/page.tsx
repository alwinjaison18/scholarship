"use client";

import { useState } from "react";
import Link from "next/link";
import {
  ArrowLeft,
  Calendar,
  MapPin,
  IndianRupee,
  GraduationCap,
  Building,
  Clock,
  Eye,
  Heart,
  Share2,
  ExternalLink,
  CheckCircle,
  AlertCircle,
  Info,
  Download,
  Bell,
  Users,
  TrendingUp,
  Award,
  BookOpen,
  FileText,
  Phone,
  Mail,
  Globe,
  Star,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import Navigation from "@/components/navigation";
import {
  cn,
  formatDate,
  getDaysUntilDeadline,
  getDeadlineStatusWithColors,
} from "@/lib/utils";

// Mock scholarship data
const SCHOLARSHIP_DETAIL = {
  id: 1,
  title: "National Scholarship Portal - Merit Scholarship",
  provider: "Ministry of Education, Government of India",
  amount: 12000,
  deadline: "2025-03-31",
  applicationStart: "2024-10-01",
  category: "Merit Based",
  eligibility:
    "Students who have passed Class 10th with minimum 60% marks from a recognized board",
  description:
    "This is a merit-based scholarship scheme for students from economically weaker sections of society. The scholarship aims to support students in pursuing higher education by providing financial assistance for tuition fees, books, and other educational expenses.",
  detailedDescription: `The National Scholarship Portal Merit Scholarship is designed to support academically excellent students from economically disadvantaged backgrounds. This comprehensive program ensures that financial constraints do not become a barrier to quality education.

The scholarship covers various aspects of education including tuition fees, examination fees, library fees, and other compulsory charges. Additionally, it provides maintenance allowance for day scholars and hostel charges for students living in hostels.

This initiative is part of the Government of India's commitment to promoting inclusive education and ensuring that every meritorious student gets the opportunity to pursue higher education regardless of their economic background.`,
  location: "All India",
  verified: true,
  trending: true,
  views: 2456,
  applications: 1234,
  tags: ["Government", "Merit", "All India", "Class 10th"],
  educationLevel: "Class 10th Pass",
  field: "All Fields",

  // Additional details
  benefits: [
    "Tuition fee reimbursement up to ₹12,000 per year",
    "Maintenance allowance for day scholars",
    "Additional allowance for hostel students",
    "Book and stationery allowance",
    "One-time computer/laptop allowance",
    "Internet connectivity support",
  ],

  eligibilityDetails: [
    "Must have passed Class 10th with minimum 60% marks",
    "Family income should not exceed ₹6 lakh per annum",
    "Must be enrolled in a recognized educational institution",
    "Indian citizen with valid identity proof",
    "Should not be receiving any other scholarship",
    "Must maintain minimum 75% attendance",
  ],

  requiredDocuments: [
    "Class 10th marksheet and certificate",
    "Income certificate (issued by competent authority)",
    "Caste certificate (if applicable)",
    "Bank account details and passbook copy",
    "Aadhaar card",
    "Passport size photographs",
    "Institution admission letter",
    "Fee receipt of current academic year",
  ],

  applicationProcess: [
    "Visit the National Scholarship Portal (scholarships.gov.in)",
    "Register using your mobile number and email ID",
    "Fill the online application form with accurate details",
    "Upload all required documents in prescribed format",
    "Submit the application and note down the application ID",
    "Take a printout of the submitted application",
    "Submit physical documents to your institution if required",
    "Track application status regularly on the portal",
  ],

  selectionCriteria: [
    "Academic merit (Class 10th percentage)",
    "Family income verification",
    "Document verification",
    "Institution verification",
    "State/UT wise allocation",
    "Category-wise distribution",
  ],

  importantDates: [
    { event: "Application Start", date: "2024-10-01" },
    { event: "Application Deadline", date: "2025-03-31" },
    { event: "Document Verification", date: "2025-04-15" },
    { event: "Merit List Declaration", date: "2025-05-30" },
    { event: "Scholarship Disbursement", date: "2025-06-30" },
  ],

  contactInfo: {
    website: "https://scholarships.gov.in",
    email: "helpdesk@nsp.gov.in",
    phone: "+91-120-6619540",
    address: "Ministry of Education, Shastri Bhawan, New Delhi - 110001",
  },

  faqs: [
    {
      question: "Can I apply if I'm already receiving another scholarship?",
      answer:
        "No, you cannot receive multiple government scholarships simultaneously. You need to choose one scholarship program.",
    },
    {
      question: "What happens if I don't maintain the required attendance?",
      answer:
        "Your scholarship may be discontinued if you fail to maintain minimum 75% attendance consistently.",
    },
    {
      question: "How is the scholarship amount disbursed?",
      answer:
        "The scholarship amount is directly transferred to your bank account through DBT (Direct Benefit Transfer) system.",
    },
    {
      question: "Can I apply for renewal of this scholarship?",
      answer:
        "Yes, you can apply for renewal every year subject to maintaining academic performance and eligibility criteria.",
    },
  ],
};

export default function ScholarshipDetailPage() {
  const [isSaved, setIsSaved] = useState(false);
  const [activeTab, setActiveTab] = useState("overview");

  const deadlineStatusInfo = getDeadlineStatusWithColors(
    SCHOLARSHIP_DETAIL.deadline
  );
  const daysLeft = getDaysUntilDeadline(SCHOLARSHIP_DETAIL.deadline);

  const formatAmount = (amount: number) => {
    if (amount >= 100000) {
      return `₹${(amount / 100000).toFixed(1)} Lakh`;
    } else if (amount >= 1000) {
      return `₹${(amount / 1000).toFixed(1)}K`;
    } else {
      return `₹${amount.toLocaleString()}`;
    }
  };

  const tabs = [
    { id: "overview", label: "Overview", icon: Info },
    { id: "eligibility", label: "Eligibility", icon: CheckCircle },
    { id: "documents", label: "Documents", icon: FileText },
    { id: "process", label: "How to Apply", icon: BookOpen },
    { id: "faq", label: "FAQ", icon: AlertCircle },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation />

      {/* Header */}
      <div className="bg-white border-b border-gray-200 shadow-sm">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center gap-4 mb-4">
            <Link href="/scholarships">
              <Button
                variant="ghost"
                size="sm"
                className="flex items-center gap-2"
              >
                <ArrowLeft className="h-4 w-4" />
                Back to Search
              </Button>
            </Link>
          </div>

          <div className="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-6">
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-3">
                <Badge variant="secondary" className="text-sm">
                  {SCHOLARSHIP_DETAIL.category}
                </Badge>
                {SCHOLARSHIP_DETAIL.verified && (
                  <Badge
                    variant="outline"
                    className="text-sm text-green-600 border-green-200"
                  >
                    <CheckCircle className="h-3 w-3 mr-1" />
                    Verified
                  </Badge>
                )}
                {SCHOLARSHIP_DETAIL.trending && (
                  <Badge
                    variant="outline"
                    className="text-sm text-orange-600 border-orange-200"
                  >
                    <TrendingUp className="h-3 w-3 mr-1" />
                    Trending
                  </Badge>
                )}
              </div>

              <h1 className="text-2xl lg:text-3xl font-bold text-gray-900 mb-2 leading-tight">
                {SCHOLARSHIP_DETAIL.title}
              </h1>

              <p className="text-lg text-gray-600 mb-4">
                {SCHOLARSHIP_DETAIL.provider}
              </p>

              <div className="flex flex-wrap items-center gap-4 text-sm text-gray-600">
                <div className="flex items-center gap-1">
                  <Eye className="h-4 w-4" />
                  {SCHOLARSHIP_DETAIL.views.toLocaleString()} views
                </div>
                <div className="flex items-center gap-1">
                  <Users className="h-4 w-4" />
                  {SCHOLARSHIP_DETAIL.applications.toLocaleString()}{" "}
                  applications
                </div>
                <div className="flex items-center gap-1">
                  <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                  4.8 rating
                </div>
              </div>
            </div>

            {/* Quick Actions */}
            <div className="flex items-center gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setIsSaved(!isSaved)}
                className="flex items-center gap-2"
              >
                <Heart
                  className={cn(
                    "h-4 w-4",
                    isSaved ? "fill-red-500 text-red-500" : "text-gray-500"
                  )}
                />
                {isSaved ? "Saved" : "Save"}
              </Button>

              <Button
                variant="outline"
                size="sm"
                className="flex items-center gap-2"
              >
                <Share2 className="h-4 w-4" />
                Share
              </Button>

              <Button
                variant="outline"
                size="sm"
                className="flex items-center gap-2"
              >
                <Bell className="h-4 w-4" />
                Notify
              </Button>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-6">
        <div className="flex flex-col lg:flex-row gap-6">
          {/* Main Content */}
          <div className="flex-1">
            {/* Key Information Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
              <Card className="bg-gradient-to-br from-green-50 to-emerald-50 border-green-200">
                <CardContent className="p-4">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-green-100 rounded-lg">
                      <IndianRupee className="h-5 w-5 text-green-600" />
                    </div>
                    <div>
                      <p className="text-sm text-green-700 font-medium">
                        Amount
                      </p>
                      <p className="text-lg font-bold text-green-800">
                        {formatAmount(SCHOLARSHIP_DETAIL.amount)}
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card
                className={cn(
                  "border-2",
                  deadlineStatusInfo.bgColor,
                  deadlineStatusInfo.status === "urgent"
                    ? "border-red-200"
                    : "border-orange-200"
                )}
              >
                <CardContent className="p-4">
                  <div className="flex items-center gap-3">
                    <div
                      className={cn(
                        "p-2 rounded-lg",
                        deadlineStatusInfo.status === "urgent"
                          ? "bg-red-100"
                          : "bg-orange-100"
                      )}
                    >
                      <Clock
                        className={cn("h-5 w-5", deadlineStatusInfo.color)}
                      />
                    </div>
                    <div>
                      <p
                        className={cn(
                          "text-sm font-medium",
                          deadlineStatusInfo.color
                        )}
                      >
                        Deadline
                      </p>
                      <p
                        className={cn(
                          "text-lg font-bold",
                          deadlineStatusInfo.color
                        )}
                      >
                        {daysLeft > 0 ? `${daysLeft} days left` : "Expired"}
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-gradient-to-br from-blue-50 to-indigo-50 border-blue-200">
                <CardContent className="p-4">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-blue-100 rounded-lg">
                      <MapPin className="h-5 w-5 text-blue-600" />
                    </div>
                    <div>
                      <p className="text-sm text-blue-700 font-medium">
                        Location
                      </p>
                      <p className="text-lg font-bold text-blue-800">
                        {SCHOLARSHIP_DETAIL.location}
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-gradient-to-br from-purple-50 to-violet-50 border-purple-200">
                <CardContent className="p-4">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-purple-100 rounded-lg">
                      <GraduationCap className="h-5 w-5 text-purple-600" />
                    </div>
                    <div>
                      <p className="text-sm text-purple-700 font-medium">
                        Level
                      </p>
                      <p className="text-lg font-bold text-purple-800">
                        {SCHOLARSHIP_DETAIL.educationLevel}
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Navigation Tabs */}
            <div className="border-b border-gray-200 mb-6">
              <nav className="flex space-x-8 overflow-x-auto">
                {tabs.map((tab) => {
                  const Icon = tab.icon;
                  return (
                    <button
                      key={tab.id}
                      onClick={() => setActiveTab(tab.id)}
                      className={cn(
                        "flex items-center gap-2 py-3 px-1 border-b-2 font-medium text-sm whitespace-nowrap",
                        activeTab === tab.id
                          ? "border-blue-500 text-blue-600"
                          : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
                      )}
                    >
                      <Icon className="h-4 w-4" />
                      {tab.label}
                    </button>
                  );
                })}
              </nav>
            </div>

            {/* Tab Content */}
            <div className="space-y-6">
              {activeTab === "overview" && (
                <div className="space-y-6">
                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2">
                        <Info className="h-5 w-5 text-blue-600" />
                        About This Scholarship
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-gray-700 leading-relaxed mb-4">
                        {SCHOLARSHIP_DETAIL.description}
                      </p>
                      <div className="prose prose-gray max-w-none">
                        {SCHOLARSHIP_DETAIL.detailedDescription
                          .split("\n\n")
                          .map((paragraph, index) => (
                            <p
                              key={index}
                              className="text-gray-700 leading-relaxed mb-4"
                            >
                              {paragraph}
                            </p>
                          ))}
                      </div>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2">
                        <Award className="h-5 w-5 text-green-600" />
                        Benefits & Coverage
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <ul className="space-y-3">
                        {SCHOLARSHIP_DETAIL.benefits.map((benefit, index) => (
                          <li key={index} className="flex items-start gap-3">
                            <CheckCircle className="h-5 w-5 text-green-600 mt-0.5 flex-shrink-0" />
                            <span className="text-gray-700">{benefit}</span>
                          </li>
                        ))}
                      </ul>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2">
                        <Calendar className="h-5 w-5 text-purple-600" />
                        Important Dates
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-3">
                        {SCHOLARSHIP_DETAIL.importantDates.map(
                          (item, index) => (
                            <div
                              key={index}
                              className="flex items-center justify-between py-2 border-b border-gray-100 last:border-0"
                            >
                              <span className="font-medium text-gray-900">
                                {item.event}
                              </span>
                              <span className="text-gray-600">
                                {formatDate(item.date)}
                              </span>
                            </div>
                          )
                        )}
                      </div>
                    </CardContent>
                  </Card>
                </div>
              )}

              {activeTab === "eligibility" && (
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <CheckCircle className="h-5 w-5 text-green-600" />
                      Eligibility Criteria
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-3">
                      {SCHOLARSHIP_DETAIL.eligibilityDetails.map(
                        (criteria, index) => (
                          <li key={index} className="flex items-start gap-3">
                            <div className="w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                              <span className="text-blue-600 text-sm font-semibold">
                                {index + 1}
                              </span>
                            </div>
                            <span className="text-gray-700">{criteria}</span>
                          </li>
                        )
                      )}
                    </ul>

                    <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
                      <h4 className="font-semibold text-blue-900 mb-2">
                        Selection Criteria
                      </h4>
                      <ul className="space-y-2">
                        {SCHOLARSHIP_DETAIL.selectionCriteria.map(
                          (criteria, index) => (
                            <li
                              key={index}
                              className="flex items-center gap-2 text-blue-800"
                            >
                              <div className="w-1.5 h-1.5 bg-blue-600 rounded-full"></div>
                              {criteria}
                            </li>
                          )
                        )}
                      </ul>
                    </div>
                  </CardContent>
                </Card>
              )}

              {activeTab === "documents" && (
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <FileText className="h-5 w-5 text-orange-600" />
                      Required Documents
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {SCHOLARSHIP_DETAIL.requiredDocuments.map(
                        (document, index) => (
                          <div
                            key={index}
                            className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg"
                          >
                            <FileText className="h-5 w-5 text-gray-600 mt-0.5 flex-shrink-0" />
                            <span className="text-gray-700">{document}</span>
                          </div>
                        )
                      )}
                    </div>

                    <div className="mt-6 p-4 bg-yellow-50 rounded-lg border border-yellow-200">
                      <div className="flex items-start gap-3">
                        <AlertCircle className="h-5 w-5 text-yellow-600 mt-0.5 flex-shrink-0" />
                        <div>
                          <h4 className="font-semibold text-yellow-900 mb-1">
                            Important Notes
                          </h4>
                          <ul className="text-yellow-800 text-sm space-y-1">
                            <li>
                              • All documents must be in PDF format and under
                              200KB
                            </li>
                            <li>
                              • Scanned copies should be clear and readable
                            </li>
                            <li>
                              • Self-attested copies are required for
                              verification
                            </li>
                            <li>
                              • Original documents may be required during final
                              verification
                            </li>
                          </ul>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )}

              {activeTab === "process" && (
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <BookOpen className="h-5 w-5 text-blue-600" />
                      Application Process
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {SCHOLARSHIP_DETAIL.applicationProcess.map(
                        (step, index) => (
                          <div key={index} className="flex items-start gap-4">
                            <div className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center flex-shrink-0 font-semibold">
                              {index + 1}
                            </div>
                            <div className="flex-1">
                              <p className="text-gray-700 leading-relaxed">
                                {step}
                              </p>
                              {index <
                                SCHOLARSHIP_DETAIL.applicationProcess.length -
                                  1 && (
                                <div className="w-0.5 h-6 bg-gray-200 ml-4 mt-2"></div>
                              )}
                            </div>
                          </div>
                        )
                      )}
                    </div>
                  </CardContent>
                </Card>
              )}

              {activeTab === "faq" && (
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <AlertCircle className="h-5 w-5 text-purple-600" />
                      Frequently Asked Questions
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {SCHOLARSHIP_DETAIL.faqs.map((faq, index) => (
                        <div
                          key={index}
                          className="border border-gray-200 rounded-lg p-4"
                        >
                          <h4 className="font-semibold text-gray-900 mb-2">
                            {faq.question}
                          </h4>
                          <p className="text-gray-700 leading-relaxed">
                            {faq.answer}
                          </p>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              )}
            </div>
          </div>

          {/* Sidebar */}
          <div className="lg:w-80">
            <div className="lg:sticky lg:top-6 space-y-6">
              {/* Apply Now Card */}
              <Card className="border-2 border-blue-200 bg-gradient-to-br from-blue-50 to-indigo-50">
                <CardContent className="p-6">
                  <div className="text-center">
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">
                      Ready to Apply?
                    </h3>
                    <p className="text-sm text-gray-600 mb-4">
                      Don&apos;t miss this opportunity. Apply before{" "}
                      {formatDate(SCHOLARSHIP_DETAIL.deadline)}
                    </p>
                    <Button
                      size="lg"
                      className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 mb-3"
                    >
                      <ExternalLink className="h-4 w-4 mr-2" />
                      Apply Now
                    </Button>
                    <Button variant="outline" size="sm" className="w-full">
                      <Download className="h-4 w-4 mr-2" />
                      Download Details
                    </Button>
                  </div>
                </CardContent>
              </Card>

              {/* Contact Information */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Contact Information</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-start gap-3">
                    <Globe className="h-5 w-5 text-gray-500 mt-0.5 flex-shrink-0" />
                    <div>
                      <p className="text-sm text-gray-600">Website</p>
                      <a
                        href={SCHOLARSHIP_DETAIL.contactInfo.website}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-600 hover:text-blue-800 font-medium"
                      >
                        scholarships.gov.in
                      </a>
                    </div>
                  </div>

                  <div className="flex items-start gap-3">
                    <Mail className="h-5 w-5 text-gray-500 mt-0.5 flex-shrink-0" />
                    <div>
                      <p className="text-sm text-gray-600">Email</p>
                      <a
                        href={`mailto:${SCHOLARSHIP_DETAIL.contactInfo.email}`}
                        className="text-blue-600 hover:text-blue-800 font-medium"
                      >
                        {SCHOLARSHIP_DETAIL.contactInfo.email}
                      </a>
                    </div>
                  </div>

                  <div className="flex items-start gap-3">
                    <Phone className="h-5 w-5 text-gray-500 mt-0.5 flex-shrink-0" />
                    <div>
                      <p className="text-sm text-gray-600">Phone</p>
                      <a
                        href={`tel:${SCHOLARSHIP_DETAIL.contactInfo.phone}`}
                        className="text-blue-600 hover:text-blue-800 font-medium"
                      >
                        {SCHOLARSHIP_DETAIL.contactInfo.phone}
                      </a>
                    </div>
                  </div>

                  <div className="flex items-start gap-3">
                    <Building className="h-5 w-5 text-gray-500 mt-0.5 flex-shrink-0" />
                    <div>
                      <p className="text-sm text-gray-600">Address</p>
                      <p className="text-gray-900">
                        {SCHOLARSHIP_DETAIL.contactInfo.address}
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Related Scholarships */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">
                    Similar Scholarships
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {[
                    {
                      title: "Central Sector Scholarship",
                      amount: "₹20K",
                      deadline: "Feb 28",
                    },
                    {
                      title: "INSPIRE Scholarship",
                      amount: "₹80K",
                      deadline: "Apr 30",
                    },
                    {
                      title: "Post Matric Scholarship",
                      amount: "₹15K",
                      deadline: "Mar 15",
                    },
                  ].map((scholarship, index) => (
                    <div
                      key={index}
                      className="p-3 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer"
                    >
                      <h4 className="font-medium text-gray-900 text-sm mb-1">
                        {scholarship.title}
                      </h4>
                      <div className="flex items-center justify-between text-xs text-gray-600">
                        <span>Up to {scholarship.amount}</span>
                        <span>Due {scholarship.deadline}</span>
                      </div>
                    </div>
                  ))}
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
