"use client";

import React from "react";
import Link from "next/link";
import Image from "next/image";
import {
  Calendar,
  MapPin,
  IndianRupee,
  Eye,
  Users,
  Clock,
  BookOpen,
  CheckCircle,
  AlertCircle,
  ExternalLink,
  Heart,
  Share2,
  Timer,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { Progress } from "@/components/ui/progress";
import {
  cn,
  formatAmount,
  getDaysUntilDeadline,
  getDeadlineStatus,
} from "@/lib/utils";

export interface ScholarshipCardProps {
  id: string;
  title: string;
  description: string;
  amount: number;
  deadline: string;
  source: string;
  category: string;
  level: string;
  state?: string;
  isVerified?: boolean;
  viewCount?: number;
  applicationCount?: number;
  qualityScore?: number;
  tags?: string[];
  provider?: string;
  logoUrl?: string;
  className?: string;
  variant?: "default" | "compact" | "featured";
  onBookmark?: (id: string) => void;
  onShare?: (id: string) => void;
  isBookmarked?: boolean;
}

export function ScholarshipCard({
  id,
  title,
  description,
  amount,
  deadline,
  source,
  category,
  level,
  state,
  isVerified = false,
  viewCount = 0,
  applicationCount = 0,
  qualityScore = 0,
  tags = [],
  provider,
  logoUrl,
  className,
  variant = "default",
  onBookmark,
  onShare,
  isBookmarked = false,
}: ScholarshipCardProps) {
  const daysUntilDeadline = getDaysUntilDeadline(deadline);
  const deadlineStatus = getDeadlineStatus(deadline);

  const getDeadlineColor = () => {
    switch (deadlineStatus) {
      case "expired":
        return "text-red-600 bg-red-50";
      case "urgent":
        return "text-orange-600 bg-orange-50";
      case "soon":
        return "text-yellow-600 bg-yellow-50";
      default:
        return "text-green-600 bg-green-50";
    }
  };

  const getDeadlineIcon = () => {
    switch (deadlineStatus) {
      case "expired":
        return <AlertCircle className="h-4 w-4" />;
      case "urgent":
        return <Timer className="h-4 w-4" />;
      case "soon":
        return <Clock className="h-4 w-4" />;
      default:
        return <Calendar className="h-4 w-4" />;
    }
  };

  const getDeadlineText = () => {
    if (deadlineStatus === "expired") return "Expired";
    if (daysUntilDeadline === 0) return "Today";
    if (daysUntilDeadline === 1) return "Tomorrow";
    return `${daysUntilDeadline} days left`;
  };

  const handleBookmark = (e: React.MouseEvent) => {
    e.preventDefault();
    onBookmark?.(id);
  };

  const handleShare = (e: React.MouseEvent) => {
    e.preventDefault();
    onShare?.(id);
  };

  if (variant === "compact") {
    return (
      <Card
        className={cn(
          "group hover:shadow-lg transition-all duration-300",
          className
        )}
      >
        <CardContent className="p-4">
          <div className="flex justify-between items-start mb-3">
            <div className="flex-1">
              <Link
                href={`/scholarships/${id}`}
                className="group-hover:text-primary transition-colors"
              >
                <h3 className="font-semibold text-lg line-clamp-2 mb-1">
                  {title}
                </h3>
              </Link>
              <p className="text-sm text-muted-foreground line-clamp-1">
                {description}
              </p>
            </div>
            <div className="flex items-center gap-1 ml-2">
              <Badge variant="secondary" className="text-xs">
                {formatAmount(amount)}
              </Badge>
            </div>
          </div>
          <div className="flex justify-between items-center text-sm text-muted-foreground">
            <div className="flex items-center gap-1">
              {getDeadlineIcon()}
              <span
                className={cn("font-medium", getDeadlineColor().split(" ")[0])}
              >
                {getDeadlineText()}
              </span>
            </div>
            <span className="text-xs">{category}</span>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (variant === "featured") {
    return (
      <Card
        className={cn(
          "group hover:shadow-xl transition-all duration-300 border-2 border-primary/20",
          className
        )}
      >
        <CardHeader className="pb-3">
          <div className="flex justify-between items-start">
            <div className="flex items-start gap-3">
              {logoUrl && (
                <Image
                  src={logoUrl}
                  alt={`${provider} logo`}
                  width={48}
                  height={48}
                  className="w-12 h-12 rounded-lg object-cover"
                />
              )}
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <Link
                    href={`/scholarships/${id}`}
                    className="group-hover:text-primary transition-colors"
                  >
                    <CardTitle className="text-xl line-clamp-2">
                      {title}
                    </CardTitle>
                  </Link>
                  {isVerified && (
                    <TooltipProvider>
                      <Tooltip>
                        <TooltipTrigger>
                          <CheckCircle className="h-5 w-5 text-green-600 flex-shrink-0" />
                        </TooltipTrigger>
                        <TooltipContent>
                          <p>Verified scholarship</p>
                        </TooltipContent>
                      </Tooltip>
                    </TooltipProvider>
                  )}
                </div>
                <p className="text-sm text-muted-foreground line-clamp-2">
                  {description}
                </p>
              </div>
            </div>
            <div className="flex items-center gap-1">
              <Button
                variant="ghost"
                size="sm"
                onClick={handleBookmark}
                className={cn(
                  "h-8 w-8 p-0",
                  isBookmarked && "text-red-500 hover:text-red-600"
                )}
              >
                <Heart
                  className={cn("h-4 w-4", isBookmarked && "fill-current")}
                />
              </Button>
              <Button
                variant="ghost"
                size="sm"
                onClick={handleShare}
                className="h-8 w-8 p-0"
              >
                <Share2 className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent className="pt-0">
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div className="flex items-center gap-2">
              <IndianRupee className="h-4 w-4 text-green-600" />
              <span className="font-semibold text-lg text-green-600">
                {formatAmount(amount)}
              </span>
            </div>
            <div
              className={cn(
                "flex items-center gap-2 px-3 py-1 rounded-full",
                getDeadlineColor()
              )}
            >
              {getDeadlineIcon()}
              <span className="font-medium text-sm">{getDeadlineText()}</span>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4 mb-4 text-sm">
            <div className="flex items-center gap-2">
              <BookOpen className="h-4 w-4 text-blue-600" />
              <span>{level}</span>
            </div>
            <div className="flex items-center gap-2">
              <MapPin className="h-4 w-4 text-purple-600" />
              <span>{state || "All India"}</span>
            </div>
            <div className="flex items-center gap-2">
              <Eye className="h-4 w-4 text-gray-600" />
              <span>{viewCount.toLocaleString()} views</span>
            </div>
            <div className="flex items-center gap-2">
              <Users className="h-4 w-4 text-orange-600" />
              <span>{applicationCount.toLocaleString()} applied</span>
            </div>
          </div>

          {qualityScore > 0 && (
            <div className="mb-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium">Quality Score</span>
                <span className="text-sm font-medium">{qualityScore}%</span>
              </div>
              <Progress value={qualityScore} className="h-2" />
            </div>
          )}

          <div className="flex flex-wrap gap-2 mb-4">
            <Badge variant="secondary">{category}</Badge>
            {tags.slice(0, 3).map((tag, index) => (
              <Badge key={index} variant="outline" className="text-xs">
                {tag}
              </Badge>
            ))}
            {tags.length > 3 && (
              <Badge variant="outline" className="text-xs">
                +{tags.length - 3} more
              </Badge>
            )}
          </div>

          <div className="flex justify-between items-center">
            <span className="text-sm text-muted-foreground">
              Source: {source}
            </span>
            <div className="flex gap-2">
              <Link href={`/scholarships/${id}`}>
                <Button variant="outline" size="sm">
                  View Details
                </Button>
              </Link>
              <Button
                size="sm"
                className="bg-gradient-primary hover:opacity-90"
              >
                Apply Now
                <ExternalLink className="h-4 w-4 ml-1" />
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card
      className={cn(
        "group hover:shadow-lg transition-all duration-300",
        className
      )}
    >
      <CardHeader className="pb-3">
        <div className="flex justify-between items-start">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-1">
              <Link
                href={`/scholarships/${id}`}
                className="group-hover:text-primary transition-colors"
              >
                <CardTitle className="text-lg line-clamp-2">{title}</CardTitle>
              </Link>
              {isVerified && (
                <TooltipProvider>
                  <Tooltip>
                    <TooltipTrigger>
                      <CheckCircle className="h-4 w-4 text-green-600 flex-shrink-0" />
                    </TooltipTrigger>
                    <TooltipContent>
                      <p>Verified scholarship</p>
                    </TooltipContent>
                  </Tooltip>
                </TooltipProvider>
              )}
            </div>
            <p className="text-sm text-muted-foreground line-clamp-2">
              {description}
            </p>
          </div>
          <div className="flex items-center gap-1 ml-2">
            <Button
              variant="ghost"
              size="sm"
              onClick={handleBookmark}
              className={cn(
                "h-8 w-8 p-0",
                isBookmarked && "text-red-500 hover:text-red-600"
              )}
            >
              <Heart
                className={cn("h-4 w-4", isBookmarked && "fill-current")}
              />
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={handleShare}
              className="h-8 w-8 p-0"
            >
              <Share2 className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </CardHeader>
      <CardContent className="pt-0">
        <div className="flex justify-between items-center mb-3">
          <div className="flex items-center gap-2">
            <IndianRupee className="h-4 w-4 text-green-600" />
            <span className="font-semibold text-lg text-green-600">
              {formatAmount(amount)}
            </span>
          </div>
          <div
            className={cn(
              "flex items-center gap-2 px-3 py-1 rounded-full",
              getDeadlineColor()
            )}
          >
            {getDeadlineIcon()}
            <span className="font-medium text-sm">{getDeadlineText()}</span>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-2 mb-3 text-sm">
          <div className="flex items-center gap-2">
            <BookOpen className="h-4 w-4 text-blue-600" />
            <span className="text-muted-foreground">{level}</span>
          </div>
          <div className="flex items-center gap-2">
            <MapPin className="h-4 w-4 text-purple-600" />
            <span className="text-muted-foreground">
              {state || "All India"}
            </span>
          </div>
        </div>

        <div className="flex flex-wrap gap-2 mb-4">
          <Badge variant="secondary">{category}</Badge>
          {tags.slice(0, 2).map((tag, index) => (
            <Badge key={index} variant="outline" className="text-xs">
              {tag}
            </Badge>
          ))}
          {tags.length > 2 && (
            <Badge variant="outline" className="text-xs">
              +{tags.length - 2} more
            </Badge>
          )}
        </div>

        <div className="flex justify-between items-center">
          <div className="flex items-center gap-3 text-xs text-muted-foreground">
            <span className="flex items-center gap-1">
              <Eye className="h-3 w-3" />
              {viewCount.toLocaleString()}
            </span>
            <span className="flex items-center gap-1">
              <Users className="h-3 w-3" />
              {applicationCount.toLocaleString()}
            </span>
          </div>
          <div className="flex gap-2">
            <Link href={`/scholarships/${id}`}>
              <Button variant="outline" size="sm">
                View Details
              </Button>
            </Link>
            <Button size="sm" className="bg-gradient-primary hover:opacity-90">
              Apply Now
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

export default ScholarshipCard;
