import React, { useState } from "react";
import ChatbotService from "../../services/ChatBot/index";

function Chatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [sessionId, setSessionId] = useState("");
  const [isLoadingData, setIsLoadingData] = useState(false);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const handleInputChange = (e) => {
    setInput(e.target.value);
  };

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    if (!input) return;
    const newMessages = [...messages, { sender: "You", text: input }];
    setMessages(newMessages);
    setInput("");
    setIsLoadingData(true);
    const data = (await ChatbotService.talkToBot({ input, sessionId })) || {};
    setIsLoadingData(false);
    setSessionId(data.session_id);
    setMessages([...newMessages, { sender: "Bot", text: data.response }]);
  };

  return (
    <div>
      {/* Floating Chat Button */}
      <div className="fixed bottom-5 right-5">
        <button
          onClick={toggleChat}
          className="bg-blue-500 text-white p-4 rounded-full shadow-lg hover:bg-blue-600"
        >
          💬
        </button>
      </div>

      {/* Chat Window */}
      {isOpen && (
        <div className="fixed bottom-20 right-5 w-80 h-96 bg-white border border-gray-300 rounded-lg shadow-lg">
          <div className="flex flex-col h-full">
            <div className="flex-1 p-4 overflow-y-auto">
              {messages.map((msg, index) => (
                <div
                  key={index}
                  className={`my-2 p-2 rounded-lg ${
                    msg.sender === "You" ? "bg-blue-100" : "bg-gray-100"
                  }`}
                >
                  <strong>{msg.sender}: </strong> {msg.text}
                </div>
              ))}
            </div>
            {isLoadingData ? (
              <div className="flex justify-center items-center">
                <svg
                  className="animate-spin h-8 w-8 text-blue-500"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  ></circle>
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
                  ></path>
                </svg>
              </div>
            ) : null}
            <div className="p-4 border-t border-gray-200">
              <form onSubmit={handleFormSubmit} className="flex">
                <input
                  type="text"
                  value={input}
                  onChange={handleInputChange}
                  placeholder="Type a message..."
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-l-lg focus:outline-none"
                />
                <button
                  type="submit"
                  disabled={isLoadingData}
                  className="bg-blue-500 text-white px-4 py-2 rounded-r-lg hover:bg-blue-600"
                >
                  Send
                </button>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Chatbot;
