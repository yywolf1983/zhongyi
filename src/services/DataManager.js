import syndromesData from '../../assets/data/syndromes.json'
import medicinesData from '../../assets/data/medicines.json'
import acupointsData from '../../assets/data/acupoints.json'
import formulasData from '../../assets/data/formulas.json'
import needlePrescriptionsData from '../../assets/data/needle_prescriptions.json'
import acupuncturePrescriptionsData from '../../assets/data/acupuncture_prescriptions.json'
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
  ACUPUNCTURE_PRESCRIPTIONS: 'acupuncture_prescriptions',
  TREATMENTS: 'treatments',
  MERIDIANS: 'meridians',
  EFFECTS: 'effects',
  MODERN_MAPPING: 'modern_mapping'
}

const dataStore = {
  [DATA_TYPES.SYNDROMES]: syndromesData,
  [DATA_TYPES.MEDICINES]: medicinesData,
  [DATA_TYPES.ACUPOINTS]: acupointsData,
  [DATA_TYPES.FORMULAS]: formulasData,
  [DATA_TYPES.NEEDLE_PRESCRIPTIONS]: needlePrescriptionsData,
  [DATA_TYPES.ACUPUNCTURE_PRESCRIPTIONS]: acupuncturePrescriptionsData,
  [DATA_TYPES.TREATMENTS]: treatmentsData,
  [DATA_TYPES.MERIDIANS]: meridiansData,
  [DATA_TYPES.EFFECTS]: effectsData,
  [DATA_TYPES.MODERN_MAPPING]: modernMappingData
}

export class DataManager {
  static getAll(type) {
    return dataStore[type] || []
  }

  static getById(type, id) {
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
      [DATA_TYPES.NEEDLE_PRESCRIPTIONS]: ['name', 'pinyin', 'acupoints[].name', 'indications'],
      [DATA_TYPES.ACUPUNCTURE_PRESCRIPTIONS]: ['name', 'pinyin', 'indications', 'effects'],
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
    const store = dataStore[type] || []
    const newId = this.generateId(type)
    const newItem = { id: newId, ...data }
    store.push(newItem)
    this.saveToLocalStorage(type, store)
    return newItem
  }

  static update(type, id, data) {
    const store = dataStore[type] || []
    const index = store.findIndex(item => item.id === id)
    if (index !== -1) {
      store[index] = { ...store[index], ...data }
      this.saveToLocalStorage(type, store)
      return store[index]
    }
    return null
  }

  static delete(type, id) {
    const store = dataStore[type] || []
    const index = store.findIndex(item => item.id === id)
    if (index !== -1) {
      const deleted = store.splice(index, 1)[0]
      this.saveToLocalStorage(type, store)
      return deleted
    }
    return null
  }

  static generateId(type) {
    const prefixMap = {
      [DATA_TYPES.SYNDROMES]: 'syndrome',
      [DATA_TYPES.MEDICINES]: 'medicine',
      [DATA_TYPES.ACUPOINTS]: 'acupoint',
      [DATA_TYPES.FORMULAS]: 'formula',
      [DATA_TYPES.NEEDLE_PRESCRIPTIONS]: 'needle',
      [DATA_TYPES.ACUPUNCTURE_PRESCRIPTIONS]: 'acu_presc',
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

  static saveToLocalStorage(type, data) {
    try {
      localStorage.setItem(`custom_${type}`, JSON.stringify(data))
    } catch (e) {
      console.warn('Failed to save to localStorage:', e)
    }
  }

  static loadFromLocalStorage(type) {
    try {
      const customData = localStorage.getItem(`custom_${type}`)
      if (customData) {
        const parsed = JSON.parse(customData)
        dataStore[type] = parsed
        return parsed
      }
    } catch (e) {
      console.warn('Failed to load from localStorage:', e)
    }
    return null
  }

  static getTypes() {
    return DATA_TYPES
  }
}

export default DataManager
