import syndromesData from '../../assets/data/syndromes.json'
import medicinesData from '../../assets/data/medicines.json'
import acupointsData from '../../assets/data/acupoints.json'
import formulasData from '../../assets/data/formulas.json'
import needlePrescriptionsData from '../../assets/data/needle_prescriptions.json'
import treatmentsData from '../../assets/data/treatments.json'
import meridiansData from '../../assets/data/meridians.json'
import effectsData from '../../assets/data/effects.json'
import modernMappingData from '../../assets/data/modern_mapping.json'

export const DATA_TYPES = {
  SYNDROMES: 'syndromes',
  MEDICINES: 'medicines',
  ACUPOINTS: 'acupoints',
  FORMULAS: 'formulas',
  NEEDLE_PRESCRIPTIONS: 'needle_prescriptions',
  TREATMENTS: 'treatments',
  MERIDIANS: 'meridians',
  EFFECTS: 'effects',
  MODERN_MAPPING: 'modern_mapping'
}

// ============================================================
// 数据源映射 & 校验
// ============================================================
const DATA_SOURCES = {
  [DATA_TYPES.SYNDROMES]: syndromesData,
  [DATA_TYPES.MEDICINES]: medicinesData,
  [DATA_TYPES.ACUPOINTS]: acupointsData,
  [DATA_TYPES.FORMULAS]: formulasData,
  [DATA_TYPES.NEEDLE_PRESCRIPTIONS]: needlePrescriptionsData,
  [DATA_TYPES.TREATMENTS]: treatmentsData,
  [DATA_TYPES.MERIDIANS]: meridiansData,
  [DATA_TYPES.EFFECTS]: effectsData,
  [DATA_TYPES.MODERN_MAPPING]: modernMappingData
}

// 运行时状态：loading / ready / error
let _state = 'loading'
let _errorMsg = ''
const _listeners = []

function _setState(state, errorMsg) {
  _state = state
  _errorMsg = errorMsg || ''
  _listeners.forEach(fn => { try { fn(state, _errorMsg) } catch {} })
}

// 校验单个数据集的完整性
function _validateDataset(type, data) {
  const errors = []
  if (!Array.isArray(data)) {
    errors.push(`${type}: 不是数组格式`)
    return errors
  }
  if (data.length === 0) {
    errors.push(`${type}: 数据集为空`)
    return errors
  }
  // 检查必要字段
  const requiredFields = {
    [DATA_TYPES.SYNDROMES]: ['id', 'name'],
    [DATA_TYPES.MEDICINES]: ['id', 'name'],
    [DATA_TYPES.ACUPOINTS]: ['id', 'name'],
    [DATA_TYPES.FORMULAS]: ['id', 'name'],
    [DATA_TYPES.NEEDLE_PRESCRIPTIONS]: ['id', 'name'],
    [DATA_TYPES.TREATMENTS]: ['id', 'name'],
    [DATA_TYPES.MERIDIANS]: ['id', 'name'],
    [DATA_TYPES.EFFECTS]: ['id', 'name'],
    [DATA_TYPES.MODERN_MAPPING]: ['id']
  }
  const fields = requiredFields[type] || ['id', 'name']
  const missingIds = []
  const dupIds = new Set()
  const seenIds = new Set()
  for (let i = 0; i < data.length; i++) {
    const item = data[i]
    for (const f of fields) {
      if (item[f] == null || item[f] === '') {
        missingIds.push(`  [${i}] 缺少字段 "${f}"`)
      }
    }
    if (item.id && seenIds.has(item.id)) {
      dupIds.add(item.id)
    }
    if (item.id) seenIds.add(item.id)
  }
  if (missingIds.length > 0) {
    errors.push(`${type}: ${missingIds.slice(0, 3).join('; ')}${missingIds.length > 3 ? ` ... 共${missingIds.length}处` : ''}`)
  }
  if (dupIds.size > 0) {
    errors.push(`${type}: 存在重复 ID: ${[...dupIds].slice(0, 3).join(', ')}`)
  }
  return errors
}

const dataStore = { ...DATA_SOURCES }

// ============================================================
// DataManager
// ============================================================
export class DataManager {
  // ---- 状态查询 ----
  static get state() { return _state }
  static get error() { return _errorMsg }
  static get isReady() { return _state === 'ready' }
  static get isLoading() { return _state === 'loading' }

  /** 订阅状态变化 */
  static onStateChange(fn) {
    _listeners.push(fn)
    // 如果已经 ready，立即回调
    if (_state === 'ready') {
      try { fn('ready', '') } catch {}
    }
    return () => {
      const idx = _listeners.indexOf(fn)
      if (idx >= 0) _listeners.splice(idx, 1)
    }
  }

