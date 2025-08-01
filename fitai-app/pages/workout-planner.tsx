// pages/workout-planner.tsx
import { useState } from "react";

export default function WorkoutPlanner() {
  const [goal, setGoal] = useState("build muscle");
  const [experience, setExperience] = useState("beginner");
  const [equipment, setEquipment] = useState("");
  const [plan, setPlan] = useState("");
  const [loading, setLoading] = useState(false);

  const generatePlan = async () => {
    setLoading(true);
    setPlan("");

    try {
      const res = await fetch("/api/workout", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ goal, experience, equipment }),
      });

      const data = await res.json();
      setPlan(data.plan);
    } catch {
      setPlan("Error generating plan.");
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-50 p-4 max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">AI Workout Planner</h2>

      <label className="block mb-2">Goal</label>
      <select
        className="w-full border p-2 mb-4 rounded"
        value={goal}
        onChange={(e) => setGoal(e.target.value)}
      >
        <option value="build muscle">Build Muscle</option>
        <option value="lose fat">Lose Fat</option>
        <option value="increase endurance">Increase Endurance</option>
      </select>

      <label className="block mb-2">Experience Level</label>
      <select
        className="w-full border p-2 mb-4 rounded"
        value={experience}
        onChange={(e) => setExperience(e.target.value)}
      >
        <option value="beginner">Beginner</option>
        <option value="intermediate">Intermediate</option>
        <option value="advanced">Advanced</option>
      </select>

      <label className="block mb-2">Available Equipment</label>
      <input
        type="text"
        className="w-full border p-2 mb-4 rounded"
        placeholder="e.g., dumbbells, squat rack"
        value={equipment}
        onChange={(e) => setEquipment(e.target.value)}
      />

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
