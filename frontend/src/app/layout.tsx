import type { Metadata } from "next";
import "./globals.css";
import Navbar from "@/components/Navbar";

export const metadata: Metadata = {
  title: "Pura Pata - Adopciones de Perros en Costa Rica",
  description: "Plataforma para ayudar a perros a encontrar un hogar en Costa Rica",
  openGraph: {
    title: "Pura Pata - Adopciones de Perros en Costa Rica",
    description: "Plataforma para ayudar a perros a encontrar un hogar en Costa Rica",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es">
      <body>
        <Navbar />
        {children}
      </body>
    </html>
  );
}
