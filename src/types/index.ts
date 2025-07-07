/* eslint-disable @typescript-eslint/no-explicit-any */
// This file contains type definitions that legitimately need 'any' types
// for generic interfaces and flexible API structures

export interface Scholarship {
  id: string;
  title: string;
  description: string;
  amount: number;
  deadline: string;
  eligibility: string[];
  applicationUrl: string;
  source: string;
  category: ScholarshipCategory;
  level: EducationLevel;
  state?: string;
  qualityScore: number;
  isVerified: boolean;
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
  lastValidated: string;
  tags: string[];
  requiredDocuments: string[];
  provider: string;
  contactEmail?: string;
  contactPhone?: string;
  applicationProcess: string;
  benefits: string[];
  selectionCriteria: string[];
  numberOfAwards?: number;
  renewalPolicy?: string;
  disbursementSchedule?: string;
  websiteUrl?: string;
  logoUrl?: string;
  bannerImageUrl?: string;
  faqUrl?: string;
  testimonials?: Testimonial[];
  relatedScholarships?: string[];
  viewCount: number;
  applicationCount: number;
  successRate?: number;
  lastUpdated: string;
  scrapedAt: string;
  validationStatus: ValidationStatus;
  validationErrors?: string[];
  duplicateOf?: string;
  priority: Priority;
  targetAudience: TargetAudience;
  fundingType: FundingType;
  applicationFee?: number;
  currency: string;
  minAmount?: number;
  maxAmount?: number;
  averageAmount?: number;
  geographicScope: GeographicScope;
  applicationDeadline: string;
  resultDate?: string;
  disbursementDate?: string;
  duration: string;
  isRecurring: boolean;
  frequency?: string;
  eligibilityGrade?: string;
  eligibilityIncome?: string;
  eligibilityGender?: string;
  eligibilityCategory?: string;
  eligibilityDisability?: boolean;
  eligibilityMinority?: boolean;
  processingSLA?: string;
  supportContact?: string;
  applicationGuide?: string;
  sampleApplications?: string[];
  previousWinners?: string[];
  statistics?: ScholarshipStatistics;
  reviews?: Review[];
  ratings?: Rating;
  socialMedia?: SocialMediaLinks;
  externalLinks?: ExternalLink[];
  metadata?: Record<string, any>;
}

export interface ScholarshipStatistics {
  totalApplications: number;
  totalAwards: number;
  successRate: number;
  averageAmount: number;
  popularityScore: number;
  viewsThisMonth: number;
  applicationsThisMonth: number;
  competitionLevel: "low" | "medium" | "high";
  geographicDistribution: Record<string, number>;
  demographicBreakdown: Record<string, number>;
}

export interface Review {
  id: string;
  userId: string;
  userName: string;
  rating: number;
  comment: string;
  isVerified: boolean;
  helpfulCount: number;
  createdAt: string;
  status: "pending" | "approved" | "rejected";
}

export interface Rating {
  overall: number;
  applicationProcess: number;
  supportQuality: number;
  timelyDisbursement: number;
  clarity: number;
  totalReviews: number;
}

export interface SocialMediaLinks {
  facebook?: string;
  twitter?: string;
  instagram?: string;
  linkedin?: string;
  youtube?: string;
}

export interface ExternalLink {
  title: string;
  url: string;
  type: "official" | "news" | "guide" | "forum" | "other";
  isVerified: boolean;
}

export interface Testimonial {
  id: string;
  studentName: string;
  studentPhoto?: string;
  amount: number;
  year: string;
  quote: string;
  university?: string;
  course?: string;
  isVerified: boolean;
}

export type ScholarshipCategory =
  | "merit"
  | "need-based"
  | "minority"
  | "women"
  | "disabled"
  | "sports"
  | "arts"
  | "science"
  | "technology"
  | "medical"
  | "engineering"
  | "law"
  | "management"
  | "agriculture"
  | "research"
  | "international"
  | "state-specific"
  | "central-government"
  | "private"
  | "corporate"
  | "ngo"
  | "other";

export type EducationLevel =
  | "pre-matric"
  | "post-matric"
  | "graduation"
  | "post-graduation"
  | "doctorate"
  | "diploma"
  | "certificate"
  | "skill-development"
  | "research"
  | "professional"
  | "vocational"
  | "all-levels";

export type ValidationStatus =
  | "pending"
  | "validated"
  | "failed"
  | "expired"
  | "suspicious"
  | "duplicate"
  | "inactive";

