import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
// import './App.css';

const App: React.FC = () => {
  const inputRef = useRef<HTMLInputElement | null>(null);
  const [message, setMessage] = useState<string>('');
  const [chat, setChat] = useState<string[]>([]);

  useEffect(() => {
    const eventSource = new EventSource('http://localhost:8000/api/v1/stream');

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
      await axios.post('http://localhost:8000/api/v1/message', { message, chat });
      setMessage('');
      if (inputRef) {
        inputRef.current?.focus();
      }
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="App">
      <h1>ChatGPT Clone</h1>
      <div className="chat-box">
        {chat.map((msg, index) => (
          checkIndex(index, msg)
        ))}
      </div>
      <form onSubmit={sendMessage}>
        <input
          ref={inputRef}
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

function checkIndex(index: number, msg: string) {
  if (index % 2 === 0) {
    return <p key={index}>Human: {msg}</p>
  } else {
    return <p key={index}>Assistant: {msg}</p>
  }
}

export default App;