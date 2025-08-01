// components/LanguageSwitcher.tsx
import { useLanguage } from "@/context/LanguageContext";

export default function LanguageSwitcher() {
  const { language, setLanguage } = useLanguage();

  return (
    <select
      value={language}
      onChange={(e) => setLanguage(e.target.value)}
      className="border rounded px-2 py-1"
    >
      <option value="en">English</option>
      <option value="hi">हिन्दी</option>
    </select>
  );
}
