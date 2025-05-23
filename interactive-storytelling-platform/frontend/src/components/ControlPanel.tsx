import React from 'react';
import './ControlPanel.css'; // Create this for basic styling

const ControlPanel: React.FC = () => {
  return (
    <div className="control-panel">
      <h2>Control Panel</h2>
      <p>Controls for intervention, instructions, and settings will be available here in a future phase.</p>
      <div>
        <h4>Quick Actions (Phase 1 - Visual Only)</h4>
        <button disabled>Pause Agents</button>
        <button disabled>Resume Agents</button>
        <button disabled>Save State</button>
      </div>
    </div>
  );
};

export default ControlPanel;
