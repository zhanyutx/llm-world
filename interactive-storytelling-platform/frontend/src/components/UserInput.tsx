import React, { useState } from 'react';

interface UserInputProps {
  onSendMessage: (text: string) => void;
}

const UserInput: React.FC<UserInputProps> = ({ onSendMessage }) => {
  const [inputValue, setInputValue] = useState('');

  const handleSubmit = () => {
    if (inputValue.trim()) {
      onSendMessage(inputValue);
      setInputValue('');
    }
  };

  const handleKeyPress = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter') {
      handleSubmit();
    }
  };

  return (
    <div style={{ marginTop: '10px', display: 'flex' }}>
      <input
        type="text"
        placeholder="Type your message..."
        style={{ flexGrow: 1, marginRight: '5px', padding: '8px' }}
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        onKeyPress={handleKeyPress}
      />
      <button style={{ padding: '8px 15px' }} onClick={handleSubmit}>
        Send
      </button>
    </div>
  );
};

export default UserInput;
