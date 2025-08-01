// pages/api/progress.ts
import type { NextApiRequest, NextApiResponse } from "next";
import { getFirestore, doc, setDoc, getDoc } from "firebase/firestore";
import { initializeApp, getApps } from "firebase/app";

const firebaseConfig = {
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY!,
  authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN!,
  projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID!,
};

if (!getApps().length) {
  initializeApp(firebaseConfig);
}

const db = getFirestore();

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const { uid, weight, date, workout } = req.body;

  if (req.method === "POST") {
    if (!uid) return res.status(400).json({ error: "Missing UID" });

    const docRef = doc(db, "progress", uid);
    const snap = await getDoc(docRef);
    const oldData = snap.exists() ? snap.data() : { logs: [] };

    const newLogs = [
      ...oldData.logs,
      { date: date || new Date().toISOString(), weight, workout },
    ];

    await setDoc(docRef, { logs: newLogs });
    return res.status(200).json({ success: true });
  }

  if (req.method === "GET") {
    if (!uid) return res.status(400).json({ error: "Missing UID" });
    const docRef = doc(db, "progress", uid);
    const snap = await getDoc(docRef);
    return res.status(200).json(snap.exists() ? snap.data() : { logs: [] });
  }

  res.status(405).end();
}
