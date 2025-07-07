"use client";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import Navigation, { PageHeader } from "@/components/navigation";
import { Footer } from "@/components/navigation";
import {
  Target,
  Users,
  Award,
  Shield,
  ArrowRight,
  BookOpen,
  TrendingUp,
  Globe,
  Heart,
} from "lucide-react";

const MISSION_VALUES = [
  {
    icon: Target,
    title: "Our Mission",
    description:
      "To democratize access to education by connecting students with authentic scholarship opportunities from verified sources across India.",
    color: "bg-indigo-500",
  },
  {
    icon: Shield,
    title: "Trust & Verification",
    description:
      "Every scholarship on our platform is verified from trusted government and institutional sources to ensure authenticity.",
    color: "bg-emerald-500",
  },
  {
    icon: Users,
    title: "Student-Centric",
    description:
      "We put students first, providing personalized recommendations and comprehensive support throughout their scholarship journey.",
    color: "bg-purple-500",
  },
  {
    icon: Globe,
    title: "Comprehensive Coverage",
    description:
      "From government schemes to private foundations, we cover the widest range of scholarship opportunities in India.",
    color: "bg-blue-500",
  },
];

const STATS = [
  { label: "Students Helped", value: "50,000+", icon: Users },
  { label: "Scholarships Listed", value: "2,500+", icon: Award },
  { label: "Success Rate", value: "85%", icon: TrendingUp },
  { label: "Amount Distributed", value: "₹250 Cr+", icon: BookOpen },
];

