import { useNavigate } from 'react-router-dom'
import { useAppContext } from '../../context/AppContext'
import { navigateToEntity } from '../../services/EntityRoute.js'
import EmptyState from '../common/EmptyState.jsx'

const TYPE_LABELS = {
  syndrome: '证型',
  formula: '方剂',
  medicine: '中药',
  acupoint: '穴位',
  needle: '针方',
  'acu-presc': '针方'
}

const TYPE_ICONS = {
  syndrome: '📋',
  formula: '💊',
  medicine: '🌿',
  acupoint: '📍',
  needle: '💉',
  'acu-presc': '💉'
}

export default function BookmarksModule() {
  const navigate = useNavigate()
  const { bookmarks, removeBookmark, getBookmarksByType } = useAppContext()

  const handleClick = (bookmark) => {
    navigateToEntity(navigate, bookmark.type, bookmark.id)
  }

  const handleRemove = (e, bookmark) => {
    e.stopPropagation()
    removeBookmark(bookmark.id, bookmark.type)
  }

  // Group by type
  const grouped = {}
  bookmarks.forEach(b => {
    if (!grouped[b.type]) grouped[b.type] = []
    grouped[b.type].push(b)
  })

  if (bookmarks.length === 0) {
    return <EmptyState message="还没有收藏任何内容，在浏览时点击 ☆ 即可收藏" icon="⭐" />
  }

  return (
    <div>
      <div className="bookmarks-header">
        <h2>我的收藏</h2>
        <span className="bookmarks-count">共 {bookmarks.length} 项</span>
      </div>

      {Object.entries(grouped).map(([type, items]) => (
        <div key={type} className="search-result-category">
          <div className="search-result-title">
            <span>{TYPE_ICONS[type] || '📄'} {TYPE_LABELS[type] || type}</span>
            <span className="result-count">{items.length}项</span>
          </div>
          <div className="list-container">
            {items.map(item => (
              <div key={item.id} className={`list-item ${item.type}`} onClick={() => handleClick(item)}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div>
                    <div className="list-item-title">{item.name}</div>
                    {item.pinyin && <div className="list-item-pinyin">{item.pinyin}</div>}
                    {item.bookmarkedAt && (
                      <div className="list-item-desc" style={{ fontSize: '0.85rem' }}>
                        收藏于 {new Date(item.bookmarkedAt).toLocaleDateString('zh-CN')}
                      </div>
                    )}
                  </div>
                  <button
                    className="back-button"
                    style={{ margin: 0, flexShrink: 0 }}
                    onClick={(e) => handleRemove(e, item)}
                  >
                    取消收藏
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}
