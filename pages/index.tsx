import Link from "next/link";
import { useLanguage } from "@/context/LanguageContext";

export default function Home() {
  const { t } = useLanguage();

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center items-center p-6">
      <h1 className="text-4xl font-bold text-center mb-4">FitAI</h1>
      <p className="text-lg text-gray-700 text-center max-w-xl mb-8">
        {t("welcome")}  
        🚀 AI-powered fitness coach with personalized workouts, meal plans, and progress tracking.
      </p>

      <div className="flex gap-4 mb-10">
        <Link
          href="/login"
          className="bg-blue-600 text-white px-5 py-2 rounded-lg hover:bg-blue-700"
        >
          {t("login")}
        </Link>
        <Link
          href="/register"
          className="bg-green-600 text-white px-5 py-2 rounded-lg hover:bg-green-700"
        >
          {t("register")}
        </Link>
      </div>

      {/* Features */}
      <div className="grid md:grid-cols-2 gap-6 max-w-4xl">
        <FeatureCard
          title="🤖 AI Chatbot"
          description="Ask fitness questions anytime, get instant advice, motivation, and form tips."
        />
        <FeatureCard
          title="🏋️ Workout Planner"
          description="Generate personalized workout routines tailored to your goals."
        />
        <FeatureCard
          title="🥗 Meal Planner"
          description="Get AI-crafted meal plans that match your calories and dietary needs."
        />
        <FeatureCard
          title="📊 Progress Tracker"
          description="Log workouts, meals, and weight changes to see your improvement over time."
        />
      </div>
    </div>
  );
}

function FeatureCard({ title, description }: { title: string; description: string }) {
  return (
    <div className="bg-white p-6 rounded-xl shadow hover:shadow-lg transition">
      <h3 className="text-xl font-semibold mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  );
}
