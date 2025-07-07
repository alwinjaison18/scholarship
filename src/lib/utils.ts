import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDate(date: Date | string) {
  return new Date(date).toLocaleDateString("en-IN", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
}

export function formatAmount(amount: number) {
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
  }).format(amount);
}

export function getDaysUntilDeadline(deadline: Date | string) {
  const now = new Date();
  const deadlineDate = new Date(deadline);
  const diffTime = deadlineDate.getTime() - now.getTime();
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  return diffDays;
}

export function getDeadlineStatus(deadline: Date | string) {
  const days = getDaysUntilDeadline(deadline);
  if (days < 0) return "expired";
  if (days <= 7) return "urgent";
  if (days <= 30) return "soon";
  return "open";
}

export function getDeadlineStatusWithColors(deadline: Date | string) {
  const days = getDaysUntilDeadline(deadline);

  if (days < 0) {
    return {
      status: "expired",
      color: "text-red-600",
      bgColor: "bg-red-100",
    };
  }

  if (days <= 7) {
    return {
      status: "urgent",
      color: "text-red-600",
      bgColor: "bg-red-100",
    };
  }

  if (days <= 30) {
    return {
      status: "soon",
      color: "text-orange-600",
      bgColor: "bg-orange-100",
    };
  }

  return {
    status: "open",
    color: "text-green-600",
    bgColor: "bg-green-100",
  };
}

export function slugify(text: string) {
  return text
    .toString()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .trim()
    .replace(/\s+/g, "-")
    .replace(/[^\w-]+/g, "")
    .replace(/--+/g, "-");
}

export function truncateText(text: string, length: number) {
  if (text.length <= length) return text;
  return text.substring(0, length) + "...";
}

export function isValidUrl(url: string) {
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
}

export function getInitials(name: string) {
  return name
    .split(" ")
    .map((word) => word[0])
    .join("")
    .toUpperCase()
    .slice(0, 2);
}

export function debounce<T extends (...args: unknown[]) => void>(
  func: T,
  delay: number
): (...args: Parameters<T>) => void {
  let timeoutId: NodeJS.Timeout;
  return (...args: Parameters<T>) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func(...args), delay);
  };
}

export function generateScholarshipId() {
  return `SCH_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

export function validateScholarshipData(data: Record<string, unknown>) {
  const required = [
    "title",
    "description",
    "deadline",
    "eligibility",
    "amount",
  ];
  return required.every(
    (field) => data[field] && data[field].toString().trim()
  );
}

export const TRUSTED_SOURCES = [
  "scholarships.gov.in",
  "buddy4study.com",
  "scholarshipsindia.com",
  "aicte-india.org",
  "ugc.ac.in",
  "scholarship.up.gov.in",
  "ekalyan.cgg.gov.in",
  "scholarship.rajasthan.gov.in",
  "scholarship.mp.gov.in",
  "scholarship.kerala.gov.in",
];

export function isTrustedSource(url: string) {
  try {
    const domain = new URL(url).hostname.toLowerCase();
    return TRUSTED_SOURCES.some((source) => domain.includes(source));
  } catch {
    return false;
  }
}

interface ScholarshipData {
  title?: string;
  description?: string;
  applicationUrl?: string;
  deadline?: string | Date;
  amount?: number;
  eligibility?: string;
  [key: string]: unknown;
}

export function getQualityScore(scholarship: ScholarshipData) {
  let score = 0;

  // Title quality (0-20)
  if (scholarship.title && scholarship.title.length > 10) score += 20;
  else if (scholarship.title && scholarship.title.length > 5) score += 15;
  else score += 10;

  // Description quality (0-20)
  if (scholarship.description && scholarship.description.length > 200)
    score += 20;
  else if (scholarship.description && scholarship.description.length > 100)
    score += 15;
  else if (scholarship.description && scholarship.description.length > 50)
    score += 10;
  else score += 5;

  // Contact/Link quality (0-20)
  if (scholarship.applicationUrl && isValidUrl(scholarship.applicationUrl))
    score += 20;
  else score += 5;

  // Deadline validity (0-15)
  if (scholarship.deadline) {
    const days = getDaysUntilDeadline(scholarship.deadline);
    if (days > 0) score += 15;
    else score += 5;
  }

  // Amount specification (0-15)
  if (scholarship.amount && scholarship.amount > 0) score += 15;
  else score += 5;

  // Eligibility details (0-10)
  if (scholarship.eligibility && scholarship.eligibility.length > 50)
    score += 10;
  else if (scholarship.eligibility && scholarship.eligibility.length > 20)
    score += 7;
  else score += 3;

  return Math.min(score, 100);
}
