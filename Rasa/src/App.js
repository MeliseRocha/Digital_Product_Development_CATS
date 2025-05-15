import React from 'react';
import ChatBot from './components/ChatBot'; // or correct path to ChatBot

const App = () => {
  return (
    <div>
      <ChatBot
        host="http://localhost:5005/webhooks/rest/webhook"
        botLogo="./imgs/bot-logo.png"
        title="Covid Bot"
        welcomeMessage="Hi, how can I help you?"
        inactiveMsg="Server is down. Please contact support."
        theme={{
          background: "linear-gradient(19deg, #21D4FD 0%, #B721FF 100%)"
        }}
      />
    </div>
  );
};

export default App; // ✅ This is the critical line
