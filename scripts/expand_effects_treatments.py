#!/usr/bin/env python3
"""扩展功效和治法，与新增证型/针方配套"""
import json, os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'data')

# === 扩展功效 ===
with open(os.path.join(DATA_DIR, 'effects.json')) as f:
    effects = json.load(f)

max_eff = max(int(e['id'].replace('effect_', '')) for e in effects)

new_effects = [
    {"id": f"effect_{max_eff+1:03d}", "name": "清热凉血", "description": "清除热邪并凉血清营的治疗作用",
     "mechanism": "通过药物的苦寒清热及凉血作用，清除营分、血分之热邪",
     "indications": ["热入营血", "斑疹吐衄", "邪热迫血", "舌绛脉数"],
     "related_medicines": [], "related_formulas": [], "related_syndromes": []},
    {"id": f"effect_{max_eff+2:03d}", "name": "益气固表", "description": "补益正气，巩固肌表防卫功能的治疗作用",
     "mechanism": "通过补气药物的温补作用，增强卫外功能，防止外邪侵入",
     "indications": ["自汗", "表虚不固", "反复感冒", "恶风"],
     "related_medicines": [], "related_formulas": [], "related_syndromes": []},
    {"id": f"effect_{max_eff+3:03d}", "name": "镇肝熄风", "description": "平镇肝阳上亢，熄风止痉的治疗作用",
     "mechanism": "通过重镇和清降药物，平定上亢之肝阳，制止内风扰动",
     "indications": ["肝阳上亢", "高血压", "头痛眩晕", "中风先兆"],
     "related_medicines": [], "related_formulas": [], "related_syndromes": []},
    {"id": f"effect_{max_eff+4:03d}", "name": "祛风除湿通络", "description": "祛除风湿，疏通经络的复合治疗作用",
     "mechanism": "通过药物的辛散走窜和祛湿作用，清除关节经络之风寒湿邪并通经活络",
     "indications": ["痹证", "关节疼痛", "肢体麻木", "屈伸不利"],
     "related_medicines": [], "related_formulas": [], "related_syndromes": []},
    {"id": f"effect_{max_eff+5:03d}", "name": "养心安神", "description": "滋养心血、安定心神的治疗作用",
     "mechanism": "通过药物的甘润滋养作用，补养心血，安定神志",
     "indications": ["心悸失眠", "虚烦不寐", "多梦易醒", "健忘"],
     "related_medicines": [], "related_formulas": [], "related_syndromes": []},
    {"id": f"effect_{max_eff+6:03d}", "name": "固肾涩精", "description": "固摄肾气，收涩精关的治疗作用",
     "mechanism": "通过收涩药物的固摄作用，增强肾气封藏功能，防止精液滑泄",
     "indications": ["遗精滑泄", "小便频数", "带下过多", "遗尿"],
     "related_medicines": [], "related_formulas": [], "related_syndromes": []},
    {"id": f"effect_{max_eff+7:03d}", "name": "宣畅气机", "description": "宣通调畅全身气机升降出入的治疗作用",
     "mechanism": "通过药物的辛开苦降作用，恢复气机的正常升降出入",
     "indications": ["胸闷脘痞", "气机不畅", "湿温发热", "呕恶不食"],
     "related_medicines": [], "related_formulas": [], "related_syndromes": []},
    {"id": f"effect_{max_eff+8:03d}", "name": "消痈散结", "description": "消除痈肿，消散结块的治疗作用",
     "mechanism": "通过药物的清热解毒和活血散结作用，使痈肿消散",
     "indications": ["痈疡肿毒", "红肿热痛", "瘰疬", "乳腺炎"],
     "related_medicines": [], "related_formulas": [], "related_syndromes": []},
    {"id": f"effect_{max_eff+9:03d}", "name": "豁痰开窍", "description": "化散痰浊，开窍醒神的治疗作用",
     "mechanism": "通过药物的化痰和芳香开窍作用，清除痰浊蒙蔽，恢复神志清醒",
     "indications": ["痰蒙心窍", "神昏谵语", "癫痫", "中风昏迷"],
     "related_medicines": [], "related_formulas": [], "related_syndromes": []},
    {"id": f"effect_{max_eff+10:03d}", "name": "升阳举陷", "description": "升举阳气，提振下陷的脏腑之气",
     "mechanism": "通过补气兼升提的药物，将下陷之气提升复位",
     "indications": ["中气下陷", "脱肛", "子宫脱垂", "胃下垂", "久泻"],
     "related_medicines": [], "related_formulas": [], "related_syndromes": []},
    {"id": f"effect_{max_eff+11:03d}", "name": "温经散寒通脉", "description": "温通经脉、驱散寒邪、畅通血脉的复合作用",
     "mechanism": "通过辛温药物温通十二经脉，驱散寒邪，使血脉通畅",
     "indications": ["血虚寒厥", "手足厥冷", "痛经", "冻疮"],
     "related_medicines": [], "related_formulas": [], "related_syndromes": []},
    {"id": f"effect_{max_eff+12:03d}", "name": "熄风止痉", "description": "平息内风、制止抽搐的治疗作用",
     "mechanism": "通过平肝息风药物的镇静作用，制止肝风内动所致的抽搐痉挛",
     "indications": ["痉厥抽搐", "小儿惊风", "癫痫", "高热惊厥"],
     "related_medicines": [], "related_formulas": [], "related_syndromes": []},
    {"id": f"effect_{max_eff+13:03d}", "name": "清热化湿", "description": "清除热邪兼化湿邪的治疗作用",
     "mechanism": "通过清热药与化湿药的配伍，同时清除湿热之邪",
     "indications": ["湿热内蕴", "身热不扬", "口渴不欲饮", "脘痞呕恶"],
     "related_medicines": [], "related_formulas": [], "related_syndromes": []},
]

