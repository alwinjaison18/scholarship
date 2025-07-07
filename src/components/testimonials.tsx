"use client";

import React, { useState, useCallback } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import {
  Quote,
  Star,
  ChevronLeft,
  ChevronRight,
  Award,
  GraduationCap,
  IndianRupee,
} from "lucide-react";
import { cn, getInitials, formatAmount } from "@/lib/utils";

export interface TestimonialItem {
  id: string;
  name: string;
  amount: number;
  scholarship: string;
  quote: string;
  image?: string;
  university: string;
  rating: number;
  course?: string;
  year?: string;
  location?: string;
}

export interface TestimonialsProps {
  title?: string;
  subtitle?: string;
  testimonials: TestimonialItem[];
  showNavigation?: boolean;
  autoplay?: boolean;
  className?: string;
}

export function Testimonials({
  title = "Success Stories",
  subtitle = "See how ShikshaSetu has helped students achieve their dreams",
  testimonials,
  showNavigation = true,
  autoplay = false,
  className,
}: TestimonialsProps) {
  const [currentIndex, setCurrentIndex] = useState(0);

  const nextTestimonial = useCallback(() => {
    setCurrentIndex((prev) => (prev + 1) % testimonials.length);
  }, [testimonials.length]);

  const prevTestimonial = () => {
    setCurrentIndex(
      (prev) => (prev - 1 + testimonials.length) % testimonials.length
    );
  };

  const goToTestimonial = (index: number) => {
    setCurrentIndex(index);
  };

  // Auto-play functionality
  React.useEffect(() => {
    if (autoplay) {
      const interval = setInterval(nextTestimonial, 5000);
      return () => clearInterval(interval);
    }
  }, [autoplay, nextTestimonial]);

  const renderStars = (rating: number) => {
    return Array.from({ length: 5 }, (_, i) => (
      <Star
        key={i}
        className={cn(
          "h-4 w-4",
          i < rating ? "fill-yellow-400 text-yellow-400" : "text-gray-300"
        )}
      />
    ));
  };

  const renderTestimonialCard = (
    testimonial: TestimonialItem,
    index: number
  ) => (
    <Card
      key={testimonial.id}
      className={cn(
        "group relative overflow-hidden border-2 transition-all duration-300",
        index === currentIndex
          ? "border-primary shadow-xl scale-105"
          : "border-gray-200 hover:border-gray-300"
      )}
    >
      <CardContent className="p-6">
        {/* Quote Icon */}
        <div className="absolute top-4 right-4">
          <Quote className="h-8 w-8 text-primary/20" />
        </div>

        {/* Rating */}
        <div className="flex items-center gap-1 mb-4">
          {renderStars(testimonial.rating)}
        </div>

        {/* Quote */}
        <blockquote className="text-lg text-gray-700 mb-6 leading-relaxed">
          &ldquo;{testimonial.quote}&rdquo;
        </blockquote>

        {/* Scholarship Info */}
        <div className="space-y-3 mb-6">
          <div className="flex items-center gap-2">
            <Award className="h-4 w-4 text-green-600" />
            <span className="text-sm font-medium">
              {testimonial.scholarship}
            </span>
          </div>
          <div className="flex items-center gap-2">
            <IndianRupee className="h-4 w-4 text-blue-600" />
            <span className="text-sm font-semibold text-green-600">
              {formatAmount(testimonial.amount)}
            </span>
          </div>
          <div className="flex items-center gap-2">
            <GraduationCap className="h-4 w-4 text-purple-600" />
            <span className="text-sm">{testimonial.university}</span>
          </div>
        </div>

        {/* Author Info */}
        <div className="flex items-center gap-3 pt-4 border-t">
          <Avatar className="h-12 w-12">
            <AvatarImage src={testimonial.image} alt={testimonial.name} />
            <AvatarFallback className="bg-primary text-white">
              {getInitials(testimonial.name)}
            </AvatarFallback>
          </Avatar>
          <div className="flex-1">
            <div className="font-semibold text-gray-900">
              {testimonial.name}
            </div>
            <div className="text-sm text-gray-600">
              {testimonial.course && `${testimonial.course} • `}
              {testimonial.year && `${testimonial.year} • `}
              {testimonial.location}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );

  return (
    <section className={cn("py-16 lg:py-24 bg-gray-50", className)}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            {title}
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">{subtitle}</p>
        </div>

        {/* Testimonials */}
        <div className="relative">
          {/* Desktop View - Show 3 testimonials */}
          <div className="hidden md:grid md:grid-cols-3 gap-8">
            {testimonials
              .slice(0, 3)
              .map((testimonial, index) =>
                renderTestimonialCard(testimonial, index)
              )}
          </div>

          {/* Mobile View - Show 1 testimonial with navigation */}
          <div className="md:hidden">
            <div className="relative">
              {renderTestimonialCard(testimonials[currentIndex], currentIndex)}

              {/* Navigation */}
              {showNavigation && testimonials.length > 1 && (
                <div className="flex items-center justify-between mt-6">
                  <Button
                    variant="outline"
                    size="icon"
                    onClick={prevTestimonial}
                    className="h-10 w-10"
                  >
                    <ChevronLeft className="h-4 w-4" />
                  </Button>

                  {/* Dots Indicator */}
                  <div className="flex items-center gap-2">
                    {testimonials.map((_, index) => (
                      <button
                        key={index}
                        onClick={() => goToTestimonial(index)}
                        className={cn(
                          "h-2 w-2 rounded-full transition-all duration-300",
                          index === currentIndex
                            ? "bg-primary w-6"
                            : "bg-gray-300"
                        )}
                      />
                    ))}
                  </div>

                  <Button
                    variant="outline"
                    size="icon"
                    onClick={nextTestimonial}
                    className="h-10 w-10"
                  >
                    <ChevronRight className="h-4 w-4" />
                  </Button>
                </div>
              )}
            </div>
          </div>

          {/* Show More Button */}
          {testimonials.length > 3 && (
            <div className="text-center mt-12">
              <Button variant="outline" size="lg">
                View All Success Stories
              </Button>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}

export default Testimonials;
