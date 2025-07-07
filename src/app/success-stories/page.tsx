"use client";

import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import Navigation, { PageHeader } from "@/components/navigation";
import { Footer } from "@/components/navigation";
import {
  Star,
  Quote,
  ArrowRight,
  GraduationCap,
  Award,
  BookOpen,
  MapPin,
  Calendar,
} from "lucide-react";

const SUCCESS_STORIES = [
  {
    id: 1,
    name: "Priya Sharma",
    scholarship: "National Merit Scholarship",
    amount: "₹2.5L",
    year: "2024",
    course: "Computer Science Engineering",
    university: "IIT Delhi",
    location: "Delhi",
    image: "/api/placeholder/80/80",
    story:
      "The National Merit Scholarship helped me pursue my dream of studying at IIT Delhi. Without this support, it would have been impossible for my family to afford the expenses. Today, I'm working at a leading tech company and giving back to the community.",
    category: "Merit Based",
  },
  {
    id: 2,
    name: "Rahul Kumar",
    scholarship: "Minority Scholarship Scheme",
    amount: "₹50K",
    year: "2023",
    course: "Medical Sciences",
    university: "AIIMS Mumbai",
    location: "Mumbai",
    image: "/api/placeholder/80/80",
    story:
      "This scholarship was a game-changer for me. Coming from a small village, I never imagined I could study medicine. The financial support helped me focus on my studies without worrying about expenses.",
    category: "Minority",
  },
  {
    id: 3,
    name: "Anita Patel",
    scholarship: "Research Excellence Grant",
    amount: "₹1.2L",
    year: "2024",
    course: "Environmental Science",
    university: "JNU Delhi",
    location: "Delhi",
    image: "/api/placeholder/80/80",
    story:
      "The research grant allowed me to conduct groundbreaking research in environmental conservation. I've published three papers and my work is being used by policy makers.",
    category: "Research",
  },
  {
    id: 4,
    name: "Vikram Singh",
    scholarship: "Sports Excellence Scholarship",
    amount: "₹75K",
    year: "2023",
    course: "Sports Management",
    university: "Panjab University",
    location: "Chandigarh",
    image: "/api/placeholder/80/80",
    story:
      "Balancing sports and academics was challenging, but this scholarship helped me pursue both my passion for cricket and my education. I'm now a certified sports manager working with national teams.",
    category: "Sports",
  },
];

const STATS = [
  { label: "Success Stories", value: "2,500+", icon: Star },
  { label: "Total Amount Awarded", value: "₹50 Cr+", icon: Award },
  { label: "Universities Covered", value: "500+", icon: GraduationCap },
  { label: "Career Achievements", value: "95%", icon: BookOpen },
];

export default function SuccessStoriesPage() {
  return (
    <div className="min-h-screen bg-white">
      <Navigation />

      <PageHeader
        title="Success Stories"
        description="Inspiring journeys of students who achieved their dreams through scholarships"
      />

      {/* Stats Section */}
      <section className="py-16 bg-slate-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {STATS.map((stat, index) => (
              <div key={index} className="text-center">
                <div className="flex justify-center mb-4">
                  <div className="w-12 h-12 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-lg flex items-center justify-center">
                    <stat.icon className="w-6 h-6 text-white" />
                  </div>
                </div>
                <div className="text-2xl md:text-3xl font-bold text-slate-900 mb-2">
                  {stat.value}
                </div>
                <div className="text-sm text-slate-600">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Success Stories */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="space-y-12">
            {SUCCESS_STORIES.map((story, index) => (
              <Card
                key={story.id}
                className="overflow-hidden hover:shadow-medium transition-shadow"
              >
                <div
                  className={`grid grid-cols-1 lg:grid-cols-3 gap-8 ${
                    index % 2 === 1 ? "lg:grid-flow-col-dense" : ""
                  }`}
                >
                  <div
                    className={`lg:col-span-1 p-8 bg-gradient-to-br from-indigo-50 to-purple-50 flex items-center justify-center ${
                      index % 2 === 1 ? "lg:order-2" : ""
                    }`}
                  >
                    <div className="text-center">
                      <div className="w-24 h-24 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full flex items-center justify-center mx-auto mb-4">
                        <span className="text-2xl font-bold text-white">
                          {story.name
                            .split(" ")
                            .map((n) => n[0])
                            .join("")}
                        </span>
                      </div>
                      <h3 className="text-xl font-semibold text-slate-900 mb-2">
                        {story.name}
                      </h3>
                      <div className="flex items-center justify-center space-x-2 mb-2">
                        <MapPin className="w-4 h-4 text-slate-500" />
                        <span className="text-sm text-slate-600">
                          {story.location}
                        </span>
                      </div>
                      <div className="flex items-center justify-center space-x-2">
                        <Calendar className="w-4 h-4 text-slate-500" />
                        <span className="text-sm text-slate-600">
                          {story.year}
                        </span>
                      </div>
                    </div>
                  </div>

                  <div className="lg:col-span-2 p-8">
                    <div className="flex items-center justify-between mb-6">
                      <div>
                        <Badge variant="secondary" className="mb-2">
                          {story.category}
                        </Badge>
                        <h4 className="text-lg font-semibold text-slate-900">
                          {story.scholarship}
                        </h4>
                        <p className="text-slate-600">
                          {story.course} • {story.university}
                        </p>
                      </div>
                      <div className="text-right">
                        <div className="text-2xl font-bold text-emerald-600 mb-1">
                          {story.amount}
                        </div>
                        <div className="text-sm text-slate-600">
                          Scholarship Amount
                        </div>
                      </div>
                    </div>

                    <div className="relative">
                      <Quote className="absolute -top-2 -left-2 w-8 h-8 text-indigo-200" />
                      <blockquote className="text-slate-700 italic pl-6 mb-6">
                        &ldquo;{story.story}&rdquo;
                      </blockquote>
                    </div>

                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-1">
                        {[...Array(5)].map((_, i) => (
                          <Star
                            key={i}
                            className="w-4 h-4 text-amber-400 fill-current"
                          />
                        ))}
                        <span className="text-sm text-slate-600 ml-2">
                          Verified Success Story
                        </span>
                      </div>
                      <Button variant="outline" size="sm">
                        Read Full Story
                        <ArrowRight className="w-4 h-4 ml-2" />
                      </Button>
                    </div>
                  </div>
                </div>
              </Card>
            ))}
          </div>

          {/* CTA Section */}
          <div className="mt-16 text-center">
            <div className="max-w-3xl mx-auto">
              <h3 className="text-title font-semibold text-slate-900 mb-4">
                Ready to Write Your Success Story?
              </h3>
              <p className="text-slate-600 mb-8">
                Join thousands of students who have transformed their lives
                through scholarships. Start your journey today.
              </p>
              <Button size="lg" className="bg-gradient-primary">
                <BookOpen className="w-5 h-5 mr-2" />
                Find Your Scholarship
                <ArrowRight className="w-5 h-5 ml-2" />
              </Button>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
}
