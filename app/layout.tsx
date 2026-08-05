import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
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
  metadataBase: new URL(
    process.env.NEXT_PUBLIC_SITE_URL ?? "https://mehtanandini.github.io/",
  ),
  title: {
    default: "Nandini Mehta | Software Engineer",
    template: "%s | Nandini Mehta",
  },
  description:
    "Interactive project roadmap of Nandini Mehta, a software engineer based in Germany.",
  keywords: [
    "Nandini Mehta",
    "Software Engineer",
    "Python",
    "Three.js portfolio",
    "ETL",
    "PostgreSQL",
    "Cloud Backend",
  ],
  authors: [{ name: "Nandini Mehta" }],
  openGraph: {
    title: "Nandini Mehta | Software Engineer",
    description: "An interactive roadmap through four connected software projects.",
    type: "website",
    images: [
      {
        url: "og.png",
        width: 1731,
        height: 909,
        alt: "Nandini Mehta — Software Engineer — Project Roadmap",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Nandini Mehta | Software Engineer",
    description: "An interactive roadmap through four connected software projects.",
    images: ["og.png"],
  },
  robots: { index: true, follow: true },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body className={`${geistSans.variable} ${geistMono.variable}`}>
        {children}
      </body>
    </html>
  );
}
