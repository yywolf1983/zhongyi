import { useLocation, useNavigate } from 'react-router-dom'

const tabs = [
  { id: 'home', path: '/', label: '首页', icon: '🏠' },
  { id: 'syndromes', path: '/syndromes', label: '辨证论治', icon: '📋' },
  { id: 'acupuncture', path: '/acupuncture', label: '针灸针方', icon: '💉' },
  { id: 'formulas', path: '/formulas', label: '中药方剂', icon: '🌿' },
  { id: 'knowledge', path: '/knowledge-graph', label: '知识图谱', icon: '🔗' },
  { id: 'mapping', path: '/modern-mapping', label: '中西对照', icon: '🔄' }
]

export default function Navigation() {
  const location = useLocation()
  const navigate = useNavigate()

  const isActive = (tab) =>
    tab.path === '/' ? location.pathname === '/' : location.pathname.startsWith(tab.path)

  return (
    <nav className="nav-container">
      {tabs.map(tab => (
        <button
          key={tab.id}
          className={`nav-item ${isActive(tab) ? 'active' : ''}`}
          onClick={() => navigate(tab.path)}
        >
          <span className="nav-icon">{tab.icon}</span>
          {tab.label}
        </button>
      ))}
    </nav>
  )
}
