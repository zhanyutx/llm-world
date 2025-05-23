import React, { useState } from 'react';
import AgentView from './AgentView';
import UserInput from './UserInput';
import { Message } from '../../../shared/types'; // Corrected path
import { v4 as uuidv4 } from 'uuid'; // For generating unique IDs

const initialAgent1Messages: Message[] = [
  { id: uuidv4(), text: "The ancient ruins whisper secrets of the old kingdom...", sender: 'agent1', timestamp: new Date() },
  { id: uuidv4(), text: "I found a strange symbol carved into this stone.", sender: 'agent1', timestamp: new Date() }
];

const initialAgent2Messages: Message[] = [
  { id: uuidv4(), text: "I sense dark magic here. We should proceed with caution, my friend.", sender: 'agent2', timestamp: new Date() },
  { id: uuidv4(), text: "The air grows cold. Something is watching us.", sender: 'agent2', timestamp: new Date() }
];

const ChatPanel: React.FC = () => {
  const [agent1Messages, setAgent1Messages] = useState<Message[]>(initialAgent1Messages);
  const [agent2Messages, setAgent2Messages] = useState<Message[]>(initialAgent2Messages);
  const [userNarratorMessages, setUserNarratorMessages] = useState<Message[]>([]);

  const handleSendMessage = (text: string) => {
    if (text.trim() === '') return;

    const newMessage: Message = {
      id: uuidv4(),
      text,
      sender: 'user',
      timestamp: new Date()
    };
    setUserNarratorMessages(prevMessages => [...prevMessages, newMessage]);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: 'calc(100vh - 50px)', padding: '10px' }}>
      <h2>Story Agents</h2>
      <div style={{ display: 'flex', flexGrow: 1, marginBottom: '10px', overflowY: 'auto' }}>
        <AgentView agentName="Agent 1: Elara" messages={agent1Messages.map(msg => ({ ...msg, timestamp: msg.timestamp.toLocaleTimeString() }))} />
        <AgentView agentName="Agent 2: Marcus" messages={agent2Messages.map(msg => ({ ...msg, timestamp: msg.timestamp.toLocaleTimeString() }))} />
        <AgentView agentName="User/Narrator" messages={userNarratorMessages.map(msg => ({ ...msg, timestamp: msg.timestamp.toLocaleTimeString() }))} />
      </div>
      <UserInput onSendMessage={handleSendMessage} />
    </div>
  );
};

export default ChatPanel;
