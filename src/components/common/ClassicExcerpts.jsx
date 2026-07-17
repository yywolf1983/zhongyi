export default function ClassicExcerpts({ excerpts }) {
  if (!excerpts || excerpts.length === 0) return null
  return (
    <div className="section">
      <h2 className="section-title">经典摘录</h2>
      <div className="classic-excerpt-list">
        {excerpts.map((ex, i) => (
          <div className="classic-excerpt" key={i}>
            <span className="classic-source">{ex.source}</span>
            {ex.text ? <p className="classic-text">{ex.text}</p> : null}
          </div>
        ))}
      </div>
    </div>
  )
}
