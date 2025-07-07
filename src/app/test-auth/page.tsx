"use client";

import { useState } from "react";
import { signIn } from "next-auth/react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { User, Shield, LogIn } from "lucide-react";

export default function TestAuthPage() {
  const [loading, setLoading] = useState("");
  const router = useRouter();

  const handleTestSignIn = async (role: "admin" | "student") => {
    setLoading(role);

    try {
      const email =
        role === "admin" ? "admin@shikshasetu.com" : "test@shikshasetu.com";
      const password = role === "admin" ? "admin123" : "test123";

      console.log(`Attempting ${role} signin with:`, email);

      const result = await signIn("credentials", {
        email,
        password,
        redirect: false,
      });

      console.log("Signin result:", result);

      if (result?.error) {
        console.error("Sign in error:", result.error);
        alert(`Sign in failed: ${result.error}`);
      } else if (result?.ok) {
        console.log("Sign in successful, redirecting...");
        // Use window.location for immediate redirect
        if (role === "admin") {
          window.location.href = "/admin";
        } else {
          window.location.href = "/dashboard";
        }
      } else {
        alert("Sign in failed. Please check console for details.");
      }
    } catch (error) {
      console.error("Sign in error:", error);
      alert("Sign in failed. Please check console for details.");
    } finally {
      setLoading("");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-purple-50 flex items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <CardTitle className="text-2xl font-bold">
            Test Authentication
          </CardTitle>
          <p className="text-slate-600">Quick login for testing purposes</p>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-3">
            <Button
              onClick={() => handleTestSignIn("admin")}
              disabled={loading === "admin"}
              className="w-full h-12 flex items-center justify-center space-x-2"
            >
              <Shield className="h-5 w-5" />
              <span>Sign in as Admin</span>
              {loading === "admin" && (
                <div className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full ml-2"></div>
              )}
            </Button>

            <Button
              onClick={() => handleTestSignIn("student")}
              disabled={loading === "student"}
              variant="outline"
              className="w-full h-12 flex items-center justify-center space-x-2"
            >
              <User className="h-5 w-5" />
              <span>Sign in as Student</span>
              {loading === "student" && (
                <div className="animate-spin h-4 w-4 border-2 border-slate-600 border-t-transparent rounded-full ml-2"></div>
              )}
            </Button>
          </div>

          <div className="border-t pt-4">
            <h3 className="font-semibold mb-3">Default Credentials:</h3>
            <div className="space-y-2 text-sm">
              <div className="flex items-center justify-between p-2 bg-slate-50 rounded">
                <span className="flex items-center space-x-2">
                  <Shield className="h-4 w-4 text-indigo-600" />
                  <span>Admin</span>
                </span>
                <Badge variant="secondary">admin@shikshasetu.com</Badge>
              </div>
              <div className="flex items-center justify-between p-2 bg-slate-50 rounded">
                <span className="flex items-center space-x-2">
                  <User className="h-4 w-4 text-blue-600" />
                  <span>Student</span>
                </span>
                <Badge variant="outline">test@shikshasetu.com</Badge>
              </div>
            </div>
          </div>

          <div className="border-t pt-4">
            <Button
              onClick={() => router.push("/auth/signin")}
              variant="ghost"
              className="w-full"
            >
              <LogIn className="h-4 w-4 mr-2" />
              Manual Sign In
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
