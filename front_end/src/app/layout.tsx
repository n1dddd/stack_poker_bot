import "~/styles/globals.css";
import { TopNav } from "./_components/topnav";

import { Arimo } from "next/font/google";

const arimo = Arimo({
  subsets: ["latin"],
  variable: "--font-sans",
});

export const metadata = {
  title: "Create T3 App",
  description: "Generated by create-t3-app",
  icons: [{ rel: "icon", url: "/favicon.ico" }],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={`font-sans ${arimo.variable}`}>
        <div className="flex flex-col">
          <TopNav/>
          <main>
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
