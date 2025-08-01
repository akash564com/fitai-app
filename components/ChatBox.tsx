// components/ChatBox.tsx
import { useState } from "react";
import { fetchAIResponse } from "@/lib/openai";

export default function ChatBox() {
  const [messages, setMessages] = useState<{ role: string; text: string }[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMsg = { role: "user", text: input };
    setMessages((msgs) => [...msgs, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const reply = await fetchAIResponse(input);
      const botMsg = { role: "bot", text: reply };
      setMessages((msgs) => [...msgs, botMsg]);
    } catch {
      setMessages((msgs) => [...msgs, { role: "bot", text: "Error from AI." }]);
    }

    setLoading(false);
  };

  return (
    <div className="max-w-2xl mx-auto p-4">
      <h2 className="text-2xl font-semibold mb-4">AI Chat Assistant</h2>
      <div className="h-96 overflow-y-auto border p-3 mb-4 bg-white rounded shadow">
        {messages.map((msg, i) => (
          <div key={i} className={`mb-2 ${msg.role === "user" ? "text-right" : "text-left"}`}>
            <div className={`inline-block p-2 rounded ${msg.role === "user" ? "bg-blue-100" : "bg-gray-200"}`}>
              {msg.text}
            </div>
          </div>
        ))}
        {loading && <p className="text-gray-500">AI is typing...</p>}
      </div>
      <div className="flex gap-2">
        <input
          className="flex-grow border p-2 rounded"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message..."
        />
        <button
          onClick={handleSend}
          className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
        >
          Send
        </button>
      </div>
    </div>
  );
}
