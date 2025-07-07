"use client";

import { useState } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import Navigation, { PageHeader } from "@/components/navigation";
import { Footer } from "@/components/navigation";
import {
  Phone,
  Mail,
  MapPin,
  MessageCircle,
  Send,
  CheckCircle,
  HelpCircle,
} from "lucide-react";

const CONTACT_METHODS = [
  {
    icon: Phone,
    title: "Phone Support",
    description: "Speak directly with our support team",
    contact: "+91 80-4000-5000",
    availability: "Mon-Fri, 9 AM - 6 PM",
    color: "bg-indigo-500",
  },
  {
    icon: Mail,
    title: "Email Support",
    description: "Send us your queries and concerns",
    contact: "support@shikhasetu.com",
    availability: "24/7 Response within 4 hours",
    color: "bg-emerald-500",
  },
  {
    icon: MessageCircle,
    title: "Live Chat",
    description: "Get instant help from our chat support",
    contact: "Available on website",
    availability: "Mon-Fri, 9 AM - 9 PM",
    color: "bg-purple-500",
  },
  {
    icon: MapPin,
    title: "Office Address",
    description: "Visit our headquarters",
    contact: "Bangalore, Karnataka, India",
    availability: "Mon-Fri, 10 AM - 5 PM",
    color: "bg-blue-500",
  },
];

const FAQ_ITEMS = [
  {
    question: "How do I know if a scholarship is genuine?",
    answer:
      "All scholarships on ShikshaSetu are verified from official sources. Look for the 'Verified' badge on each scholarship listing.",
    category: "Verification",
  },
  {
    question: "Is there any fee to use ShikshaSetu?",
    answer:
      "No, ShikshaSetu is completely free for students. We never charge any fees for scholarship information or applications.",
    category: "Pricing",
  },
  {
    question: "How often are scholarships updated?",
    answer:
      "Our system updates scholarship information in real-time. New opportunities are added daily and deadlines are monitored continuously.",
    category: "Updates",
  },
  {
    question: "Can I apply for multiple scholarships?",
    answer:
      "Yes, you can apply for multiple scholarships. We recommend applying for all scholarships you're eligible for to maximize your chances.",
    category: "Applications",
  },
];

