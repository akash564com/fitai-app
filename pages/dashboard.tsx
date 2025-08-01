import ProtectedRoute from "@/components/ProtectedRoute";
import { useState, useEffect } from "react";
import { auth } from "@/lib/firebase";
import { onAuthStateChanged } from "firebase/auth";

export default function Dashboard() {
  const [uid, setUid] = useState("");

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      if (user) setUid(user.uid);
    });
    return () => unsubscribe();
  }, []);

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-50 p-4 max-w-2xl mx-auto">
        <h2 className="text-2xl font-bold mb-4">Your Progress</h2>
        {/* Your dashboard UI here */}
      </div>
    </ProtectedRoute>
  );
}
