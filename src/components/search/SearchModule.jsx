import { useState, useEffect, useRef, useCallback } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { SearchService } from '../../services/SearchService.js'
import EmptyState from '../common/EmptyState.jsx'

const typeLabels = {
  syndromes: '证型',
  formulas: '方剂',
  medicines: '中药',
  acupoints: '穴位',
  needles: '针方',
  acupuncture_prescriptions: '针灸处方',
  treatments: '治法',
  meridians: '经络',
  effects: '功效',
  modern_mapping: '中西对照'
}

const typeIcons = {
  syndromes: '📋',
  formulas: '💊',
  medicines: '🌿',
  acupoints: '📍',
  needles: '💉',
  acupuncture_prescriptions: '💉',
  treatments: '⚕️',
  meridians: '🔗',
  effects: '✨',
  modern_mapping: '🔄'
}

const typeRouteMap = {
  syndromes: (id) => `/syndromes/${id}`,
  formulas: (id) => `/formulas/${id}`,
  medicines: (id) => `/formulas/medicine/${id}`,
  acupoints: (id) => `/acupuncture/${id}`,
  needles: (id) => `/acupuncture/needle/${id}`,
  acupuncture_prescriptions: (id) => `/acupuncture`,
  treatments: (id) => `/syndromes?treatment=${id}`,
  meridians: (id) => `/acupuncture?meridian=${id}`,
  effects: (id) => `/syndromes?effect=${id}`,
  modern_mapping: (id) => `/modern-mapping?id=${id}`
}

// 关键词高亮
function highlightText(text, keyword) {
  if (!text || !keyword) return text
  if (typeof text !== 'string') return text
  try {
    const escapedKeyword = keyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
    const regex = new RegExp(`(${escapedKeyword})`, 'gi')
    const parts = text.split(regex)
    return parts.map((part, i) =>
      regex.test(part) ? <mark key={i}>{part}</mark> : part
    )
  } catch {
    return text
  }
}

