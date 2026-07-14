import { useState, useEffect } from 'react'
import { useNavigate, useParams, useSearchParams } from 'react-router-dom'
import { DataManager } from '../../services/DataManager.js'
import { RelationService } from '../../services/RelationService.js'
import { DATA_TYPES } from '../../services/DataManager.js'
import BookmarkButton from '../common/BookmarkButton.jsx'
import EmptyState from '../common/EmptyState.jsx'

export default function AcupunctureModule() {
  const navigate = useNavigate()
  const { acupointId, needleId } = useParams()
  const [searchParams] = useSearchParams()

  const [acupoints, setAcupoints] = useState(() => DataManager.getAll(DATA_TYPES.ACUPOINTS))
  const [needles, setNeedles] = useState(() => DataManager.getAll(DATA_TYPES.NEEDLE_PRESCRIPTIONS))
  const [selectedAcupoint, setSelectedAcupoint] = useState(null)
  const [selectedNeedle, setSelectedNeedle] = useState(null)
  const [viewMode, setViewMode] = useState('acupoints')
  const [expandedMeridian, setExpandedMeridian] = useState(false)

  // Category filter states
  const [acupointMeridianFilter, setAcupointMeridianFilter] = useState('all')
  const [needleCategoryFilter, setNeedleCategoryFilter] = useState('all')
  const [meridianCategoryFilter, setMeridianCategoryFilter] = useState('all')

  // Handle URL deep linking
  useEffect(() => {
    if (acupointId) {
      const found = DataManager.getById(DATA_TYPES.ACUPOINTS, acupointId)
      if (found) {
        const relations = RelationService.getAcupointRelations(found.id)
        setSelectedAcupoint(relations)
        setSelectedNeedle(null)
        setExpandedMeridian(false)
      }
    } else if (needleId) {
      const found = DataManager.getById(DATA_TYPES.NEEDLE_PRESCRIPTIONS, needleId)
      if (found) {
        const relations = RelationService.getNeedleRelations(found.id)
        setSelectedNeedle(relations)
        setSelectedAcupoint(null)
      }
    } else {
      setSelectedAcupoint(null)
      setSelectedNeedle(null)
      setExpandedMeridian(false)
      setAcupoints(DataManager.getAll(DATA_TYPES.ACUPOINTS))
      setNeedles(DataManager.getAll(DATA_TYPES.NEEDLE_PRESCRIPTIONS))
      // Handle ?meridian= param for deep linking
      const meridianId = searchParams.get('meridian')
      if (meridianId) {
        const meridian = DataManager.getById(DATA_TYPES.MERIDIANS, meridianId)
        if (meridian) {
          setViewMode('meridians')
          setMeridianCategoryFilter('all')
          // Scroll to meridian after render
          setTimeout(() => {
            const el = document.getElementById(`meridian-${meridianId}`)
            el?.scrollIntoView({ behavior: 'smooth', block: 'center' })
          }, 300)
        }
      }
    }
  }, [acupointId, needleId, searchParams])

  const handleSelectAcupoint = (acupoint) => {
    navigate(`/acupuncture/${acupoint.id}`)
  }

  const handleSelectNeedle = (needle) => {
    navigate(`/acupuncture/needle/${needle.id}`)
  }

  const handleBack = () => {
    if (window.history.length > 1) {
      navigate(-1)
    } else {
      navigate('/acupuncture')
    }
  }

  const handleSearchClick = (term) => {
    navigate(`/search?q=${encodeURIComponent(term)}`)
  }

  const handleViewModeChange = (mode) => {
    setViewMode(mode)
    setSelectedAcupoint(null)
    setSelectedNeedle(null)
    setExpandedMeridian(false)
    if (mode === 'acupoints') {
      setAcupoints(DataManager.getAll(DATA_TYPES.ACUPOINTS))
      setAcupointMeridianFilter('all')
    } else if (mode === 'needles') {
      setNeedles(DataManager.getAll(DATA_TYPES.NEEDLE_PRESCRIPTIONS))
      setNeedleCategoryFilter('all')
    } else if (mode === 'meridians') {
      setMeridianCategoryFilter('all')
    }
  }

  // Get acupoints on same meridian
  const getMeridianAcupoints = (meridianId) => {
    return DataManager.getAll(DATA_TYPES.ACUPOINTS)
      .filter(a => a.meridian_id === meridianId)
      .sort((a, b) => (a.sort_order || 0) - (b.sort_order || 0))
  }

  // ============ Acupoint Detail ============
  if (selectedAcupoint) {
    const { acupoint, meridian, needles: relatedNeedles, syndromes, modernMapping } = selectedAcupoint
    const meridianAcupoints = meridian ? getMeridianAcupoints(meridian.id) : []

    return (
      <div className="detail-container">
        <button className="back-button" onClick={handleBack}>← 返回</button>

        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
          <div className="detail-header" style={{ flex: 1 }}>
            <h1 className="detail-title">{acupoint.name}</h1>
            <p className="detail-pinyin">{acupoint.pinyin} ({acupoint.code})</p>
            <div className="detail-category">
              <span className="category-tag">{acupoint.meridian}</span>
            </div>
          </div>
          <BookmarkButton item={acupoint} type="acupoint" />
        </div>

        <div className="section">
          <h2 className="section-title">位置描述</h2>
          <div className="acupoint-location">{acupoint.location}</div>
          {acupoint.location_method && (
            <div className="section-content"><strong>取穴方法：</strong>{acupoint.location_method}</div>
          )}
        </div>

        {acupoint.anatomy && (
          <div className="section">
            <h2 className="section-title">解剖位置</h2>
            <p className="section-content">{acupoint.anatomy}</p>
          </div>
        )}

        <div className="section">
          <h2 className="section-title">主治病症</h2>
          <div className="tag-list">
            {acupoint.indications?.map((indication, i) => (
              <span key={i} className="tag-item clickable-tag" onClick={() => handleSearchClick(indication)}>{indication}</span>
            ))}
            {(!acupoint.indications || acupoint.indications.length === 0) && (
              <span className="section-content" style={{ color: '#999' }}>暂无数据</span>
            )}
          </div>
        </div>

        {(acupoint.methods || acupoint.method) && (
          <div className="section">
            <h2 className="section-title">针灸方法</h2>
            {Array.isArray(acupoint.methods || acupoint.method) ? (
              <div className="tag-list">
                {(acupoint.methods || acupoint.method).map((method, i) => (
                  <span key={i} className="tag-item primary">{method}</span>
                ))}
              </div>
            ) : (
              <p className="section-content">{acupoint.method || acupoint.methods}</p>
            )}
          </div>
        )}

        {meridian && (
          <div className="section">
            <h2 className="section-title">所属经络</h2>
            <div className="card meridian-card">
              <div className="card-title"
                style={{ cursor: meridianAcupoints.length > 0 ? 'pointer' : 'default' }}
                onClick={() => meridianAcupoints.length > 0 && setExpandedMeridian(!expandedMeridian)}>
                <span>{meridian.name}</span>
                {meridianAcupoints.length > 0 && (
                  <span className="expand-icon">{expandedMeridian ? '▲' : '▼'}</span>
                )}
              </div>
              <div className="section-content"><strong>类别：</strong>{meridian.category}</div>
              <div className="section-content"><strong>阴阳：</strong>{meridian.yin_yang}</div>
              {meridian.element && <div className="section-content"><strong>五行：</strong>{meridian.element}</div>}
              <div className="section-content"><strong>主治概要：</strong>{meridian.indications?.join('、')}</div>
              <div className="section-content" style={{ marginTop: '8px', fontSize: '0.88rem', color: '#8a8276' }}>
                本经共 {meridianAcupoints.length} 穴
              </div>

              {expandedMeridian && meridianAcupoints.length > 0 && (
                <div className="meridian-acupoints" style={{ marginTop: '12px', borderTop: '1px solid var(--color-divider)', paddingTop: '10px' }}>
                  <div style={{ fontSize: '0.88rem', color: '#6b5f52', marginBottom: '8px', fontWeight: 500 }}>
                    {meridian.name}全部穴位（点击跳转）：
                  </div>
                  <div className="tag-list">
                    {meridianAcupoints.map(ap => (
                      <span key={ap.id} className="tag-item clickable-tag"
                        style={{ background: ap.id === acupoint.id ? '#e8f5f0' : '#f5efe6',
                                 color: ap.id === acupoint.id ? '#2e7d6b' : '#5c5246',
                                 fontWeight: ap.id === acupoint.id ? 600 : 400 }}
                        onClick={() => navigate(`/acupuncture/${ap.id}`)}>
                        {ap.name}
                        <span style={{ fontSize: '0.78rem', marginLeft: '4px', opacity: 0.7 }}>{ap.code}</span>
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {relatedNeedles && relatedNeedles.length > 0 && (
          <div className="section">
            <h2 className="section-title">关联针方</h2>
            <div className="list-container">
              {relatedNeedles.map(needle => (
                <div key={needle.id} className="list-item" onClick={() => handleSelectNeedle(needle)}>
                  <div className="list-item-title">{needle.name}</div>
                  <div className="list-item-desc">{needle.effects?.join('、')}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {syndromes && syndromes.length > 0 && (
          <div className="section">
            <h2 className="section-title">适用证型</h2>
            <div className="tag-list">
              {syndromes.map(syndrome => (
                <span key={syndrome.id} className="tag-item clickable-tag"
                  onClick={() => navigate(`/syndromes/${syndrome.id}`)}>{syndrome.name}</span>
              ))}
            </div>
          </div>
        )}

        {modernMapping && modernMapping.length > 0 && (
          <div className="section">
            <h2 className="section-title mapping-title">中西对照</h2>
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

        {acupoint.modern_anatomy && (
          <div className="section">
            <h2 className="section-title">现代解剖</h2>
            <p className="acupoint-anatomy">{acupoint.modern_anatomy}</p>
          </div>
        )}

        {acupoint.modern_applications && acupoint.modern_applications.length > 0 && (
          <div className="section">
            <h2 className="section-title">现代应用领域</h2>
            <div className="tag-list">
              {acupoint.modern_applications.map((app, i) => (
                <span key={i} className="tag-item warning clickable-tag" onClick={() => handleSearchClick(app)}>{app}</span>
              ))}
            </div>
          </div>
        )}
      </div>
    )
  }

  // ============ Needle Detail ============
  if (selectedNeedle) {
    const { needle, acupoints: needleAcupoints, syndromes } = selectedNeedle

    return (
      <div className="detail-container">
        <button className="back-button" onClick={handleBack}>← 返回</button>

        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
          <div className="detail-header" style={{ flex: 1 }}>
            <h1 className="detail-title">{needle.name}</h1>
            <div className="detail-category">
              <span className="category-tag">{needle.category}</span>
              {needle.source && (
                <span className="category-tag" style={{ background: '#faf3e0', color: '#a88a4a', marginLeft: '6px' }}>
                  {needle.source}
                </span>
              )}
            </div>
          </div>
          <BookmarkButton item={needle} type="needle" />
        </div>

        {needle.effects && needle.effects.length > 0 && (
          <div className="section">
            <h2 className="section-title">功效</h2>
            <div className="tag-list">
              {needle.effects.map((effect, i) => (
                <span key={i} className="tag-item primary clickable-tag" onClick={() => handleSearchClick(effect)}>{effect}</span>
              ))}
            </div>
          </div>
        )}

        {needle.indications && needle.indications.length > 0 && (
          <div className="section">
            <h2 className="section-title">适应症</h2>
            <div className="tag-list">
              {needle.indications.map((indication, i) => (
                <span key={i} className="tag-item clickable-tag" onClick={() => handleSearchClick(indication)}>{indication}</span>
              ))}
            </div>
          </div>
        )}

        {needleAcupoints && needleAcupoints.length > 0 && (
          <div className="section">
            <h2 className="section-title">穴位组成</h2>
            <div className="table-wrapper">
              <table className="composition-table">
                <thead>
                  <tr>
                    <th>穴位</th>
                    <th>归经</th>
                    <th>操作方法</th>
                  </tr>
                </thead>
                <tbody>
                  {needleAcupoints.map(acupoint => (
                    <tr key={acupoint.id} onClick={() => handleSelectAcupoint(acupoint)} style={{ cursor: 'pointer' }}>
                      <td><strong>{acupoint.name}</strong> ({acupoint.code})</td>
                      <td>{acupoint.meridian}</td>
                      <td><span className="tag-item">{acupoint.method}</span></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {syndromes && syndromes.length > 0 && (
          <div className="section">
            <h2 className="section-title">适用证型</h2>
            <div className="tag-list">
              {syndromes.map(syndrome => (
                <span key={syndrome.id} className="tag-item clickable-tag"
                  onClick={() => navigate(`/syndromes/${syndrome.id}`)}>{syndrome.name}</span>
              ))}
            </div>
          </div>
        )}

        {needle.modern_applications && needle.modern_applications.length > 0 && (
          <div className="section">
            <h2 className="section-title">现代应用</h2>
            <div className="tag-list">
              {needle.modern_applications.map((app, i) => (
                <span key={i} className="tag-item warning clickable-tag" onClick={() => handleSearchClick(app)}>{app}</span>
              ))}
            </div>
          </div>
        )}
      </div>
    )
  }

  // ============ List Views ============
  // Acupoint meridian filter options
  const meridianOptions = (() => {
    const all = DataManager.getAll(DATA_TYPES.ACUPOINTS)
    const meridians = new Set()
    all.forEach(a => { if (a.meridian) meridians.add(a.meridian) })
    return ['all', ...Array.from(meridians).sort()]
  })()

  const filteredAcupoints = (() => {
    if (acupointMeridianFilter === 'all') return acupoints
    return acupoints.filter(a => a.meridian === acupointMeridianFilter)
  })()

  // Needle category filter options
  const needleCategoryOptions = (() => {
    const all = DataManager.getAll(DATA_TYPES.NEEDLE_PRESCRIPTIONS)
    const cats = new Set()
    all.forEach(n => { if (n.category) cats.add(n.category) })
    return ['all', ...Array.from(cats).sort()]
  })()

  const filteredNeedles = (() => {
    if (needleCategoryFilter === 'all') return needles
    return needles.filter(n => n.category === needleCategoryFilter)
  })()

  // Meridian filter options
  const meridianCategoryOptions = ['all', '十二正经', '奇经八脉', '经外奇穴']

  const allMeridians = (() => {
    const meridians = DataManager.getAll(DATA_TYPES.MERIDIANS)
    if (meridianCategoryFilter === 'all') return meridians
    return meridians.filter(m => m.category === meridianCategoryFilter)
  })()

  return (
    <div>
      <div className="view-toggle">
        <button
          className={`toggle-btn ${viewMode === 'acupoints' ? 'active' : ''}`}
          onClick={() => handleViewModeChange('acupoints')}
        >
          穴位查询（{DataManager.getAll(DATA_TYPES.ACUPOINTS).length}）
        </button>
        <button
          className={`toggle-btn ${viewMode === 'needles' ? 'active' : ''}`}
          onClick={() => handleViewModeChange('needles')}
        >
          针方查询（{DataManager.getAll(DATA_TYPES.NEEDLE_PRESCRIPTIONS).length}）
        </button>
        <button
          className={`toggle-btn ${viewMode === 'meridians' ? 'active' : ''}`}
          onClick={() => handleViewModeChange('meridians')}
        >
          经络信息（{DataManager.getAll(DATA_TYPES.MERIDIANS).length}）
        </button>
      </div>

      {/* ========== ACUPOINT VIEW ========== */}
      {viewMode === 'acupoints' && (
        <>
          {/* Meridian filter */}
          <div className="tag-filter-bar" style={{ marginBottom: '16px', display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
            {meridianOptions.map(m => (
              <button
                key={m}
                className={`tag-filter-btn ${acupointMeridianFilter === m ? 'active' : ''}`}
                onClick={() => setAcupointMeridianFilter(m)}
              >
                {m === 'all' ? '全部经络' : m}
              </button>
            ))}
          </div>

          {filteredAcupoints.length === 0 ? (
            <EmptyState message="未找到匹配的穴位" icon="🔍" />
          ) : (
            <div className="list-container">
              {filteredAcupoints.map(acupoint => (
                <div key={acupoint.id} className="list-item" onClick={() => handleSelectAcupoint(acupoint)}>
                  <div className="list-item-title">
                    {acupoint.name} ({acupoint.code})
                    <span style={{ fontSize: '0.85rem', color: '#8b5ba0', marginLeft: '8px', fontWeight: 'normal' }}>
                      {acupoint.meridian}
                    </span>
                  </div>
                  <div className="list-item-pinyin">{acupoint.pinyin}</div>
                  <div className="list-item-desc">{acupoint.location}</div>
                </div>
              ))}
            </div>
          )}
        </>
      )}

      {/* ========== NEEDLE VIEW ========== */}
      {viewMode === 'needles' && (
        <>
          {/* Category filter */}
          <div className="tag-filter-bar" style={{ marginBottom: '16px', display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
            {needleCategoryOptions.map(cat => (
              <button
                key={cat}
                className={`tag-filter-btn ${needleCategoryFilter === cat ? 'active' : ''}`}
                onClick={() => setNeedleCategoryFilter(cat)}
              >
                {cat === 'all' ? '全部类别' : cat}
              </button>
            ))}
          </div>

          {filteredNeedles.length === 0 ? (
            <EmptyState message="未找到匹配的针方" icon="🔍" />
          ) : (
            <div className="list-container">
              {filteredNeedles.map(needle => (
                <div key={needle.id} className="list-item" onClick={() => handleSelectNeedle(needle)}>
                  <div className="list-item-title">
                    {needle.name}
                    {needle.source && (
                      <span style={{ fontSize: '0.85rem', color: '#c98b3c', marginLeft: '8px', fontWeight: 'normal' }}>
                        {needle.source}
                      </span>
                    )}
                  </div>
                  <div className="list-item-pinyin">{needle.category}</div>
                  <div className="list-item-desc">{needle.effects?.join('、')}</div>
                </div>
              ))}
            </div>
          )}
        </>
      )}

      {/* ========== MERIDIAN VIEW ========== */}
      {viewMode === 'meridians' && (
        <>
          {/* Meridian category filter */}
          <div className="tag-filter-bar" style={{ marginBottom: '16px', display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
            {meridianCategoryOptions.map(cat => (
              <button
                key={cat}
                className={`tag-filter-btn ${meridianCategoryFilter === cat ? 'active' : ''}`}
                onClick={() => setMeridianCategoryFilter(cat)}
              >
                {cat === 'all' ? '全部经络' : cat}
              </button>
            ))}
          </div>

          {allMeridians.length === 0 ? (
            <EmptyState message="暂无经络数据" icon="🔍" />
          ) : (
            <div className="meridian-list">
              {allMeridians.map(meridian => {
                const acupointsOnMeridian = getMeridianAcupoints(meridian.id)
                return (
                  <div key={meridian.id} id={`meridian-${meridian.id}`} className="card meridian-info-card" style={{ marginBottom: '16px' }}>
                    <div className="card-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '8px' }}>
                      <div>
                        <h3 style={{ margin: 0, fontSize: '1.15rem', color: '#4a9c8c' }}>
                          {meridian.name}
                        </h3>
                        <p style={{ margin: '4px 0 0', fontSize: '0.92rem', color: '#8a8276' }}>{meridian.pinyin}</p>
                      </div>
                      <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                        <span className="tag-item" style={{ background: '#e8f5f0', color: '#3d8b63' }}>{meridian.category}</span>
                        {meridian.yin_yang && <span className="tag-item" style={{ background: '#f5edf8', color: '#7b5ea0' }}>{meridian.yin_yang}经</span>}
                        {meridian.element && <span className="tag-item" style={{ background: '#fef6ee', color: '#d4813c' }}>{meridian.element}行</span>}
                      </div>
                    </div>

                    {/* 循行路线 */}
                    {meridian.path && (
                      <div style={{ marginTop: '12px' }}>
                        <strong style={{ fontSize: '0.92rem', color: '#6b5f52' }}>循行路线：</strong>
                        <p style={{ fontSize: '0.92rem', color: '#6b5f52', lineHeight: 1.8, marginTop: '4px', padding: '12px', background: '#fbf9f4', borderRadius: '10px' }}>
                          {meridian.path}
                        </p>
                      </div>
                    )}

                    {/* 主治概要 */}
                    {meridian.indications && meridian.indications.length > 0 && (
                      <div style={{ marginTop: '10px' }}>
                        <strong style={{ fontSize: '0.92rem', color: '#6b5f52' }}>主治概要：</strong>
                        <div className="tag-list" style={{ marginTop: '6px' }}>
                          {meridian.indications.map((ind, i) => (
                            <span key={i} className="tag-item clickable-tag" style={{ fontSize: '0.85rem' }}
                              onClick={() => handleSearchClick(ind)}>{ind}</span>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* 主要穴位 */}
                    {meridian.main_points && meridian.main_points.length > 0 && (
                      <div style={{ marginTop: '10px' }}>
                        <strong style={{ fontSize: '0.92rem', color: '#6b5f52' }}>
                          主要穴位（{meridian.main_points.length}穴）：
                        </strong>
                        <div className="tag-list" style={{ marginTop: '6px' }}>
                          {meridian.main_points.map((pt, i) => {
                            const matchedAcupoint = acupointsOnMeridian.find(a => a.name === pt)
                            return (
                              <span key={i} className="tag-item clickable-tag"
                                style={{ fontSize: '0.88rem', cursor: matchedAcupoint ? 'pointer' : 'default' }}
                                onClick={() => {
                                  if (matchedAcupoint) handleSelectAcupoint(matchedAcupoint)
                                }}
                              >
                                {pt}
                              </span>
                            )
                          })}
                        </div>
                      </div>
                    )}

                    {/* 本经所有穴位 */}
                    {acupointsOnMeridian.length > 0 && (
                      <div style={{ marginTop: '10px' }}>
                        <strong style={{ fontSize: '0.92rem', color: '#6b5f52' }}>
                          本经收录穴位（{acupointsOnMeridian.length}穴）：
                        </strong>
                        <div className="tag-list" style={{ marginTop: '6px' }}>
                          {acupointsOnMeridian.map(ap => (
                            <span key={ap.id} className="tag-item clickable-tag"
                              style={{ fontSize: '0.88rem' }}
                              onClick={() => handleSelectAcupoint(ap)}>
                              {ap.name}
                              <span style={{ fontSize: '0.78rem', marginLeft: '3px', opacity: 0.7 }}>{ap.code}</span>
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* 关联证型 */}
                    {meridian.related_syndromes && meridian.related_syndromes.length > 0 && (
                      <div style={{ marginTop: '10px' }}>
                        <strong style={{ fontSize: '0.92rem', color: '#6b5f52' }}>关联证型：</strong>
                        <div className="tag-list" style={{ marginTop: '6px' }}>
                          {meridian.related_syndromes.map(sid => {
                            const s = DataManager.getById(DATA_TYPES.SYNDROMES, sid)
                            return s ? (
                              <span key={sid} className="tag-item clickable-tag" style={{ fontSize: '0.88rem', background: '#edf4fa', color: '#4a7fb5' }}
                                onClick={() => navigate(`/syndromes/${sid}`)}>{s.name}</span>
                            ) : null
                          })}
                        </div>
                      </div>
                    )}
                  </div>
                )
              })}
            </div>
          )}
        </>
      )}
    </div>
  )
}
