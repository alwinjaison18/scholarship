import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import Providers from "@/components/providers";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: {
    default: "ShikshaSetu - Find Your Perfect Scholarship in India",
    template: "%s | ShikshaSetu",
  },
  description:
    "Discover authentic scholarship opportunities in India. Find government, merit-based, and need-based scholarships with real-time updates and verified information.",
  keywords: [
    "scholarship",
    "education",
    "India",
    "government scholarship",
    "merit scholarship",
    "student funding",
    "education loan",
    "financial aid",
    "study abroad",
    "higher education",
  ],
  authors: [{ name: "ShikshaSetu Team" }],
  creator: "ShikshaSetu",
  publisher: "ShikshaSetu",
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  metadataBase: new URL("https://shikhasetu.com"),
  alternates: {
    canonical: "/",
  },
  openGraph: {
    type: "website",
    locale: "en_IN",
    url: "https://shikhasetu.com",
    title: "ShikshaSetu - Find Your Perfect Scholarship in India",
    description:
      "Discover authentic scholarship opportunities in India. Find government, merit-based, and need-based scholarships with real-time updates and verified information.",
    siteName: "ShikshaSetu",
    images: [
      {
        url: "/og-image.jpg",
        width: 1200,
        height: 630,
        alt: "ShikshaSetu - Scholarship Discovery Platform",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "ShikshaSetu - Find Your Perfect Scholarship in India",
    description:
      "Discover authentic scholarship opportunities in India. Find government, merit-based, and need-based scholarships with real-time updates and verified information.",
    images: ["/og-image.jpg"],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
  verification: {
    google: "your-google-verification-code",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="scroll-smooth">
      <head>
        <link rel="icon" href="/favicon.ico" sizes="any" />
        <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
        <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
        <link rel="manifest" href="/manifest.json" />
        <meta name="theme-color" content="#f97316" />
        <meta name="msapplication-TileColor" content="#f97316" />
        <meta
          name="viewport"
          content="width=device-width, initial-scale=1, maximum-scale=5"
        />
      </head>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased min-h-screen bg-background font-sans`}
      >
        <Providers>
          <div className="relative flex min-h-screen flex-col">
            <main className="flex-1">{children}</main>
          </div>
        </Providers>
      </body>
    </html>
  );
}