export default function SearchModule() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const [keyword, setKeyword] = useState('')
  const [searchResults, setSearchResults] = useState(null)
  const [searchHistory, setSearchHistory] = useState([])
  const hasAutoSearched = useRef(false)

  useEffect(() => {
    setSearchHistory(SearchService.getSearchHistory())
  }, [])

  // Auto-search from URL query param
  useEffect(() => {
    const q = searchParams.get('q')
    if (q && !hasAutoSearched.current) {
      const decoded = decodeURIComponent(q)
      setKeyword(decoded)
      const results = SearchService.globalSearch(decoded)
      setSearchResults(results)
      SearchService.addSearchHistory(decoded)
      setSearchHistory(SearchService.getSearchHistory())
      hasAutoSearched.current = true
    }
    // Reset when URL changes
    return () => { hasAutoSearched.current = false }
  }, [searchParams])

  const handleHistoryClick = (kw) => {
    setKeyword(kw)
    const results = SearchService.globalSearch(kw)
    setSearchResults(results)
    SearchService.addSearchHistory(kw)
    setSearchHistory(SearchService.getSearchHistory())
  }

  const handleClearHistory = () => {
    SearchService.clearSearchHistory()
    setSearchHistory([])
  }

  const handleResultClick = (item) => {
    const routeFn = typeRouteMap[item.type]
    if (routeFn) {
      navigate(routeFn(item.id))
    }
  }

  const renderContext = (item) => {
    const ctx = item.context
    if (!ctx) return null

    switch (item.type) {
      case 'syndromes':
        return (
          <div className="result-context">
            {ctx.classification && ctx.classification.length > 0 && (
              <div className="result-tags">
                {ctx.classification.map((c, i) => <span key={i} className="result-tag">{c}</span>)}
              </div>
            )}
            {ctx.diagnosis_points && ctx.diagnosis_points.length > 0 && (
              <div className="result-points">
                辨证要点：{ctx.diagnosis_points.join('；')}
              </div>
            )}
            {ctx.pathogenesis && (
              <div className="result-sub">病机：{ctx.pathogenesis}</div>
            )}
            {ctx.modern_medicine && ctx.modern_medicine.length > 0 && (
              <div className="result-sub">现代对应：{ctx.modern_medicine.join('、')}</div>
            )}
          </div>
        )
      case 'medicines':
        return (
          <div className="result-context">
            <div className="result-tags">
              <span className="result-tag">{ctx.category}</span>
              {ctx.nature && <span className="result-tag nature-tag">{ctx.nature}</span>}
              {ctx.flavor && ctx.flavor.map((f, i) => <span key={i} className="result-tag flavor-tag">{f}</span>)}
            </div>
            {ctx.latin_name && <div className="result-sub">拉丁名：{ctx.latin_name}</div>}
            {ctx.effects && ctx.effects.length > 0 && (
              <div className="result-points">功效：{ctx.effects.join('、')}</div>
            )}
            {ctx.meridian && ctx.meridian.length > 0 && (
              <div className="result-sub">归经：{ctx.meridian.join('、')}</div>
            )}
          </div>
        )
      case 'formulas':
        return (
          <div className="result-context">
            <div className="result-tags">
              <span className="result-tag">{ctx.category}</span>
              {ctx.subcategory && <span className="result-tag">{ctx.subcategory}</span>}
            </div>
            {ctx.source && <div className="result-sub">出处：{ctx.author ? `${ctx.source}（${ctx.author}）` : ctx.source}</div>}
            {ctx.effects && ctx.effects.length > 0 && (
              <div className="result-points">功效：{ctx.effects.join('、')}</div>
            )}
            {ctx.ingredients_count > 0 && (
              <div className="result-sub">组成：共{ctx.ingredients_count}味药</div>
            )}
          </div>
        )
      case 'acupoints':
        return (
          <div className="result-context">
            <div className="result-tags">
              <span className="result-tag">{ctx.meridian}</span>
            </div>
            {ctx.location && <div className="result-points">定位：{ctx.location}</div>}
            {ctx.indications && ctx.indications.length > 0 && (
              <div className="result-sub">主治：{ctx.indications.join('、')}</div>
            )}
          </div>
        )
      case 'needles':
        return (
          <div className="result-context">
            <div className="result-tags">
              {ctx.category && <span className="result-tag">{ctx.category}</span>}
            </div>
            {ctx.acupoints && ctx.acupoints.length > 0 && (
              <div className="result-points">取穴：{ctx.acupoints.join('、')}</div>
            )}
            {ctx.effects && ctx.effects.length > 0 && (
              <div className="result-sub">功效：{ctx.effects.join('、')}</div>
            )}
          </div>
        )
      case 'acupuncture_prescriptions':
        return (
          <div className="result-context">
            <div className="result-tags">
              {ctx.category && <span className="result-tag">{ctx.category}</span>}
              {ctx.subcategory && <span className="result-tag">{ctx.subcategory}</span>}
            </div>
            {ctx.acupoints && ctx.acupoints.length > 0 && (
              <div className="result-points">取穴：{ctx.acupoints.join('、')}</div>
            )}
            {ctx.effects && ctx.effects.length > 0 && (
              <div className="result-sub">功效：{ctx.effects.join('、')}</div>
            )}
          </div>
        )
      case 'treatments':
        return (
          <div className="result-context">
            <div className="result-tags">
              {ctx.category && <span className="result-tag">{ctx.category}</span>}
            </div>
            {ctx.principle && <div className="result-points">治则：{ctx.principle}</div>}
            {ctx.indications && ctx.indications.length > 0 && (
              <div className="result-sub">适用：{ctx.indications.join('、')}</div>
            )}
          </div>
        )
      case 'meridians':
        return (
          <div className="result-context">
            <div className="result-tags">
              <span className="result-tag">{ctx.category}</span>
              {ctx.yin_yang && <span className="result-tag">{ctx.yin_yang}经</span>}
              {ctx.element && <span className="result-tag">{ctx.element}行</span>}
            </div>
            {ctx.main_points && ctx.main_points.length > 0 && (
              <div className="result-points">主要穴位：{ctx.main_points.join('、')}</div>
            )}
          </div>
        )
      case 'effects':
        return (
          <div className="result-context">
            {ctx.description && <div className="result-points">{ctx.description}</div>}
            {ctx.indications && ctx.indications.length > 0 && (
              <div className="result-sub">适用：{ctx.indications.join('、')}</div>
            )}
          </div>
        )
      case 'modern_mapping':
        return (
          <div className="result-context">
            {ctx.category && (
              <div className="result-tags">
                <span className="result-tag">{ctx.category}</span>
              </div>
            )}
            <div className="result-sub">
              <span style={{ fontWeight: 500, color: '#ea6b52' }}>🀄 中医：</span>
              {ctx.chinese_term}
              <span style={{ margin: '0 6px', color: '#999' }}>↔</span>
              <span style={{ fontWeight: 500, color: '#4a7fb5' }}>🏥 西医：</span>
              {ctx.modern_term}
            </div>
            {ctx.comparison && ctx.comparison.length > 0 && (
              <div className="result-points">
                {ctx.comparison.map((c, i) => (
                  <span key={i} style={{ display: 'inline-block', marginRight: '12px', fontSize: '0.88rem' }}>
                    {c.aspect}：{c.tcm} | {c.western}
                  </span>
                ))}
              </div>
            )}
          </div>
        )
      default:
        return null
    }
  }

  // No query + no manual search → show history / empty prompt
  if (!keyword) {
    return (
      <div>
        {searchHistory.length > 0 ? (
          <div className="card">
            <div className="card-title">
              搜索历史
              <button onClick={handleClearHistory} className="clear-history-btn">清空</button>
            </div>
            <div className="tag-list">
              {searchHistory.map((h, index) => (
                <span
                  key={index}
                  className="tag-item"
                  style={{ cursor: 'pointer' }}
                  onClick={() => handleHistoryClick(h)}
                >
                  {h}
                </span>
              ))}
            </div>
          </div>
        ) : (
          <EmptyState message="在顶部搜索框输入关键词开始搜索" icon="🔍" />
        )}
      </div>
    )
  }

  // Search in progress but no results loaded yet
  if (!searchResults) {
    return (
      <EmptyState message={`正在搜索 "${keyword}"...`} icon="🔍" />
    )
  }

  // Results loaded
  return (
    <div>
      <div className="search-results-header">
        搜索 "<strong>{searchResults.keyword}</strong>" 共找到 <strong>{searchResults.total}</strong> 条结果
      </div>

      {searchResults.total > 0 ? (
        <div className="search-results">
          {Object.entries(searchResults.results).map(([type, items]) => {
            if (items.length === 0) return null
            return (
              <div key={type} className="search-result-category">
                <div className="search-result-title">
                  <span>{typeIcons[type] || '📄'} {typeLabels[type]}</span>
                  <span className="result-count">{items.length}条</span>
                </div>
                <div className="list-container">
                  {items.map(item => (
                    <div key={item.id} className="list-item search-result-item" onClick={() => handleResultClick(item)}>
                      <div className="list-item-header">
                        <span className="list-item-title">{highlightText(item.name, searchResults.keyword)}</span>
                        {item.pinyin && <span className="list-item-pinyin">{highlightText(item.pinyin, searchResults.keyword)}</span>}
                      </div>
                      {renderContext(item)}
                    </div>
                  ))}
                </div>
              </div>
            )
          })}
        </div>
      ) : (
        <EmptyState message={`未找到与 "${keyword}" 相关的结果，请尝试其他关键词`} icon="🔍" />
      )}
    </div>
  )
}
