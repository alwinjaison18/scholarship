import { withAuth } from "next-auth/middleware";
import { NextResponse } from "next/server";

export default withAuth(
  function middleware(req) {
    const { token } = req.nextauth;
    const { pathname } = req.nextUrl;

    // Check if user is trying to access admin routes
    if (pathname.startsWith("/admin")) {
      // If user is not authenticated, redirect to signin with callback
      if (!token) {
        return NextResponse.redirect(
          new URL(`/auth/signin?callbackUrl=${pathname}`, req.url)
        );
      }

      // If user is authenticated but not an admin, redirect to dashboard
      if (token.role !== "admin") {
        return NextResponse.redirect(new URL("/dashboard", req.url));
      }
    }

    // Check if user is trying to access test scraping (admin only)
    if (pathname.startsWith("/test-scraping")) {
      if (!token) {
        return NextResponse.redirect(
          new URL(`/auth/signin?callbackUrl=${pathname}`, req.url)
        );
      }

      if (token.role !== "admin") {
        return NextResponse.redirect(new URL("/dashboard", req.url));
      }
    }

    // Check if user is trying to access dashboard
    if (pathname.startsWith("/dashboard")) {
      if (!token) {
        return NextResponse.redirect(
          new URL(`/auth/signin?callbackUrl=${pathname}`, req.url)
        );
      }
    }

    return NextResponse.next();
  },
  {
    callbacks: {
      authorized: ({ token, req }) => {
        const { pathname } = req.nextUrl;

        // Always allow access to auth pages
        if (pathname.startsWith("/auth/")) {
          return true;
        }

        // Allow access to public routes
        if (
          pathname === "/" ||
          pathname.startsWith("/scholarships") ||
          pathname.startsWith("/about") ||
          pathname.startsWith("/contact") ||
          pathname.startsWith("/categories") ||
          pathname.startsWith("/deadlines") ||
          pathname.startsWith("/success-stories")
        ) {
          return true;
        }

        // For admin routes, require admin role
        if (
          pathname.startsWith("/admin") ||
          pathname.startsWith("/test-scraping")
        ) {
          return !!token && token.role === "admin";
        }

        // For dashboard, require any authenticated user
        if (pathname.startsWith("/dashboard")) {
          return !!token;
        }

        return true;
      },
    },
  }
);

export const config = {
  matcher: [
    "/admin/:path*",
    "/test-scraping/:path*",
    "/dashboard/:path*",
    "/profile/:path*",
  ],
};
