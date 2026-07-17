import { DataManager } from './DataManager'
import { DATA_TYPES } from './DataManager'

export class SearchService {
  static globalSearch(keyword) {
    if (!keyword.trim()) {
      return { keyword: '', results: {}, total: 0 }
    }

    const searchResults = {
      syndromes: [],
      formulas: [],
      medicines: [],
      acupoints: [],
      needles: [],
      treatments: [],
      meridians: [],
      effects: [],
      modern_mapping: []
    }

    const types = [
      { type: DATA_TYPES.SYNDROMES, key: 'syndromes' },
      { type: DATA_TYPES.FORMULAS, key: 'formulas' },
      { type: DATA_TYPES.MEDICINES, key: 'medicines' },
      { type: DATA_TYPES.ACUPOINTS, key: 'acupoints' },
      { type: DATA_TYPES.NEEDLE_PRESCRIPTIONS, key: 'needles' },
      { type: DATA_TYPES.TREATMENTS, key: 'treatments' },
      { type: DATA_TYPES.MERIDIANS, key: 'meridians' },
      { type: DATA_TYPES.EFFECTS, key: 'effects' },
      { type: DATA_TYPES.MODERN_MAPPING, key: 'modern_mapping' }
    ]

    let total = 0

    types.forEach(({ type, key }) => {
      const results = DataManager.fuzzySearch(type, keyword, {
        matchMode: 'contains',
        caseSensitive: false
      })

      searchResults[key] = results.map(item => ({
        id: item.id,
        name: item.name || item.chinese_term || '-',
        pinyin: item.pinyin || item.modern_term || '',
        score: this.calculateScore(item, keyword, type),
        type: key,
        context: this.extractContext(item, type)
      }))

      searchResults[key].sort((a, b) => b.score - a.score)
      total += searchResults[key].length
    })

    return { keyword, results: searchResults, total }
  }

  static extractContext(item, type) {
    switch (type) {
      case DATA_TYPES.SYNDROMES:
        return {
          category: item.category || [],
          classification: item.classification || [],
          diagnosis_points: (item.diagnosis_points || []).slice(0, 3),
          pathogenesis: item.pathogenesis || '',
          modern_medicine: item.modern_medicine || []
        }
      case DATA_TYPES.MEDICINES:
        return {
          category: item.category || '',
          subcategory: item.subcategory || '',
          latin_name: item.latin_name || '',
          nature: item.nature || '',
          flavor: item.flavor || [],
          meridian: item.meridian || [],
          effects: (item.effects || []).slice(0, 3)
        }
      case DATA_TYPES.FORMULAS:
        return {
          category: item.category || '',
          subcategory: item.subcategory || '',
          source: item.source || '',
          author: item.author || '',
          effects: (item.effects || []).slice(0, 3),
          ingredients_count: (item.ingredients || []).length
        }
      case DATA_TYPES.ACUPOINTS:
        return {
          meridian: item.meridian || '',
          location: item.location || '',
          indications: (item.indications || []).slice(0, 3)
        }
      case DATA_TYPES.NEEDLE_PRESCRIPTIONS:
        return {
          category: item.category || '',
          subcategory: item.subcategory || '',
          syndrome: item.syndrome || '',
          pinyin: item.pinyin || '',
          acupoints: (item.acupoints || []).map(a => a.name).slice(0, 5),
          effects: (item.effects || []).slice(0, 3)
        }
      case DATA_TYPES.TREATMENTS:
        return {
          category: item.category || '',
          principle: item.principle || '',
          indications: (item.indications || []).slice(0, 3)
        }
      case DATA_TYPES.MERIDIANS:
        return {
          category: item.category || '',
          yin_yang: item.yin_yang || '',
          element: item.element || '',
          main_points: (item.main_points || []).slice(0, 5)
        }
      case DATA_TYPES.EFFECTS:
        return {
          description: item.description || '',
          mechanism: item.mechanism || '',
          indications: (item.indications || []).slice(0, 3)
        }
      case DATA_TYPES.MODERN_MAPPING:
        return {
          chinese_term: item.chinese_term || '',
          modern_term: item.modern_term || '',
          category: item.category || '',
          comparison: (item.comparison || []).map(c => ({
            aspect: c.aspect,
            tcm: c.tcm,
            western: c.western
          }))
        }
      default:
        return {}
    }
  }

  static calculateScore(item, keyword, type) {
    let score = 0
    const lowerKeyword = keyword.toLowerCase()

    if (item.name && item.name.toLowerCase().includes(lowerKeyword)) {
      score += 10
      if (item.name.toLowerCase().startsWith(lowerKeyword)) {
        score += 5
      }
    }

    if (item.pinyin && item.pinyin.toLowerCase().includes(lowerKeyword)) {
      score += 8
    }

    const fields = DataManager.getSearchFields(type)
    fields.forEach(field => {
      const value = DataManager.getValueByPath(item, field)
      if (value && String(value).toLowerCase().includes(lowerKeyword)) {
        score += 2
      }
    })

    return score
  }

  static getSuggestions(keyword) {
    if (!keyword.trim()) return []

    const allSuggestions = []
    const types = [
      DATA_TYPES.SYNDROMES,
      DATA_TYPES.MEDICINES,
      DATA_TYPES.ACUPOINTS,
      DATA_TYPES.FORMULAS,
      DATA_TYPES.NEEDLE_PRESCRIPTIONS,
      DATA_TYPES.TREATMENTS,
      DATA_TYPES.MERIDIANS,
      DATA_TYPES.EFFECTS,
      DATA_TYPES.MODERN_MAPPING
    ]

    types.forEach(type => {
      const results = DataManager.fuzzySearch(type, keyword, {
        matchMode: 'startsWith',
        caseSensitive: false
      }).slice(0, 3)
      
      results.forEach(item => {
        allSuggestions.push({
          id: item.id,
          name: item.name || item.chinese_term || '-',
          pinyin: item.pinyin || item.modern_term || '',
          type: this.getTypeLabel(type)
        })
      })
    })

    return allSuggestions.slice(0, 8)
  }

  static getTypeLabel(type) {
    const labelMap = {
      [DATA_TYPES.SYNDROMES]: '证型',
      [DATA_TYPES.MEDICINES]: '中药',
      [DATA_TYPES.ACUPOINTS]: '穴位',
      [DATA_TYPES.FORMULAS]: '方剂',
      [DATA_TYPES.NEEDLE_PRESCRIPTIONS]: '针方',
      [DATA_TYPES.TREATMENTS]: '治疗',
      [DATA_TYPES.MERIDIANS]: '经络',
      [DATA_TYPES.EFFECTS]: '功效',
      [DATA_TYPES.MODERN_MAPPING]: '中西对照'
    }
    return labelMap[type] || '其他'
  }

  static getSearchHistory() {
    try {
      const history = localStorage.getItem('search_history')
      return history ? JSON.parse(history) : []
    } catch (e) {
      return []
    }
  }

  static addSearchHistory(keyword) {
    try {
      const history = this.getSearchHistory()
      const filtered = history.filter(k => k !== keyword)
      filtered.unshift(keyword)
      const limited = filtered.slice(0, 10)
      localStorage.setItem('search_history', JSON.stringify(limited))
      return limited
    } catch (e) {
      return []
    }
  }

  static clearSearchHistory() {
    try {
      localStorage.removeItem('search_history')
      return []
    } catch (e) {
      return []
    }
  }
}

export default SearchService