export type Priority = "low" | "medium" | "high" | "urgent";

export type TargetAudience =
  | "students"
  | "researchers"
  | "professionals"
  | "artists"
  | "athletes"
  | "entrepreneurs"
  | "women"
  | "minorities"
  | "disabled"
  | "rural"
  | "urban"
  | "general";

export type FundingType =
  | "government"
  | "private"
  | "corporate"
  | "international"
  | "ngo"
  | "university"
  | "trust"
  | "foundation"
  | "crowdfunded";

export type GeographicScope =
  | "national"
  | "state"
  | "district"
  | "local"
  | "international"
  | "regional";

export interface ScholarshipFilter {
  category?: ScholarshipCategory[];
  level?: EducationLevel[];
  state?: string[];
  amount?: {
    min?: number;
    max?: number;
  };
  deadline?: {
    from?: string;
    to?: string;
  };
  isActive?: boolean;
  isVerified?: boolean;
  source?: string[];
  tags?: string[];
  priority?: Priority[];
  targetAudience?: TargetAudience[];
  fundingType?: FundingType[];
  geographicScope?: GeographicScope[];
  search?: string;
  sortBy?:
    | "deadline"
    | "amount"
    | "created"
    | "updated"
    | "relevance"
    | "popularity";
  sortOrder?: "asc" | "desc";
  page?: number;
  limit?: number;
}