for e in new_effects:
    effects.append(e)

for i, e in enumerate(effects, 1):
    e['id'] = f"effect_{i:03d}"

with open(os.path.join(DATA_DIR, 'effects.json'), 'w', encoding='utf-8') as f:
    json.dump(effects, f, ensure_ascii=False, indent=2)

print(f"功效：{len(effects) - len(new_effects)} → {len(effects)}（新增 {len(new_effects)} 条）")

# === 扩展治法 ===
with open(os.path.join(DATA_DIR, 'treatments.json')) as f:
    treatments = json.load(f)

max_treat = max(int(t['id'].replace('treatment_', '')) for t in treatments)

new_treatments = [
    {"id": f"treatment_{max_treat+1:03d}", "name": "清营凉血法",
     "category": "清热法", "principle": "清泄营分热邪，凉散血分瘀热",
     "indications": ["热入营血", "高热烦躁", "斑疹吐衄", "神昏谵语"],
     "methods": ["药物治疗：清营汤", "针刺治疗：大椎放血、曲池、十宣"],
     "modern_explanation": "清营凉血法通过抗炎、降体温、改善微循环、防止DIC等机制治疗重症感染",
     "related_syndromes": [], "related_formulas": [], "related_needle": []},
    {"id": f"treatment_{max_treat+2:03d}", "name": "益气固表法",
     "category": "补益法", "principle": "补益正气，增强肌表防御功能",
     "indications": ["表虚自汗", "反复感冒", "恶风", "过敏性鼻炎"],
     "methods": ["药物治疗：玉屏风散", "针刺治疗：足三里、关元、气海"],
     "modern_explanation": "益气固表法通过调节免疫功能、增强呼吸道黏膜防御来预防感染性疾病",
     "related_syndromes": [], "related_formulas": [], "related_needle": []},
    {"id": f"treatment_{max_treat+3:03d}", "name": "镇肝熄风法",
     "category": "治风法", "principle": "平镇肝阳，熄风止痉",
     "indications": ["肝阳上亢", "中风先兆", "头痛眩晕", "高血压"],
     "methods": ["药物治疗：镇肝熄风汤、天麻钩藤饮", "针刺治疗：太冲、风池、百会"],
     "modern_explanation": "镇肝熄风法通过降血压、改善脑循环、镇静安神来防治脑血管意外",
     "related_syndromes": [], "related_formulas": [], "related_needle": []},
    {"id": f"treatment_{max_treat+4:03d}", "name": "祛风胜湿法",
     "category": "祛湿法", "principle": "祛除风湿之邪，蠲痹通络止痛",
     "indications": ["风湿痹证", "关节疼痛", "筋脉拘挛", "腰膝冷痛"],
     "methods": ["药物治疗：独活寄生汤、羌活胜湿汤", "针刺治疗：阳陵泉、足三里、阿是穴"],
     "modern_explanation": "祛风胜湿法通过抗炎镇痛、改善关节功能、调节免疫来治疗风湿类疾病",
     "related_syndromes": [], "related_formulas": [], "related_needle": []},
    {"id": f"treatment_{max_treat+5:03d}", "name": "豁痰开窍法",
     "category": "开窍法", "principle": "化散痰浊，开窍醒神",
     "indications": ["痰蒙心窍", "中风昏迷", "癫痫", "热闭神昏"],
     "methods": ["药物治疗：安宫牛黄丸、紫雪丹", "针刺治疗：人中、十宣放血、涌泉"],
     "modern_explanation": "豁痰开窍法通过保护脑细胞、抗惊厥、降颅内压等机制治疗昏迷和脑损伤",
     "related_syndromes": [], "related_formulas": [], "related_needle": []},
    {"id": f"treatment_{max_treat+6:03d}", "name": "健脾利湿法",
     "category": "祛湿法", "principle": "健脾运湿，利水消肿",
     "indications": ["脾虚水肿", "小便不利", "腹胀泄泻", "湿困脾胃"],
     "methods": ["药物治疗：参苓白术散、五苓散", "针刺治疗：阴陵泉、三阴交、足三里"],
     "modern_explanation": "健脾利湿法通过调节水盐代谢、促进肾脏排尿、改善消化功能来治疗水湿内停",
     "related_syndromes": [], "related_formulas": [], "related_needle": []},
    {"id": f"treatment_{max_treat+7:03d}", "name": "活血通窍法",
     "category": "理血法", "principle": "活血化瘀，通利清窍",
     "indications": ["瘀阻头面", "头痛不愈", "耳聋", "脱发"],
     "methods": ["药物治疗：通窍活血汤", "针刺治疗：百会、风池、血海"],
     "modern_explanation": "活血通窍法通过改善头部微循环、促进神经修复来治疗头面部瘀血性疾病",
     "related_syndromes": [], "related_formulas": [], "related_needle": []},
]

for t in new_treatments:
    treatments.append(t)

for i, t in enumerate(treatments, 1):
    t['id'] = f"treatment_{i:03d}"

with open(os.path.join(DATA_DIR, 'treatments.json'), 'w', encoding='utf-8') as f:
    json.dump(treatments, f, ensure_ascii=False, indent=2)

print(f"治法：{len(treatments) - len(new_treatments)} → {len(treatments)}（新增 {len(new_treatments)} 条）")