export default function ContactPage() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    subject: "",
    message: "",
    category: "general",
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    // Simulate form submission
    await new Promise((resolve) => setTimeout(resolve, 2000));

    setIsSubmitting(false);
    setIsSubmitted(true);
  };

  const handleInputChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement
    >
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  return (
    <div className="min-h-screen bg-white">
      <Navigation />

      <PageHeader
        title="Contact Us"
        description="Get in touch with our support team for any queries or assistance"
      />

      {/* Contact Methods */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-title font-semibold text-slate-900 mb-4">
              Multiple Ways to Reach Us
            </h2>
            <p className="text-slate-600">
              Choose the most convenient way to get in touch with our support
              team
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
            {CONTACT_METHODS.map((method, index) => (
              <Card
                key={index}
                className="text-center hover:shadow-medium transition-shadow"
              >
                <CardHeader className="pb-4">
                  <div className="flex justify-center mb-4">
                    <div
                      className={`w-12 h-12 ${method.color} rounded-lg flex items-center justify-center`}
                    >
                      <method.icon className="w-6 h-6 text-white" />
                    </div>
                  </div>
                  <CardTitle className="text-lg font-semibold text-slate-900">
                    {method.title}
                  </CardTitle>
                  <CardDescription className="text-slate-600">
                    {method.description}
                  </CardDescription>
                </CardHeader>
                <CardContent className="pt-0">
                  <div className="text-sm font-medium text-slate-900 mb-2">
                    {method.contact}
                  </div>
                  <div className="text-xs text-slate-500">
                    {method.availability}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Contact Form */}
      <section className="py-16 bg-slate-50">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h3 className="text-title font-semibold text-slate-900 mb-4">
              Send Us a Message
            </h3>
            <p className="text-slate-600">
              Fill out the form below and we&apos;ll get back to you as soon as
              possible
            </p>
          </div>

          {!isSubmitted ? (
            <Card className="shadow-medium">
              <CardContent className="p-8">
                <form onSubmit={handleSubmit} className="space-y-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-2">
                        Full Name *
                      </label>
                      <Input
                        type="text"
                        name="name"
                        value={formData.name}
                        onChange={handleInputChange}
                        placeholder="Enter your full name"
                        required
                        className="w-full"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-2">
                        Email Address *
                      </label>
                      <Input
                        type="email"
                        name="email"
                        value={formData.email}
                        onChange={handleInputChange}
                        placeholder="Enter your email address"
                        required
                        className="w-full"
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-2">
                        Subject *
                      </label>
                      <Input
                        type="text"
                        name="subject"
                        value={formData.subject}
                        onChange={handleInputChange}
                        placeholder="What is this about?"
                        required
                        className="w-full"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-700 mb-2">
                        Category
                      </label>
                      <select
                        name="category"
                        value={formData.category}
                        onChange={handleInputChange}
                        className="w-full h-10 px-3 rounded-lg border border-slate-200 bg-white text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                      >
                        <option value="general">General Inquiry</option>
                        <option value="scholarship">
                          Scholarship Question
                        </option>
                        <option value="technical">Technical Support</option>
                        <option value="verification">Verification Issue</option>
                        <option value="feedback">Feedback</option>
                      </select>
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-2">
                      Message *
                    </label>
                    <textarea
                      name="message"
                      value={formData.message}
                      onChange={handleInputChange}
                      rows={6}
                      placeholder="Describe your question or concern in detail..."
                      required
                      className="w-full px-3 py-2 rounded-lg border border-slate-200 bg-white text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                    />
                  </div>

                  <div className="flex items-center justify-between">
                    <div className="text-sm text-slate-500">
                      * Required fields
                    </div>
                    <Button
                      type="submit"
                      size="lg"
                      disabled={isSubmitting}
                      className="bg-gradient-primary"
                    >
                      {isSubmitting ? (
                        <>Sending...</>
                      ) : (
                        <>
                          <Send className="w-4 h-4 mr-2" />
                          Send Message
                        </>
                      )}
                    </Button>
                  </div>
                </form>
              </CardContent>
            </Card>
          ) : (
            <Card className="shadow-medium">
              <CardContent className="p-8 text-center">
                <div className="w-16 h-16 bg-emerald-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <CheckCircle className="w-8 h-8 text-emerald-600" />
                </div>
                <h3 className="text-lg font-semibold text-slate-900 mb-2">
                  Message Sent Successfully!
                </h3>
                <p className="text-slate-600 mb-6">
                  Thank you for contacting us. We&apos;ll get back to you within
                  24 hours.
                </p>
                <Button
                  variant="outline"
                  onClick={() => {
                    setIsSubmitted(false);
                    setFormData({
                      name: "",
                      email: "",
                      subject: "",
                      message: "",
                      category: "general",
                    });
                  }}
                >
                  Send Another Message
                </Button>
              </CardContent>
            </Card>
          )}
        </div>
      </section>

      {/* FAQ Section */}
      <section className="py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h3 className="text-title font-semibold text-slate-900 mb-4">
              Frequently Asked Questions
            </h3>
            <p className="text-slate-600">Quick answers to common questions</p>
          </div>

          <div className="space-y-6">
            {FAQ_ITEMS.map((faq, index) => (
              <Card key={index} className="hover:shadow-soft transition-shadow">
                <CardHeader className="pb-3">
                  <div className="flex items-start space-x-3">
                    <div className="w-6 h-6 bg-indigo-100 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                      <HelpCircle className="w-4 h-4 text-indigo-600" />
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center justify-between mb-2">
                        <h4 className="text-lg font-semibold text-slate-900">
                          {faq.question}
                        </h4>
                        <Badge variant="muted" className="text-xs">
                          {faq.category}
                        </Badge>
                      </div>
                      <p className="text-slate-600">{faq.answer}</p>
                    </div>
                  </div>
                </CardHeader>
              </Card>
            ))}
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
}
