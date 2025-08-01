import Link from "next/link";
import { useState, useEffect } from "react";
import { auth } from "@/lib/firebase";
import { onAuthStateChanged, signOut } from "firebase/auth";
import LanguageSwitcher from "@/components/LanguageSwitcher";
import { useLanguage } from "@/context/LanguageContext";

export default function Navbar() {
  const { t } = useLanguage();
  const [menuOpen, setMenuOpen] = useState(false);
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (u) => setUser(u));
    return () => unsubscribe();
  }, []);

  const logout = async () => {
    await signOut(auth);
  };

  return (
    <nav className="bg-blue-600 text-white shadow-md">
      <div className="max-w-6xl mx-auto px-4">
        <div className="flex justify-between items-center h-14">
          {/* Logo */}
          <Link href="/">
            <span className="text-xl font-bold cursor-pointer">FitAI</span>
          </Link>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center gap-4">
            {user && (
              <>
                <Link href="/dashboard">{t("dashboard")}</Link>
                <Link href="/chatbot">{t("chatbot")}</Link>
                <Link href="/workout-planner">{t("workoutPlanner")}</Link>
                <Link href="/meal-planner">{t("mealPlanner")}</Link>
              </>
            )}

            <LanguageSwitcher />

            {user ? (
              <button
                onClick={logout}
                className="bg-red-500 px-3 py-1 rounded hover:bg-red-600"
              >
                {t("logout")}
              </button>
            ) : (
              <>
                <Link href="/login">{t("login")}</Link>
                <Link href="/register">{t("register")}</Link>
              </>
            )}
          </div>

          {/* Mobile Hamburger */}
          <button
            onClick={() => setMenuOpen(!menuOpen)}
            className="md:hidden focus:outline-none"
          >
            ☰
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {menuOpen && (
        <div className="md:hidden bg-blue-700 px-4 pb-3">
          {user && (
            <>
              <Link href="/dashboard" className="block py-2" onClick={() => setMenuOpen(false)}>
                {t("dashboard")}
              </Link>
              <Link href="/chatbot" className="block py-2" onClick={() => setMenuOpen(false)}>
                {t("chatbot")}
              </Link>
              <Link href="/workout-planner" className="block py-2" onClick={() => setMenuOpen(false)}>
                {t("workoutPlanner")}
              </Link>
              <Link href="/meal-planner" className="block py-2" onClick={() => setMenuOpen(false)}>
                {t("mealPlanner")}
              </Link>
            </>
          )}

          <div className="py-2">
            <LanguageSwitcher />
          </div>

          {user ? (
            <button
              onClick={logout}
              className="bg-red-500 px-3 py-1 rounded hover:bg-red-600 mt-2"
            >
              {t("logout")}
            </button>
          ) : (
            <>
              <Link href="/login" className="block py-2" onClick={() => setMenuOpen(false)}>
                {t("login")}
              </Link>
              <Link href="/register" className="block py-2" onClick={() => setMenuOpen(false)}>
                {t("register")}
              </Link>
            </>
          )}
        </div>
      )}
    </nav>
  );
}
