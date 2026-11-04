
import { useState } from "react";
import Message from "./Message";
import { sendMessage } from "../services/api";

function ChatWindow() {

  const [messages, setMessages] = useState([
    {
      role: "assistant",
      text: "Hello! Welcome to Géant AI Care. How can I help you today?"
    }
  ]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  // One unique ID per conversation
  const [sessionId] = useState(() => crypto.randomUUID());

  async function sendUserMessage() {

    if (!input.trim() || loading) return;

    const messageToSend = input.trim();

    const userMessage = {
      role: "user",
      text: messageToSend
    };

    setMessages(previous => [...previous, userMessage]);

    setInput("");
    setLoading(true);

    try {

      // Send only the new message
      const data = await sendMessage(
        messageToSend,
        sessionId
      );

      const aiMessage = {
        role: "assistant",
        text: data.answer
      };

      setMessages(previous => [...previous, aiMessage]);

    } catch (error) {

      console.error("API Error:", error);

      setMessages(previous => [
        ...previous,
        {
          role: "assistant",
          text: "Sorry, I couldn't connect to Géant AI Care. Please try again."
        }
      ]);

    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="chat-container">

      <header className="chat-header">
        <h2>Géant AI Care</h2>
        <p>Your intelligent product support assistant</p>
      </header>

      <div className="chat-messages">

        {messages.map((message, index) => (
          <Message key={index} message={message} />
        ))}

        {loading && (
          <div className="typing-indicator">
            AI Care is thinking...
          </div>
        )}

      </div>

      <div className="chat-input">

        <input
          type="text"
          placeholder="Ask me about your Géant device..."
          value={input}
          onChange={event => setInput(event.target.value)}
          onKeyDown={event => {
            if (event.key === "Enter") sendUserMessage();
          }}
        />

        <button
          onClick={sendUserMessage}
          disabled={loading || !input.trim()}
        >
          Send
        </button>

      </div>

    </div>
  );
}

export default ChatWindow;
