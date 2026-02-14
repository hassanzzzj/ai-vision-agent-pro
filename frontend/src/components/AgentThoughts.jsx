import './AgentThoughts.css';

export function AgentThoughts({ thoughts }) {
  if (!thoughts || thoughts.length === 0) return null;

  return (
    <div className="agent-thoughts">
      <h3>🧠 Agent Workflow</h3>
      
      <div className="thoughts-list">
        {thoughts.map((thought, index) => (
          <div 
            key={index} 
            className="thought-item"
            style={{ animationDelay: `${index * 0.1}s` }}
          >
            <div className="thought-timestamp">{thought.timestamp}</div>
            <div className="thought-message">{thought.message}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
