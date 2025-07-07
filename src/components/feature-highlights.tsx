"use client";

import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import { LucideIcon } from "lucide-react";

export interface FeatureItem {
  title: string;
  description: string;
  icon: LucideIcon;
  color: string;
  badge?: string;
  stats?: string;
}

export interface FeatureHighlightsProps {
  title?: string;
  subtitle?: string;
  features: FeatureItem[];
  layout?: "grid" | "list";
  variant?: "default" | "compact" | "detailed";
  className?: string;
}

export function FeatureHighlights({
  title = "Why Choose ShikshaSetu?",
  subtitle = "Discover the features that make us the trusted choice for scholarship seekers",
  features,
  layout = "grid",
  variant = "default",
  className,
}: FeatureHighlightsProps) {
  const getGridClasses = () => {
    if (layout === "list") return "space-y-4";
    if (features.length <= 2) return "grid grid-cols-1 md:grid-cols-2 gap-6";
    if (features.length <= 4)
      return "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-6";
    return "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6";
  };

  const renderFeatureCard = (feature: FeatureItem, index: number) => {
    const Icon = feature.icon;

    if (variant === "compact") {
      return (
        <Card
          key={index}
          className="group hover:shadow-lg transition-all duration-300"
        >
          <CardContent className="p-6">
            <div className="flex items-start gap-4">
              <div className={cn("p-3 rounded-lg", feature.color)}>
                <Icon className="h-6 w-6 text-white" />
              </div>
              <div className="flex-1">
                <h3 className="font-semibold text-lg mb-2">{feature.title}</h3>
                <p className="text-sm text-muted-foreground">
                  {feature.description}
                </p>
                {feature.stats && (
                  <p className="text-sm font-medium text-primary mt-2">
                    {feature.stats}
                  </p>
                )}
              </div>
            </div>
          </CardContent>
        </Card>
      );
    }

    if (variant === "detailed") {
      return (
        <Card
          key={index}
          className="group hover:shadow-xl transition-all duration-300 border-2 hover:border-primary/20"
        >
          <CardHeader className="pb-4">
            <div className="flex items-center justify-between">
              <div className={cn("p-4 rounded-xl", feature.color)}>
                <Icon className="h-8 w-8 text-white" />
              </div>
              {feature.badge && (
                <Badge variant="secondary" className="text-xs">
                  {feature.badge}
                </Badge>
              )}
            </div>
          </CardHeader>
          <CardContent className="pt-0">
            <CardTitle className="text-xl mb-3">{feature.title}</CardTitle>
            <p className="text-muted-foreground leading-relaxed mb-4">
              {feature.description}
            </p>
            {feature.stats && (
              <div className="text-lg font-semibold text-primary">
                {feature.stats}
              </div>
            )}
          </CardContent>
        </Card>
      );
    }

    return (
      <Card
        key={index}
        className="group hover:shadow-lg transition-all duration-300"
      >
        <CardContent className="p-6 text-center">
          <div
            className={cn(
              "w-16 h-16 rounded-full mx-auto mb-4 flex items-center justify-center",
              feature.color
            )}
          >
            <Icon className="h-8 w-8 text-white" />
          </div>
          <h3 className="font-semibold text-lg mb-3">{feature.title}</h3>
          <p className="text-muted-foreground mb-4">{feature.description}</p>
          {feature.badge && (
            <Badge variant="secondary" className="text-xs">
              {feature.badge}
            </Badge>
          )}
          {feature.stats && (
            <div className="text-sm font-medium text-primary mt-2">
              {feature.stats}
            </div>
          )}
        </CardContent>
      </Card>
    );
  };

  return (
    <section className={cn("py-16 lg:py-24", className)}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            {title}
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">{subtitle}</p>
        </div>

        {/* Features Grid */}
        <div className={getGridClasses()}>
          {features.map((feature, index) => renderFeatureCard(feature, index))}
        </div>
      </div>
    </section>
  );
}

export default FeatureHighlights;
