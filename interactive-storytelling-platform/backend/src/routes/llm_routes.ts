import express, { Request, Response, Router } from 'express';
import { spawn } from 'child_process';
import path from 'path';

const router: Router = express.Router();

router.post('/generate', (req: Request, res: Response) => {
  const { prompt, provider = 'openai' } = req.body;

  if (!prompt) {
    return res.status(400).json({ error: 'Prompt is required' });
  }

  // For security, ensure provider is one of the expected values if more are added
  if (provider !== 'openai') {
      return res.status(400).json({ error: 'Invalid provider specified' });
  }

  const scriptPath = path.join(__dirname, '..', 'agents', 'llm_handler.py');
  const pythonProcess = spawn('python3', [
    scriptPath,
    JSON.stringify({ prompt, provider }),
  ]);

  let scriptOutput = '';
  let scriptError = '';

  pythonProcess.stdout.on('data', (data) => {
    scriptOutput += data.toString();
  });

  pythonProcess.stderr.on('data', (data) => {
    scriptError += data.toString();
  });

  pythonProcess.on('close', (code) => {
    if (code !== 0) {
      console.error(`Python script exited with code ${code}`);
      console.error('Error output from script:', scriptError);
      return res.status(500).json({ 
        error: 'Failed to generate LLM response.', 
        details: scriptError || `Python script exited with code ${code}`
      });
    }

    try {
      const outputJson = JSON.parse(scriptOutput);
      if (outputJson.error) {
        console.error('Python script returned an error:', outputJson.error);
        return res.status(500).json({ error: outputJson.error });
      }
      res.json({ response: outputJson.response });
    } catch (e) {
      console.error('Failed to parse Python script output:', e);
      console.error('Raw output:', scriptOutput);
      res.status(500).json({ error: 'Failed to parse LLM response.', details: scriptOutput });
    }
  });

  pythonProcess.on('error', (err) => {
    console.error('Failed to start Python process:', err);
    res.status(500).json({ error: 'Failed to start LLM process.', details: err.message });
  });
});

export default router;
