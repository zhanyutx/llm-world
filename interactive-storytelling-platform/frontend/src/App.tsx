import './App.css';
import ChatPanel from './components/ChatPanel';
import ControlPanel from './components/ControlPanel'; // Import ControlPanel

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Interactive Storytelling Platform</h1>
      </header>
      <main>
        <ChatPanel />
        <ControlPanel /> {/* Add ControlPanel here */}
      </main>
    </div>
  );
}

export default App;
