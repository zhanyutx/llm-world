import express from 'express';
import llmRouter from './routes/llm_routes'; // Import the new LLM router
import path from 'path';

const app = express();

// Middleware to parse JSON bodies
app.use(express.json());

// Use the LLM routes
app.use('/api/llm', llmRouter);

// Basic route for testing
app.get('/', (req, res) => {
  res.send('Backend server is running!');
});

// Serve static files from 'dist' (for frontend build, if co-located or for other static assets)
// This might be adjusted depending on your final deployment strategy
app.use(express.static(path.join(__dirname, '..', 'dist'))); 

export default app;
