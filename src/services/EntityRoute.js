import { DataManager, DATA_TYPES } from './DataManager'

// 规范 type 统一为 DATA_TYPES 枚举值，单一事实来源
const ROUTE_BY_TYPE = {
  [DATA_TYPES.SYNDROMES]: (id) => `/syndromes/${id}`,
  [DATA_TYPES.FORMULAS]: (id) => `/formulas/${id}`,
  [DATA_TYPES.MEDICINES]: (id) => `/formulas/medicine/${id}`,
  [DATA_TYPES.ACUPOINTS]: (id) => `/acupuncture/${id}`,
  [DATA_TYPES.NEEDLE_PRESCRIPTIONS]: (id) => `/acupuncture/needle/${id}`,
  [DATA_TYPES.ACUPUNCTURE_PRESCRIPTIONS]: (id) => `/acupuncture/acu-presc/${id}`,
  [DATA_TYPES.TREATMENTS]: (id) => `/syndromes?treatment=${id}`,
  [DATA_TYPES.MERIDIANS]: (id) => `/acupuncture?meridian=${id}`,
  [DATA_TYPES.EFFECTS]: (id) => `/syndromes?effect=${id}`,
  [DATA_TYPES.MODERN_MAPPING]: (id) => `/modern-mapping?id=${id}`
}

// 任意 type 表示（中文标签 / 搜索 key / DATA_TYPES 值）→ DATA_TYPES 枚举值
const ANY_TO_TYPE = {
  // 中文标签（搜索建议用）
  '证型': DATA_TYPES.SYNDROMES, '方剂': DATA_TYPES.FORMULAS, '中药': DATA_TYPES.MEDICINES,
  '穴位': DATA_TYPES.ACUPOINTS, '针方': DATA_TYPES.NEEDLE_PRESCRIPTIONS, '针灸处方': DATA_TYPES.ACUPUNCTURE_PRESCRIPTIONS,
  '治疗': DATA_TYPES.TREATMENTS, '治法': DATA_TYPES.TREATMENTS, '经络': DATA_TYPES.MERIDIANS,
  '功效': DATA_TYPES.EFFECTS, '中西对照': DATA_TYPES.MODERN_MAPPING,
  // 搜索结果 key（globalSearch 用）
  'syndromes': DATA_TYPES.SYNDROMES, 'formulas': DATA_TYPES.FORMULAS, 'medicines': DATA_TYPES.MEDICINES,
  'acupoints': DATA_TYPES.ACUPOINTS, 'needles': DATA_TYPES.NEEDLE_PRESCRIPTIONS, 'acupuncture_prescriptions': DATA_TYPES.ACUPUNCTURE_PRESCRIPTIONS,
  'treatments': DATA_TYPES.TREATMENTS, 'meridians': DATA_TYPES.MERIDIANS, 'effects': DATA_TYPES.EFFECTS, 'modern_mapping': DATA_TYPES.MODERN_MAPPING,
  // 书签存储使用的 type
  'syndrome': DATA_TYPES.SYNDROMES, 'formula': DATA_TYPES.FORMULAS, 'medicine': DATA_TYPES.MEDICINES,
  'acupoint': DATA_TYPES.ACUPOINTS, 'needle': DATA_TYPES.NEEDLE_PRESCRIPTIONS, 'acu-presc': DATA_TYPES.ACUPUNCTURE_PRESCRIPTIONS
}

function normalizeType(typeInput) {
  if (!typeInput) return null
  return ANY_TO_TYPE[typeInput] || typeInput
}

export function entityHref(typeInput, id) {
  const t = normalizeType(typeInput)
  const fn = t && ROUTE_BY_TYPE[t]
  return fn ? fn(id) : null
}

export function navigateToEntity(navigate, typeInput, id) {
  const href = entityHref(typeInput, id)
  if (href) navigate(href)
}

// 按名称反查实体 id（用于详情页里的"归经/功效"等名称标签跳转枢纽页）
export function resolveIdByName(typeInput, name) {
  if (!name) return null
  const t = normalizeType(typeInput)
  if (!t) return null
  const list = DataManager.getAll(t)
  const found = list.find(item => item.name === name)
  return found ? found.id : null
}

// 已知实体名称 → 跳详情/枢纽页；找不到则回退到搜索
export function navigateToEntityByName(navigate, typeInput, name) {
  const id = resolveIdByName(typeInput, name)
  if (id) navigateToEntity(navigate, typeInput, id)
  else navigate(`/search?q=${encodeURIComponent(name)}`)
}

export function navigateToSearch(navigate, term) {
  navigate(`/search?q=${encodeURIComponent(term)}`)
}