export interface ScholarshipSearchResult {
  scholarships: Scholarship[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
  hasNextPage: boolean;
  hasPreviousPage: boolean;
  filters: ScholarshipFilter;
  aggregations?: {
    categories: Record<string, number>;
    levels: Record<string, number>;
    states: Record<string, number>;
    sources: Record<string, number>;
    amounts: {
      min: number;
      max: number;
      avg: number;
    };
  };
}

export interface User {
  id: string;
  email: string;
  name: string;
  avatar?: string;
  role: UserRole;
  isActive: boolean;
  isVerified: boolean;
  createdAt: string;
  updatedAt: string;
  lastLogin?: string;
  preferences?: UserPreferences;
  profile?: UserProfile;
  bookmarks?: string[];
  applications?: Application[];
  notifications?: Notification[];
  activityLog?: ActivityLog[];
}

export type UserRole = "student" | "admin" | "moderator" | "scraper" | "guest";

export interface UserPreferences {
  emailNotifications: boolean;
  pushNotifications: boolean;
  categories: ScholarshipCategory[];
  states: string[];
  levels: EducationLevel[];
  minAmount: number;
  maxAmount: number;
  language: string;
  theme: "light" | "dark" | "auto";
  currency: string;
  timezone: string;
  digestFrequency: "daily" | "weekly" | "monthly" | "never";
  alertDeadline: number; // days before deadline
}

export interface UserProfile {
  firstName: string;
  lastName: string;
  dateOfBirth?: string;
  gender?: string;
  phone?: string;
  address?: Address;
  education?: Education[];
  documents?: Document[];
  income?: number;
  category?: string;
  isDisabled?: boolean;
  isMinority?: boolean;
  parentOccupation?: string;
  academicPerformance?: AcademicPerformance;
  extracurriculars?: string[];
  achievements?: string[];
  languagesKnown?: string[];
  socialMedia?: SocialMediaLinks;
  bio?: string;
  profileCompleted: boolean;
  verificationStatus: "pending" | "verified" | "rejected";
  verificationDocuments?: string[];
}

export interface Address {
  street?: string;
  city: string;
  state: string;
  pincode: string;
  country: string;
  isCurrentAddress: boolean;
  isPermanentAddress: boolean;
}

export interface Education {
  id: string;
  level: EducationLevel;
  institution: string;
  course: string;
  year: number;
  percentage?: number;
  cgpa?: number;
  isCompleted: boolean;
  certificates?: string[];
}

export interface Document {
  id: string;
  type: DocumentType;
  title: string;
  url: string;
  isVerified: boolean;
  uploadedAt: string;
  expiresAt?: string;
  size: number;
  format: string;
}

export type DocumentType =
  | "identity"
  | "address"
  | "income"
  | "caste"
  | "academic"
  | "bank"
  | "photo"
  | "signature"
  | "disability"
  | "other";

export interface AcademicPerformance {
  overall?: number;
  subjects?: Record<string, number>;
  rank?: number;
  percentile?: number;
  grade?: string;
  awards?: string[];
  publications?: string[];
  projects?: string[];
}

export interface Application {
  id: string;
  scholarshipId: string;
  userId: string;
  status: ApplicationStatus;
  submittedAt: string;
  reviewedAt?: string;
  approvedAt?: string;
  rejectedAt?: string;
  disbursedAt?: string;
  amount?: number;
  reviewerNotes?: string;
  documents: string[];
  responses: Record<string, any>;
  score?: number;
  rank?: number;
  feedback?: string;
  trackingId: string;
  communicationHistory?: Communication[];
  deadlineReminders?: Reminder[];
  followUpRequired?: boolean;
  priority: Priority;
  source: string;
  referenceNumber?: string;
  bankDetails?: BankDetails;
  disbursementDetails?: DisbursementDetails;
  renewalEligible?: boolean;
  nextRenewalDate?: string;
  conditions?: string[];
  reportingRequirements?: string[];
  acknowledgments?: string[];
  certifications?: string[];
  appeals?: Appeal[];
  metadata?: Record<string, any>;
}

export type ApplicationStatus =
  | "draft"
  | "submitted"
  | "under-review"
  | "shortlisted"
  | "approved"
  | "rejected"
  | "waitlisted"
  | "withdrawn"
  | "expired"
  | "disbursed"
  | "completed"
  | "appeal-pending"
  | "appeal-approved"
  | "appeal-rejected";

export interface Communication {
  id: string;
  type: "email" | "sms" | "push" | "call" | "letter";
  subject: string;
  content: string;
  sender: string;
  recipient: string;
  sentAt: string;
  isRead: boolean;
  isDelivered: boolean;
  attachments?: string[];
  priority: Priority;
  category:
    | "application"
    | "deadline"
    | "approval"
    | "rejection"
    | "disbursement"
    | "reminder"
    | "general";
}

export interface Reminder {
  id: string;
  type: "deadline" | "document" | "interview" | "disbursement" | "renewal";
  title: string;
  description: string;
  dueDate: string;
  isCompleted: boolean;
  reminderDates: string[];
  methods: ("email" | "sms" | "push")[];
  priority: Priority;
}

export interface BankDetails {
  accountNumber: string;
  ifscCode: string;
  bankName: string;
  branchName: string;
  accountHolderName: string;
  accountType: "savings" | "current";
  isVerified: boolean;
  verificationMethod?: string;
  verifiedAt?: string;
}

export interface DisbursementDetails {
  amount: number;
  disbursedAmount: number;
  currency: string;
  method: "bank-transfer" | "cheque" | "cash" | "digital-wallet";
  transactionId?: string;
  transactionDate?: string;
  processingFee?: number;
  taxes?: number;
  netAmount: number;
  installments?: Installment[];
  conditions?: string[];
  acknowledgment?: string;
  receipt?: string;
  status: "pending" | "processing" | "completed" | "failed" | "reversed";
  failureReason?: string;
  retryAttempts?: number;
  nextRetryDate?: string;
}

export interface Installment {
  sequence: number;
  amount: number;
  dueDate: string;
  disbursedDate?: string;
  status: "pending" | "disbursed" | "overdue" | "cancelled";
  transactionId?: string;
  conditions?: string[];
}

export interface Appeal {
  id: string;
  reason: string;
  description: string;
  evidence?: string[];
  submittedAt: string;
  reviewedAt?: string;
  decision?: "approved" | "rejected" | "pending";
  reviewerNotes?: string;
  appealLevel: 1 | 2 | 3;
  nextAppealDate?: string;
  supportingDocuments?: string[];
  hearingDate?: string;
  hearingMode?: "online" | "offline";
  finalDecision?: boolean;
}

export interface Notification {
  id: string;
  userId: string;
  type: NotificationType;
  title: string;
  message: string;
  data?: Record<string, any>;
  isRead: boolean;
  isClicked: boolean;
  createdAt: string;
  expiresAt?: string;
  priority: Priority;
  category:
    | "scholarship"
    | "application"
    | "deadline"
    | "system"
    | "promotional";
  channels: ("email" | "sms" | "push" | "in-app")[];
  deliveryStatus: Record<string, "pending" | "sent" | "delivered" | "failed">;
  actions?: NotificationAction[];
  metadata?: Record<string, any>;
}

export type NotificationType =
  | "new-scholarship"
  | "deadline-reminder"
  | "application-status"
  | "document-required"
  | "interview-scheduled"
  | "approval-notification"
  | "rejection-notification"
  | "disbursement-notification"
  | "renewal-reminder"
  | "system-maintenance"
  | "security-alert"
  | "promotional"
  | "feedback-request"
  | "survey-invitation"
  | "newsletter";

export interface NotificationAction {
  id: string;
  label: string;
  type: "link" | "button" | "form";
  url?: string;
  action?: string;
  data?: Record<string, any>;
  isPrimary?: boolean;
  isDestructive?: boolean;
}

export interface ActivityLog {
  id: string;
  userId: string;
  action: string;
  resource: string;
  resourceId?: string;
  details?: Record<string, any>;
  ipAddress?: string;
  userAgent?: string;
  timestamp: string;
  sessionId?: string;
  location?: string;
  device?: string;
  success: boolean;
  errorMessage?: string;
  metadata?: Record<string, any>;
}

export interface ScrapingJob {
  id: string;
  source: string;
  url: string;
  status: "pending" | "running" | "completed" | "failed" | "cancelled";
  startedAt?: string;
  completedAt?: string;
  duration?: number;
  itemsScraped: number;
  itemsValidated: number;
  itemsStored: number;
  errors?: string[];
  warnings?: string[];
  metadata?: Record<string, any>;
  priority: Priority;
  retryCount: number;
  maxRetries: number;
  nextRetryAt?: string;
  scheduledFor?: string;
  isRecurring: boolean;
  frequency?: string;
  lastSuccessAt?: string;
  consecutiveFailures: number;
  healthScore: number;
  configuration?: ScrapingConfiguration;
  performance?: ScrapingPerformance;
}

export interface ScrapingConfiguration {
  selectors?: Record<string, string>;
  pagination?: {
    enabled: boolean;
    maxPages?: number;
    nextPageSelector?: string;
    pageUrlPattern?: string;
  };
  rateLimit?: {
    delay: number;
    randomDelay: boolean;
    maxConcurrency: number;
  };
  validation?: {
    requiredFields: string[];
    minQualityScore: number;
    duplicateCheckEnabled: boolean;
  };
  filters?: {
    includePatterns?: string[];
    excludePatterns?: string[];
    minDeadlineDays?: number;
    maxAge?: number;
  };
  headers?: Record<string, string>;
  cookies?: Record<string, string>;
  proxy?: {
    enabled: boolean;
    rotation: boolean;
    servers?: string[];
  };
  browserOptions?: {
    headless: boolean;
    timeout: number;
    userAgent?: string;
    viewport?: {
      width: number;
      height: number;
    };
  };
  dataTransformation?: {
    fieldMappings?: Record<string, string>;
    textNormalization?: boolean;
    dateFormat?: string;
    currencyFormat?: string;
  };
  storage?: {
    temporary: boolean;
    compression: boolean;
    encryption: boolean;
    retention: number;
  };
}

export interface ScrapingPerformance {
  averageResponseTime: number;
  successRate: number;
  errorRate: number;
  throughput: number;
  memoryUsage: number;
  cpuUsage: number;
  networkUsage: number;
  cacheHitRate: number;
  duplicateRate: number;
  validationRate: number;
  qualityScore: number;
  trends?: {
    responseTime: number[];
    successRate: number[];
    errorRate: number[];
    throughput: number[];
  };
}

export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
  timestamp: string;
  requestId?: string;
  pagination?: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
    hasNextPage: boolean;
    hasPreviousPage: boolean;
  };
  metadata?: Record<string, any>;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
  hasNextPage: boolean;
  hasPreviousPage: boolean;
}

