export default function EmptyState({ message = '这里暂时空空如也', icon = '🌿', hint }) {
  return (
    <div className="empty-state">
      <div className="empty-icon">{icon}</div>
      <div className="empty-message">{message}</div>
      {hint && <div className="empty-hint">{hint}</div>}
    </div>
  )
}
