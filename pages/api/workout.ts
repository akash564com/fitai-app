// pages/api/workout.ts
import type { NextApiRequest, NextApiResponse } from "next";

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== "POST") return res.status(405).end();

  const { goal, experience, equipment } = req.body;

  const prompt = `
Create a detailed ${experience} level ${goal} workout plan.
Available equipment: ${equipment || "bodyweight only"}.
Include sets, reps, and rest times for 1 week.
`;

  const openaiRes = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model: "gpt-3.5-turbo",
      messages: [{ role: "user", content: prompt }],
    }),
  });

  const data = await openaiRes.json();

  if (!data.choices) {
    return res.status(500).json({ plan: "Error generating workout plan." });
  }

  const plan = data.choices[0].message.content;
  res.status(200).json({ plan });
}
