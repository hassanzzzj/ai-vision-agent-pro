/**
 * Main App Component
 * Complete UI layout with all components
 */
import { useState } from 'react';
import { Brain, Github, Zap } from 'lucide-react';
import PromptBar from './components/PromptBar';
import ImageCanvas from './components/ImageCanvas';
import { useImageGeneration } from './hooks/useImageGeneration';
import { motion } from 'framer-motion';

function App() {
  const {
    generateImage,
    submitFeedback,
    reset,
    loading,
    error,
    progress,
    generatedImage,
    feedback,
    currentStep
  } = useImageGeneration();

  const [showLogs, setShowLogs] = useState(false);

  const handleGenerate = async (prompt, options) => {
    try {
      await generateImage(prompt, options);
    } catch (err) {
      console.error('Generation error:', err);
    }
  };

  const handleFeedback = (rating, comment) => {
    submitFeedback(rating, comment);
  };

  return (
    <div className="min-h-screen p-4 md:p-8">
      {/* Header */}
      <motion.header 
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="mb-8"
      >
        <div className="max-w-7xl mx-auto">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="bg-gradient-to-br from-primary-500 to-purple-600 p-3 rounded-xl shadow-lg">
                <Brain className="w-8 h-8" />
              </div>
              <div>
                <h1 className="text-3xl md:text-4xl font-bold bg-gradient-to-r from-primary-400 to-purple-400 bg-clip-text text-transparent">
                  AI Vision Agent Pro
                </h1>
                <p className="text-gray-400 text-sm md:text-base">
                  Powered by LangGraph + SiliconFlow + Langfuse
                </p>
              </div>
            </div>

            <div className="flex items-center space-x-3">
              {/* Status Badge */}
              <div className="hidden md:flex items-center space-x-2 glass-effect px-4 py-2 rounded-lg">
                <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                <span className="text-sm">System Online</span>
              </div>

              {/* GitHub Link */}
              <a
                href="https://github.com/hassanzzzj/ai-vision-agent-pro"
                target="_blank"
                rel="noopener noreferrer"
                className="glass-effect p-3 rounded-lg hover:bg-white/20 transition-all"
              >
                <Github className="w-5 h-5" />
              </a>
            </div>
          </div>
        </div>
      </motion.header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Input & Controls */}
          <motion.div
            initial={{ x: -20, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ delay: 0.1 }}
            className="lg:col-span-1 space-y-6"
          >
            <PromptBar
              onGenerate={handleGenerate}
              loading={loading}
              onReset={reset}
            />

            {/* Agent Logs */}
            <div className="card">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold flex items-center space-x-2">
                  <Zap className="w-5 h-5 text-yellow-400" />
                  <span>Agent Activity</span>
                </h3>
                <button
                  onClick={() => setShowLogs(!showLogs)}
                  className="text-sm text-primary-400 hover:text-primary-300"
                >
                  {showLogs ? 'Hide' : 'Show'}
                </button>
              </div>

              {showLogs && (
                <div className="space-y-2 max-h-64 overflow-y-auto">
                  {loading && (
                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="text-sm space-y-2"
                    >
                      <div className="flex items-start space-x-2">
                        <div className="w-2 h-2 bg-primary-400 rounded-full mt-1.5 animate-pulse"></div>
                        <div>
                          <p className="text-gray-300">Step: {currentStep}</p>
                          <p className="text-gray-500 text-xs">Progress: {progress}%</p>
                        </div>
                      </div>
                    </motion.div>
                  )}

                  {!loading && !generatedImage && (
                    <p className="text-sm text-gray-500">Waiting for generation...</p>
                  )}

                  {generatedImage && (
                    <div className="text-sm space-y-2">
                      <div className="flex items-start space-x-2">
                        <div className="w-2 h-2 bg-green-400 rounded-full mt-1.5"></div>
                        <div>
                          <p className="text-gray-300">✅ Generation Complete</p>
                          {feedback && (
                            <p className="text-gray-500 text-xs mt-1">{feedback}</p>
                          )}
                        </div>
                      </div>
                    </div>
                  )}

                  {error && (
                    <div className="flex items-start space-x-2">
                      <div className="w-2 h-2 bg-red-400 rounded-full mt-1.5"></div>
                      <div>
                        <p className="text-red-400 text-sm">❌ Error</p>
                        <p className="text-gray-500 text-xs">{error}</p>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Features Info */}
            <div className="card space-y-3">
              <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wide">
                Features
              </h3>
              <ul className="space-y-2 text-sm text-gray-300">
                <li className="flex items-center space-x-2">
                  <div className="w-1.5 h-1.5 bg-primary-400 rounded-full"></div>
                  <span>Agentic workflow with LangGraph</span>
                </li>
                <li className="flex items-center space-x-2">
                  <div className="w-1.5 h-1.5 bg-primary-400 rounded-full"></div>
                  <span>Real-time generation tracking</span>
                </li>
                <li className="flex items-center space-x-2">
                  <div className="w-1.5 h-1.5 bg-primary-400 rounded-full"></div>
                  <span>Quality assessment & iteration</span>
                </li>
                <li className="flex items-center space-x-2">
                  <div className="w-1.5 h-1.5 bg-primary-400 rounded-full"></div>
                  <span>Observability with Langfuse</span>
                </li>
              </ul>
            </div>
          </motion.div>

          {/* Right Column - Image Display */}
          <motion.div
            initial={{ x: 20, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="lg:col-span-2"
          >
            <ImageCanvas
              image={generatedImage}
              loading={loading}
              progress={progress}
              currentStep={currentStep}
              error={error}
              feedback={feedback}
              onFeedback={handleFeedback}
            />
          </motion.div>
        </div>
      </main>

      {/* Footer */}
      <motion.footer
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.3 }}
        className="mt-12 text-center text-gray-500 text-sm"
      >
        <p>
          Built with ❤️ using FastAPI, LangGraph, React, and SiliconFlow
        </p>
        <p className="mt-1">
          Monitoring powered by Langfuse
        </p>
      </motion.footer>
    </div>
  );
}

export default App;
