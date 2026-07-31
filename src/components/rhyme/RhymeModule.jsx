import { useState, useMemo, useCallback } from 'react'
import { rhymes, CATEGORIES, SUB_CATEGORIES } from '../../data/rhymes.js'
import GroupedList from '../common/GroupedList.jsx'

function CatRow({ options, active, onSelect, small }) {
  return (
    <div className={`cat-grid ${small ? 'small' : ''}`}>
      {options.map((opt) => (
        <button
          key={opt.value}
          type="button"
          className={`cat-chip ${active === opt.value ? 'active' : ''}`}
          onClick={() => onSelect(opt.value)}
        >
          <span className="cat-chip-label">{opt.label}</span>
          <span className="cat-chip-count">{opt.count}</span>
        </button>
      ))}
    </div>
  )
}

export default function RhymeModule() {
  const [activeCategory, setActiveCategory] = useState('all')
  const [activeSubCategory, setActiveSubCategory] = useState('all')
  const [expandedId, setExpandedId] = useState(null)
  const [categoryOpen, setCategoryOpen] = useState(false)
  const [subOpen, setSubOpen] = useState(false)

  // 当一级分类切换时，重置子分类
  const handleCategoryChange = useCallback((catId) => {
    setActiveCategory(catId)
    setActiveSubCategory('all')
  }, [])

  const currentSubCategories = useMemo(
    () => SUB_CATEGORIES[activeCategory] || null,
    [activeCategory]
  )

  // 一级分类选项 + 数量
  const categoryOpts = useMemo(() => {
    const m = {}
    rhymes.forEach(r => { if (r.category) m[r.category] = (m[r.category] || 0) + 1 })
    return [
      { value: 'all', label: '全部', count: rhymes.length },
      ...CATEGORIES.map(cat => ({ value: cat.id, label: `${cat.icon} ${cat.label}`, count: m[cat.id] || 0 })),
    ]
  }, [rhymes])

  // 子分类选项 + 数量（依赖当前大类）
  const subOpts = useMemo(() => {
    if (!currentSubCategories) return []
    const base = activeCategory === 'all' ? rhymes : rhymes.filter(r => r.category === activeCategory)
    const m = {}
    base.forEach(r => { if (r.subCategory) m[r.subCategory] = (m[r.subCategory] || 0) + 1 })
    return [
      { value: 'all', label: '全部子类', count: base.length },
      ...currentSubCategories.map(sub => ({ value: sub.id, label: sub.label, count: m[sub.id] || 0 })),
    ]
  }, [currentSubCategories, activeCategory, rhymes])

  const filtered = useMemo(() => {
    let result = rhymes
    if (activeCategory !== 'all') {
      result = result.filter((r) => r.category === activeCategory)
      if (currentSubCategories && activeSubCategory !== 'all') {
        result = result.filter((r) => r.subCategory === activeSubCategory)
      }
    }
    return result
  }, [activeCategory, activeSubCategory, currentSubCategories])

  const toggleExpand = useCallback((id) => {
    setExpandedId((prev) => (prev === id ? null : id))
  }, [])

  return (
    <div className="rhyme-container">
      {/* 一级分类（可折叠，默认收起，选中自动收起） */}
      <div className="cat-filter">
        <button
          type="button"
          className="cat-filter-toggle"
          onClick={() => setCategoryOpen(o => !o)}
        >
          <span className="cat-filter-title">分类</span>
          <span className="cat-filter-summary">
            {activeCategory === 'all'
              ? '全部'
              : CATEGORIES.find((c) => c.id === activeCategory)?.label}
          </span>
          <span className={`cat-filter-caret ${categoryOpen ? 'open' : ''}`}>▾</span>
        </button>
        {categoryOpen && (
          <CatRow
            options={categoryOpts}
            active={activeCategory}
            onSelect={(v) => { handleCategoryChange(v); setCategoryOpen(false) }}
          />
        )}

        {currentSubCategories && (
          <button
            type="button"
            className="cat-filter-toggle"
            onClick={() => setSubOpen(o => !o)}
          >
            <span className="cat-filter-title">子分类</span>
            <span className="cat-filter-summary">
              {activeSubCategory === 'all'
                ? '全部'
                : currentSubCategories.find((s) => s.id === activeSubCategory)?.label}
            </span>
            <span className={`cat-filter-caret ${subOpen ? 'open' : ''}`}>▾</span>
          </button>
        )}
        {subOpen && currentSubCategories && (
          <CatRow
            options={subOpts}
            active={activeSubCategory}
            onSelect={(v) => { setActiveSubCategory(v); setSubOpen(false) }}
            small
          />
        )}
      </div>

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
                  <h3 className="rhyme-card-title">{rhyme.title}</h3>
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
