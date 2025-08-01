import { createContext, useState, useContext, ReactNode } from "react";
import en from "@/locales/en.json";
import hi from "@/locales/hi.json";

type LocaleStrings = typeof en;

interface LanguageContextType {
  lang: "en" | "hi";
  t: (key: keyof LocaleStrings) => string;
  setLang: (lang: "en" | "hi") => void;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export const LanguageProvider = ({ children }: { children: ReactNode }) => {
  const [lang, setLang] = useState<"en" | "hi">("en");

  const t = (key: keyof LocaleStrings) => {
    const translations = lang === "en" ? en : hi;
    return translations[key] || key;
  };

  return (
    <LanguageContext.Provider value={{ lang, t, setLang }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => {
  const ctx = useContext(LanguageContext);
  if (!ctx) throw new Error("useLanguage must be used within LanguageProvider");
  return ctx;
};