  // ---- 初始化 ----
  static init() {
    if (_state === 'ready') return { ok: true }

    const allErrors = []
    for (const [type, data] of Object.entries(DATA_SOURCES)) {
      try {
        const errs = _validateDataset(type, data)
        if (errs.length > 0) {
          allErrors.push(...errs)
          // 错误的数据集用空数组兜底
          if (!Array.isArray(data)) {
            dataStore[type] = []
          }
        }
      } catch (e) {
        allErrors.push(`${type}: 校验异常 - ${e.message}`)
      }
    }

    // 校验跨实体引用
    try {
      const allIds = {}
      for (const [type, data] of Object.entries(dataStore)) {
        if (Array.isArray(data)) {
          for (const item of data) {
            if (item.id) allIds[item.id] = true
          }
        }
      }
      const refFields = [
        'related_formulas', 'related_needle', 'related_treatments', 'related_effects',
        'related_syndromes', 'related_acupoints', 'related_medicines', 'related_meridians',
        'related_acupoint', 'related_medicine', 'related_formula', 'related_syndrome',
        'medicine_id', 'acupoint_id', 'meridian_id'
      ]
      let brokenRefs = 0
      for (const [type, data] of Object.entries(dataStore)) {
        if (!Array.isArray(data)) continue
        for (const item of data) {
          for (const field of refFields) {
            const values = item[field]
            if (values == null) continue
            const list = Array.isArray(values) ? values : [values]
            for (const refId of list) {
              if (refId && !allIds[refId]) {
                brokenRefs++
                if (brokenRefs <= 3) {
                  allErrors.push(`${item.id || '?'}.${field} → 无效引用: ${refId}`)
                }
              }
            }
          }
        }
      }
      if (brokenRefs > 3) allErrors.push(`... 共 ${brokenRefs} 处无效引用`)
    } catch (e) {
      allErrors.push(`跨实体引用检查异常: ${e.message}`)
    }

    if (allErrors.length > 0) {
      console.warn('[DataManager] 数据校验发现问题:', allErrors)
    }

    // 加载自定义数据（从 localStorage 合并，不覆盖原始数据）
    for (const type of Object.keys(DATA_SOURCES)) {
      try { this._safeLoad(type) } catch {}
    }

    if (allErrors.length > 0) {
      // 不阻塞启动，降级运行
      _setState('ready', allErrors.join('; '))
      return { ok: false, errors: allErrors }
    }

    _setState('ready', '')
    return { ok: true }
  }

  // ---- 数据访问 ----
  static getAll(type) {
    // 惰性初始化：首次访问时自动 init
    if (_state === 'loading') this.init()
    return dataStore[type] || []
  }

  static getById(type, id) {
    if (_state === 'loading') this.init()
    const data = dataStore[type] || []
    return data.find(item => item.id === id)
  }

  static search(type, keyword) {
    if (!keyword.trim()) {
      return this.getAll(type)
    }
    const data = dataStore[type] || []
    const lowerKeyword = keyword.toLowerCase()
    return data.filter(item => {
      const searchFields = this.getSearchFields(type)
      return searchFields.some(field => {
        const value = this.getValueByPath(item, field)
        return value && String(value).toLowerCase().includes(lowerKeyword)
      })
    })
  }

  static fuzzySearch(type, keyword, options = {}) {
    const {
      fields = this.getSearchFields(type),
      matchMode = 'contains',
      caseSensitive = false
    } = options

    if (!keyword.trim()) {
      return this.getAll(type)
    }

    const data = dataStore[type] || []
    const searchKeyword = caseSensitive ? keyword : keyword.toLowerCase()

    return data.filter(item => {
      return fields.some(field => {
        const value = this.getValueByPath(item, field)
        if (!value) return false
        const strValue = caseSensitive ? String(value) : String(value).toLowerCase()
        
        switch (matchMode) {
          case 'startsWith':
            return strValue.startsWith(searchKeyword)
          case 'exact':
            return strValue === searchKeyword
          case 'contains':
          default:
            return strValue.includes(searchKeyword)
        }
      })
    })
  }

  static getSearchFields(type) {
    const fieldMap = {
      [DATA_TYPES.SYNDROMES]: ['name', 'pinyin', 'diagnosis_points', 'indications', 'pathogenesis', 'etiology', 'modern_medicine', 'comparison[].tcm', 'comparison[].western'],
      [DATA_TYPES.MEDICINES]: ['name', 'pinyin', 'latin_name', 'effects', 'indications'],
      [DATA_TYPES.ACUPOINTS]: ['name', 'pinyin', 'code', 'location', 'indications', 'meridian'],
      [DATA_TYPES.FORMULAS]: ['name', 'pinyin', 'source', 'composition[].name', 'indications'],
      [DATA_TYPES.NEEDLE_PRESCRIPTIONS]: ['name', 'pinyin', 'subcategory', 'syndrome', 'acupoints[].name', 'indications', 'effects'],
      [DATA_TYPES.TREATMENTS]: ['name', 'category', 'indications'],
      [DATA_TYPES.MERIDIANS]: ['name', 'pinyin', 'main_points'],
      [DATA_TYPES.EFFECTS]: ['name', 'description', 'indications'],
      [DATA_TYPES.MODERN_MAPPING]: ['chinese_term', 'modern_term', 'comparison[].tcm', 'comparison[].western']
    }
    return fieldMap[type] || ['name']
  }

