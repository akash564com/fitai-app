// pages/api/meal.ts
import type { NextApiRequest, NextApiResponse } from "next";

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== "POST") return res.status(405).end();

  const { calories, dietType, goal } = req.body;

  const prompt = `
Create a detailed ${dietType} meal plan for someone whose goal is ${goal}.
Daily calories target: ${calories}.
Include breakfast, lunch, dinner, and snacks for 7 days.
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
    return res.status(500).json({ plan: "Error generating meal plan." });
  }

  const plan = data.choices[0].message.content;
  res.status(200).json({ plan });
}
