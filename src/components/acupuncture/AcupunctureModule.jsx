import { useState, useEffect, useMemo } from 'react'
import { useNavigate, useParams, useSearchParams } from 'react-router-dom'
import { DataManager } from '../../services/DataManager.js'
import { RelationService } from '../../services/RelationService.js'
import { DATA_TYPES } from '../../services/DataManager.js'
import { navigateToEntityByName } from '../../services/EntityRoute.js'
import BookmarkButton from '../common/BookmarkButton.jsx'
import EmptyState from '../common/EmptyState.jsx'
import ClassicExcerpts from '../common/ClassicExcerpts.jsx'

// 经外奇穴部位子类列表（固定顺序）
const EXTRA_POINT_SUBCATEGORIES = ['头颈部奇穴', '胸腹部奇穴', '背腰部奇穴', '上肢部奇穴', '下肢部奇穴', '其他奇穴']

export default function AcupunctureModule() {
  const navigate = useNavigate()
  const { acupointId, needleId, acuPrescId, prescId } = useParams()
  const [searchParams] = useSearchParams()

  const [acupoints, setAcupoints] = useState(() => DataManager.getAll(DATA_TYPES.ACUPOINTS))
  const [prescriptions, setPrescriptions] = useState(() => DataManager.getAll(DATA_TYPES.NEEDLE_PRESCRIPTIONS))
  const [selectedAcupoint, setSelectedAcupoint] = useState(null)
  const [selectedPresc, setSelectedPresc] = useState(null)
  const [viewMode, setViewMode] = useState('acupoints')
  const [expandedMeridian, setExpandedMeridian] = useState(false)

  // 针方（已合并原“针灸处方”，统一为单一针方数据集）：分类筛选
  const [prescCategoryFilter, setPrescCategoryFilter] = useState('all')

  const prescCategoryOptions = useMemo(() => {
    const cats = new Set()
    prescriptions.forEach(n => { if (n.category) cats.add(n.category) })
    return ['all', ...Array.from(cats).sort()]
  }, [prescriptions])

  const filteredPrescs = useMemo(() => {
    let list = prescriptions
    if (prescCategoryFilter !== 'all') list = list.filter(p => p.category === prescCategoryFilter)
    return list
  }, [prescriptions, prescCategoryFilter])

  // 两级穴位筛选
  const [acupointCatFilter, setAcupointCatFilter] = useState('all')   // 全部 / 十二正经 / 奇经八脉 / 经外奇穴
  const [acupointSubFilter, setAcupointSubFilter] = useState('all')   // 具体经络名 / 部位名

  const [meridianCategoryFilter, setMeridianCategoryFilter] = useState('all')
  const [meridianSubFilter, setMeridianSubFilter] = useState('all')

  // ---- 经络大类 → 子类层级 ----
  const meridianHierarchy = useMemo(() => {
    const meridians = DataManager.getAll(DATA_TYPES.MERIDIANS)
    const tree = { '十二正经': {}, '奇经八脉': [], '经外奇穴': [] }
    meridians.forEach(m => {
      if (m.category === '十二正经') {
        const sub = m.subcategory || '其他'
        if (!tree['十二正经'][sub]) tree['十二正经'][sub] = []
        tree['十二正经'][sub].push(m.name)
      } else if (tree[m.category]) {
        tree[m.category].push(m.name)
      }
    })
    return tree
  }, [])

  // 经外奇穴部位子类（从穴位数据的 subcategory 字段读取）
  const extraPointSubCategories = useMemo(() => {
    const all = DataManager.getAll(DATA_TYPES.ACUPOINTS)
    const regions = new Set()
    all.forEach(a => {
      if (a.meridian !== '经外奇穴') return
      const sub = a.subcategory || '其他奇穴'
      regions.add(sub)
    })
    // 按固定顺序排列
    const ordered = EXTRA_POINT_SUBCATEGORIES.filter(s => regions.has(s))
    // 把不在固定列表中的也加入
    regions.forEach(s => { if (!ordered.includes(s)) ordered.push(s) })
    return ['all', ...ordered]
  }, [])

  // 当前选中大类下的子类列表
  const acupointSubCategories = useMemo(() => {
    if (acupointCatFilter === 'all') return []
    if (acupointCatFilter === '经外奇穴') return extraPointSubCategories
    if (acupointCatFilter === '十二正经') {
      // 十二正经的子类直接列出12条经络名
      const subCats = meridianHierarchy['十二正经'] || {}
      const allMeridianNames = Object.values(subCats).flat().sort()
      if (allMeridianNames.length <= 1) return []
      return ['all', ...allMeridianNames]
    }
    // 奇经八脉的子类是具体经络名
    const subList = meridianHierarchy[acupointCatFilter] || []
    if (subList.length <= 1) return []
    return ['all', ...subList.sort()]
  }, [acupointCatFilter, meridianHierarchy, extraPointSubCategories])

  // Handle URL deep linking
  useEffect(() => {
    if (acupointId) {
      const found = DataManager.getById(DATA_TYPES.ACUPOINTS, acupointId)
      if (found) {
        const relations = RelationService.getAcupointRelations(found.id)
        setSelectedAcupoint(relations)
        setSelectedPresc(null)
        setExpandedMeridian(false)
      }
    } else if (needleId || acuPrescId || prescId) {
      const id = needleId || acuPrescId || prescId
      const found = DataManager.getById(DATA_TYPES.NEEDLE_PRESCRIPTIONS, id)
      if (found) {
        const relations = RelationService.getNeedleRelations(found.id)
        setSelectedPresc(relations)
        setSelectedAcupoint(null)
      }
    } else {
      setSelectedAcupoint(null)
      setSelectedPresc(null)
      setExpandedMeridian(false)
      setAcupoints(DataManager.getAll(DATA_TYPES.ACUPOINTS))
      setPrescriptions(DataManager.getAll(DATA_TYPES.NEEDLE_PRESCRIPTIONS))
      // Handle ?meridian= param for deep linking
      const meridianId = searchParams.get('meridian')
      if (meridianId) {
        const meridian = DataManager.getById(DATA_TYPES.MERIDIANS, meridianId)
        if (meridian) {
          setViewMode('acupoints')
          setAcupointCatFilter(meridian.category)
          setAcupointSubFilter(meridian.name)
        }
      }
    }
  }, [acupointId, needleId, acuPrescId, prescId, searchParams])

  const handleSelectAcupoint = (acupoint) => {
    navigate(`/acupuncture/${acupoint.id}`)
  }

  const handleSelectNeedle = (needle) => {
    navigate(`/acupuncture/presc/${needle.id}`)
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

  const handleMeridianClick = (e, acupoint) => {
    e.stopPropagation()
    const meridian = DataManager.getById(DATA_TYPES.MERIDIANS, acupoint.meridian_id)
    if (meridian) {
      setAcupointCatFilter(meridian.category)
      setAcupointSubFilter(meridian.name)
    }
  }

  const handleViewModeChange = (mode) => {
    setViewMode(mode)
    setSelectedAcupoint(null)
    setSelectedPresc(null)
    setExpandedMeridian(false)
    if (mode === 'acupoints') {
      setAcupoints(DataManager.getAll(DATA_TYPES.ACUPOINTS))
      setAcupointCatFilter('all')
      setAcupointSubFilter('all')
      setMeridianCategoryFilter('all')
      setMeridianSubFilter('all')
    } else if (mode === 'prescriptions') {
      setPrescriptions(DataManager.getAll(DATA_TYPES.NEEDLE_PRESCRIPTIONS))
      setPrescCategoryFilter('all')
    }
  }

  // 当子类选中的是具体经络时，获取该经络数据（用于信息融合展示）
  const selectedMeridian = useMemo(() => {
    if (!acupointSubFilter || acupointSubFilter === 'all') return null
    // 经外奇穴的子类是部位名不是经络名
    if (acupointCatFilter === '经外奇穴') return null
    const allMeridians = DataManager.getAll(DATA_TYPES.MERIDIANS)
    // 按名称精确匹配
    const found = allMeridians.find(m => m.name === acupointSubFilter)
    return found || null
  }, [acupointSubFilter, acupointCatFilter])

  // Get acupoints on same meridian
  const getMeridianAcupoints = (meridianId) => {
    return DataManager.getAll(DATA_TYPES.ACUPOINTS)
      .filter(a => a.meridian_id === meridianId)
      .sort((a, b) => (a.sort_order || 0) - (b.sort_order || 0))
  }

  // ============ Acupoint Detail ============
  if (selectedAcupoint) {
    const { acupoint, meridian, needles: relatedNeedles, modernMapping } = selectedAcupoint
    const meridianAcupoints = meridian ? getMeridianAcupoints(meridian.id) : []

    return (
      <div className="detail-container">
        <button className="back-fab" onClick={handleBack} aria-label="返回">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><polyline points="15 18 9 12 15 6"></polyline></svg>
        </button>

        <div className="detail-header-row">
          <div className="detail-header">
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
              <span className="section-content empty-hint">暂无数据</span>
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
              <div className="section-content"><strong>类别：</strong>{meridian.category}{meridian.subcategory ? ` · ${meridian.subcategory}` : ''}</div>
              <div className="section-content"><strong>阴阳：</strong>{meridian.yin_yang}</div>
              {meridian.element && <div className="section-content"><strong>五行：</strong>{meridian.element}</div>}
              <div className="section-content"><strong>主治概要：</strong>{meridian.indications?.join('、')}</div>
              <div className="section-content" style={{ marginTop: '8px', fontSize: '0.88rem', color: 'var(--color-text-hint)' }}>
                本经共 {meridianAcupoints.length} 穴
              </div>

              {expandedMeridian && meridianAcupoints.length > 0 && (
                <div className="meridian-acupoints" style={{ marginTop: '12px', borderTop: '1px solid var(--color-divider)', paddingTop: '10px' }}>
                  <div style={{ fontSize: '0.88rem', color: 'var(--color-text-secondary)', marginBottom: '8px', fontWeight: 500 }}>
                    {meridian.name}全部穴位（点击跳转）：
                  </div>
                  <div className="tag-list">
                    {meridianAcupoints.map(ap => (
                      <span key={ap.id} className="tag-item clickable-tag"
                        style={{ background: ap.id === acupoint.id ? 'var(--color-primary-bg)' : 'var(--color-surface-warm)',
                                 color: ap.id === acupoint.id ? 'var(--color-primary-dark)' : 'var(--color-text-secondary)',
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
                <div key={needle.id} className="list-item needle" onClick={() => handleSelectNeedle(needle)}>
                  <div className="list-item-title">{needle.name}</div>
                  <div className="list-item-desc">{needle.effects?.join('、')}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {modernMapping && modernMapping.length > 0 && (
          <div className="section">
            <h2 className="section-title mapping-title">中西对照</h2>
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

        <ClassicExcerpts excerpts={acupoint.classic_excerpts} />

        {acupoint.modern_anatomy && (
          <div className="section secondary">
            <h2 className="section-title">现代解剖</h2>
            <p className="acupoint-anatomy">{acupoint.modern_anatomy}</p>
          </div>
        )}

        {acupoint.modern_applications && acupoint.modern_applications.length > 0 && (
          <div className="section secondary">
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

  // ============ Unified Prescription Detail ============
  if (selectedPresc) {
    const { needle: presc, acupoints: prescAcupoints, syndromes } = selectedPresc

    return (
      <div className="detail-container">
        <button className="back-fab" onClick={handleBack} aria-label="返回">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><polyline points="15 18 9 12 15 6"></polyline></svg>
        </button>

        <div className="detail-header-row">
          <div className="detail-header">
            <h1 className="detail-title">{presc.name}</h1>
            {presc.pinyin && <p className="detail-pinyin">{presc.pinyin}</p>}
            <div className="detail-category">
              <span className="category-tag" style={{ background: 'var(--color-acupoint-bg)', color: 'var(--color-acupoint)' }}>
                针方
              </span>
              {presc.category && <span className="category-tag">{presc.category}</span>}
              {presc.subcategory && <span className="category-tag">{presc.subcategory}</span>}
              {presc.source && (
                <span className="category-tag" style={{ background: 'var(--color-accent-bg)', color: 'var(--color-accent-dark)', marginLeft: '6px' }}>
                  {presc.source}
                </span>
              )}
            </div>
          </div>
          <BookmarkButton item={presc} type="needle" />
        </div>

        {presc.effects && presc.effects.length > 0 && (
          <div className="section">
            <h2 className="section-title">功效</h2>
            <div className="tag-list">
              {presc.effects.map((effect, i) => (
                <span key={i} className="tag-item primary clickable-tag" onClick={() => navigateToEntityByName(navigate, DATA_TYPES.EFFECTS, effect)}>{effect}</span>
              ))}
            </div>
          </div>
        )}

        {presc.indications && presc.indications.length > 0 && (
          <div className="section">
            <h2 className="section-title">适应症</h2>
            <div className="tag-list">
              {presc.indications.map((indication, i) => (
                <span key={i} className="tag-item clickable-tag" onClick={() => handleSearchClick(indication)}>{indication}</span>
              ))}
            </div>
          </div>
        )}

        {prescAcupoints && prescAcupoints.length > 0 && (
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
                  {prescAcupoints.map(ap => (
                    <tr key={ap.id} onClick={() => handleSelectAcupoint(ap)} style={{ cursor: 'pointer' }}>
                      <td><strong>{ap.name}</strong> ({ap.code})</td>
                      <td>{ap.meridian}</td>
                      <td><span className="tag-item">{ap.method}</span></td>
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

        {presc.method && (
          <div className="section">
            <h2 className="section-title">操作说明</h2>
            <p className="section-content">{presc.method}</p>
          </div>
        )}

        <ClassicExcerpts excerpts={presc.classic_excerpts} />

        {presc.modern_applications && presc.modern_applications.length > 0 && (
          <div className="section secondary">
            <h2 className="section-title">现代应用</h2>
            <div className="tag-list">
              {presc.modern_applications.map((app, i) => (
                <span key={i} className="tag-item warning clickable-tag" onClick={() => handleSearchClick(app)}>{app}</span>
              ))}
            </div>
          </div>
        )}

        {presc.beginner_note && (
          <div className="section secondary">
            <h2 className="section-title">初学者要点</h2>
            <p className="section-content">{presc.beginner_note}</p>
          </div>
        )}

        {presc.advanced_clinical_note && (
          <div className="section secondary">
            <h2 className="section-title">进阶要点</h2>
            <p className="section-content">{presc.advanced_clinical_note}</p>
          </div>
        )}
      </div>
    )
  }

  // ============ List Views ============
  // 穴位两级筛选
  const filteredAcupoints = (() => {
    if (acupointCatFilter === 'all') return acupoints
    const inCat = acupoints.filter(a => {
      const m = DataManager.getById(DATA_TYPES.MERIDIANS, a.meridian_id)
      return m?.category === acupointCatFilter
    })
    if (acupointSubFilter === 'all' || !acupointSubFilter) return inCat
    // 经外奇穴按穴位自身的 subcategory 筛选
    if (acupointCatFilter === '经外奇穴') {
      return inCat.filter(a => (a.subcategory || '其他奇穴') === acupointSubFilter)
    }
    // 十二正经按具体经络名筛选
    if (acupointCatFilter === '十二正经') {
      return inCat.filter(a => a.meridian === acupointSubFilter)
    }
    // 奇经八脉按具体经络名筛选
    return inCat.filter(a => a.meridian === acupointSubFilter)
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
          className={`toggle-btn ${viewMode === 'prescriptions' ? 'active' : ''}`}
          onClick={() => handleViewModeChange('prescriptions')}
        >
          针方（{DataManager.getAll(DATA_TYPES.NEEDLE_PRESCRIPTIONS).length}）
        </button>
      </div>

      {/* ========== ACUPOINT VIEW ========== */}
      {viewMode === 'acupoints' && (
        <>
          {/* 两级筛选：大类 → 子类 */}
          <div className="tag-filter-bar" style={{ marginBottom: '8px' }}>
            {['all', '十二正经', '奇经八脉', '经外奇穴'].map(cat => (
              <button
                key={cat}
                className={`tag-filter-btn ${acupointCatFilter === cat ? 'active' : ''}`}
                onClick={() => { setAcupointCatFilter(cat); setAcupointSubFilter('all') }}
              >
                {cat === 'all' ? '全部经络' : cat}
              </button>
            ))}
          </div>
          {acupointSubCategories.length > 0 && (
            <div className="tag-filter-bar" style={{ marginBottom: '16px', marginTop: '0', borderTopLeftRadius: '0', borderTopRightRadius: '0', borderTop: 'none' }}>
              {acupointSubCategories.map(sub => (
                <button
                  key={sub}
                  className={`tag-filter-btn ${acupointSubFilter === sub ? 'active' : ''}`}
                  onClick={() => setAcupointSubFilter(sub)}
                  style={acupointSubFilter !== sub ? { background: 'var(--color-filter-inactive)' } : {}}
                >
                  {sub === 'all' ? '全部子类' : sub}
                </button>
              ))}
            </div>
          )}

          {/* ===== 选中经络介绍（信息融合）===== */}
          {selectedMeridian && (() => {
            const meridian = selectedMeridian
            const acupointsOnMeridian = getMeridianAcupoints(meridian.id)
            return (
              <div className="card meridian-intro-card">
                <div className="card-header">
                  <div>
                    <h3 className="meridian-title">{meridian.name}</h3>
                    <p className="meridian-pinyin">{meridian.pinyin}</p>
                  </div>
                  <div className="meridian-meta-row">
                    <span className="tag-item meridian-meta-tag category">{meridian.category}</span>
                    {meridian.subcategory && <span className="tag-item meridian-meta-tag subcategory">{meridian.subcategory}</span>}
                    {meridian.yin_yang && <span className="tag-item meridian-meta-tag yinyang">{meridian.yin_yang}经</span>}
                    {meridian.element && <span className="tag-item meridian-meta-tag element">{meridian.element}行</span>}
                  </div>
                </div>

                {meridian.path && (
                  <div className="meridian-section">
                    <strong className="meridian-section-label">循行路线：</strong>
                    <p className="meridian-path-box">{meridian.path}</p>
                  </div>
                )}

                {meridian.indications && meridian.indications.length > 0 && (
                  <div className="meridian-section">
                    <strong className="meridian-section-label">主治概要：</strong>
                    <div className="tag-list meridian-tags">
                      {meridian.indications.map((ind, i) => (
                        <span key={i} className="tag-item clickable-tag"
                          onClick={() => handleSearchClick(ind)}>{ind}</span>
                      ))}
                    </div>
                  </div>
                )}

                {acupointsOnMeridian.length > 0 && (
                  <div className="meridian-section">
                    <strong className="meridian-section-label">
                      全部穴位（{acupointsOnMeridian.length}穴）：
                    </strong>
                    <div className="tag-list meridian-tags">
                      {filteredAcupoints.map(ap => (
                        <span key={ap.id} className="tag-item clickable-tag meridian-point-tag"
                          onClick={() => handleSelectAcupoint(ap)}>
                          {ap.name}
                          <span className="meridian-point-code">{ap.code}</span>
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )
          })()}

          {/* 未选具体经络时：显示穴位列表 */}
          {!selectedMeridian && (
            filteredAcupoints.length === 0 ? (
              <EmptyState message="未找到匹配的穴位" icon="🔍" />
            ) : (
              <div className="list-container">
                {filteredAcupoints.map(acupoint => (
                  <div key={acupoint.id} className="list-item acupoint" onClick={() => handleSelectAcupoint(acupoint)}>
                    <div className="list-item-title">
                      {acupoint.name} ({acupoint.code})
                      <span
                        onClick={(e) => handleMeridianClick(e, acupoint)}
                        title={`查看${acupoint.meridian}详情`}
                        style={{
                          fontSize: '0.85rem', color: 'var(--color-acupoint)',
                          marginLeft: '8px', fontWeight: 'normal', cursor: 'pointer',
                          padding: '2px 6px', borderRadius: '4px',
                          transition: 'background 0.2s'
                        }}
                        onMouseEnter={(e) => { e.currentTarget.style.background = 'var(--color-acupoint-bg)' }}
                        onMouseLeave={(e) => { e.currentTarget.style.background = 'transparent' }}
                      >
                        {acupoint.meridian}
                      </span>
                    </div>
                    <div className="list-item-pinyin">{acupoint.pinyin}</div>
                    <div className="list-item-desc">{acupoint.location}</div>
                  </div>
                ))}
              </div>
            )
          )}
        </>
      )}

      {/* ========== PRESCRIPTIONS VIEW（针方，已合并原“针灸处方”） ========== */}
      {viewMode === 'prescriptions' && (
        <>
          {/* 分类筛选 */}
          <div className="tag-filter-bar" style={{ marginBottom: '16px', display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
            {prescCategoryOptions.map(cat => (
              <button
                key={cat}
                className={`tag-filter-btn ${prescCategoryFilter === cat ? 'active' : ''}`}
                onClick={() => setPrescCategoryFilter(cat)}
              >
                {cat === 'all' ? '全部类别' : cat}
              </button>
            ))}
          </div>

          {filteredPrescs.length === 0 ? (
            <EmptyState message="未找到匹配的针方" icon="🔍" />
          ) : (
            <div className="list-container">
              {filteredPrescs.map(presc => (
                <div key={presc.id} className="list-item needle" onClick={() => handleSelectNeedle(presc)}>
                  <div className="list-item-title">
                    {presc.name}
                    {presc.subcategory && (
                      <span style={{ fontSize: '0.78rem', color: 'var(--color-mapping)', marginLeft: '8px', fontWeight: 'normal' }}>
                        {presc.subcategory}
                      </span>
                    )}
                  </div>
                  <div className="list-item-pinyin">{presc.category}</div>
                  <div className="list-item-desc">{presc.effects?.join('、')}</div>
                </div>
              ))}
            </div>
          )}
        </>
      )}

    </div>
  )
}
