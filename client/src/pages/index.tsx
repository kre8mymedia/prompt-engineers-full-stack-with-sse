import React, { useState, useEffect } from 'react';
import axios from 'axios';
// import './App.css';

const App: React.FC = () => {
  const [message, setMessage] = useState<string>('');
  const [chat, setChat] = useState<string[]>([]);

  useEffect(() => {
    const eventSource = new EventSource('http://localhost:8000/stream');

    eventSource.onmessage = (e: MessageEvent) => {
      setChat((prevChat) => [...prevChat, e.data]);
    };

    return () => {
      eventSource.close();
    };
  }, []);

  const sendMessage = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (message === '') return;

    try {
      await axios.post('http://localhost:8000/message', { message });
      setMessage('');
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="App">
      <h1>ChatGPT-like App</h1>
      <div className="chat-box">
        {chat.map((msg, index) => (
          <p key={index}>{msg}</p>
        ))}
      </div>
      <form onSubmit={sendMessage}>
        <input
          type="text"
          placeholder="Type your message"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
};

export default App;