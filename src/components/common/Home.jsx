import { useMemo } from 'react'
import { useNavigate } from 'react-router-dom'
import { DataManager } from '../../services/DataManager.js'
import { DATA_TYPES } from '../../services/DataManager.js'
import { useAppContext } from '../../context/AppContext.jsx'
import modernMappingData from '../../../assets/data/modern_mapping.json'

export default function Home() {
  const navigate = useNavigate()
  const { bookmarks } = useAppContext()

  const counts = useMemo(() => {
    const get = (t) => {
      try { return DataManager.getAll(t).length } catch { return 0 }
    }
    const syndromes = get(DATA_TYPES.SYNDROMES)
    const medicines = get(DATA_TYPES.MEDICINES)
    const acupoints = get(DATA_TYPES.ACUPOINTS)
    const formulas = get(DATA_TYPES.FORMULAS)
    const needles = get(DATA_TYPES.NEEDLE_PRESCRIPTIONS) + get(DATA_TYPES.ACUPUNCTURE_PRESCRIPTIONS)
    const mappings = modernMappingData.length
    return { syndromes, medicines, acupoints, formulas, needles, mappings }
  }, [])

  const totalEntries =
    counts.syndromes + counts.medicines + counts.acupoints + counts.formulas + counts.needles + counts.mappings

  const modules = [
    { key: 'syndromes', path: '/syndromes', icon: '📋', title: '辨证论治', desc: '证型 · 治法 · 方药关联', color: 'var(--color-syndrome)', count: counts.syndromes },
    { key: 'acupuncture', path: '/acupuncture', icon: '💉', title: '针灸针方', desc: '经络 · 穴位 · 针方', color: 'var(--color-acupoint)', count: counts.acupoints + counts.needles },
    { key: 'formulas', path: '/formulas', icon: '🌿', title: '中药方剂', desc: '经典名方 · 君臣佐使', color: 'var(--color-formula)', count: counts.formulas + counts.medicines },
    { key: 'knowledge', path: '/knowledge-graph', icon: '🔗', title: '知识图谱', desc: '跨模块关系可视化', color: 'var(--color-primary)', count: totalEntries },
    { key: 'mapping', path: '/modern-mapping', icon: '🔄', title: '中西对照', desc: '中医 · 现代医学', color: 'var(--color-mapping)', count: counts.mappings },
    { key: 'bookmarks', path: '/bookmarks', icon: '⭐', title: '我的收藏', desc: '个人常用条目', color: 'var(--color-accent)', count: bookmarks.length }
  ]

  const stats = [
    { label: '证型', value: counts.syndromes, color: 'var(--color-syndrome)' },
    { label: '中药', value: counts.medicines, color: 'var(--color-medicine)' },
    { label: '方剂', value: counts.formulas, color: 'var(--color-formula)' },
    { label: '穴位', value: counts.acupoints, color: 'var(--color-acupoint)' }
  ]

  return (
    <div className="home-container">
      <section className="home-hero">
        <div className="home-hero-badge">中医知识库</div>
        <h1 className="home-hero-title">中医辨证论治系统</h1>
        <p className="home-hero-sub">传承经典 · 辨证施治 · 一站查阅</p>
        <div className="home-hero-stats">
          {stats.map(s => (
            <div className="home-stat" key={s.label}>
              <span className="home-stat-value">{s.value}</span>
              <span className="home-stat-label">{s.label}</span>
            </div>
          ))}
          <div className="home-stat">
            <span className="home-stat-value">{totalEntries}</span>
            <span className="home-stat-label">总条目</span>
          </div>
        </div>
      </section>

      <section className="home-section">
        <h2 className="home-section-title">快速入口</h2>
        <div className="home-grid">
          {modules.map(m => (
            <button
              key={m.key}
              className="home-card"
              style={{ '--card-accent': m.color }}
              onClick={() => navigate(m.path)}
            >
              <span className="home-card-icon" style={{ background: m.color }}>{m.icon}</span>
              <span className="home-card-body">
                <span className="home-card-title">{m.title}</span>
                <span className="home-card-desc">{m.desc}</span>
              </span>
              <span className="home-card-count">{m.count}</span>
            </button>
          ))}
        </div>
      </section>

      {bookmarks.length > 0 && (
        <section className="home-section">
          <div className="home-section-head">
            <h2 className="home-section-title">最近收藏</h2>
            <button className="home-link" onClick={() => navigate('/bookmarks')}>查看全部 →</button>
          </div>
          <div className="home-recent">
            {bookmarks.slice(0, 4).map(b => (
              <button
                key={`${b.type}-${b.id}`}
                className="home-recent-item"
                onClick={() => navigate(b.route || '/bookmarks')}
              >
                <span className="home-recent-name">{b.name}</span>
                <span className="home-recent-type">{b.type}</span>
              </button>
            ))}
          </div>
        </section>
      )}
    </div>
  )
}
