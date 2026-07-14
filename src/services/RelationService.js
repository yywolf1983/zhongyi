import { DataManager } from './DataManager'
import { DATA_TYPES } from './DataManager'

export class RelationService {
  static getFormulasBySyndrome(syndromeId) {
    const formulas = DataManager.getAll(DATA_TYPES.FORMULAS)
    return formulas.filter(f => f.syndrome_ids?.includes(syndromeId) || f.related_syndromes?.includes(syndromeId))
  }

  static getMedicinesByFormula(formulaId) {
    const formula = DataManager.getById(DATA_TYPES.FORMULAS, formulaId)
    const ingredients = formula?.ingredients || formula?.composition
    if (!formula || !ingredients) return []
    
    return ingredients.map(item => {
      const medicine = DataManager.getById(DATA_TYPES.MEDICINES, item.medicine_id)
      return {
        ...medicine,
        dose: item.dose || item.quantity,
        role: item.role
      }
    }).filter(Boolean)
  }

  static getAcupointsByNeedle(needleId) {
    const needle = DataManager.getById(DATA_TYPES.NEEDLE_PRESCRIPTIONS, needleId)
    if (!needle || !needle.acupoints) return []
    
    return needle.acupoints.map(item => {
      const acupoint = DataManager.getById(DATA_TYPES.ACUPOINTS, item.acupoint_id)
      return {
        ...acupoint,
        method: item.method
      }
    }).filter(Boolean)
  }

  static getNeedlesBySyndrome(syndromeId) {
    const needles = DataManager.getAll(DATA_TYPES.NEEDLE_PRESCRIPTIONS)
    return needles.filter(n => n.related_syndromes?.includes(syndromeId))
  }

  static getEffectsByMedicine(medicineId) {
    const effects = DataManager.getAll(DATA_TYPES.EFFECTS)
    return effects.filter(e => e.related_medicines?.includes(medicineId))
  }

  static getModernMapping(chineseTerm) {
    const mappings = DataManager.getAll(DATA_TYPES.MODERN_MAPPING)
    return mappings.filter(m => 
      m.chinese_term.includes(chineseTerm) || m.modern_term.includes(chineseTerm)
    )
  }

  static getModernMappingBySyndrome(syndromeId) {
    const mappings = DataManager.getAll(DATA_TYPES.MODERN_MAPPING)
    return mappings.filter(m => m.related_syndrome === syndromeId)
  }

  static getModernMappingByAcupoint(acupointId) {
    const mappings = DataManager.getAll(DATA_TYPES.MODERN_MAPPING)
    return mappings.filter(m => m.related_acupoint === acupointId)
  }

  static getModernMappingByMedicine(medicineId) {
    const mappings = DataManager.getAll(DATA_TYPES.MODERN_MAPPING)
    return mappings.filter(m => m.related_medicine === medicineId)
  }

  static getModernMappingByFormula(formulaId) {
    const mappings = DataManager.getAll(DATA_TYPES.MODERN_MAPPING)
    return mappings.filter(m => m.related_formula === formulaId)
  }

  static getTreatmentBySyndrome(syndromeId) {
    const treatments = DataManager.getAll(DATA_TYPES.TREATMENTS)
    return treatments.filter(t => t.related_syndromes?.includes(syndromeId))
  }

  static getAcupointsByMeridian(meridianId) {
    const acupoints = DataManager.getAll(DATA_TYPES.ACUPOINTS)
    return acupoints.filter(a => a.meridian_id === meridianId)
  }

  static getMeridianByAcupoint(acupointId) {
    const acupoint = DataManager.getById(DATA_TYPES.ACUPOINTS, acupointId)
    if (!acupoint?.meridian_id) return null
    return DataManager.getById(DATA_TYPES.MERIDIANS, acupoint.meridian_id)
  }

  static getMedicinesByEffect(effectId) {
    const medicines = DataManager.getAll(DATA_TYPES.MEDICINES)
    return medicines.filter(m => m.related_effects?.includes(effectId))
  }

