
import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
  headers: {
    "Content-Type": "application/json",
  },
});

export async function sendMessage(message, sessionId) {

  const response = await api.post("/chat", {
    message: message,
    session_id: sessionId,
  });

  return response.data;
}
