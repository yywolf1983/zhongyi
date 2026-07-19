import initSqlJs from 'sql.js'

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

// SQLite 文件与 wasm 位置（放在 public/ 下，构建后位于应用根目录）
const DB_PATH = './zhongyi.db'
const WASM_PATH = './sql-wasm.wasm'

// 数据库表名（与 import_to_sqlite.py 中的 FILES 一致）
const TABLE_OF = {
  [DATA_TYPES.SYNDROMES]: 'syndromes',
  [DATA_TYPES.MEDICINES]: 'medicines',
  [DATA_TYPES.ACUPOINTS]: 'acupoints',
  [DATA_TYPES.FORMULAS]: 'formulas',
  [DATA_TYPES.NEEDLE_PRESCRIPTIONS]: 'needle_prescriptions',
  [DATA_TYPES.TREATMENTS]: 'treatments',
  [DATA_TYPES.MERIDIANS]: 'meridians',
  [DATA_TYPES.EFFECTS]: 'effects',
  [DATA_TYPES.MODERN_MAPPING]: 'modern_mapping'
}

// 每个表的 list 字段（在 SQLite 中被拆成 `${table}_${field}` 子表），物化时重新组装回数组
const LIST_FIELDS = {
  syndromes: ['category', 'classic_excerpts', 'classification', 'comparison', 'diagnosis_points', 'modern_medicine', 'related_effects', 'related_formulas', 'related_needle', 'related_treatments'],
  medicines: ['classic_excerpts', 'contraindications', 'effect_ids', 'effects', 'flavor', 'indications', 'meridian', 'meridian_ids'],
  acupoints: ['classic_excerpts', 'indications'],
  formulas: ['classic_excerpts', 'comparison', 'effect_ids', 'effects', 'indications', 'ingredients', 'modern_applications', 'related_syndromes', 'syndrome_ids'],
  needle_prescriptions: ['acupoints', 'classic_excerpts', 'effects', 'indications', 'modern_applications', 'related_syndromes'],
  treatments: ['classic_excerpts', 'indications', 'methods', 'related_formulas', 'related_needle', 'related_syndromes'],
  meridians: ['indications', 'main_points', 'related_acupoints', 'related_syndromes'],
  effects: ['indications', 'related_formulas', 'related_medicines', 'related_syndromes'],
  modern_mapping: ['comparison'],
}

// ============================================================
// SQLite 加载 & 物化
// ============================================================
let _sql = null
let _db = null

async function ensureDb() {
  if (_db) return _db
  _sql = await initSqlJs({ locateFile: () => WASM_PATH })
  const resp = await fetch(DB_PATH)
  if (!resp.ok) throw new Error(`无法加载数据库文件: ${DB_PATH} (HTTP ${resp.status})`)
  const buf = await resp.arrayBuffer()
  _db = new _sql.Database(new Uint8Array(buf))
  return _db
}

function asRows(db, sql) {
  const res = db.exec(sql)
  if (!res.length) return []
  const { columns, values } = res[0]
  return values.map(v => {
    const o = {}
    columns.forEach((c, i) => { o[c] = v[i] })
    return o
  })
}

// 把 SQLite 主表 + 子表重新组装成与原 JSON 完全等价的嵌套对象数组
function hydrate(db, table) {
  const listFields = LIST_FIELDS[table] || []
  const rows = asRows(db, `SELECT * FROM "${table}"`)
  if (!listFields.length) return rows
  const child = {}
  for (const f of listFields) {
    const crows = asRows(db, `SELECT * FROM "${table}_${f}"`)
    const byParent = {}
    for (const r of crows) {
      ;(byParent[r.parent_id] = byParent[r.parent_id] || []).push(r)
    }
    child[f] = byParent
  }
  return rows.map(row => {
    const obj = { ...row }
    for (const f of listFields) {
      const arr = child[f][row.id] || []
      if (arr.length && 'value' in arr[0]) {
        obj[f] = arr.map(r => r.value)
      } else {
        obj[f] = arr.map(r => {
          const { parent_id, ...rest } = r
          return rest
        })
      }
    }
    return obj
  })
}

// ============================================================
// 运行时状态：loading / ready / error
// ============================================================
let _state = 'loading'
let _errorMsg = ''
let _dataStore = {}
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

