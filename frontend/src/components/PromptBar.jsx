/**
 * PromptBar Component
 * User input for image generation prompts
 */
import { useState } from 'react';
import { Sparkles, Send, RotateCcw } from 'lucide-react';
import { motion } from 'framer-motion';

export default function PromptBar({ onGenerate, loading, onReset }) {
  const [prompt, setPrompt] = useState('');
  const [maxIterations, setMaxIterations] = useState(3);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (prompt.trim() && !loading) {
      onGenerate(prompt, { maxIterations });
    }
  };

  const handleReset = () => {
    setPrompt('');
    setMaxIterations(3);
    onReset();
  };

  const examplePrompts = [
    "A futuristic cyberpunk city at night with neon lights",
    "A serene mountain landscape with aurora borealis",
    "A cute robot reading a book in a cozy library",
    "An astronaut riding a horse on Mars"
  ];

  const handleExampleClick = (example) => {
    setPrompt(example);
  };

  return (
    <div className="card space-y-6">
      {/* Header */}
      <div className="flex items-center space-x-3">
        <div className="bg-gradient-to-br from-primary-500 to-purple-600 p-3 rounded-lg">
          <Sparkles className="w-6 h-6" />
        </div>
        <div>
          <h2 className="text-2xl font-bold">AI Vision Agent</h2>
          <p className="text-gray-400 text-sm">Agentic image generation with LangGraph</p>
        </div>
      </div>

      {/* Prompt Form */}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="prompt" className="block text-sm font-medium text-gray-300 mb-2">
            Describe your image
          </label>
          <textarea
            id="prompt"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Enter a detailed description of the image you want to generate..."
            className="input-field w-full min-h-[120px] resize-none"
            disabled={loading}
            required
          />
          <p className="text-xs text-gray-500 mt-1">
            {prompt.length} characters
          </p>
        </div>

        {/* Settings */}
        <div className="flex items-center space-x-4">
          <div className="flex-1">
            <label htmlFor="iterations" className="block text-sm font-medium text-gray-300 mb-2">
              Max Iterations: {maxIterations}
            </label>
            <input
              id="iterations"
              type="range"
              min="1"
              max="5"
              value={maxIterations}
              onChange={(e) => setMaxIterations(parseInt(e.target.value))}
              className="w-full"
              disabled={loading}
            />
            <div className="flex justify-between text-xs text-gray-500 mt-1">
              <span>Fast</span>
              <span>Quality</span>
            </div>
          </div>
        </div>

        {/* Buttons */}
        <div className="flex space-x-3">
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            type="submit"
            disabled={loading || !prompt.trim()}
            className="btn-primary flex-1 flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send className="w-5 h-5" />
            <span>{loading ? 'Generating...' : 'Generate Image'}</span>
          </motion.button>

          {(loading || prompt) && (
            <motion.button
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              type="button"
              onClick={handleReset}
              className="btn-secondary flex items-center space-x-2"
            >
              <RotateCcw className="w-5 h-5" />
              <span>Reset</span>
            </motion.button>
          )}
        </div>
      </form>

      {/* Example Prompts */}
      {!loading && (
        <div className="space-y-2">
          <p className="text-sm font-medium text-gray-400">Try an example:</p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {examplePrompts.map((example, index) => (
              <motion.button
                key={index}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => handleExampleClick(example)}
                className="text-left text-sm px-3 py-2 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 transition-all duration-200"
              >
                {example}
              </motion.button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
