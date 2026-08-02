import { useState, useEffect, useMemo } from 'react'
import { useNavigate, useParams, useSearchParams, useLocation } from 'react-router-dom'
import { DataManager } from '../../services/DataManager.js'
import { RelationService } from '../../services/RelationService.js'
import { DATA_TYPES } from '../../services/DataManager.js'
import { navigateToEntityByName } from '../../services/EntityRoute.js'
import { useAppContext } from '../../context/AppContext.jsx'
import BookmarkButton from '../common/BookmarkButton.jsx'
import EmptyState from '../common/EmptyState.jsx'
import ClassicExcerpts from '../common/ClassicExcerpts.jsx'
import ComparisonItems from '../common/ComparisonItems.jsx'
import FloatingBackButton from '../common/FloatingBackButton.jsx'
import GroupedList from '../common/GroupedList.jsx'
import { FORMULA_CAT_ALIAS, MEDICINE_CAT_ALIAS, canonCat } from '../../data/categories.js'

// 横滑 chip 行（手机友好）：一行展示分类/子类，带数量，超出横向滚动
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

export default function FormulaModule() {
  const navigate = useNavigate()
  const location = useLocation()
  const { formulaId, medicineId } = useParams()
  const [searchParams] = useSearchParams()

  const allFormulas = useMemo(() => DataManager.getAll(DATA_TYPES.FORMULAS), [])
  const allMedicines = useMemo(() => DataManager.getAll(DATA_TYPES.MEDICINES), [])

  const [selectedFormula, setSelectedFormula] = useState(null)
  const [selectedMedicine, setSelectedMedicine] = useState(null)
  // 支持从首页「中药百科」卡片带 ?tab=medicines，或从独立路由 /medicines 直达中药列表
  const isMedicineRoute = location.pathname.startsWith('/medicines')
  const [viewMode, setViewMode] = useState(() =>
    (searchParams.get('tab') === 'medicines' || isMedicineRoute) ? 'medicines' : 'formulas'
  )
  const { addRecent } = useAppContext()
  const [formulaCatFilter, setFormulaCatFilter] = useState('all')
  const [formulaSubFilter, setFormulaSubFilter] = useState('all')
  const [medicineCatFilter, setMedicineCatFilter] = useState('all')
  const [medicineSubFilter, setMedicineSubFilter] = useState('all')
  const [formulaCatOpen, setFormulaCatOpen] = useState(false)
  const [medicineCatOpen, setMedicineCatOpen] = useState(false)
  const [formulaSubOpen, setFormulaSubOpen] = useState(false)
  const [medicineSubOpen, setMedicineSubOpen] = useState(false)

  // 分类归并映射统一维护在 src/data/categories.js（数据库已同步归并，此处为兜底）

  // 大类选项（带数量，按数量降序，便于手机上优先看到常用类）
  const formulaCatOpts = useMemo(() => {
    const m = {}
    allFormulas.forEach(f => {
      const c = canonCat(f.category, FORMULA_CAT_ALIAS)
      m[c] = (m[c] || 0) + 1
    })
    const entries = Object.entries(m).sort((a, b) => b[1] - a[1])
    return [
      { value: 'all', label: '全部', count: allFormulas.length },
      ...entries.map(([k, v]) => ({ value: k, label: k, count: v })),
    ]
  }, [allFormulas])

  const formulaSubOpts = useMemo(() => {
    const base = formulaCatFilter === 'all'
      ? allFormulas
      : allFormulas.filter(f => canonCat(f.category, FORMULA_CAT_ALIAS) === formulaCatFilter)
    const m = {}
    base.forEach(f => {
      const arr = Array.isArray(f.subcategory) ? f.subcategory : (f.subcategory ? [f.subcategory] : [])
      arr.forEach(s => { if (s) m[s] = (m[s] || 0) + 1 })
    })
    const entries = Object.entries(m).sort((a, b) => b[1] - a[1])
    return [
      { value: 'all', label: '全部子类', count: base.length },
      ...entries.map(([k, v]) => ({ value: k, label: k, count: v })),
    ]
  }, [allFormulas, formulaCatFilter])

  const formulas = useMemo(() => {
    let list = allFormulas
    if (formulaCatFilter !== 'all') {
      list = list.filter(f => canonCat(f.category, FORMULA_CAT_ALIAS) === formulaCatFilter)
    }
    if (formulaSubFilter !== 'all') {
      list = list.filter(f => {
        const arr = Array.isArray(f.subcategory) ? f.subcategory : (f.subcategory ? [f.subcategory] : [])
        return arr.includes(formulaSubFilter)
      })
    }
    return list
  }, [allFormulas, formulaCatFilter, formulaSubFilter])

  // 中药大类选项
  const medicineCatOpts = useMemo(() => {
    const m = {}
    allMedicines.forEach(x => {
      const c = canonCat(x.category, MEDICINE_CAT_ALIAS)
      m[c] = (m[c] || 0) + 1
    })
    const entries = Object.entries(m).sort((a, b) => b[1] - a[1])
    return [
      { value: 'all', label: '全部分类', count: allMedicines.length },
      ...entries.map(([k, v]) => ({ value: k, label: k, count: v })),
    ]
  }, [allMedicines])

  const medicineSubOpts = useMemo(() => {
    const base = medicineCatFilter === 'all'
      ? allMedicines
      : allMedicines.filter(x => canonCat(x.category, MEDICINE_CAT_ALIAS) === medicineCatFilter)
    const m = {}
    base.forEach(x => {
      const arr = Array.isArray(x.subcategory) ? x.subcategory : (x.subcategory ? [x.subcategory] : [])
      arr.forEach(s => { if (s) m[s] = (m[s] || 0) + 1 })
    })
    const entries = Object.entries(m).sort((a, b) => b[1] - a[1])
    return [
      { value: 'all', label: '全部子类', count: base.length },
      ...entries.map(([k, v]) => ({ value: k, label: k, count: v })),
    ]
  }, [allMedicines, medicineCatFilter])

  const medicines = useMemo(() => {
    let list = allMedicines
    if (medicineCatFilter !== 'all') {
      list = list.filter(x => canonCat(x.category, MEDICINE_CAT_ALIAS) === medicineCatFilter)
    }
    if (medicineSubFilter !== 'all') {
      list = list.filter(x => {
        const arr = Array.isArray(x.subcategory) ? x.subcategory : (x.subcategory ? [x.subcategory] : [])
        return arr.includes(medicineSubFilter)
      })
    }
    return list
  }, [allMedicines, medicineCatFilter, medicineSubFilter])

  // Handle URL deep linking
  useEffect(() => {
    if (formulaId) {
      const found = DataManager.getById(DATA_TYPES.FORMULAS, formulaId)
      if (found) {
        const relations = RelationService.getFormulaRelations(found.id)
        setSelectedFormula(relations)
        setSelectedMedicine(null)
        addRecent({ type: 'formula', id: found.id, name: found.name, sub: found.category, navPath: `/formulas/${found.id}` })
      }
    } else if (medicineId) {
      const found = DataManager.getById(DATA_TYPES.MEDICINES, medicineId)
      if (found) {
        const relations = RelationService.getMedicineRelations(found.id)
        setSelectedMedicine(relations)
        setSelectedFormula(null)
        addRecent({ type: 'medicine', id: found.id, name: found.name, sub: found.category, navPath: `/formulas/medicine/${found.id}` })
      }
    } else {
      setSelectedFormula(null)
      setSelectedMedicine(null)
    }
  }, [formulaId, medicineId])

  const handleSelectFormula = (formula) => {
    navigate(`/formulas/${formula.id}`)
  }

  const handleSelectMedicine = (medicine) => {
    navigate(`/formulas/medicine/${medicine.id}`)
  }

  const handleBack = () => {
    if (window.history.length > 1) {
      navigate(-1)
    } else {
      navigate('/formulas')
    }
  }

  const handleSearchClick = (term) => {
    navigate(`/search?q=${encodeURIComponent(term)}`)
  }

  const handleEffectClick = (name) => {
    navigateToEntityByName(navigate, DATA_TYPES.EFFECTS, name)
  }

  const handleViewModeChange = (mode) => {
    setViewMode(mode)
    setFormulaCatFilter('all')
    setFormulaSubFilter('all')
    setMedicineCatFilter('all')
    setMedicineSubFilter('all')
  }

  const handleMeridianClick = (meridianName) => {
    navigateToEntityByName(navigate, DATA_TYPES.MERIDIANS, meridianName)
  }

  const getRoleClass = (role) => {
    const roleMap = {
      '君': 'monarch',
      '臣': 'minister',
      '佐': 'adjuvant',
      '使': 'guide'
    }
    return roleMap[role] || ''
  }

  const getRoleLabel = (role) => {
    const roleMap = {
      '君': '君药',
      '臣': '臣药',
      '佐': '佐药',
      '使': '使药'
    }
    return roleMap[role] || role
  }

  if (selectedFormula) {
    const { formula, medicines: formulaMedicines, syndromes, modernMapping } = selectedFormula

    return (
      <div className="detail-container">
      <FloatingBackButton onClick={handleBack} />


        <div className="detail-header-row">
          <div className="detail-header">
            <h1 className="detail-title">{formula.name}</h1>
            <p className="detail-pinyin">{formula.pinyin}</p>
            <div className="detail-category">
              <span className="category-tag">{formula.category}</span>
              {formula.subcategory && <span className="category-tag">{Array.isArray(formula.subcategory) ? formula.subcategory.join('、') : formula.subcategory}</span>}
            </div>
          </div>
          <BookmarkButton item={formula} type="formula" />
        </div>

        <div className="section">
          <h2 className="section-title">来源</h2>
          <div className="section-content"><strong>书籍：</strong>{formula.source}</div>
          {formula.author && <div className="section-content"><strong>作者：</strong>{formula.author}</div>}
        </div>

        <ClassicExcerpts excerpts={formula.classic_excerpts} />

        {formula.effects && formula.effects.length > 0 && (
          <div className="section">
            <h2 className="section-title">功效</h2>
            <div className="tag-list">
              {formula.effects.map((effect, i) => (
                <span key={i} className="tag-item primary clickable-tag"
                  onClick={() => handleEffectClick(effect)}>{effect}</span>
              ))}
            </div>
          </div>
        )}

        {formula.indications && (
          <div className="section">
            <h2 className="section-title">适应症</h2>
            <div className="tag-list">
              {(Array.isArray(formula.indications) ? formula.indications : formula.indications.split(/[；;，,、]/).filter(Boolean)).map((ind, i) => (
                <span key={i} className="tag-item clickable-tag" onClick={() => handleSearchClick(ind.trim())}>{ind.trim()}</span>
              ))}
            </div>
          </div>
        )}

        {formulaMedicines && formulaMedicines.length > 0 && (
          <div className="section">
            <h2 className="section-title">方剂组成</h2>
            <div className="table-wrapper">
              <table className="composition-table">
                <thead>
                  <tr>
                    <th>中药</th>
                    <th>剂量</th>
                    <th>君臣佐使</th>
                  </tr>
                </thead>
                <tbody>
                  {formulaMedicines.map(medicine => (
                    <tr key={medicine.id} onClick={() => handleSelectMedicine(medicine)} style={{ cursor: 'pointer' }}>
                      <td><strong>{medicine.name}</strong> ({medicine.pinyin})</td>
                      <td>{medicine.dose}</td>
                      <td><span className={`role-tag ${getRoleClass(medicine.role)}`}>{getRoleLabel(medicine.role)}</span></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {formula.usage && (
          <div className="section">
            <h2 className="section-title">用法</h2>
            <p className="section-content">{formula.usage}</p>
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



        {/* Comparison items if formula has it */}
        {formula.comparison && formula.comparison.length > 0 && (
          <div className="section">
            <h2 className="section-title mapping-title">中西对照</h2>
            <ComparisonItems comparison={formula.comparison} />
          </div>
        )}

        {modernMapping && modernMapping.length > 0 && (
          <div className="section">
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

        {formula.modern_applications && formula.modern_applications.length > 0 && (
          <div className="section secondary">
            <h2 className="section-title">现代应用</h2>
            <div className="tag-list">
              {formula.modern_applications.map((app, i) => (
                <span key={i} className="tag-item warning clickable-tag" onClick={() => handleSearchClick(app)}>{app}</span>
              ))}
            </div>
          </div>
        )}

        {formula.modern_explanation && (
          <div className="section secondary">
            <h2 className="section-title">现代医学解释</h2>
            <p className="section-content">{formula.modern_explanation}</p>
          </div>
        )}

        {formula.pharmacological_effect && (
          <div className="section secondary">
            <h2 className="section-title">药理作用</h2>
            <p className="section-content">{formula.pharmacological_effect}</p>
          </div>
        )}

        {formula.beginner_note && (
          <div className="section secondary">
            <h2 className="section-title">初学者要点</h2>
            <p className="section-content">{formula.beginner_note}</p>
          </div>
        )}

        {formula.advanced_clinical_note && (
          <div className="section secondary">
            <h2 className="section-title">进阶要点</h2>
            <p className="section-content">{formula.advanced_clinical_note}</p>
          </div>
        )}
      </div>
    )
  }

  if (selectedMedicine) {
    const { medicine, formulas: medicineFormulas, modernMapping } = selectedMedicine

    // Determine meridians for display
    const meridians = medicine.meridian_tropism || medicine.meridian || []

    return (
      <div className="detail-container">
      <FloatingBackButton onClick={handleBack} />


        <div className="detail-header-row">
          <div className="detail-header">
            <h1 className="detail-title">{medicine.name}</h1>
            <p className="detail-pinyin">{medicine.pinyin}{medicine.latin_name ? ` (${medicine.latin_name})` : ''}</p>
            <div className="detail-category">
              <span className="category-tag">{medicine.category}</span>
              {medicine.subcategory && <span className="category-tag">{Array.isArray(medicine.subcategory) ? medicine.subcategory.join('、') : medicine.subcategory}</span>}
            </div>
          </div>
          <BookmarkButton item={medicine} type="medicine" />
        </div>

        <div className="section">
          <h2 className="section-title">性味归经</h2>
          <div className="section-content"><strong>药性：</strong>{medicine.nature}</div>
          {medicine.flavor && <div className="section-content"><strong>药味：</strong>{Array.isArray(medicine.flavor) ? medicine.flavor.join('、') : medicine.flavor}</div>}
          {meridians.length > 0 && (
            <div className="section-content">
              <strong>归经：</strong>
              <span className="tag-list" style={{ display: 'inline-flex', flexWrap: 'wrap', marginLeft: '8px', verticalAlign: 'middle' }}>
                {(Array.isArray(meridians) ? meridians : []).map((m, i) => (
                  <span key={i} className="tag-item clickable-tag"
                    style={{ fontSize: '0.82rem' }}
                    onClick={() => handleMeridianClick(m)}>{m}</span>
                ))}
              </span>
            </div>
          )}
        </div>

        {medicine.effects && medicine.effects.length > 0 && (
          <div className="section">
            <h2 className="section-title">功效</h2>
            <div className="tag-list">
              {medicine.effects.map((effect, i) => (
                <span key={i} className="tag-item primary clickable-tag"
                  onClick={() => handleEffectClick(effect)}>{effect}</span>
              ))}
            </div>
            {medicine.has_reference_effects ? (
              <p className="reference-note">部分功效由常识补充，仅供参考，待校对</p>
            ) : null}
          </div>
        )}

        {medicine.indications && medicine.indications.length > 0 && (
          <div className="section">
            <h2 className="section-title">主治病症</h2>
            <div className="tag-list">
              {medicine.indications.map((indication, i) => (
                <span key={i} className="tag-item clickable-tag" onClick={() => handleSearchClick(indication)}>{indication}</span>
              ))}
            </div>
          </div>
        )}

        {medicine.usage && (
          <div className="section">
            <h2 className="section-title">用法用量</h2>
            <p className="section-content">{medicine.usage}</p>
          </div>
        )}

        <ClassicExcerpts excerpts={medicine.classic_excerpts} />

        {medicine.contraindications && medicine.contraindications.length > 0 && (
          <div className="section">
            <h2 className="section-title">禁忌</h2>
            <div className="tag-list">
              {medicine.contraindications.map((contra, i) => (
                <span key={i} className="tag-item warning">{contra}</span>
              ))}
            </div>
          </div>
        )}

        {medicineFormulas && medicineFormulas.length > 0 && (
          <div className="section">
            <h2 className="section-title">关联方剂</h2>
            <div className="list-container">
              {medicineFormulas.map(formula => (
                <div key={formula.id} className="list-item formula" onClick={() => handleSelectFormula(formula)}>
                  <div className="list-item-title">{formula.name}</div>
                  <div className="list-item-pinyin">{formula.pinyin}</div>
                  <div className="list-item-desc">{formula.effects?.join('、')}</div>
                </div>
              ))}
            </div>
          </div>
        )}



        {/* Comparison items if medicine has it */}
        {medicine.comparison && medicine.comparison.length > 0 && (
          <div className="section">
            <h2 className="section-title mapping-title">中西对照</h2>
            <ComparisonItems comparison={medicine.comparison} />
          </div>
        )}

        {modernMapping && modernMapping.length > 0 && (
          <div className="section">
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

        {medicine.modern_pharmacology && medicine.modern_pharmacology.length > 0 && (
          <div className="section secondary">
            <h2 className="section-title">现代药理作用</h2>
            <ul>
              {medicine.modern_pharmacology.map((pharmacology, i) => (
                <li key={i} className="section-content clickable-tag" style={{ cursor: 'pointer' }}
                  onClick={() => handleSearchClick(pharmacology)}>{pharmacology}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    )
  }

  return (
    <div>
      <div className="module-page-header">
        <span className="module-page-icon">💊</span>
        <div className="module-page-text">
          <span className="module-page-title">方剂 · 中药</span>
          <span className="module-page-sub">经方配伍 · 本草性味</span>
        </div>
        <span className="module-page-count">方 {allFormulas.length} · 药 {allMedicines.length}</span>
      </div>
      <div className="view-toggle">
        <button
          className={`toggle-btn ${viewMode === 'formulas' ? 'active' : ''}`}
          onClick={() => handleViewModeChange('formulas')}
        >
          方剂查询（{allFormulas.length}）
        </button>
        <button
          className={`toggle-btn ${viewMode === 'medicines' ? 'active' : ''}`}
          onClick={() => handleViewModeChange('medicines')}
        >
          中药查询（{allMedicines.length}）
        </button>
      </div>

      {viewMode === 'formulas' && (
        <div className="cat-filter">
          <button
            type="button"
            className="cat-filter-toggle"
            onClick={() => setFormulaCatOpen(o => !o)}
          >
            <span className="cat-filter-title">分类</span>
            <span className="cat-filter-summary">
              {formulaCatFilter === 'all' ? '全部' : formulaCatFilter}
            </span>
            <span className={`cat-filter-caret ${formulaCatOpen ? 'open' : ''}`}>▾</span>
          </button>
          {formulaCatOpen && (
            <CatRow
              options={formulaCatOpts}
              active={formulaCatFilter}
              onSelect={(v) => { setFormulaCatFilter(v); setFormulaSubFilter('all'); setFormulaCatOpen(false) }}
            />
          )}

          {formulaSubOpts.length > 1 && (
            <button
              type="button"
              className="cat-filter-toggle"
              onClick={() => setFormulaSubOpen(o => !o)}
            >
              <span className="cat-filter-title">子类</span>
              <span className="cat-filter-summary">
                {formulaSubFilter === 'all' ? '全部子类' : formulaSubFilter}
              </span>
              <span className={`cat-filter-caret ${formulaSubOpen ? 'open' : ''}`}>▾</span>
            </button>
          )}
          {formulaSubOpen && formulaSubOpts.length > 1 && (
            <CatRow
              options={formulaSubOpts}
              active={formulaSubFilter}
              onSelect={(v) => { setFormulaSubFilter(v); setFormulaSubOpen(false) }}
              small
            />
          )}
        </div>
      )}

      {viewMode === 'medicines' && (
        <div className="cat-filter">
          <button
            type="button"
            className="cat-filter-toggle"
            onClick={() => setMedicineCatOpen(o => !o)}
          >
            <span className="cat-filter-title">分类</span>
            <span className="cat-filter-summary">
              {medicineCatFilter === 'all' ? '全部分类' : medicineCatFilter}
            </span>
            <span className={`cat-filter-caret ${medicineCatOpen ? 'open' : ''}`}>▾</span>
          </button>
          {medicineCatOpen && (
            <CatRow
              options={medicineCatOpts}
              active={medicineCatFilter}
              onSelect={(v) => { setMedicineCatFilter(v); setMedicineSubFilter('all'); setMedicineCatOpen(false) }}
            />
          )}

          {medicineSubOpts.length > 1 && (
            <button
              type="button"
              className="cat-filter-toggle"
              onClick={() => setMedicineSubOpen(o => !o)}
            >
              <span className="cat-filter-title">子类</span>
              <span className="cat-filter-summary">
                {medicineSubFilter === 'all' ? '全部子类' : medicineSubFilter}
              </span>
              <span className={`cat-filter-caret ${medicineSubOpen ? 'open' : ''}`}>▾</span>
            </button>
          )}
          {medicineSubOpen && medicineSubOpts.length > 1 && (
            <CatRow
              options={medicineSubOpts}
              active={medicineSubFilter}
              onSelect={(v) => { setMedicineSubFilter(v); setMedicineSubOpen(false) }}
              small
            />
          )}
        </div>
      )}

      {viewMode === 'formulas' ? (
        <GroupedList
          items={formulas}
          getGroup={(f) => {
            const s = f.subcategory
            const sub = Array.isArray(s) ? s[0] : s
            return sub || canonCat(f.category, FORMULA_CAT_ALIAS) || '未分类'
          }}
          getKey={(f) => f.id}
          emptyMessage="未找到匹配的方剂"
          renderItem={(formula) => (
            <div key={formula.id} className="list-item formula" onClick={() => handleSelectFormula(formula)}>
              <div className="list-item-title">{formula.name}</div>
              <div className="list-item-pinyin">{formula.pinyin}</div>
              <div className="list-item-desc">{formula.effects?.join('、')}</div>
            </div>
          )}
        />
      ) : (
        <GroupedList
          items={medicines}
          getGroup={(m) => {
            const s = m.subcategory
            const sub = Array.isArray(s) ? s[0] : s
            return sub || canonCat(m.category, MEDICINE_CAT_ALIAS) || '未分类'
          }}
          getKey={(m) => m.id}
          emptyMessage="未找到匹配的中药"
          renderItem={(medicine) => (
            <div key={medicine.id} className="list-item medicine" onClick={() => handleSelectMedicine(medicine)}>
              <div className="list-item-title">{medicine.name}</div>
              <div className="list-item-pinyin">{medicine.pinyin}</div>
              <div className="list-item-desc">{medicine.effects?.join('、')}</div>
            </div>
          )}
        />
      )}
    </div>
  )
}
