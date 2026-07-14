import { useState, useMemo, useEffect, useRef, useCallback } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { DataManager } from '../../services/DataManager.js'
import { DATA_TYPES } from '../../services/DataManager.js'
import EmptyState from '../common/EmptyState.jsx'

const CATEGORY_LABELS = {
  'all': '全部',
  '症状': '临床症状',
  '疾病': '疾病证型',
  '心理': '心理情绪'
}

const CATEGORY_ICONS = {
  '症状': '🩺',
  '疾病': '🏥',
  '心理': '🧠'
}

export default function ModernMapping() {
  const navigate = useNavigate()
  const [searchParams, setSearchParams] = useSearchParams()
  const [searchKeyword, setSearchKeyword] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [activeMappingId, setActiveMappingId] = useState(null)
  const itemRefs = useRef({})

  const mappings = useMemo(() => DataManager.getAll(DATA_TYPES.MODERN_MAPPING), [])
  const syndromes = useMemo(() => DataManager.getAll(DATA_TYPES.SYNDROMES), [])

  const syndromeMap = useMemo(() => {
    const map = {}
    syndromes.forEach(s => { map[s.id] = s })
    return map
  }, [syndromes])

  const categories = useMemo(() => {
    const cats = new Set()
    mappings.forEach(m => { if (m.category) cats.add(m.category) })
    return ['all', ...Array.from(cats).sort()]
  }, [mappings])

  // Read URL params to pre-filter and scroll to target
  useEffect(() => {
    const q = searchParams.get('q')
    const cat = searchParams.get('cat')
    const id = searchParams.get('id')

    if (q) {
      setSearchKeyword(decodeURIComponent(q))
    }
    if (cat && cat !== 'all') {
      setSelectedCategory(cat)
    }
    if (id) {
      setActiveMappingId(id)
    }
  }, [searchParams])

  const filteredMappings = useMemo(() => {
    let result = mappings
    if (selectedCategory !== 'all') {
      result = result.filter(m => m.category === selectedCategory)
    }
    if (searchKeyword.trim()) {
      const kw = searchKeyword.toLowerCase()
      result = result.filter(m =>
        m.chinese_term.toLowerCase().includes(kw) ||
        m.modern_term.toLowerCase().includes(kw) ||
        (m.comparison && m.comparison.some(c =>
          c.tcm?.toLowerCase().includes(kw) ||
          c.western?.toLowerCase().includes(kw)
        ))
      )
    }
    return result
  }, [mappings, selectedCategory, searchKeyword])

  // Scroll to target item after filtered list renders
  useEffect(() => {
    if (activeMappingId && itemRefs.current[activeMappingId]) {
      // Small delay to ensure DOM is rendered
      const timer = setTimeout(() => {
        itemRefs.current[activeMappingId]?.scrollIntoView({
          behavior: 'smooth',
          block: 'center'
        })
        setActiveMappingId(null)
      }, 150)
      return () => clearTimeout(timer)
    }
  }, [filteredMappings, activeMappingId])

  const handleSyndromeClick = (syndromeId) => {
    if (syndromeId) navigate(`/syndromes/${syndromeId}`)
  }

  // In-page search/filter instead of navigating away
  const handleTermClick = (term) => {
    setSearchKeyword(term)
    // Update URL to reflect the in-page filter
    const params = new URLSearchParams(searchParams)
    params.set('q', term)
    setSearchParams(params, { replace: true })
  }

  // Highlight active (targeted via ?id=) item
  const isTargetItem = (mappingId) => {
    return searchParams.get('id') === mappingId
  }

  return (
    <div>
      <div className="view-toggle" style={{ marginBottom: '20px', flexWrap: 'wrap' }}>
        {categories.map(cat => (
          <button
            key={cat}
            className={`toggle-btn ${selectedCategory === cat ? 'active' : ''}`}
            onClick={() => {
              setSelectedCategory(cat)
              const params = new URLSearchParams(searchParams)
              if (cat === 'all') {
                params.delete('cat')
              } else {
                params.set('cat', cat)
              }
              setSearchParams(params, { replace: true })
            }}
          >
            {cat !== 'all' && (CATEGORY_ICONS[cat] || '')} {CATEGORY_LABELS[cat] || cat}
          </button>
        ))}
      </div>

      {filteredMappings.length === 0 ? (
        <EmptyState message="未找到匹配的中西对照" icon="🔍" />
      ) : (
        <div className="mapping-list">
          {filteredMappings.map(mapping => {
            const syndrome = mapping.related_syndrome ? syndromeMap[mapping.related_syndrome] : null
            const hasComparison = mapping.comparison && mapping.comparison.length > 0
            const isTarget = isTargetItem(mapping.id)

            return (
              <div
                key={mapping.id}
                ref={el => { if (el) itemRefs.current[mapping.id] = el }}
                className={`mapping-item${isTarget ? ' mapping-item-highlight' : ''}`}
              >
                {/* Header: TCM ↔ Western */}
                <div className="mapping-header">
                  <div className="mapping-term-section">
                    <div className="mapping-term-chinese" style={{ cursor: 'pointer' }}
                      onClick={() => handleTermClick(mapping.chinese_term)} title="点击筛选此中医术语">
                      {mapping.chinese_term}
                    </div>
                    <div className="mapping-arrow">↔</div>
                    <div className="mapping-term-modern" style={{ cursor: 'pointer' }}
                      onClick={() => handleTermClick(mapping.modern_term)} title="点击筛选此西医术语">
                      {mapping.modern_term}
                    </div>
                  </div>
                  {mapping.category && (
                    <span className="tag-item mapping-category-tag">
                      {CATEGORY_ICONS[mapping.category] || ''} {mapping.category}
                    </span>
                  )}
                </div>

                {/* Comparison Table */}
                {hasComparison && (
                  <div className="comparison-table-wrapper">
                    <table className="comparison-table">
                      <thead>
                        <tr>
                          <th className="comparison-aspect-col">对比维度</th>
                          <th className="comparison-tcm-col">
                            <span className="comparison-col-label">🀄 中医</span>
                          </th>
                          <th className="comparison-western-col">
                            <span className="comparison-col-label">🏥 西医</span>
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        {mapping.comparison.map((row, idx) => (
                          <tr key={idx}>
                            <td className="comparison-aspect">{row.aspect}</td>
                            <td className="comparison-tcm">{row.tcm}</td>
                            <td className="comparison-western">{row.western}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}

                {/* Related Syndrome Link */}
                {syndrome && (
                  <div className="comparison-related">
                    <span className="related-label">关联证型：</span>
                    <span
                      className="tag-item clickable-tag"
                      onClick={() => handleSyndromeClick(syndrome.id)}
                    >
                      {syndrome.name}
                    </span>
                  </div>
                )}
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