  static getFormulasByEffect(effectId) {
    const formulas = DataManager.getAll(DATA_TYPES.FORMULAS)
    return formulas.filter(f => f.related_effects?.includes(effectId))
  }

  static getSyndromeRelations(syndromeId) {
    const syndrome = DataManager.getById(DATA_TYPES.SYNDROMES, syndromeId)
    if (!syndrome) return null

    return {
      syndrome,
      formulas: this.getFormulasBySyndrome(syndromeId),
      needles: this.getNeedlesBySyndrome(syndromeId),
      treatments: this.getTreatmentBySyndrome(syndromeId),
      effects: syndrome.related_effects?.map(id => 
        DataManager.getById(DATA_TYPES.EFFECTS, id)
      ).filter(Boolean) || [],
      modernMapping: this.getModernMappingBySyndrome(syndromeId)
    }
  }

  static getFormulaRelations(formulaId) {
    const formula = DataManager.getById(DATA_TYPES.FORMULAS, formulaId)
    if (!formula) return null

    // Support both naming conventions: syndrome_ids / related_syndromes
    const syndIds = formula.syndrome_ids || formula.related_syndromes || []
    const effectIds = formula.effect_ids || formula.related_effects || []

    return {
      formula,
      medicines: this.getMedicinesByFormula(formulaId),
      syndromes: syndIds.map(id => 
        DataManager.getById(DATA_TYPES.SYNDROMES, id)
      ).filter(Boolean),
      effects: effectIds.map(id => 
        DataManager.getById(DATA_TYPES.EFFECTS, id)
      ).filter(Boolean),
      modernMapping: this.getModernMappingByFormula(formulaId)
    }
  }

  static getAcupointRelations(acupointId) {
    const acupoint = DataManager.getById(DATA_TYPES.ACUPOINTS, acupointId)
    if (!acupoint) return null

    return {
      acupoint,
      meridian: this.getMeridianByAcupoint(acupointId),
      needles: DataManager.getAll(DATA_TYPES.NEEDLE_PRESCRIPTIONS).filter(n => 
        n.acupoints?.some(a => a.acupoint_id === acupointId)
      ),
      syndromes: acupoint.related_syndromes?.map(id => 
        DataManager.getById(DATA_TYPES.SYNDROMES, id)
      ).filter(Boolean) || [],
      modernMapping: this.getModernMappingByAcupoint(acupointId)
    }
  }

  static getMedicineRelations(medicineId) {
    const medicine = DataManager.getById(DATA_TYPES.MEDICINES, medicineId)
    if (!medicine) return null

    // Reverse lookup: find all formulas that contain this medicine
    const allFormulas = DataManager.getAll(DATA_TYPES.FORMULAS)
    const formulas = allFormulas.filter(f => {
      const ingredients = f.ingredients || f.composition || []
      return ingredients.some(ing => ing.medicine_id === medicineId)
    })

    return {
      medicine,
      formulas: formulas,
      effects: this.getEffectsByMedicine(medicineId),
      modernMapping: this.getModernMappingByMedicine(medicineId)
    }
  }

  static getNeedleRelations(needleId) {
    const needle = DataManager.getById(DATA_TYPES.NEEDLE_PRESCRIPTIONS, needleId)
    if (!needle) return null

    return {
      needle,
      acupoints: this.getAcupointsByNeedle(needleId),
      syndromes: needle.related_syndromes?.map(id => 
        DataManager.getById(DATA_TYPES.SYNDROMES, id)
      ).filter(Boolean) || []
    }
  }

  static getRelations(entityId, entityType) {
    const relationMap = {
      [DATA_TYPES.SYNDROMES]: () => this.getSyndromeRelations(entityId),
      [DATA_TYPES.FORMULAS]: () => this.getFormulaRelations(entityId),
      [DATA_TYPES.ACUPOINTS]: () => this.getAcupointRelations(entityId),
      [DATA_TYPES.MEDICINES]: () => this.getMedicineRelations(entityId),
      [DATA_TYPES.NEEDLE_PRESCRIPTIONS]: () => this.getNeedleRelations(entityId)
    }

    return relationMap[entityType] ? relationMap[entityType]() : null
  }
}

export default RelationService