  static getValueByPath(obj, path) {
    if (!obj || !path) return null
    const parts = path.split('.')
    let value = obj
    for (let i = 0; i < parts.length; i++) {
      const part = parts[i]
      // Match array[index] like 'composition[0]'
      const indexMatch = part.match(/^(\w+)\[(\d+)\]$/)
      if (indexMatch) {
        const [, key, index] = indexMatch
        value = value?.[key]?.[parseInt(index)]
      } else if (part.endsWith('[]')) {
        // Match array of objects: like 'comparison[]' → iterate all items
        const key = part.slice(0, -2)
        const arr = value?.[key]
        if (!Array.isArray(arr) || arr.length === 0) return null
        const remainingParts = parts.slice(i + 1)
        if (remainingParts.length === 0) {
          value = arr
          break
        }
        const results = arr
          .map(item => this.getValueByPath(item, remainingParts.join('.')))
          .filter(Boolean)
        return results.join(' ')
      } else {
        value = value?.[part]
      }
      if (!value) return null
    }
    return Array.isArray(value) ? value.join(' ') : value
  }

  static add(type, data) {
    const store = dataStore[type]
    if (!Array.isArray(store)) return null
    const newId = this.generateId(type)
    const newItem = { id: newId, ...data }
    store.push(newItem)
    this._safeSave(type)
    return newItem
  }

  static update(type, id, data) {
    const store = dataStore[type]
    if (!Array.isArray(store)) return null
    const index = store.findIndex(item => item.id === id)
    if (index !== -1) {
      store[index] = { ...store[index], ...data }
      this._safeSave(type)
      return store[index]
    }
    return null
  }

  static delete(type, id) {
    const store = dataStore[type]
    if (!Array.isArray(store)) return null
    const index = store.findIndex(item => item.id === id)
    if (index !== -1) {
      const deleted = store.splice(index, 1)[0]
      this._safeSave(type)
      return deleted
    }
    return null
  }

  /** 安全写入 localStorage，失败时仅 warn 不抛异常 */
  static _safeSave(type) {
    try {
      const str = JSON.stringify(dataStore[type])
      if (str && str.length > 0) {
        localStorage.setItem(`custom_${type}`, str)
      }
    } catch (e) {
      if (e.name === 'QuotaExceededError') {
        console.warn(`[DataManager] localStorage 空间不足，无法保存 ${type}`)
      } else {
        console.warn(`[DataManager] 保存 ${type} 失败:`, e.message)
      }
    }
  }

  /** 安全加载自定义数据，只叠加不覆盖 */
  static _safeLoad(type) {
    try {
      const raw = localStorage.getItem(`custom_${type}`)
      if (!raw) return
      const parsed = JSON.parse(raw)
      if (!Array.isArray(parsed) || parsed.length === 0) return
      const source = DATA_SOURCES[type]
      const sourceIds = new Set((Array.isArray(source) ? source : []).map(item => item.id))
      // 只合并 source 中不存在的自定义条目
      let added = 0
      for (const item of parsed) {
        if (item.id && !sourceIds.has(item.id)) {
          dataStore[type].push(item)
          added++
        }
      }
      if (added > 0) {
        console.log(`[DataManager] 已加载 ${added} 条自定义 ${type} 数据`)
      }
    } catch (e) {
      console.warn(`[DataManager] 加载自定义 ${type} 失败，已清除:`, e.message)
      try { localStorage.removeItem(`custom_${type}`) } catch {}
    }
  }

  /** 重新初始化：清空自定义数据，回到原始状态 */
  static reload() {
    for (const type of Object.keys(DATA_SOURCES)) {
      dataStore[type] = [...DATA_SOURCES[type]]
    }
    _state = 'loading'
    _errorMsg = ''
    return this.init()
  }

  static generateId(type) {
    const prefixMap = {
      [DATA_TYPES.SYNDROMES]: 'syndrome',
      [DATA_TYPES.MEDICINES]: 'medicine',
      [DATA_TYPES.ACUPOINTS]: 'acupoint',
      [DATA_TYPES.FORMULAS]: 'formula',
      [DATA_TYPES.NEEDLE_PRESCRIPTIONS]: 'needle',
      [DATA_TYPES.TREATMENTS]: 'treatment',
      [DATA_TYPES.MERIDIANS]: 'meridian',
      [DATA_TYPES.EFFECTS]: 'effect',
      [DATA_TYPES.MODERN_MAPPING]: 'mapping'
    }
    const prefix = prefixMap[type] || 'item'
    const maxId = dataStore[type]?.reduce((max, item) => {
      const match = item.id.match(/\d+/)
      return match ? Math.max(max, parseInt(match[0])) : max
    }, 0) || 0
    return `${prefix}_${String(maxId + 1).padStart(3, '0')}`
  }

  /** @deprecated 使用 _safeSave */
  static saveToLocalStorage(type, data) {
    dataStore[type] = data
    this._safeSave(type)
  }

  /** @deprecated 使用 _safeLoad（init 时自动调用） */
  static loadFromLocalStorage(type) {
    return this._safeLoad(type)
  }

  static getTypes() {
    return DATA_TYPES
  }
}

export default DataManager
