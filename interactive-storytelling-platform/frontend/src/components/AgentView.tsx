import React from 'react';

interface Message {
  text: string;
  timestamp: string;
}

interface AgentViewProps {
  agentName: string;
  messages: Message[];
}

const AgentView: React.FC<AgentViewProps> = ({ agentName, messages }) => {
  return (
    <div style={{ border: '1px solid #ccc', padding: '10px', margin: '5px', flex: 1 }}>
      <h3>{agentName}</h3>
      <div>
        {messages.map((msg, index) => (
          <div key={index} style={{ marginBottom: '5px', padding: '5px', background: '#f9f9f9', borderRadius: '4px' }}>
            <p>{msg.text}</p>
            <small style={{ color: '#888' }}>{msg.timestamp}</small>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AgentView;
