import type { Metadata } from "next";
import '@/app/ui/globals.css'


export const metadata: Metadata = {
  title: "Vacation Planner",
  description: "Plan your vacation now!",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        {children}
      </body>
    </html>
  );
}
