// File: components/LanguageSwitcher.tsx
import { useLanguage } from "@/context/LanguageContext";

export default function LanguageSwitcher() {
  const { lang, setLang } = useLanguage();

  return (
    <select
      value={lang}
      onChange={(e) => setLang(e.target.value as "en" | "hi")}
      className="border rounded p-1"
    >
      <option value="en">English</option>
      <option value="hi">हिन्दी</option>
    </select>
  );
}
