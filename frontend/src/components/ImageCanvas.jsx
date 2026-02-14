/**
 * ImageCanvas Component
 * Display generated images with progress and status
 */
import { useState } from 'react';
import { Download, ThumbsUp, ThumbsDown, Image as ImageIcon, Loader2, AlertCircle, CheckCircle2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function ImageCanvas({ 
  image, 
  loading, 
  progress, 
  currentStep, 
  error,
  feedback,
  onFeedback 
}) {
  const [showFeedbackDialog, setShowFeedbackDialog] = useState(false);
  const [rating, setRating] = useState(0.8);
  const [comment, setComment] = useState('');

  const handleDownload = () => {
    if (!image) return;

    const link = document.createElement('a');
    link.href = `data:image/png;base64,${image}`;
    link.download = `ai-vision-${Date.now()}.png`;
    link.click();
  };

  const handleSubmitFeedback = () => {
    onFeedback(rating, comment);
    setShowFeedbackDialog(false);
    setComment('');
  };

  return (
    <div className="card h-full flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-semibold flex items-center space-x-2">
          <ImageIcon className="w-6 h-6 text-primary-400" />
          <span>Generated Image</span>
        </h3>

        {image && !loading && (
          <div className="flex space-x-2">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleDownload}
              className="btn-secondary py-2 px-4 text-sm flex items-center space-x-2"
            >
              <Download className="w-4 h-4" />
              <span>Download</span>
            </motion.button>

            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => setShowFeedbackDialog(true)}
              className="btn-secondary py-2 px-4 text-sm flex items-center space-x-2"
            >
              <ThumbsUp className="w-4 h-4" />
              <span>Feedback</span>
            </motion.button>
          </div>
        )}
      </div>

      {/* Canvas Area */}
      <div className="flex-1 relative bg-black/30 rounded-lg overflow-hidden min-h-[400px]">
        <AnimatePresence mode="wait">
          {/* Loading State */}
          {loading && (
            <motion.div
              key="loading"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="absolute inset-0 flex flex-col items-center justify-center space-y-6"
            >
              <Loader2 className="w-16 h-16 text-primary-400 animate-spin" />
              
              <div className="text-center space-y-2 max-w-md">
                <p className="text-lg font-medium">{currentStep || 'Initializing...'}</p>
                
                {/* Progress Bar */}
                <div className="w-64 bg-white/10 rounded-full h-2 overflow-hidden">
                  <motion.div
                    className="h-full bg-gradient-to-r from-primary-500 to-purple-600"
                    initial={{ width: 0 }}
                    animate={{ width: `${progress}%` }}
                    transition={{ duration: 0.5 }}
                  />
                </div>
                <p className="text-sm text-gray-400">{progress}% Complete</p>
              </div>

              {/* Progress Steps */}
              <div className="flex items-center space-x-4 text-sm">
                {['Planning', 'Generating', 'Reviewing'].map((step, index) => {
                  const stepProgress = (index + 1) * 33;
                  const isActive = progress >= stepProgress - 33 && progress < stepProgress;
                  const isCompleted = progress >= stepProgress;

                  return (
                    <div key={step} className="flex items-center space-x-2">
                      <div className={`w-8 h-8 rounded-full flex items-center justify-center border-2 transition-all ${
                        isCompleted 
                          ? 'bg-primary-500 border-primary-500' 
                          : isActive 
                          ? 'bg-primary-500/50 border-primary-400 animate-pulse' 
                          : 'bg-white/10 border-white/20'
                      }`}>
                        {isCompleted ? (
                          <CheckCircle2 className="w-5 h-5" />
                        ) : (
                          <span className="text-xs">{index + 1}</span>
                        )}
                      </div>
                      <span className={isActive || isCompleted ? 'text-white' : 'text-gray-500'}>
                        {step}
                      </span>
                    </div>
                  );
                })}
              </div>
            </motion.div>
          )}

          {/* Error State */}
          {error && !loading && (
            <motion.div
              key="error"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              className="absolute inset-0 flex flex-col items-center justify-center space-y-4"
            >
              <AlertCircle className="w-16 h-16 text-red-400" />
              <div className="text-center max-w-md">
                <h4 className="text-xl font-semibold mb-2">Generation Failed</h4>
                <p className="text-gray-400">{error}</p>
              </div>
            </motion.div>
          )}

          {/* Image Display */}
          {image && !loading && !error && (
            <motion.div
              key="image"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="absolute inset-0"
            >
              <img
                src={`data:image/png;base64,${image}`}
                alt="Generated"
                className="w-full h-full object-contain"
              />
              
              {/* Feedback Badge */}
              {feedback && (
                <div className="absolute bottom-4 left-4 right-4">
                  <div className="glass-effect rounded-lg p-3">
                    <p className="text-sm">
                      <span className="font-semibold text-primary-400">AI Feedback:</span> {feedback}
                    </p>
                  </div>
                </div>
              )}
            </motion.div>
          )}

          {/* Empty State */}
          {!image && !loading && !error && (
            <motion.div
              key="empty"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="absolute inset-0 flex flex-col items-center justify-center space-y-4 text-gray-500"
            >
              <ImageIcon className="w-24 h-24 opacity-20" />
              <p className="text-lg">Your generated image will appear here</p>
              <p className="text-sm">Enter a prompt to get started</p>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Feedback Dialog */}
      <AnimatePresence>
        {showFeedbackDialog && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4"
            onClick={() => setShowFeedbackDialog(false)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              onClick={(e) => e.stopPropagation()}
              className="card max-w-md w-full space-y-4"
            >
              <h3 className="text-xl font-semibold">Rate this generation</h3>
              
              <div>
                <label className="block text-sm font-medium mb-2">
                  Quality Score: {(rating * 100).toFixed(0)}%
                </label>
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.1"
                  value={rating}
                  onChange={(e) => setRating(parseFloat(e.target.value))}
                  className="w-full"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">
                  Comments (optional)
                </label>
                <textarea
                  value={comment}
                  onChange={(e) => setComment(e.target.value)}
                  placeholder="Share your thoughts..."
                  className="input-field w-full min-h-[80px]"
                />
              </div>

              <div className="flex space-x-3">
                <button
                  onClick={handleSubmitFeedback}
                  className="btn-primary flex-1"
                >
                  Submit Feedback
                </button>
                <button
                  onClick={() => setShowFeedbackDialog(false)}
                  className="btn-secondary"
                >
                  Cancel
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
