import { useMemo } from 'react'
import { useNavigate } from 'react-router-dom'
import { DataManager, DATA_TYPES } from '../../services/DataManager.js'
import { useAppContext } from '../../context/AppContext.jsx'

const TYPE_LABEL = {
  syndrome: '证型',
  formula: '方剂',
  medicine: '中药',
  acupoint: '穴位',
  needle: '针方',
  treatment: '治法',
  effect: '功效',
  meridian: '经络',
  mapping: '对照'
}

export default function HomeModule() {
  const navigate = useNavigate()
  const { recent, bookmarks } = useAppContext()

  const stats = useMemo(() => ({
    syndromes: DataManager.getAll(DATA_TYPES.SYNDROMES).length,
    formulas: DataManager.getAll(DATA_TYPES.FORMULAS).length,
    medicines: DataManager.getAll(DATA_TYPES.MEDICINES).length,
    acupoints: DataManager.getAll(DATA_TYPES.ACUPOINTS).length,
    needles: DataManager.getAll(DATA_TYPES.NEEDLE_PRESCRIPTIONS).length
  }), [])

  const domains = [
    { icon: '📋', title: '辨证论治', desc: '证型 · 治法', count: stats.syndromes, nav: '/syndromes' },
    { icon: '💉', title: '针灸针方', desc: '经络 · 穴位', count: stats.acupoints + stats.needles, nav: '/acupuncture' },
    { icon: '🌿', title: '方剂查询', desc: '经典名方', count: stats.formulas, nav: '/formulas' },
    { icon: '🪴', title: '中药百科', desc: '性味归经', count: stats.medicines, nav: '/formulas?tab=medicines' }
  ]

  const explores = [
    { icon: '🔗', title: '知识图谱', desc: '实体关系网络', nav: '/knowledge-graph' },
    { icon: '🔄', title: '中西对照', desc: '中医 · 现代映射', nav: '/modern-mapping' }
  ]

  return (
    <div className="home-container">
      <section>
        <h2 className="home-section-title">浏览内容</h2>
        <div className="home-grid">
          {domains.map((d) => (
            <button key={d.title} className="home-card" onClick={() => navigate(d.nav)} type="button">
              <span className="home-card-icon">{d.icon}</span>
              <span className="home-card-body">
                <span className="home-card-title">{d.title}</span>
                <span className="home-card-count">{d.desc} · {d.count}</span>
              </span>
            </button>
          ))}
        </div>
      </section>

      <section>
        <h2 className="home-section-title">探索</h2>
        <div className="home-grid">
          {explores.map((e) => (
            <button key={e.title} className="home-card" onClick={() => navigate(e.nav)} type="button">
              <span className="home-card-icon">{e.icon}</span>
              <span className="home-card-body">
                <span className="home-card-title">{e.title}</span>
                <span className="home-card-count">{e.desc}</span>
              </span>
            </button>
          ))}
        </div>
      </section>

      <section>
        <div className="home-section-head">
          <h2 className="home-section-title">我的</h2>
          <button className="home-link" onClick={() => navigate('/bookmarks')} type="button">查看全部</button>
        </div>
        <button className="home-card" style={{ width: '100%' }} onClick={() => navigate('/bookmarks')} type="button">
          <span className="home-card-icon">⭐</span>
          <span className="home-card-body">
            <span className="home-card-title">我的收藏</span>
            <span className="home-card-count">已收藏 {bookmarks.length} 条</span>
          </span>
        </button>
      </section>

      {recent.length > 0 && (
        <section>
          <h2 className="home-section-title">最近浏览</h2>
          <div className="home-recent">
            {recent.map((r) => (
              <button
                key={`${r.type}-${r.id}`}
                className="home-recent-item"
                onClick={() => navigate(r.navPath)}
                type="button"
              >
                <span className="home-recent-name">{r.name}</span>
                <span className="home-recent-type">{r.sub || TYPE_LABEL[r.type] || ''}</span>
              </button>
            ))}
          </div>
        </section>
      )}
    </div>
  )
}
