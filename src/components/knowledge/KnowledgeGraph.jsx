import { useState, useMemo, useRef, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { DataManager } from '../../services/DataManager.js'
import { DATA_TYPES } from '../../services/DataManager.js'
import EmptyState from '../common/EmptyState.jsx'
import CollapsibleFilter from '../common/CollapsibleFilter.jsx'

const NODE_COLORS = {
  syndrome: '#2f5d7c',
  formula: '#3a6f93',
  medicine: '#b8802f',
  acupoint: '#7a5a93',
  needle: '#2f7d75',
  treatment: '#4a7d5e',
  effect: '#b04a6a',
  meridian: '#3a6f93',
  modern: '#b8802f'
}

const NODE_LABELS = {
  syndrome: '证型',
  formula: '方剂',
  medicine: '中药',
  acupoint: '穴位',
  needle: '针方',
  treatment: '治法',
  effect: '功效',
  meridian: '经络',
  modern: '中西对照'
}

const NODE_ICONS = {
  syndrome: '📋',
  formula: '💊',
  medicine: '🌿',
  acupoint: '📍',
  needle: '💉',
  treatment: '⚕️',
  effect: '✨',
  meridian: '🔗',
  modern: '🔄'
}

export default function KnowledgeGraph() {
  const navigate = useNavigate()
  const detailPanelRef = useRef(null)
  const [focusEntity, setFocusEntity] = useState(null)
  const [focusType, setFocusType] = useState(null)
  const [viewMode, setViewMode] = useState('syndrome')

  // Auto-scroll to detail panel when a node is clicked
  useEffect(() => {
    if (focusEntity && detailPanelRef.current) {
      setTimeout(() => {
        detailPanelRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' })
      }, 100)
    }
  }, [focusEntity])

  const syndromes = useMemo(() => DataManager.getAll(DATA_TYPES.SYNDROMES), [])
  const formulas = useMemo(() => DataManager.getAll(DATA_TYPES.FORMULAS), [])
  const medicines = useMemo(() => DataManager.getAll(DATA_TYPES.MEDICINES), [])
  const acupoints = useMemo(() => DataManager.getAll(DATA_TYPES.ACUPOINTS), [])
  const needles = useMemo(() => DataManager.getAll(DATA_TYPES.NEEDLE_PRESCRIPTIONS), [])
  const meridians = useMemo(() => DataManager.getAll(DATA_TYPES.MERIDIANS), [])
  const treatments = useMemo(() => DataManager.getAll(DATA_TYPES.TREATMENTS), [])
  const modernMappings = useMemo(() => DataManager.getAll(DATA_TYPES.MODERN_MAPPING), [])

  // Build entity lookup (all types)
  const entityMap = useMemo(() => {
    const map = {}
    syndromes.forEach(s => { map[`syndrome_${s.id}`] = { ...s, entityType: 'syndrome' } })
    formulas.forEach(f => { map[`formula_${f.id}`] = { ...f, entityType: 'formula' } })
    medicines.forEach(m => { map[`medicine_${m.id}`] = { ...m, entityType: 'medicine' } })
    acupoints.forEach(a => { map[`acupoint_${a.id}`] = { ...a, entityType: 'acupoint' } })
    needles.forEach(n => { map[`needle_${n.id}`] = { ...n, entityType: 'needle' } })
    meridians.forEach(m => { map[`meridian_${m.id}`] = { ...m, entityType: 'meridian' } })
    treatments.forEach(t => { map[`treatment_${t.id}`] = { ...t, entityType: 'treatment' } })
    modernMappings.forEach(mm => { map[`modern_${mm.id}`] = { ...mm, entityType: 'modern' } })
    return map
  }, [syndromes, formulas, medicines, acupoints, needles, meridians, treatments, modernMappings])

  // Build edges
  const edges = useMemo(() => {
    const result = []

    // Syndrome -> Formula
    syndromes.forEach(s => {
      if (s.related_formulas) {
        s.related_formulas.forEach(fid => {
          if (entityMap[`formula_${fid}`]) {
            result.push({ from: `syndrome_${s.id}`, to: `formula_${fid}`, label: '推荐方剂' })
          }
        })
      }
    })

    // Formula -> Medicine (ingredients)
    formulas.forEach(f => {
      const ingredients = f.ingredients || f.composition
      if (ingredients) {
        ingredients.forEach(comp => {
          if (comp.medicine_id && entityMap[`medicine_${comp.medicine_id}`]) {
            result.push({ from: `formula_${f.id}`, to: `medicine_${comp.medicine_id}`, label: comp.role ? `${comp.role}药` : '组成' })
          }
        })
      }
    })

    // Syndrome -> Needle
    syndromes.forEach(s => {
      if (s.related_needle) {
        s.related_needle.forEach(nid => {
          if (entityMap[`needle_${nid}`]) {
            result.push({ from: `syndrome_${s.id}`, to: `needle_${nid}`, label: '推荐针方' })
          }
        })
      }
    })

    // Needle -> Acupoint
    needles.forEach(n => {
      if (n.acupoints) {
        n.acupoints.forEach(ap => {
          if (ap.acupoint_id && entityMap[`acupoint_${ap.acupoint_id}`]) {
            result.push({ from: `needle_${n.id}`, to: `acupoint_${ap.acupoint_id}`, label: '取穴' })
          }
        })
      }
    })

    // Syndrome -> Treatment
    treatments.forEach(t => {
      if (t.related_syndromes) {
        t.related_syndromes.forEach(sid => {
          if (entityMap[`syndrome_${sid}`]) {
            result.push({ from: `syndrome_${sid}`, to: `treatment_${t.id}`, label: '治法' })
          }
        })
      }
    })

    // Syndrome -> ModernMapping
    modernMappings.forEach(mm => {
      if (mm.related_syndrome && entityMap[`syndrome_${mm.related_syndrome}`]) {
        result.push({ from: `syndrome_${mm.related_syndrome}`, to: `modern_${mm.id}`, label: '中西对照' })
      }
    })

    // Acupoint -> Meridian
    acupoints.forEach(a => {
      if (a.meridian_id && entityMap[`meridian_${a.meridian_id}`]) {
        result.push({ from: `acupoint_${a.id}`, to: `meridian_${a.meridian_id}`, label: '归经' })
      }
    })

    // Medicine -> Formula (reverse from formula composition)
    // Already covered by Formula->Medicine edges (bidirectional display)

    return result
  }, [syndromes, formulas, medicines, acupoints, needles, meridians, treatments, modernMappings, entityMap])

  // Get related nodes for focus
  const relatedNodes = useMemo(() => {
    if (!focusEntity || !focusType) return []
    const prefix = `${focusType}_${focusEntity}`
    const related = new Set()

    edges.forEach(edge => {
      if (edge.from === prefix) related.add(edge.to)
      if (edge.to === prefix) related.add(edge.from)
    })

    return Array.from(related)
  }, [focusEntity, focusType, edges])

  const handleEntityClick = (entityId, entityType) => {
    if (focusEntity === entityId && focusType === entityType) {
      setFocusEntity(null)
      setFocusType(null)
    } else {
      setFocusEntity(entityId)
      setFocusType(entityType)
    }
  }

  const handleNavigate = (entityId, entityType) => {
    const routes = {
      syndrome: (id) => navigate(`/syndromes/${id}`),
      formula: (id) => navigate(`/formulas/${id}`),
      medicine: (id) => navigate(`/formulas/medicine/${id}`),
      acupoint: (id) => navigate(`/acupuncture/${id}`),
      needle: (id) => navigate(`/acupuncture/needle/${id}`),
      meridian: (id) => navigate(`/acupuncture?meridian=${id}`),
      treatment: (id) => {
        const t = treatments.find(x => x.id === id)
        const firstSyndrome = t?.related_syndromes?.[0]
        if (firstSyndrome) {
          navigate(`/syndromes/${firstSyndrome}?treatment=${id}`)
        } else {
          navigate('/syndromes')
        }
      },
      modern: (id) => navigate(`/modern-mapping`)
    }
    if (routes[entityType]) routes[entityType](entityId)
  }

  const getViewData = () => {
    const dataMap = {
      syndrome: syndromes.map(s => ({ id: s.id, name: s.name, type: 'syndrome', category: s.classification?.[0] || '未分类' })),
      formula: formulas.map(f => ({ id: f.id, name: f.name, type: 'formula', category: f.category || f.subcategory || '未分类' })),
      medicine: medicines.map(m => ({ id: m.id, name: m.name, type: 'medicine', category: m.category || '未分类' })),
      acupoint: acupoints.map(a => ({ id: a.id, name: a.name, type: 'acupoint', category: a.meridian || '未分类' })),
      needle: needles.map(n => ({ id: n.id, name: n.name, type: 'needle', category: n.category || '未分类' })),
      meridian: meridians.map(m => ({ id: m.id, name: m.name, type: 'meridian', category: m.category || '未分类' })),
      treatment: treatments.map(t => ({ id: t.id, name: t.name, type: 'treatment', category: t.category || '未分类' })),
      modern: modernMappings.map(mm => ({ id: mm.id, name: `${mm.chinese_term}↔${mm.modern_term}`, type: 'modern', category: mm.category || '未分类' }))
    }
    return dataMap[viewMode] || []
  }

  const viewData = useMemo(getViewData, [viewMode, syndromes, formulas, medicines, acupoints, needles, meridians, treatments, modernMappings])

  // Category filters for current view
  const { categories, categoryFilter, setCategoryFilter } = (() => {
    // Dynamic category state per view - defined as top-level state instead
    return {}
  })()

  // Get focus entity details
  const focusDetails = useMemo(() => {
    if (!focusEntity) return null
    const key = `${focusType}_${focusEntity}`
    const entity = entityMap[key]
    if (!entity) return null

    const nodeEdges = edges.filter(e => e.from === key || e.to === key)
    const connections = nodeEdges.map(edge => {
      const targetKey = edge.from === key ? edge.to : edge.from
      const targetEntity = entityMap[targetKey]
      return { ...edge, target: targetEntity }
    })

    return { entity, connections }
  }, [focusEntity, focusType, entityMap, edges])

  // Type list with counts for the category bar
  const typeStats = useMemo(() => [
    { type: 'syndrome', label: '证型', count: syndromes.length },
    { type: 'formula', label: '方剂', count: formulas.length },
    { type: 'medicine', label: '中药', count: medicines.length },
    { type: 'acupoint', label: '穴位', count: acupoints.length },
    { type: 'needle', label: '针方', count: needles.length },
    { type: 'meridian', label: '经络', count: meridians.length },
    { type: 'treatment', label: '治法', count: treatments.length },
    { type: 'modern', label: '中西对照', count: modernMappings.length }
  ], [syndromes, formulas, medicines, acupoints, needles, meridians, treatments, modernMappings])

  // Category extraction for current view
  const viewCategories = useMemo(() => {
    const catSet = new Set()
    viewData.forEach(d => { if (d.category) catSet.add(d.category) })
    return Array.from(catSet).sort()
  }, [viewData])

  // Internal category filter state
  const [innerCatFilter, setInnerCatFilter] = useState('all')
  const displayedData = useMemo(() => {
    if (innerCatFilter === 'all') return viewData
    return viewData.filter(d => d.category === innerCatFilter)
  }, [viewData, innerCatFilter])

  // Reset category filter when view mode changes
  const handleViewModeChange = (mode) => {
    setViewMode(mode)
    setFocusEntity(null)
    setFocusType(null)
    setInnerCatFilter('all')
  }

  return (
    <div>
      {/* Type selector bar */}
      <div className="graph-category-bar">
        {typeStats.map(stat => (
          <div
            key={stat.type}
            className={`graph-category-item ${viewMode === stat.type ? 'active' : ''}`}
            style={{ 
              borderColor: viewMode === stat.type ? NODE_COLORS[stat.type] : 'var(--color-border)',
              color: viewMode === stat.type ? NODE_COLORS[stat.type] : 'var(--color-text-secondary)',
              background: viewMode === stat.type ? `${NODE_COLORS[stat.type]}10` : 'var(--color-surface-warm)'
            }}
            onClick={() => handleViewModeChange(stat.type)}
          >
            <span>{NODE_ICONS[stat.type]}</span>
            <span>{stat.label}</span>
            <span className="category-count">{stat.count}</span>
          </div>
        ))}
      </div>

      {/* Sub-category filter */}
      {viewCategories.length > 0 && (
        <div style={{ marginBottom: '16px' }}>
          <CollapsibleFilter
            label="分类"
            summary={innerCatFilter === 'all' ? `全部分类（${viewData.length}）` : innerCatFilter}
          >
            <div className="tag-filter-bar" style={{ marginBottom: 0 }}>
              <button
                className={`tag-filter-btn ${innerCatFilter === 'all' ? 'active' : ''}`}
                onClick={() => setInnerCatFilter('all')}
                style={innerCatFilter !== 'all' ? { background: 'var(--color-filter-inactive)' } : {}}
              >
                全部分类（{viewData.length}）
              </button>
              {viewCategories.map(cat => (
                <button
                  key={cat}
                  className={`tag-filter-btn ${innerCatFilter === cat ? 'active' : ''}`}
                  onClick={() => setInnerCatFilter(cat)}
                  style={innerCatFilter !== cat ? { background: 'var(--color-filter-inactive)' } : {}}
                >
                  {cat}
                </button>
              ))}
            </div>
          </CollapsibleFilter>
        </div>
      )}

      <div className="graph-container">
        <div className="graph-nodes">
          {displayedData.map(item => {
            const isFocus = focusEntity === item.id && focusType === item.type
            const isRelated = !!focusEntity && relatedNodes.includes(`${item.type}_${item.id}`)
            const isDimmed = !!focusEntity && !isFocus && !isRelated

            return (
              <div
                key={`${item.type}_${item.id}`}
                className={`graph-node ${isFocus ? 'focused' : ''} ${isRelated ? 'related' : ''} ${isDimmed ? 'dimmed' : ''}`}
                style={{ borderColor: NODE_COLORS[item.type] }}
                onClick={() => handleEntityClick(item.id, item.type)}
                onDoubleClick={() => handleNavigate(item.id, item.type)}
              >
                <span className="graph-node-type" style={{ background: NODE_COLORS[item.type] }}>
                  {NODE_LABELS[item.type]}
                </span>
                <span className="graph-node-name">{item.name}</span>
                {item.category && item.category !== '未分类' && (
                  <span className="graph-node-category" style={{ fontSize: '0.7rem', color: 'var(--color-text-hint)', marginTop: '2px' }}>
                    {item.category}
                  </span>
                )}
              </div>
            )
          })}
        </div>

      </div>

      {focusDetails && (
        <div className="graph-detail-panel" ref={detailPanelRef}>
          <h3
            style={{
              color: NODE_COLORS[focusDetails.entity.entityType],
              cursor: 'pointer',
              display: 'inline-flex',
              alignItems: 'center',
              gap: '6px',
              transition: 'opacity 0.15s'
            }}
            onClick={() => handleNavigate(focusDetails.entity.id, focusDetails.entity.entityType)}
            title="点击进入详情"
          >
            {NODE_LABELS[focusDetails.entity.entityType]}：{focusDetails.entity.name}
            <span style={{ fontSize: '0.75rem', opacity: 0.5, fontWeight: 400 }}>↗</span>
          </h3>
          <p className="section-content" style={{ fontSize: '0.9rem', color: 'var(--color-text-hint)' }}>
            {focusDetails.entity.pinyin}
          </p>

          {/* 经络类型补充详情 */}
          {focusDetails.entity.entityType === 'meridian' && (
            <div style={{ marginTop: '12px', padding: '12px', background: 'var(--color-surface-warm)', borderRadius: '10px', fontSize: '0.9rem', color: 'var(--color-text-secondary)', lineHeight: 1.8 }}>
              {focusDetails.entity.category && <div><strong>类别：</strong>{focusDetails.entity.category}{focusDetails.entity.subcategory ? ` · ${focusDetails.entity.subcategory}` : ''}</div>}
              {focusDetails.entity.yin_yang && <div><strong>阴阳：</strong>{focusDetails.entity.yin_yang}</div>}
              {focusDetails.entity.element && <div><strong>五行：</strong>{focusDetails.entity.element}</div>}
              {focusDetails.entity.path && <div style={{ marginTop: '6px' }}><strong>循行路线：</strong>{focusDetails.entity.path}</div>}
              {focusDetails.entity.indications && focusDetails.entity.indications.length > 0 && (
                <div style={{ marginTop: '6px' }}>
                  <strong>主治概要：</strong>
                  <div className="tag-list" style={{ marginTop: '4px' }}>
                    {focusDetails.entity.indications.map((ind, i) => (
                      <span key={i} className="tag-item" style={{ fontSize: '0.82rem' }}>{ind}</span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {focusDetails.connections.length > 0 && (
            <>
              <h4 style={{ marginTop: '16px', marginBottom: '8px' }}>关联实体</h4>
              <div className="graph-connections">
                {focusDetails.connections.map((conn, i) => (
                  <div
                    key={i}
                    className="graph-connection-item"
                    onClick={() => conn.target && handleNavigate(conn.target.id, conn.target.entityType)}
                  >
                    <span className="connection-label">{conn.label}</span>
                    <span className="connection-arrow">→</span>
                    <span className="connection-name">{conn.target?.name || '未知'}</span>
                    <span className="connection-type" style={{ color: NODE_COLORS[conn.target?.entityType] }}>
                      {NODE_LABELS[conn.target?.entityType]}
                    </span>
                  </div>
                ))}
              </div>
            </>
          )}
        </div>
      )}
      {viewData.length === 0 && <EmptyState message="暂无数据" />}
    </div>
  )
}