const TEAM_VALUES = [
  {
    title: "Transparency",
    description:
      "We believe in complete transparency in all our processes and scholarship listings.",
    icon: Shield,
  },
  {
    title: "Accessibility",
    description:
      "Education should be accessible to all, regardless of economic background or social status.",
    icon: Heart,
  },
  {
    title: "Excellence",
    description:
      "We strive for excellence in everything we do, from platform design to student support.",
    icon: Award,
  },
  {
    title: "Innovation",
    description:
      "We continuously innovate to make scholarship discovery and application easier for students.",
    icon: TrendingUp,
  },
];

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-white">
      <Navigation />

      <PageHeader
        title="About ShikshaSetu"
        description="Empowering students through verified scholarship opportunities"
      />

      {/* Mission Section */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-headline font-bold text-slate-900 mb-6">
              Bridging Dreams with Opportunities
            </h2>
            <p className="text-subtitle text-slate-600 max-w-4xl mx-auto">
              ShikshaSetu is India&apos;s most trusted scholarship portal,
              dedicated to connecting deserving students with authentic
              scholarship opportunities. We believe that financial constraints
              should never be a barrier to quality education.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {MISSION_VALUES.map((item, index) => (
              <Card
                key={index}
                className="hover:shadow-medium transition-shadow"
              >
                <CardHeader className="pb-4">
                  <div className="flex items-center space-x-4 mb-4">
                    <div
                      className={`w-12 h-12 ${item.color} rounded-lg flex items-center justify-center`}
                    >
                      <item.icon className="w-6 h-6 text-white" />
                    </div>
                    <CardTitle className="text-lg font-semibold text-slate-900">
                      {item.title}
                    </CardTitle>
                  </div>
                  <CardDescription className="text-slate-600 leading-relaxed">
                    {item.description}
                  </CardDescription>
                </CardHeader>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-slate-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h3 className="text-title font-semibold text-slate-900 mb-4">
              Our Impact in Numbers
            </h3>
            <p className="text-slate-600">
              See how we&apos;re making a difference in students&apos; lives
              across India
            </p>
          </div>

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

      {/* Values Section */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h3 className="text-title font-semibold text-slate-900 mb-4">
              Our Core Values
            </h3>
            <p className="text-slate-600">
              The principles that guide everything we do
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {TEAM_VALUES.map((value, index) => (
              <div key={index} className="text-center">
                <div className="flex justify-center mb-4">
                  <div className="w-16 h-16 bg-gradient-to-br from-indigo-100 to-purple-100 rounded-full flex items-center justify-center">
                    <value.icon className="w-8 h-8 text-indigo-600" />
                  </div>
                </div>
                <h4 className="text-lg font-semibold text-slate-900 mb-3">
                  {value.title}
                </h4>
                <p className="text-sm text-slate-600 leading-relaxed">
                  {value.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How We Work Section */}
      <section className="py-16 bg-slate-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h3 className="text-title font-semibold text-slate-900 mb-4">
              How We Ensure Quality
            </h3>
            <p className="text-slate-600">
              Our rigorous process to maintain the highest standards
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-12 h-12 bg-indigo-500 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-lg font-bold text-white">1</span>
              </div>
              <h4 className="text-lg font-semibold text-slate-900 mb-3">
                Source Verification
              </h4>
              <p className="text-slate-600">
                We verify every scholarship from official government and
                institutional sources.
              </p>
            </div>

            <div className="text-center">
              <div className="w-12 h-12 bg-emerald-500 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-lg font-bold text-white">2</span>
              </div>
              <h4 className="text-lg font-semibold text-slate-900 mb-3">
                Real-time Updates
              </h4>
              <p className="text-slate-600">
                Our system continuously monitors and updates scholarship
                information and deadlines.
              </p>
            </div>

            <div className="text-center">
              <div className="w-12 h-12 bg-purple-500 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-lg font-bold text-white">3</span>
              </div>
              <h4 className="text-lg font-semibold text-slate-900 mb-3">
                Student Support
              </h4>
              <p className="text-slate-600">
                We provide comprehensive guidance and support throughout the
                application process.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Success Stories Section */}
      <section
        id="success-stories"
        className="py-16 bg-gradient-to-r from-indigo-50 to-purple-50"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h3 className="text-title font-semibold text-slate-900 mb-4">
              Success Stories
            </h3>
            <p className="text-slate-600 max-w-2xl mx-auto">
              Real stories from students who transformed their lives through
              scholarships
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <Card className="bg-white border-0 shadow-lg">
              <CardHeader className="pb-4">
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-indigo-500 rounded-full flex items-center justify-center">
                    <span className="text-white font-semibold">PS</span>
                  </div>
                  <div>
                    <h4 className="font-semibold text-slate-900">
                      Priya Sharma
                    </h4>
                    <p className="text-sm text-slate-600">
                      IIT Delhi, Computer Science
                    </p>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-slate-600 mb-4">
                  &ldquo;The National Merit Scholarship helped me pursue my
                  dream of studying at IIT Delhi. Today, I&apos;m working at a
                  leading tech company.&rdquo;
                </p>
                <div className="flex items-center justify-between">
                  <Badge variant="secondary">Merit Based</Badge>
                  <span className="text-sm text-emerald-600 font-medium">
                    ₹2.5L
                  </span>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-white border-0 shadow-lg">
              <CardHeader className="pb-4">
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-emerald-500 rounded-full flex items-center justify-center">
                    <span className="text-white font-semibold">RK</span>
                  </div>
                  <div>
                    <h4 className="font-semibold text-slate-900">
                      Rahul Kumar
                    </h4>
                    <p className="text-sm text-slate-600">
                      AIIMS Mumbai, Medical Sciences
                    </p>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-slate-600 mb-4">
                  &ldquo;Coming from a small village, I never imagined I could
                  study medicine. This scholarship changed my life
                  completely.&rdquo;
                </p>
                <div className="flex items-center justify-between">
                  <Badge variant="secondary">Minority</Badge>
                  <span className="text-sm text-emerald-600 font-medium">
                    ₹50K
                  </span>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-white border-0 shadow-lg">
              <CardHeader className="pb-4">
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-purple-500 rounded-full flex items-center justify-center">
                    <span className="text-white font-semibold">AP</span>
                  </div>
                  <div>
                    <h4 className="font-semibold text-slate-900">
                      Anita Patel
                    </h4>
                    <p className="text-sm text-slate-600">
                      Research Scholar, Chemistry
                    </p>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-slate-600 mb-4">
                  &ldquo;The Research Excellence Grant enabled me to focus on my
                  PhD without financial stress. Now I&apos;m contributing to
                  breakthrough research.&rdquo;
                </p>
                <div className="flex items-center justify-between">
                  <Badge variant="secondary">Research</Badge>
                  <span className="text-sm text-emerald-600 font-medium">
                    ₹1.2L
                  </span>
                </div>
              </CardContent>
            </Card>
          </div>

          <div className="text-center mt-12">
            <Button variant="outline" size="lg">
              <Heart className="w-5 h-5 mr-2" />
              Read More Stories
            </Button>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h3 className="text-title font-semibold text-slate-900 mb-4">
            Ready to Start Your Journey?
          </h3>
          <p className="text-slate-600 mb-8">
            Join thousands of students who have found their perfect scholarship
            through ShikshaSetu.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" className="bg-gradient-primary">
              <BookOpen className="w-5 h-5 mr-2" />
              Explore Scholarships
              <ArrowRight className="w-5 h-5 ml-2" />
            </Button>
            <Button size="lg" variant="outline">
              <Users className="w-5 h-5 mr-2" />
              Join Our Community
            </Button>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
}
