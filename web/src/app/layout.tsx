import "./globals.css";

export const metadata = {
  title: "HomeBrain",
  description: "Personal homelab AI assistant",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}