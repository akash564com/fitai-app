import type { AppProps } from "next/app";
import "@/styles/globals.css";
import { LanguageProvider } from "@/context/LanguageContext";
import Navbar from "@/components/Navbar";

export default function MyApp({ Component, pageProps }: AppProps) {
  return (
    <LanguageProvider>
      <Navbar />
      <Component {...pageProps} />
    </LanguageProvider>
  );
}
