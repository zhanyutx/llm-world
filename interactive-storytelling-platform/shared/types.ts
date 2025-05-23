// Placeholder for shared types and interfaces
// Example:
// export interface User {
//   id: string;
//   name: string;
// }

export interface Message {
  id: string;
  text: string;
  sender: 'user' | 'agent1' | 'agent2' | 'narrator'; // Extendable
  timestamp: Date;
}