export class DataManager {
  // ---- 状态查询 ----
  static get state() { return _state }
  static get error() { return _errorMsg }
  static get isReady() { return _state === 'ready' }
  static get isLoading() { return _state === 'loading' }

  /** 订阅状态变化 */
  static onStateChange(fn) {
    _listeners.push(fn)
    if (_state === 'ready') {
      try { fn('ready', _errorMsg) } catch {}
    }
    return () => {
      const idx = _listeners.indexOf(fn)
      if (idx >= 0) _listeners.splice(idx, 1)
    }
  }

  // ---- 初始化（异步：从 SQLite 物化所有数据到内存） ----
  static async init() {
    if (_state === 'ready') return { ok: true }

    _setState('loading')
    try {
      const db = await ensureDb()
      const store = {}
      for (const type of Object.values(DATA_TYPES)) {
        store[type] = hydrate(db, TABLE_OF[type])
      }

      const allErrors = []
      for (const [type, data] of Object.entries(store)) {
        const errs = _validateDataset(type, data)
        if (errs.length > 0) allErrors.push(...errs)
      }

      // 合并 localStorage 中的自定义数据（仅叠加，不覆盖 SQLite 数据）
      for (const type of Object.values(DATA_TYPES)) {
        try { this._safeLoad(type, store) } catch {}
      }

      _dataStore = store

      if (allErrors.length > 0) {
        console.warn('[DataManager] 数据校验发现问题:', allErrors)
        _setState('ready', allErrors.join('; '))
        return { ok: false, errors: allErrors }
      }
      _setState('ready', '')
      return { ok: true }
    } catch (e) {
      console.error('[DataManager] 初始化失败:', e)
      _setState('error', e.message)
      return { ok: false, errors: [e.message] }
    }
  }

  // ---- 数据访问 ----
  static getAll(type) {
    if (_state === 'loading' && Object.keys(_dataStore).length === 0) this.init()
    return _dataStore[type] || []
  }

  static getById(type, id) {
    if (_state === 'loading' && Object.keys(_dataStore).length === 0) this.init()
    const data = _dataStore[type] || []
    return data.find(item => item.id === id)
  }

  static search(type, keyword) {
    if (!keyword.trim()) {
      return this.getAll(type)
    }
    const data = _dataStore[type] || []
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

    const data = _dataStore[type] || []
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
      [DATA_TYPES.FORMULAS]: ['name', 'pinyin', 'source', 'ingredients[].name', 'indications'],
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
      const indexMatch = part.match(/^(\w+)\[(\d+)\]$/)
      if (indexMatch) {
        const [, key, index] = indexMatch
        value = value?.[key]?.[parseInt(index)]
      } else if (part.endsWith('[]')) {
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
    const store = _dataStore[type]
    if (!Array.isArray(store)) return null
    const newId = this.generateId(type)
    const newItem = { id: newId, ...data }
    store.push(newItem)
    this._safeSave(type)
    return newItem
  }

  static update(type, id, data) {
    const store = _dataStore[type]
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
    const store = _dataStore[type]
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
      const str = JSON.stringify(_dataStore[type])
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
  static _safeLoad(type, store) {
    try {
      const raw = localStorage.getItem(`custom_${type}`)
      if (!raw) return
      const parsed = JSON.parse(raw)
      if (!Array.isArray(parsed) || parsed.length === 0) return
      const sourceIds = new Set((Array.isArray(store[type]) ? store[type] : []).map(item => item.id))
      let added = 0
      for (const item of parsed) {
        if (item.id && !sourceIds.has(item.id)) {
          store[type].push(item)
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

  /** 重新初始化：从 SQLite 重新物化，回到原始状态 */
  static async reload() {
    _dataStore = {}
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
    const maxId = _dataStore[type]?.reduce((max, item) => {
      const match = item.id.match(/\d+/)
      return match ? Math.max(max, parseInt(match[0])) : max
    }, 0) || 0
    return `${prefix}_${String(maxId + 1).padStart(3, '0')}`
  }

  /** @deprecated 使用 _safeSave */
  static saveToLocalStorage(type, data) {
    _dataStore[type] = data
    this._safeSave(type)
  }

  /** @deprecated 使用 _safeLoad（init 时自动调用） */
  static loadFromLocalStorage(type) {
    return this._safeLoad(type, _dataStore)
  }

  static getTypes() {
    return DATA_TYPES
  }
}

export default DataManager
