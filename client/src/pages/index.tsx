import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

const URL = 'http://localhost:8000/api/v1/chat'

const checkIndex = (index: number, msg: string) => {
  if (index % 2 === 0) {
    return <p key={index} style={{ margin: 0 }}><b>Human:</b> {msg}</p>
  } else {
    return <p key={index} style={{ margin: 0 }}><b>Assistant:</b> {msg}</p>
  }
}

const App: React.FC = () => {
  const inputRef = useRef<HTMLInputElement | null>(null);
  const [message, setMessage] = useState<string>('');
  const [chat, setChat] = useState<string[]>([]);

  useEffect(() => {
    const eventSource = new EventSource(URL);

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
      await axios.post(URL, { question: message, messages: chat });
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
      <form onSubmit={sendMessage} style={{ marginTop: 10 }}>
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

export default App;