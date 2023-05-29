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
  const [apiKey, setApiKey] = useState<string>('');
  const [token, setToken] = useState<string>('');
  const [message, setMessage] = useState<string>('');
  const [chat, setChat] = useState<string[]>([]);

  const getHeaders = (jwt: string, apiKey: string) => {
    if (jwt) {
      return {
        "Authorization": `Bearer ${jwt}`
      }
    }

    return {
      "x-api-key": apiKey
    }
  }

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

    const headers = token || apiKey
                    ? { headers: getHeaders(token, apiKey) } 
                    : undefined

    try {
      await axios.post(
        URL,
        { question: message, messages: chat },
        headers
      );
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
      <input
          style={{ marginTop: '5px' }}
          type="text"
          placeholder="Enter JWT"
          value={token}
          onChange={(e) => setToken(e.target.value)}
        /> JWT<br/>
        <input
          style={{ marginTop: '5px' }}
          type="text"
          placeholder="Enter Token"
          value={apiKey}
          onChange={(e) => setApiKey(e.target.value)}
        /> Personal Access Token
    </div>
  );
};

export default App;