export default function EmptyState({ message = '暂无数据', icon = '📭' }) {
  return (
    <div className="empty-state">
      <div className="empty-icon">{icon}</div>
      <div className="empty-message">{message}</div>
    </div>
  )
}
