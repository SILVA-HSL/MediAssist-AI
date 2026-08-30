import { useState } from "react";
import "./App.css";

type Message = {
  role: "user" | "assistant";
  content: string;
  sources?: string[];
  ticket_id?: number | null;
  ticket_status?: string | null;
};

function App() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content:
        "Hello! I'm MediAssist, your hospital AI assistant. How can I help you today?",
    },
  ]);

  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;
    setIsLoading(true);

    const userMessage: Message = {
      role: "user",
      content: input,
    };

    setMessages((previous) => [...previous, userMessage]);
    setInput("");

    try {
      const response = await fetch("http://127.0.0.1:8000/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: input,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to communicate with MediAssist.");
      }

      const data = await response.json();

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: data.response,
          sources: data.sources || [],
          ticket_id: data.ticket_id ?? null,
          ticket_status: data.ticket_status ?? null,
        },
      ]);
    } catch (error) {
      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content:
            "Sorry, I was unable to connect to the MediAssist backend. Please try again.",
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (
    event: React.KeyboardEvent<HTMLTextAreaElement>
  ) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="app">
      <header className="header">
        <div className="brand">
          <div className="logo">🏥</div>

          <div>
            <h1>MediAssist AI</h1>
            <p>Hospital AI Assistant</p>
          </div>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          Online
        </div>
      </header>

      <main className="chat-container">
        <div className="messages">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`message-row ${message.role}`}
            >
              <div className="message-avatar">
                {message.role === "user" ? "👤" : "🏥"}
              </div>

              <div className="message-content">
                <div className="message-name">
                  {message.role === "user" ? "You" : "MediAssist"}
                </div>

                <div className="message-bubble">
  {message.content}
</div>

          {message.role === "assistant" &&
            message.sources &&
            message.sources.length > 0 && (
              <div className="sources">
                <div className="sources-title">
                  📚 Sources
                </div>

                <ul>
                  {message.sources.map((source, sourceIndex) => (
                    <li key={sourceIndex}>
                      {source}
                    </li>
                  ))}
                </ul>
              </div>
            )}
            {message.role === "assistant" &&
              message.ticket_id !== null &&
              message.ticket_id !== undefined && (
                <div className="ticket-card">
                  <div className="ticket-title">
                    🎫 Maintenance Ticket Created
                  </div>

                  <div className="ticket-details">
                    <div>
                      <strong>Ticket ID:</strong> #{message.ticket_id}
                    </div>

                    <div>
                      <strong>Status:</strong>{" "}
                      {message.ticket_status || "Open"}
                    </div>
                  </div>
                </div>
              )}
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="message-row assistant">
              <div className="message-avatar">
                🏥
              </div>

              <div className="message-content">
                <div className="message-name">
                  MediAssist
                </div>

                <div className="message-bubble typing">
                  Thinking...
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="input-area">
          <textarea
            value={input}
            onChange={(event) => setInput(event.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask MediAssist about hospital procedures, beds, equipment..."
            rows={1}
          />

          <button
            onClick={handleSend}
           disabled={!input.trim() || isLoading}
          >
          {isLoading ? "Thinking..." : "Send"}
          </button>
        </div>

        <p className="disclaimer">
          MediAssist provides information based on hospital documents
          and operational data.
        </p>
      </main>
    </div>
  );
}

export default App;