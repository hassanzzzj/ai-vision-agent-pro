import './StatusPanel.css';

export function StatusPanel({ status }) {
  if (!status) return null;

  const getStatusColor = (statusStr) => {
    if (statusStr === 'complete') return '#10b981';
    if (statusStr === 'failed') return '#ef4444';
    if (statusStr.includes('awaiting')) return '#f59e0b';
    return '#3b82f6';
  };

  return (
    <div className="status-panel">
      <h3>📊 Status</h3>
      
      <div className="status-item">
        <span className="status-label">Current Step:</span>
        <span 
          className="status-value"
          style={{ color: getStatusColor(status.status) }}
        >
          {status.current_step?.replace(/_/g, ' ').toUpperCase()}
        </span>
      </div>

      <div className="status-item">
        <span className="status-label">Progress:</span>
        <span className="status-value">{status.progress}%</span>
      </div>

      {status.result && (
        <>
          <div className="status-item">
            <span className="status-label">Quality Score:</span>
            <span className="status-value">
              {status.result.quality_score?.toFixed(1)}/10
            </span>
          </div>

          <div className="status-item">
            <span className="status-label">Iterations:</span>
            <span className="status-value">{status.result.iterations}</span>
          </div>

          {status.result.optimized_prompt && (
            <div className="status-item full-width">
              <span className="status-label">Optimized Prompt:</span>
              <p className="optimized-prompt">{status.result.optimized_prompt}</p>
            </div>
          )}
        </>
      )}

      {status.error && (
        <div className="error-message">
          ❌ Error: {status.error}
        </div>
      )}
    </div>
  );
}
