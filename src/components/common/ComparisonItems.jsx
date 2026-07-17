import React from 'react'

// 中西对照：以条目形式展示，替代原表格
export default function ComparisonItems({ comparison }) {
  if (!comparison || comparison.length === 0) return null
  return (
    <div className="comparison-list">
      {comparison.map((row, idx) => (
        <div key={idx} className="comparison-item">
          <div className="comparison-aspect">
            <span className="comparison-badge">对比维度</span>
            <span className="comparison-aspect-name">{row.aspect}</span>
            {row.classic && <span className="comparison-classic">{row.classic}</span>}
          </div>
          <div className="comparison-columns">
            <div className="comparison-col tcm">
              <span className="comparison-col-label">🀄 中医</span>
              <div className="comparison-text">{row.tcm}</div>
            </div>
            <div className="comparison-col western">
              <span className="comparison-col-label">🏥 西医</span>
              <div className="comparison-text">{row.western}</div>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