export interface SearchParams {
  q?: string;
  category?: string;
  level?: string;
  state?: string;
  minAmount?: number;
  maxAmount?: number;
  deadline?: string;
  isActive?: boolean;
  isVerified?: boolean;
  source?: string;
  tags?: string;
  sortBy?: string;
  sortOrder?: "asc" | "desc";
  page?: number;
  limit?: number;
}

export interface DashboardStats {
  totalScholarships: number;
  activeScholarships: number;
  expiredScholarships: number;
  verifiedScholarships: number;
  totalApplications: number;
  approvedApplications: number;
  pendingApplications: number;
  rejectedApplications: number;
  totalAmount: number;
  disbursedAmount: number;
  pendingAmount: number;
  averageAmount: number;
  totalUsers: number;
  activeUsers: number;
  newUsers: number;
  totalViews: number;
  monthlyViews: number;
  popularCategories: Record<string, number>;
  popularStates: Record<string, number>;
  recentActivity: ActivityLog[];
  systemHealth: {
    scrapingJobs: number;
    failedJobs: number;
    queueSize: number;
    averageProcessingTime: number;
    errorRate: number;
    uptime: number;
  };
  trends: {
    scholarships: number[];
    applications: number[];
    users: number[];
    amount: number[];
  };
}

export interface SystemSettings {
  siteName: string;
  siteDescription: string;
  siteUrl: string;
  adminEmail: string;
  supportEmail: string;
  maintenanceMode: boolean;
  registrationEnabled: boolean;
  emailVerificationRequired: boolean;
  maxFileSize: number;
  allowedFileTypes: string[];
  cacheExpiration: number;
  sessionTimeout: number;
  passwordPolicy: {
    minLength: number;
    requireUppercase: boolean;
    requireLowercase: boolean;
    requireNumbers: boolean;
    requireSpecialChars: boolean;
  };
  notificationSettings: {
    emailEnabled: boolean;
    smsEnabled: boolean;
    pushEnabled: boolean;
    slackEnabled: boolean;
    webhookUrl?: string;
  };
  scrapingSettings: {
    enabled: boolean;
    interval: number;
    maxConcurrency: number;
    retryAttempts: number;
    timeout: number;
    respectRobotsTxt: boolean;
    userAgent: string;
    minQualityScore: number;
    autoValidation: boolean;
    duplicateThreshold: number;
  };
  apiSettings: {
    rateLimit: number;
    rateLimitWindow: number;
    maxRequestSize: number;
    corsEnabled: boolean;
    corsOrigins: string[];
    apiVersion: string;
    deprecationWarnings: boolean;
  };
  securitySettings: {
    jwtSecret: string;
    jwtExpiration: number;
    refreshTokenExpiration: number;
    maxLoginAttempts: number;
    lockoutDuration: number;
    ipWhitelist: string[];
    ipBlacklist: string[];
    enableTwoFA: boolean;
    encryptionKey: string;
  };
  integrations: {
    google: {
      enabled: boolean;
      clientId?: string;
      analyticsId?: string;
      mapsApiKey?: string;
    };
    facebook: {
      enabled: boolean;
      appId?: string;
      pageId?: string;
    };
    sms: {
      enabled: boolean;
      provider?: string;
      apiKey?: string;
    };
    email: {
      enabled: boolean;
      provider?: string;
      host?: string;
      port?: number;
      username?: string;
      password?: string;
      fromAddress?: string;
      fromName?: string;
    };
    payment: {
      enabled: boolean;
      provider?: string;
      publicKey?: string;
      secretKey?: string;
      webhookSecret?: string;
    };
  };
  features: {
    aiRecommendations: boolean;
    personalizedFeed: boolean;
    socialLogin: boolean;
    mobileApp: boolean;
    offlineMode: boolean;
    darkMode: boolean;
    multiLanguage: boolean;
    accessibility: boolean;
    analytics: boolean;
    feedback: boolean;
    chat: boolean;
    forum: boolean;
    blog: boolean;
    newsletter: boolean;
    referralProgram: boolean;
    gamification: boolean;
  };
  compliance: {
    gdprCompliant: boolean;
    cookieConsent: boolean;
    privacyPolicy: string;
    termsOfService: string;
    dataRetention: number;
    rightToForgotten: boolean;
    dataPortability: boolean;
    auditLog: boolean;
    consentTracking: boolean;
  };
  performance: {
    cacheEnabled: boolean;
    cacheProvider: string;
    cdnEnabled: boolean;
    cdnUrl?: string;
    imageOptimization: boolean;
    minification: boolean;
    compression: boolean;
    lazyLoading: boolean;
    prefetching: boolean;
    serviceWorker: boolean;
  };
  monitoring: {
    enabled: boolean;
    provider?: string;
    errorTracking: boolean;
    performanceMonitoring: boolean;
    userSessionRecording: boolean;
    realUserMonitoring: boolean;
    syntheticMonitoring: boolean;
    alerting: boolean;
    reportingInterval: number;
  };
}

export interface ScholarshipFilters {
  search?: string;
  category?: ScholarshipCategory;
  level?: EducationLevel;
  state?: string;
  minAmount?: number;
  maxAmount?: number;
  deadline?: string;
  isVerified?: boolean;
  isActive?: boolean;
  tags?: string[];
  sortBy?:
    | "deadline"
    | "amount"
    | "created"
    | "updated"
    | "relevance"
    | "popularity";
  sortOrder?: "asc" | "desc";
}
