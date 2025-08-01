// pages/meal-planner.tsx
import { useState } from "react";

export default function MealPlanner() {
  const [calories, setCalories] = useState("2000");
  const [dietType, setDietType] = useState("balanced");
  const [goal, setGoal] = useState("maintain weight");
  const [plan, setPlan] = useState("");
  const [loading, setLoading] = useState(false);

  const generatePlan = async () => {
    setLoading(true);
    setPlan("");

    try {
      const res = await fetch("/api/meal", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ calories, dietType, goal }),
      });

      const data = await res.json();
      setPlan(data.plan);
    } catch {
      setPlan("Error generating meal plan.");
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-50 p-4 max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">AI Meal Planner</h2>

      <label className="block mb-2">Daily Calories</label>
      <input
        type="number"
        className="w-full border p-2 mb-4 rounded"
        value={calories}
        onChange={(e) => setCalories(e.target.value)}
      />

      <label className="block mb-2">Diet Type</label>
      <select
        className="w-full border p-2 mb-4 rounded"
        value={dietType}
        onChange={(e) => setDietType(e.target.value)}
      >
        <option value="balanced">Balanced</option>
        <option value="vegetarian">Vegetarian</option>
        <option value="vegan">Vegan</option>
        <option value="keto">Keto</option>
        <option value="paleo">Paleo</option>
      </select>

      <label className="block mb-2">Goal</label>
      <select
        className="w-full border p-2 mb-4 rounded"
        value={goal}
        onChange={(e) => setGoal(e.target.value)}
      >
        <option value="lose weight">Lose Weight</option>
        <option value="maintain weight">Maintain Weight</option>
        <option value="gain weight">Gain Weight</option>
      </select>

      <button
        onClick={generatePlan}
        className="w-full bg-green-600 text-white p-2 rounded hover:bg-green-700"
      >
        Generate Plan
      </button>

      {loading && <p className="mt-4 text-gray-500">Generating...</p>}

      {plan && (
        <div className="mt-6 p-4 bg-white rounded shadow whitespace-pre-wrap">
          {plan}
        </div>
      )}
    </div>
  );
}
