import { useState, useEffect, useMemo } from 'react'
import { useNavigate, useParams, useSearchParams } from 'react-router-dom'
import { DataManager } from '../../services/DataManager.js'
import { RelationService } from '../../services/RelationService.js'
import { DATA_TYPES } from '../../services/DataManager.js'
import BookmarkButton from '../common/BookmarkButton.jsx'
import EmptyState from '../common/EmptyState.jsx'

export default function SyndromeModule() {
  const navigate = useNavigate()
  const { syndromeId } = useParams()
  const [searchParams] = useSearchParams()

  const allSyndromes = useMemo(() => DataManager.getAll(DATA_TYPES.SYNDROMES), [])
  const [selectedSyndrome, setSelectedSyndrome] = useState(null)
  const [expandedTreatment, setExpandedTreatment] = useState(null)
  const [classificationFilter, setClassificationFilter] = useState('all')

  // Extract all unique classifications
  const classifications = useMemo(() => {
    const set = new Set()
    allSyndromes.forEach(s => {
      (s.classification || []).forEach(c => set.add(c))
    })
    return ['all', ...Array.from(set).sort()]
  }, [allSyndromes])

  // Filtered syndromes
  const syndromes = useMemo(() => {
    if (classificationFilter === 'all') return allSyndromes
    return allSyndromes.filter(s => 
      (s.classification || []).includes(classificationFilter)
    )
  }, [allSyndromes, classificationFilter])

  // Handle URL params for deep linking
  useEffect(() => {
    if (syndromeId) {
      const found = DataManager.getById(DATA_TYPES.SYNDROMES, syndromeId)
      if (found) {
        const relations = RelationService.getSyndromeRelations(found.id)
        setSelectedSyndrome(relations)
        setExpandedTreatment(null)
        // If there's a ?treatment= or ?effect= param, expand it
        const treatmentId = searchParams.get('treatment')
        const effectId = searchParams.get('effect')
        if (treatmentId && relations.treatments?.some(t => t.id === treatmentId)) {
          setTimeout(() => {
            setExpandedTreatment(treatmentId)
            document.getElementById(`treatment-${treatmentId}`)?.scrollIntoView({ behavior: 'smooth', block: 'center' })
          }, 300)
        }
        if (effectId) {
          setTimeout(() => {
            document.getElementById(`effect-${effectId}`)?.scrollIntoView({ behavior: 'smooth', block: 'center' })
          }, 300)
        }
      }
    } else {
      setSelectedSyndrome(null)
      // Handle treatment/effect deep link when no syndrome is selected
      const treatmentId = searchParams.get('treatment')
      const effectId = searchParams.get('effect')
      if (treatmentId || effectId) {
        // Find the first syndrome that has this treatment/effect
        const syndromes = allSyndromes
        for (const s of syndromes) {
          const relations = RelationService.getSyndromeRelations(s.id)
          if (treatmentId && relations.treatments?.some(t => t.id === treatmentId)) {
            navigate(`/syndromes/${s.id}?treatment=${treatmentId}`, { replace: true })
            return
          }
          if (effectId && relations.effects?.some(e => e.id === effectId)) {
            navigate(`/syndromes/${s.id}?effect=${effectId}`, { replace: true })
            return
          }
        }
      }
    }
  }, [syndromeId, searchParams, allSyndromes, navigate])

  const handleSelectSyndrome = (syndrome) => {
    navigate(`/syndromes/${syndrome.id}`)
  }

  const handleBack = () => {
    if (window.history.length > 1) {
      navigate(-1)
    } else {
      navigate('/syndromes')
    }
  }

  const handleSearchClick = (term) => {
    navigate(`/search?q=${encodeURIComponent(term)}`)
  }

  // Resolve treatment related items
  const resolveTreatmentLinks = (treatment) => {
    const result = { formulas: [], needles: [] }
    if (treatment.related_formulas) {
      result.formulas = treatment.related_formulas
        .map(id => DataManager.getById(DATA_TYPES.FORMULAS, id))
        .filter(Boolean)
    }
    if (treatment.related_needle) {
      result.needles = treatment.related_needle
        .map(id => DataManager.getById(DATA_TYPES.NEEDLE_PRESCRIPTIONS, id))
        .filter(Boolean)
    }
    return result
  }

  if (selectedSyndrome) {
    const { syndrome, formulas, needles, treatments, effects, modernMapping } = selectedSyndrome

    return (
      <div className="detail-container">
        <button className="back-button" onClick={handleBack}>← 返回</button>

        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
          <div className="detail-header" style={{ flex: 1 }}>
            <h1 className="detail-title">{syndrome.name}</h1>
            <p className="detail-pinyin">{syndrome.pinyin}</p>
            <div className="detail-category">
              {syndrome.category?.map((cat, i) => (
                <span key={i} className="category-tag">{cat}</span>
              ))}
              {syndrome.classification?.map((classif, i) => (
                <span key={i} className="category-tag">{classif}</span>
              ))}
            </div>
          </div>
          <BookmarkButton item={syndrome} type="syndrome" />
        </div>

        <div className="section">
          <h2 className="section-title">辨证要点</h2>
          <div className="tag-list">
            {syndrome.diagnosis_points?.map((point, i) => (
              <span key={i} className="tag-item clickable-tag" onClick={() => handleSearchClick(point)}>{point}</span>
            ))}
            {(!syndrome.diagnosis_points || syndrome.diagnosis_points.length === 0) && (
              <span className="section-content" style={{ color: 'var(--color-text-hint)' }}>暂无数据</span>
            )}
          </div>
        </div>

        {syndrome.pathogenesis && (
          <div className="section">
            <h2 className="section-title">病机分析</h2>
            <p className="section-content">{syndrome.pathogenesis}</p>
          </div>
        )}

        {syndrome.etiology && (
          <div className="section">
            <h2 className="section-title">病因</h2>
            <p className="section-content">{syndrome.etiology}</p>
          </div>
        )}

        {syndrome.indications && syndrome.indications.length > 0 && (
          <div className="section">
            <h2 className="section-title">临床表现</h2>
            <div className="tag-list">
              {syndrome.indications.map((ind, i) => (
                <span key={i} className="tag-item clickable-tag" onClick={() => handleSearchClick(ind)}>{ind}</span>
              ))}
            </div>
          </div>
        )}

        {formulas && formulas.length > 0 && (
          <div className="section">
            <h2 className="section-title">推荐方剂</h2>
            <div className="list-container">
              {formulas.map(formula => (
                <div key={formula.id} className="list-item" onClick={() => navigate(`/formulas/${formula.id}`)}>
                  <div className="list-item-title">{formula.name}</div>
                  <div className="list-item-pinyin">{formula.pinyin}</div>
                  <div className="list-item-desc">{formula.effects?.join('、')}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {needles && needles.length > 0 && (
          <div className="section">
            <h2 className="section-title">推荐针方</h2>
            <div className="list-container">
              {needles.map(needle => (
                <div key={needle.id} className="list-item" onClick={() => navigate(`/acupuncture/needle/${needle.id}`)}>
                  <div className="list-item-title">{needle.name}</div>
                  <div className="list-item-desc">{needle.effects?.join('、')}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {treatments && treatments.length > 0 && (
          <div className="section">
            <h2 className="section-title">治疗方法</h2>
            <div className="list-container">
              {treatments.map(treatment => {
                const links = resolveTreatmentLinks(treatment)
                const hasLinks = links.formulas.length > 0 || links.needles.length > 0
                const isExpanded = expandedTreatment === treatment.id

                return (
                  <div key={treatment.id} id={`treatment-${treatment.id}`} className="card treatment-card">
                    <div className="card-title" style={{ cursor: hasLinks ? 'pointer' : 'default' }}
                      onClick={() => hasLinks && setExpandedTreatment(isExpanded ? null : treatment.id)}>
                      <span>{treatment.name}</span>
                      {hasLinks && <span className="expand-icon">{isExpanded ? '▲' : '▼'}</span>}
                    </div>
                    <div className="section-content"><strong>治疗原则：</strong>{treatment.principle}</div>
                    <div className="section-content"><strong>适应症：</strong>{treatment.indications?.join('、')}</div>
                    <div className="section-content"><strong>方法：</strong>{treatment.methods?.join('；')}</div>
                    {isExpanded && hasLinks && (
                      <div className="treatment-links">
                        {links.formulas.length > 0 && (
                          <div style={{ marginTop: '8px' }}>
                            <strong>关联方剂：</strong>
                            <div className="tag-list" style={{ marginTop: '6px' }}>
                              {links.formulas.map(f => (
                                <span key={f.id} className="tag-item clickable-tag"
                                  onClick={(e) => { e.stopPropagation(); navigate(`/formulas/${f.id}`) }}>
                                  {f.name}
                                </span>
                              ))}
                            </div>
                          </div>
                        )}
                        {links.needles.length > 0 && (
                          <div style={{ marginTop: '8px' }}>
                            <strong>关联针方：</strong>
                            <div className="tag-list" style={{ marginTop: '6px' }}>
                              {links.needles.map(n => (
                                <span key={n.id} className="tag-item clickable-tag"
                                  onClick={(e) => { e.stopPropagation(); navigate(`/acupuncture/needle/${n.id}`) }}>
                                  {n.name}
                                </span>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                )
              })}
            </div>
          </div>
        )}

        {effects && effects.length > 0 && (
          <div className="section">
            <h2 className="section-title">功效</h2>
            <div className="tag-list">
              {effects.map(effect => (
                <span key={effect.id} id={`effect-${effect.id}`} className="tag-item primary clickable-tag"
                  onClick={() => handleSearchClick(effect.name)}>{effect.name}</span>
              ))}
            </div>
          </div>
        )}

        {/* Structured Comparison Table */}
        {syndrome.comparison && syndrome.comparison.length > 0 && (
          <div className="section">
            <h2 className="section-title mapping-title">中西对照</h2>
            <div className="comparison-table-wrapper">
              <table className="comparison-table">
                <thead>
                  <tr>
                    <th className="comparison-aspect-col">对比维度</th>
                    <th className="comparison-tcm-col"><span className="comparison-col-label">🀄 中医</span></th>
                    <th className="comparison-western-col"><span className="comparison-col-label">🏥 西医</span></th>
                  </tr>
                </thead>
                <tbody>
                  {syndrome.comparison.map((row, idx) => (
                    <tr key={idx}>
                      <td className="comparison-aspect">{row.aspect}</td>
                      <td className="comparison-tcm">{row.tcm}</td>
                      <td className="comparison-western">{row.western}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Modern medicine diseases */}
        {syndrome.modern_medicine && syndrome.modern_medicine.length > 0 && (
          <div className="section">
            <h2 className="section-title">现代医学对应疾病</h2>
            <div className="tag-list">
              {syndrome.modern_medicine.map((disease, i) => (
                <span key={i} className="tag-item warning clickable-tag" onClick={() => handleSearchClick(disease)}>{disease}</span>
              ))}
            </div>
          </div>
        )}

        {/* ModernMapping links (from modern_mapping.json) */}
        {modernMapping && modernMapping.length > 0 && (
          <div className="section">
            <h2 className="section-title mapping-title">相关中西对照</h2>
            <div className="list-container">
              {modernMapping.map(mapping => (
                <div key={mapping.id} className="list-item" onClick={() => navigate(`/modern-mapping?id=${mapping.id}`)}>
                  <div className="list-item-title">
                    {mapping.chinese_term} ↔ {mapping.modern_term}
                  </div>
                  <div className="list-item-pinyin">{mapping.category}</div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    )
  }

  return (
    <div>
      {/* Classification filter */}
      <div className="tag-filter-bar" style={{ marginBottom: '16px' }}>
        {classifications.map(cat => (
          <button
            key={cat}
            className={`tag-filter-btn ${classificationFilter === cat ? 'active' : ''}`}
            onClick={() => setClassificationFilter(cat)}
          >
            {cat === 'all' ? `全部分类（${allSyndromes.length}）` : cat}
          </button>
        ))}
      </div>

      {syndromes.length === 0 ? (
        <EmptyState message="未找到匹配的证型" icon="🔍" />
      ) : (
        <div className="list-container">
          {syndromes.map(syndrome => (
            <div
              key={syndrome.id}
              className="list-item"
              onClick={() => handleSelectSyndrome(syndrome)}
            >
              <div className="list-item-title">
                {syndrome.name}
                {syndrome.category && syndrome.category.length > 0 && (
                  <span style={{ fontSize: '0.85rem', color: 'var(--color-primary)', marginLeft: '8px', fontWeight: 'normal' }}>
                    {syndrome.category.slice(0, 2).join('·')}
                  </span>
                )}
              </div>
              <div className="list-item-pinyin">{syndrome.pinyin}</div>
              <div className="list-item-desc">
                {syndrome.pathogenesis?.substring(0, 80)}{syndrome.pathogenesis && syndrome.pathogenesis.length > 80 ? '...' : ''}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
