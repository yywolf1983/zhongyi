import { useState, useMemo, useCallback } from 'react'
import { rhymes, CATEGORIES, SUB_CATEGORIES } from '../../data/rhymes.js'
import CollapsibleFilter from '../common/CollapsibleFilter.jsx'
import GroupedList, { Highlight } from '../common/GroupedList.jsx'

export default function RhymeModule() {
  const [activeCategory, setActiveCategory] = useState('all')
  const [activeSubCategory, setActiveSubCategory] = useState('all')
  const [searchText, setSearchText] = useState('')
  const [expandedId, setExpandedId] = useState(null)

  // 当一级分类切换时，重置子分类
  const handleCategoryChange = useCallback((catId) => {
    setActiveCategory(catId)
    setActiveSubCategory('all')
  }, [])

  const currentSubCategories = useMemo(
    () => SUB_CATEGORIES[activeCategory] || null,
    [activeCategory]
  )

  const filtered = useMemo(() => {
    let result = rhymes
    if (activeCategory !== 'all') {
      result = result.filter((r) => r.category === activeCategory)
      if (currentSubCategories && activeSubCategory !== 'all') {
        result = result.filter((r) => r.subCategory === activeSubCategory)
      }
    }
    if (searchText.trim()) {
      const q = searchText.trim().toLowerCase()
      result = result.filter(
        (r) =>
          r.title.toLowerCase().includes(q) ||
          r.category.toLowerCase().includes(q) ||
          r.source.toLowerCase().includes(q) ||
          r.content.toLowerCase().includes(q) ||
          (r.notes && r.notes.toLowerCase().includes(q))
      )
    }
    return result
  }, [activeCategory, activeSubCategory, searchText, currentSubCategories])

  const toggleExpand = useCallback((id) => {
    setExpandedId((prev) => (prev === id ? null : id))
  }, [])

  const summaryLabel = useMemo(() => {
    if (activeCategory === 'all') return '全部'
    const cat = CATEGORIES.find((c) => c.id === activeCategory)
    if (!currentSubCategories || activeSubCategory === 'all') return cat?.label
    const sub = currentSubCategories.find((s) => s.id === activeSubCategory)
    return `${cat?.label} · ${sub?.label}`
  }, [activeCategory, activeSubCategory, currentSubCategories])

  return (
    <div className="rhyme-container">
      {/* 搜索栏 */}
      <div className="module-toolbar">
        <div className="rhyme-search-bar">
          <span className="rhyme-search-icon">🔍</span>
          <input
            type="text"
            className="rhyme-search-input"
            placeholder="搜索歌诀名称、内容…"
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
          />
          {searchText && (
            <button className="rhyme-search-clear" onClick={() => setSearchText('')} type="button">
              ✕
            </button>
          )}
        </div>
      </div>

      {/* 分类筛选 — 折叠 */}
      <CollapsibleFilter label="分类" summary={summaryLabel}>
        <div className="tag-filter-bar" style={{ marginBottom: 0 }}>
          {CATEGORIES.map((cat) => (
            <button
              key={cat.id}
              type="button"
              className={`tag-filter-btn ${activeCategory === cat.id ? 'active' : ''}`}
              onClick={() => handleCategoryChange(cat.id)}
            >
              {cat.icon} {cat.label}
            </button>
          ))}
        </div>
      </CollapsibleFilter>

      {/* 子分类筛选 — 仅当选中大类且有子分类时显示 */}
      {currentSubCategories && (
        <CollapsibleFilter
          label="子分类"
          summary={
            activeSubCategory === 'all'
              ? '全部'
              : currentSubCategories.find((s) => s.id === activeSubCategory)?.label
          }
        >
          <div className="tag-filter-bar" style={{ marginBottom: 0 }}>
            {currentSubCategories.map((sub) => (
              <button
                key={sub.id}
                type="button"
                className={`tag-filter-btn ${activeSubCategory === sub.id ? 'active' : ''}`}
                onClick={() => setActiveSubCategory(sub.id)}
              >
                {sub.label}
              </button>
            ))}
          </div>
        </CollapsibleFilter>
      )}

      {/* 统计 */}
      <div className="rhyme-summary">
        共 <strong>{filtered.length}</strong> 首
        {filtered.length !== rhymes.length && ` / ${rhymes.length}`} 歌诀
        {activeCategory !== 'all' && (
          <> · {CATEGORIES.find((c) => c.id === activeCategory)?.label}</>
        )}
        {activeSubCategory !== 'all' && (
          <> · {currentSubCategories?.find((s) => s.id === activeSubCategory)?.label}</>
        )}
      </div>

      {/* 歌诀列表（按子分类分组） */}
      <GroupedList
        className="rhyme-list"
        items={filtered}
        getGroup={(r) => r.subCategory || r.category || '其他'}
        getKey={(r) => r.id}
        emptyMessage="没有找到匹配的歌诀"
        renderItem={(rhyme) => {
          const isExpanded = expandedId === rhyme.id
          return (
            <div key={rhyme.id} className={`rhyme-card ${isExpanded ? 'expanded' : ''}`}>
              <button
                type="button"
                className="rhyme-card-header"
                onClick={() => toggleExpand(rhyme.id)}
              >
                <div className="rhyme-card-top">
                  <h3 className="rhyme-card-title"><Highlight text={rhyme.title} query={searchText} /></h3>
                  <div className="rhyme-card-meta">
                    <span className="rhyme-card-category">{rhyme.category}</span>
                    {rhyme.subCategory && (
                      <span className="rhyme-card-sub">{rhyme.subCategory}</span>
                    )}
                  </div>
                </div>
                <div className="rhyme-card-source">{rhyme.source}</div>
                <span className={`rhyme-card-arrow ${isExpanded ? 'open' : ''}`}>▾</span>
              </button>

              {isExpanded && (
                <div className="rhyme-card-body">
                  <pre className="rhyme-content">{rhyme.content}</pre>
                  {rhyme.notes && (
                    <div className="rhyme-notes">
                      <strong>📝 按语：</strong>
                      {rhyme.notes}
                    </div>
                  )}
                </div>
              )}
            </div>
          )
        }}
      />
    </div>
  )
}
