#!/usr/bin/env python3
import json, os
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets', 'data')
def load(n):
    with open(os.path.join(DATA_DIR, n), 'r', encoding='utf-8') as f:
        return json.load(f)
def save(n, d):
    with open(os.path.join(DATA_DIR, n), 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

meds = load('medicines.json')
formulas = load('formulas.json')
syns = load('syndromes.json')
fname2id = {f['name'].strip(): f['id'] for f in formulas}

# ---------- 新增药材: 地黄 ----------
meds.append({
    "id": "medicine_566",
    "name": "地黄",
    "pinyin": "Di Huang",
    "latin_name": "Rehmanniae Radix",
    "nature": "寒",
    "flavor": ["甘", "苦"],
    "meridian": ["心经", "肝经", "肾经"],
    "effects": ["清热凉血", "养阴生津"],
    "indications": ["热入营血", "阴虚发热", "消渴", "吐血衄血", "津伤便秘"],
    "usage": "煎服，10-15g；鲜用加倍",
    "contraindications": ["脾虚湿滞、腹满便溏者慎用"],
    "category": "清热药",
    "subcategory": "清热凉血药",
    "classic": "《神农本草经》"
})

# ---------- 新增方剂 ----------
new_formulas = [
 {
  "id": "formula_359", "name": "泻心汤", "pinyin": "Xie Xin Tang", "category": "清热剂",
  "subcategory": "清热解毒", "source": "《金匮要略》", "author": "张仲景",
  "ingredients": [
    {"medicine_id": "medicine_030", "name": "大黄", "quantity": "9g", "role": "君"},
    {"medicine_id": "medicine_018", "name": "黄连", "quantity": "3g", "role": "臣"},
    {"medicine_id": "medicine_017", "name": "黄芩", "quantity": "6g", "role": "佐"}
  ],
  "effects": ["泻火解毒", "燥湿泄热"],
  "indications": ["邪火内炽，迫血妄行，吐血衄血", "湿热内蕴，心下痞满，黄疸"],
  "usage": "麻沸汤渍之，须臾绞去滓，温服",
  "modern_applications": ["上消化道出血", "急性细菌性痢疾", "口腔溃疡"],
  "pharmacological_effect": "泻心汤具有抗炎、止血、抗菌及保护胃肠黏膜作用",
  "syndrome_ids": [], "effect_ids": [],
  "beginner_note": "初学者：记住大黄、黄连、黄芩三黄组合，主治火毒血热、上部出血。",
  "advanced_clinical_note": "高级要点：大黄黄连黄芩泻心汤用麻沸汤轻泡，取气薄泄热，不欲其速下。"
 },
 {
  "id": "formula_360", "name": "黄芪建中汤", "pinyin": "Huang Qi Jian Zhong Tang", "category": "补益剂",
  "subcategory": "补气", "source": "《金匮要略》", "author": "张仲景",
  "ingredients": [
    {"medicine_id": "medicine_073", "name": "黄芪", "quantity": "9g", "role": "君"},
    {"medicine_id": "medicine_002", "name": "桂枝", "quantity": "9g", "role": "臣"},
    {"medicine_id": "medicine_077", "name": "白芍", "quantity": "18g", "role": "臣"},
    {"medicine_id": "medicine_511", "name": "甘草", "quantity": "6g", "role": "使"},
    {"medicine_id": "medicine_004", "name": "生姜", "quantity": "9g", "role": "佐"},
    {"medicine_id": "medicine_372", "name": "大枣", "quantity": "4枚", "role": "佐"},
    {"medicine_id": "medicine_242", "name": "饴糖", "quantity": "30g", "role": "使"}
  ],
  "effects": ["温中补气", "和里缓急"],
  "indications": ["虚劳里急，诸不足", "腹中拘急疼痛，喜温喜按，面色无华"],
  "usage": "水煎服，饴糖烊化冲服",
  "modern_applications": ["慢性胃炎", "消化性溃疡", "胃下垂", "虚弱体质调理"],
  "pharmacological_effect": "黄芪建中汤具有调节胃肠运动、保护胃黏膜、增强免疫作用",
  "syndrome_ids": [], "effect_ids": [],
  "beginner_note": "初学者：小建中汤加黄芪，温中补虚、缓急止痛，用于虚寒性胃脘痛。",
  "advanced_clinical_note": "高级要点：黄芪补气固表，与建中汤相合，重在温养气血以建中州。"
 },
 {
  "id": "formula_361", "name": "加减复脉汤", "pinyin": "Jia Jian Fu Mai Tang", "category": "补益剂",
  "subcategory": "滋阴", "source": "《温病条辨》", "author": "吴鞠通",
  "ingredients": [
    {"medicine_id": "medicine_512", "name": "炙甘草", "quantity": "18g", "role": "君"},
    {"medicine_id": "medicine_025", "name": "生地黄", "quantity": "18g", "role": "君"},
    {"medicine_id": "medicine_077", "name": "白芍", "quantity": "18g", "role": "臣"},
    {"medicine_id": "medicine_079", "name": "麦冬", "quantity": "15g", "role": "臣"},
    {"medicine_id": "medicine_244", "name": "阿胶", "quantity": "9g", "role": "佐"},
    {"medicine_id": "medicine_031", "name": "火麻仁", "quantity": "9g", "role": "佐"}
  ],
  "effects": ["滋阴养血", "生津润燥"],
  "indications": ["温病后期，热伤阴血", "身热面赤，口干舌燥，脉虚大，手足心热"],
  "usage": "水煎服，阿胶烊化冲服",
  "modern_applications": ["热病恢复期", "病毒性心肌炎", "自主神经功能紊乱"],
  "pharmacological_effect": "加减复脉汤具有营养心肌、改善心功能、调节自主神经作用",
  "syndrome_ids": [], "effect_ids": [],
  "beginner_note": "初学者：炙甘草汤去参桂姜枣、加白芍而来，重在滋阴复脉，用于温病伤阴。",
  "advanced_clinical_note": "高级要点：去温阳之品，纯以甘润养阴，为温病后期阴虚证而设。"
 },
 {
  "id": "formula_362", "name": "升阳益胃汤", "pinyin": "Sheng Yang Yi Wei Tang", "category": "补益剂",
  "subcategory": "补气", "source": "《脾胃论》", "author": "李东垣",
  "ingredients": [
    {"medicine_id": "medicine_073", "name": "黄芪", "quantity": "30g", "role": "君"},
    {"medicine_id": "medicine_062", "name": "半夏", "quantity": "9g", "role": "臣"},
    {"medicine_id": "medicine_072", "name": "人参", "quantity": "9g", "role": "臣"},
    {"medicine_id": "medicine_512", "name": "炙甘草", "quantity": "6g", "role": "使"},
    {"medicine_id": "medicine_032", "name": "独活", "quantity": "6g", "role": "佐"},
    {"medicine_id": "medicine_006", "name": "防风", "quantity": "6g", "role": "佐"},
    {"medicine_id": "medicine_077", "name": "白芍", "quantity": "6g", "role": "佐"},
    {"medicine_id": "medicine_318", "name": "羌活", "quantity": "6g", "role": "佐"},
    {"medicine_id": "medicine_044", "name": "陈皮", "quantity": "4g", "role": "佐"},
    {"medicine_id": "medicine_038", "name": "茯苓", "quantity": "4g", "role": "佐"},
    {"medicine_id": "medicine_040", "name": "泽泻", "quantity": "3g", "role": "佐"},
    {"medicine_id": "medicine_012", "name": "柴胡", "quantity": "3g", "role": "佐"},
    {"medicine_id": "medicine_074", "name": "白术", "quantity": "3g", "role": "佐"},
    {"medicine_id": "medicine_018", "name": "黄连", "quantity": "1.5g", "role": "使"},
    {"medicine_id": "medicine_004", "name": "生姜", "quantity": "3片", "role": "佐"},
    {"medicine_id": "medicine_372", "name": "大枣", "quantity": "2枚", "role": "佐"}
  ],
  "effects": ["升阳益胃", "健脾化湿"],
  "indications": ["脾胃虚弱，湿热滞留", "怠惰嗜卧，体重节痛，口苦咽干，饮食无味"],
  "usage": "水煎服",
  "modern_applications": ["慢性胃炎", "慢性肠炎", "疲劳综合征", "水肿"],
  "pharmacological_effect": "升阳益胃汤具有调节胃肠功能、抗炎、增强机体免疫力作用",
  "syndrome_ids": [], "effect_ids": [],
  "beginner_note": "初学者：东垣方，黄芪为君，合柴胡、羌独防升阳，参术苓夏健脾化湿。",
  "advanced_clinical_note": "高级要点：补中有散、升中有降，治脾胃气虚兼夹湿热之证。"
 },
 {
  "id": "formula_363", "name": "调中益气汤", "pinyin": "Tiao Zhong Yi Qi Tang", "category": "补益剂",
  "subcategory": "补气", "source": "《脾胃论》", "author": "李东垣",
  "ingredients": [
    {"medicine_id": "medicine_073", "name": "黄芪", "quantity": "6g", "role": "君"},
    {"medicine_id": "medicine_515", "name": "升麻", "quantity": "3g", "role": "臣"},
    {"medicine_id": "medicine_044", "name": "陈皮", "quantity": "3g", "role": "臣"},
    {"medicine_id": "medicine_045", "name": "木香", "quantity": "1.5g", "role": "佐"},
    {"medicine_id": "medicine_072", "name": "人参", "quantity": "3g", "role": "臣"},
    {"medicine_id": "medicine_512", "name": "炙甘草", "quantity": "3g", "role": "使"},
    {"medicine_id": "medicine_035", "name": "苍术", "quantity": "3g", "role": "佐"},
    {"medicine_id": "medicine_012", "name": "柴胡", "quantity": "3g", "role": "臣"}
  ],
  "effects": ["健脾益气", "升阳除湿"],
  "indications": ["脾胃不调，胸满短气", "肢体怠惰，食欲不振，大便不调"],
  "usage": "水煎服",
  "modern_applications": ["胃肠功能紊乱", "功能性消化不良", "内脏下垂"],
  "pharmacological_effect": "调中益气汤具有促进胃肠动力、调节消化液分泌作用",
  "syndrome_ids": [], "effect_ids": [],
  "beginner_note": "初学者：益气升阳兼理气除湿，与补中益气汤意近而偏于化湿。",
  "advanced_clinical_note": "高级要点：以木香、陈皮理气，苍术燥湿，佐升柴升清，治中气下陷夹湿。"
 },
 {
  "id": "formula_364", "name": "升阳散火汤", "pinyin": "Sheng Yang San Huo Tang", "category": "解表剂",
  "subcategory": "发散风热", "source": "《脾胃论》", "author": "李东垣",
  "ingredients": [
    {"medicine_id": "medicine_515", "name": "升麻", "quantity": "9g", "role": "君"},
    {"medicine_id": "medicine_013", "name": "葛根", "quantity": "9g", "role": "君"},
    {"medicine_id": "medicine_032", "name": "独活", "quantity": "6g", "role": "臣"},
    {"medicine_id": "medicine_318", "name": "羌活", "quantity": "6g", "role": "臣"},
    {"medicine_id": "medicine_077", "name": "白芍", "quantity": "6g", "role": "佐"},
    {"medicine_id": "medicine_072", "name": "人参", "quantity": "6g", "role": "臣"},
    {"medicine_id": "medicine_012", "name": "柴胡", "quantity": "6g", "role": "臣"},
    {"medicine_id": "medicine_006", "name": "防风", "quantity": "6g", "role": "臣"},
    {"medicine_id": "medicine_512", "name": "炙甘草", "quantity": "3g", "role": "使"},
    {"medicine_id": "medicine_004", "name": "生姜", "quantity": "3片", "role": "佐"},
    {"medicine_id": "medicine_372", "name": "大枣", "quantity": "2枚", "role": "佐"},
    {"medicine_id": "medicine_319", "name": "葱白", "quantity": "3茎", "role": "佐"}
  ],
  "effects": ["升阳散火"],
  "indications": ["脾胃气虚，阴火内郁", "发热倦怠，骨蒸劳热，扪之烙手"],
  "usage": "水煎服",
  "modern_applications": ["功能性发热", "慢性低热", "机体免疫力低下"],
  "pharmacological_effect": "升阳散火汤具有解热、抗炎、调节免疫作用",
  "syndrome_ids": [], "effect_ids": [],
  "beginner_note": "初学者：东垣治气虚发热名方，升麻葛根柴胡防风羌独发越阳气以散郁火。",
  "advanced_clinical_note": "高级要点：甘温除热法之一，治气虚阳郁化火之身热，忌用苦寒直折。"
 }
]
formulas.extend(new_formulas)

# ---------- 新增证型 ----------
guitiao = fname2id.get('桂枝汤')
mahuang = fname2id.get('麻黄汤')
new_syns = [
 {
  "id": "syndrome_121", "name": "太阳病", "pinyin": "Tai Yang Bing",
  "category": ["六经辨证", "八纲辨证", "病因辨证", "六淫辨证"],
  "classification": ["表证", "寒证"],
  "diagnosis_points": ["恶寒", "发热", "头项强痛", "脉浮", "苔薄白"],
  "pathogenesis": "风寒外束肌表，卫阳被遏，营阴郁滞，营卫不和",
  "modern_medicine": ["上呼吸道感染", "流行性感冒初期"],
  "related_formulas": [x for x in [mahuang, guitiao] if x],
  "related_needle": [], "related_treatments": [], "related_effects": [],
  "comparison": []
 },
 {
  "id": "syndrome_122", "name": "阳明病", "pinyin": "Yang Ming Bing",
  "category": ["六经辨证", "八纲辨证"],
  "classification": ["里证", "热证", "实证"],
  "diagnosis_points": ["发热不恶寒反恶热", "大汗", "大渴", "脉洪大", "或潮热谵语、腹满硬痛便秘、脉沉实"],
  "pathogenesis": "伤寒化热入里，阳明燥热亢盛，胃肠实热结聚",
  "modern_medicine": ["感染性疾病高热期", "急性腹膜炎", "肠梗阻"],
  "related_formulas": [], "related_needle": [], "related_treatments": [], "related_effects": [],
  "comparison": []
 },
 {
  "id": "syndrome_123", "name": "少阴病", "pinyin": "Shao Yin Bing",
  "category": ["六经辨证", "八纲辨证"],
  "classification": ["里证", "虚证"],
  "diagnosis_points": ["脉微细", "但欲寐", "畏寒肢冷（寒化）", "或心烦不得眠、舌红绛（热化）"],
  "pathogenesis": "心肾虚衰，阴阳气血俱虚，全身正气衰惫",
  "modern_medicine": ["休克", "心力衰竭", "严重感染衰竭期"],
  "related_formulas": [], "related_needle": [], "related_treatments": [], "related_effects": [],
  "comparison": []
 },
 {
  "id": "syndrome_124", "name": "心血虚", "pinyin": "Xin Xue Xu",
  "category": ["脏腑辨证"],
  "classification": ["虚证"],
  "diagnosis_points": ["心悸", "失眠多梦", "健忘", "面色淡白无华", "舌淡", "脉细"],
  "pathogenesis": "久病耗伤，或失血过多，心血亏虚，心神失养",
  "modern_medicine": ["神经衰弱", "心律失常", "贫血"],
  "related_formulas": [], "related_needle": [], "related_treatments": [], "related_effects": [],
  "comparison": []
 },
 {
  "id": "syndrome_125", "name": "心阴虚", "pinyin": "Xin Yin Xu",
  "category": ["脏腑辨证"],
  "classification": ["虚证", "热证"],
  "diagnosis_points": ["心悸", "心烦", "失眠多梦", "口咽干燥", "形体消瘦", "手足心热", "舌红少津", "脉细数"],
  "pathogenesis": "劳神过度或热病伤阴，心阴亏虚，虚火内扰",
  "modern_medicine": ["自主神经功能紊乱", "冠心病", "更年期综合征"],
  "related_formulas": [], "related_needle": [], "related_treatments": [], "related_effects": [],
  "comparison": []
 }
]
syns.extend(new_syns)

save('medicines.json', meds)
save('formulas.json', formulas)
save('syndromes.json', syns)
print('已新增: 药材1(地黄)、方剂6、证型5')
print('桂枝汤 id =', guitiao, ' 麻黄汤 id =', mahuang)
