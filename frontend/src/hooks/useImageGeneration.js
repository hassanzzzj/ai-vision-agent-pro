/**
 * Custom Hook: useImageGeneration
 * Backend API ke saath communicate karne ke liye
 */
import { useState, useCallback, useEffect, useRef } from 'react';
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const useImageGeneration = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [taskId, setTaskId] = useState(null);
  const [status, setStatus] = useState(null);
  const [progress, setProgress] = useState(0);
  const [generatedImage, setGeneratedImage] = useState(null);
  const [feedback, setFeedback] = useState(null);
  const [currentStep, setCurrentStep] = useState('');
  
  const pollIntervalRef = useRef(null);

  /**
   * Start image generation
   */
  const generateImage = useCallback(async (prompt, options = {}) => {
    try {
      setLoading(true);
      setError(null);
      setGeneratedImage(null);
      setProgress(0);
      setStatus('pending');
      setCurrentStep('Initializing...');

      const response = await axios.post(`${API_BASE_URL}/api/v1/generate`, {
        prompt,
        reference_image: options.referenceImage || null,
        max_iterations: options.maxIterations || 3,
        enable_monitoring: true
      });

      const { task_id } = response.data;
      setTaskId(task_id);
      
      // Start polling for status
      startPolling(task_id);

      return task_id;
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to start generation';
      setError(errorMessage);
      setLoading(false);
      throw new Error(errorMessage);
    }
  }, []);

  /**
   * Poll task status
   */
  const startPolling = useCallback((task_id) => {
    // Clear existing interval
    if (pollIntervalRef.current) {
      clearInterval(pollIntervalRef.current);
    }

    // Poll every 2 seconds
    pollIntervalRef.current = setInterval(async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/api/v1/status/${task_id}`);
        const data = response.data;

        setStatus(data.status);
        setProgress(data.progress);
        setCurrentStep(data.current_step);

        // Update based on status
        if (data.status === 'completed') {
          setGeneratedImage(data.generated_image);
          setFeedback(data.feedback);
          setLoading(false);
          clearInterval(pollIntervalRef.current);
        } else if (data.status === 'failed') {
          setError(data.error || 'Generation failed');
          setLoading(false);
          clearInterval(pollIntervalRef.current);
        }
      } catch (err) {
        console.error('Polling error:', err);
        // Don't stop polling on temporary errors
      }
    }, 2000);
  }, []);

  /**
   * Submit feedback
   */
  const submitFeedback = useCallback(async (rating, comment = null) => {
    if (!taskId) return;

    try {
      await axios.post(`${API_BASE_URL}/api/v1/feedback`, {
        task_id: taskId,
        rating,
        comment
      });
    } catch (err) {
      console.error('Failed to submit feedback:', err);
    }
  }, [taskId]);

  /**
   * Reset state
   */
  const reset = useCallback(() => {
    if (pollIntervalRef.current) {
      clearInterval(pollIntervalRef.current);
    }
    setLoading(false);
    setError(null);
    setTaskId(null);
    setStatus(null);
    setProgress(0);
    setGeneratedImage(null);
    setFeedback(null);
    setCurrentStep('');
  }, []);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current);
      }
    };
  }, []);

  return {
    generateImage,
    submitFeedback,
    reset,
    loading,
    error,
    taskId,
    status,
    progress,
    generatedImage,
    feedback,
    currentStep
  };
};
