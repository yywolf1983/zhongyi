import { useState, useEffect, useMemo } from 'react'
import { useNavigate, useParams, useSearchParams } from 'react-router-dom'
import { DataManager } from '../../services/DataManager.js'
import { RelationService } from '../../services/RelationService.js'
import { DATA_TYPES } from '../../services/DataManager.js'
import BookmarkButton from '../common/BookmarkButton.jsx'
import EmptyState from '../common/EmptyState.jsx'
import ClassicExcerpts from '../common/ClassicExcerpts.jsx'
import ComparisonItems from '../common/ComparisonItems.jsx'
import GroupedList from '../common/GroupedList.jsx'
import { useAppContext } from '../../context/AppContext.jsx'

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

export default function SyndromeModule() {
  const navigate = useNavigate()
  const { syndromeId } = useParams()
  const [searchParams] = useSearchParams()
  const { addRecent } = useAppContext()

  const allSyndromes = useMemo(() => DataManager.getAll(DATA_TYPES.SYNDROMES), [])
  const [selectedSyndrome, setSelectedSyndrome] = useState(null)
  const [expandedTreatment, setExpandedTreatment] = useState(null)
  // 八纲(大类) + 辨证方法(子类) 两级筛选，列表按辨证方法扁平分组（与方剂/针灸同款）
  const [syndromeCatFilter, setSyndromeCatFilter] = useState('all')
  const [syndromeCatOpen, setSyndromeCatOpen] = useState(false)
  const [syndromeSubFilter, setSyndromeSubFilter] = useState('all')
  const [syndromeSubOpen, setSyndromeSubOpen] = useState(false)

  // 八纲大类选项 + 数量
  const syndromeCatOpts = useMemo(() => {
    const m = {}
    allSyndromes.forEach(s => {
      (s.classification || []).forEach(c => { if (c) m[c] = (m[c] || 0) + 1 })
    })
    const entries = Object.entries(m).sort((a, b) => b[1] - a[1])
    return [
      { value: 'all', label: '全部八纲', count: allSyndromes.length },
      ...entries.map(([k, v]) => ({ value: k, label: k, count: v })),
    ]
  }, [allSyndromes])

  // 辨证方法子类选项（随大类联动）
  const syndromeSubOpts = useMemo(() => {
    const base = syndromeCatFilter === 'all'
      ? allSyndromes
      : allSyndromes.filter(s => (s.classification || []).includes(syndromeCatFilter))
    const m = {}
    base.forEach(s => {
      (s.category || []).forEach(c => { if (c) m[c] = (m[c] || 0) + 1 })
    })
    const entries = Object.entries(m).sort((a, b) => b[1] - a[1])
    return [
      { value: 'all', label: '全部辨证方法', count: base.length },
      ...entries.map(([k, v]) => ({ value: k, label: k, count: v })),
    ]
  }, [allSyndromes, syndromeCatFilter])

  // 筛选后证型
  const syndromes = useMemo(() => {
    let list = allSyndromes
    if (syndromeCatFilter !== 'all') {
      list = list.filter(s => (s.classification || []).includes(syndromeCatFilter))
    }
    if (syndromeSubFilter !== 'all') {
      list = list.filter(s => (s.category || []).includes(syndromeSubFilter))
    }
    return list
  }, [allSyndromes, syndromeCatFilter, syndromeSubFilter])

  // Handle URL params for deep linking
  useEffect(() => {
    if (syndromeId) {
      const found = DataManager.getById(DATA_TYPES.SYNDROMES, syndromeId)
      if (found) {
        const relations = RelationService.getSyndromeRelations(found.id)
        setSelectedSyndrome(relations)
        setExpandedTreatment(null)
        addRecent({ type: 'syndrome', id: found.id, name: found.name, sub: found.category?.[0], navPath: `/syndromes/${found.id}` })
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
      navigate('/')
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
    const { syndrome, formulas, needles, treatments, modernMapping } = selectedSyndrome

    const anchorSections = [
      { id: 'sec-diagnosis', label: '辨证', show: syndrome.diagnosis_points?.length },
      { id: 'sec-pathogenesis', label: '病机', show: syndrome.pathogenesis },
      { id: 'sec-etiology', label: '病因', show: syndrome.etiology },
      { id: 'sec-indications', label: '表现', show: syndrome.indications?.length },
      { id: 'sec-formulas', label: '方剂', show: formulas?.length },
      { id: 'sec-needles', label: '针方', show: needles?.length },
      { id: 'sec-treatments', label: '治法', show: treatments?.length },
      { id: 'sec-comparison', label: '对照', show: syndrome.comparison?.length },
      { id: 'sec-modern', label: '西医', show: syndrome.modern_medicine?.length },
      { id: 'sec-mapping', label: '中西', show: modernMapping?.length }
    ].filter(s => s.show)

    return (
      <div className="detail-container">
        <div className="detail-header-row">
          <div className="detail-header">
            <h1 className="detail-title">{syndrome.name}</h1>
            <p className="detail-pinyin">{syndrome.pinyin}</p>
            <div className="detail-category">
              {syndrome.category?.length > 0 && syndrome.category.map((cat, i) => (
                <span key={i} className="category-tag">{cat}</span>
              ))}
            </div>
            {syndrome.classification?.length > 0 && (
              <div className="detail-meta-row">
                <span className="detail-meta-label">八纲</span>
                <div className="tag-list">
                  {syndrome.classification.map(c => (
                    <span key={c}
                      className={`tag-item ${(c === '阴证' || c === '阳证' || c === '阴阳错杂') ? 'primary' : ''}`}>
                      {c}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
          <BookmarkButton item={syndrome} type="syndrome" />
        </div>

        {anchorSections.length > 1 && (
          <nav className="detail-anchors">
            {anchorSections.map(a => (
              <button
                key={a.id}
                className="detail-anchor-chip"
                onClick={() => document.getElementById(a.id)?.scrollIntoView({ behavior: 'smooth', block: 'start' })}
              >{a.label}</button>
            ))}
          </nav>
        )}

        <div className="section" id="sec-diagnosis">
          <h2 className="section-title">辨证要点</h2>
          <div className="tag-list">
            {syndrome.diagnosis_points?.map((point, i) => (
              <span key={i} className="tag-item clickable-tag" onClick={() => handleSearchClick(point)}>{point}</span>
            ))}
            {(!syndrome.diagnosis_points || syndrome.diagnosis_points.length === 0) && (
              <span className="section-content empty-hint">暂无数据</span>
            )}
          </div>
        </div>

        <ClassicExcerpts excerpts={syndrome.classic_excerpts} />

        {syndrome.pathogenesis && (
          <div className="section" id="sec-pathogenesis">
            <h2 className="section-title">病机分析</h2>
            <p className="section-content">{syndrome.pathogenesis}</p>
          </div>
        )}

        {syndrome.etiology && (
          <div className="section" id="sec-etiology">
            <h2 className="section-title">病因</h2>
            <p className="section-content">{syndrome.etiology}</p>
          </div>
        )}

        {syndrome.indications && syndrome.indications.length > 0 && (
          <div className="section" id="sec-indications">
            <h2 className="section-title">临床表现</h2>
            <div className="tag-list">
              {syndrome.indications.map((ind, i) => (
                <span key={i} className="tag-item clickable-tag" onClick={() => handleSearchClick(ind)}>{ind}</span>
              ))}
            </div>
          </div>
        )}

        {formulas && formulas.length > 0 && (
          <div className="section" id="sec-formulas">
            <h2 className="section-title">推荐方剂</h2>
            <div className="list-container">
              {formulas.map(formula => (
                <div key={formula.id} className="list-item formula" onClick={() => navigate(`/formulas/${formula.id}`)}>
                  <div className="list-item-title">{formula.name}</div>
                  <div className="list-item-pinyin">{formula.pinyin}</div>
                  <div className="list-item-desc">{formula.effects?.join('、')}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {needles && needles.length > 0 && (
          <div className="section" id="sec-needles">
            <h2 className="section-title">推荐针方</h2>
            <div className="list-container">
              {needles.map(needle => (
                <div key={needle.id} className="list-item needle" onClick={() => navigate(`/acupuncture/needle/${needle.id}`)}>
                  <div className="list-item-title">{needle.name}</div>
                  <div className="list-item-desc">{needle.effects?.join('、')}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {treatments && treatments.length > 0 && (
          <div className="section" id="sec-treatments">
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
                    <ClassicExcerpts excerpts={treatment.classic_excerpts} />
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

        {/* Structured Comparison items */}
        {syndrome.comparison && syndrome.comparison.length > 0 && (
          <div className="section" id="sec-comparison">
            <h2 className="section-title mapping-title">中西对照</h2>
            <ComparisonItems comparison={syndrome.comparison} />
          </div>
        )}

        {/* Modern medicine diseases */}
        {syndrome.modern_medicine && syndrome.modern_medicine.length > 0 && (
          <div className="section secondary" id="sec-modern">
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
          <div className="section" id="sec-mapping">
            <h2 className="section-title mapping-title">相关中西对照</h2>
            <div className="list-container">
              {modernMapping.map(mapping => (
                <div key={mapping.id} className="list-item mapping" onClick={() => navigate(`/modern-mapping?id=${mapping.id}`)}>
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
      <div className="module-page-header">
        <span className="module-page-icon">🩺</span>
        <div className="module-page-text">
          <span className="module-page-title">中医辨证</span>
          <span className="module-page-sub">八纲辨证 · 审证求因</span>
        </div>
        <span className="module-page-count">共 {allSyndromes.length} 证</span>
      </div>
      {/* 八纲(大类) + 辨证方法(子类) 两级筛选，与方剂/针灸同款 */}
      <div className="cat-filter">
        <button
          type="button"
          className="cat-filter-toggle"
          onClick={() => setSyndromeCatOpen(o => !o)}
        >
          <span className="cat-filter-title">八纲</span>
          <span className="cat-filter-summary">
            {syndromeCatFilter === 'all' ? '全部八纲' : syndromeCatFilter}
          </span>
          <span className={`cat-filter-caret ${syndromeCatOpen ? 'open' : ''}`}>▾</span>
        </button>
        {syndromeCatOpen && (
          <CatRow
            options={syndromeCatOpts}
            active={syndromeCatFilter}
            onSelect={(v) => { setSyndromeCatFilter(v); setSyndromeSubFilter('all'); setSyndromeCatOpen(false) }}
          />
        )}
      </div>

      <div className="cat-filter">
        <button
          type="button"
          className="cat-filter-toggle"
          onClick={() => setSyndromeSubOpen(o => !o)}
        >
          <span className="cat-filter-title">辨证方法</span>
          <span className="cat-filter-summary">
            {syndromeSubFilter === 'all' ? '全部辨证方法' : syndromeSubFilter}
          </span>
          <span className={`cat-filter-caret ${syndromeSubOpen ? 'open' : ''}`}>▾</span>
        </button>
        {syndromeSubOpen && (
          <CatRow
            options={syndromeSubOpts}
            active={syndromeSubFilter}
            onSelect={(v) => { setSyndromeSubFilter(v); setSyndromeSubOpen(false) }}
          />
        )}
      </div>

      <GroupedList
        items={syndromes}
        getGroup={(s) => s.category?.[0] || s.classification?.[0] || '其他'}
        getKey={(s) => s.id}
        emptyMessage="未找到匹配的证型"
        renderItem={(syndrome) => (
          <div
            key={syndrome.id}
            className="list-item syndrome"
            onClick={() => handleSelectSyndrome(syndrome)}
          >
            <div className="list-item-title">
              {syndrome.name}
              {syndrome.category && syndrome.category.length > 0 && (
                <span className="list-item-cat">{syndrome.category.slice(0, 2).join('·')}</span>
              )}
            </div>
            <div className="list-item-pinyin">{syndrome.pinyin}</div>
            {syndrome.classification && syndrome.classification.length > 0 && (
              <div className="tag-list list-item-tags">
                {syndrome.classification.map((c) => (
                  <span
                    key={c}
                    className={`tag-item ${(c === '阴证' || c === '阳证' || c === '阴阳错杂') ? 'primary' : ''}`}
                  >{c}</span>
                ))}
              </div>
            )}
            <div className="list-item-desc">
              {syndrome.pathogenesis?.substring(0, 80)}{syndrome.pathogenesis && syndrome.pathogenesis.length > 80 ? '...' : ''}
            </div>
          </div>
        )}
      />
    </div>
  )
}
