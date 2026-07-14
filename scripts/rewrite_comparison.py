#!/usr/bin/env python3
"""
重写中西医对照数据：
仅保留 症状 和 病因/病机 对比维度
1. 重组 modern_mapping.json
2. 给 syndromes 添加 structured comparison 字段
"""

import json

data_dir = "assets/data"

# ====================
# Part 1: 重建 modern_mapping.json — 只含 症状 + 病因/病机
# ====================

new_mappings = []

def add_comparison(chinese_term, modern_term, category, comparisons, related_syndrome=None):
    """comparisons: list of {aspect, tcm, western}"""
    # 只保留 症状/病因/病机/病理/机制 维度
    filtered = [c for c in comparisons if c['aspect'] in {'病因', '病理', '病理机制', '病理意义', '机制', '症状', '核心症状'}]
    if not filtered:
        return
    new_mappings.append({
        "id": f"mapping_{len(new_mappings)+1:03d}",
        "chinese_term": chinese_term,
        "modern_term": modern_term,
        "category": category,
        "comparison": filtered,
        "related_syndrome": related_syndrome or ""
    })

# ---- 症状类 ----
add_comparison("恶寒发热", "畏寒伴体温升高 (Chills with Fever)",
    "症状", [
        {"aspect": "病因", "tcm": "外感风寒或风热之邪，正邪交争于肌表", "western": "感染性疾病引起的体温调定点上移，机体骨骼肌收缩产热期"},
        {"aspect": "病理机制", "tcm": "邪犯卫表，卫阳被郁，正气抗邪", "western": "前列腺素E2作用于下丘脑体温调节中枢，引起寒战及血管收缩"},
    ], "syndrome_001")

add_comparison("寒热往来", "间歇性发热/弛张热 (Intermittent Fever)",
    "症状", [
        {"aspect": "病因", "tcm": "邪入少阳，正邪分争于半表半里", "western": "病原体周期性释放入血（疟原虫）或局部感染周期性发作（胆道感染）"},
        {"aspect": "病理机制", "tcm": "少阳气机郁滞，枢机不利", "western": "病原体生命周期导致周期性免疫反应和体温波动"},
    ], "syndrome_020")

add_comparison("日晡潮热", "午后高热/弛张热高峰 (Afternoon Fever Spike)",
    "症状", [
        {"aspect": "病因", "tcm": "阳明腑实，热结肠道", "western": "严重腹腔感染、肠梗阻合并感染的体温高峰"},
        {"aspect": "病理机制", "tcm": "燥屎内结，郁而化热，日晡（申时3-5pm）阳明经气旺", "western": "人体皮质醇昼夜节律导致午后免疫反应强度变化"},
    ], "syndrome_019")

add_comparison("身热不扬", "低热不退/稽留热 (Persistent Low-grade Fever)",
    "症状", [
        {"aspect": "病因", "tcm": "湿热蕴蒸，湿遏热伏", "western": "结核菌、慢性病原体、肿瘤等引起的持续性低度炎症"},
        {"aspect": "病理机制", "tcm": "湿热交蒸，热为湿遏，不得外透", "western": "慢性炎症导致的持续性低度发热，炎症因子持续释放"},
    ], "syndrome_007")

add_comparison("五心烦热", "手足心及胸中发热感 (Palmar/Plantar/Chest Heat Sensation)",
    "症状", [
        {"aspect": "病因", "tcm": "阴虚内热，虚火上扰", "western": "植物神经功能紊乱导致的末梢血管扩张"},
        {"aspect": "病理机制", "tcm": "阴液亏损，阴不制阳，虚热内生", "western": "交感-副交感平衡失调，常见于更年期综合征、甲亢"},
    ], "syndrome_009")

add_comparison("自汗", "白天不活动即出汗 (Spontaneous Sweating)",
    "症状", [
        {"aspect": "病因", "tcm": "表虚卫气不固，腠理疏松", "western": "自主神经功能失调导致汗腺过度分泌"},
        {"aspect": "病理机制", "tcm": "肺气亏虚，卫外不固，津液外泄", "western": "交感神经张力增高→胆碱能纤维过度激活→汗腺分泌亢进"},
    ], "syndrome_003")

add_comparison("盗汗", "夜间睡眠时出汗 (Night Sweats)",
    "症状", [
        {"aspect": "病因", "tcm": "阴虚内热，入睡后卫阳入里，虚热迫津外出", "western": "结核病、淋巴瘤等消耗性疾病的夜间体温调节异常"},
        {"aspect": "病理机制", "tcm": "阳气入阴，虚热内生，迫津外泄", "western": "褪黑素/皮质醇节律异常导致夜间体温调节失调"},
    ], "syndrome_009")

add_comparison("头痛如裹", "压迫性头痛/紧张性头痛 (Tension-type Headache)",
    "症状", [
        {"aspect": "病因", "tcm": "湿邪困阻清阳，清窍被蒙", "western": "颅周肌肉持续收缩，肌筋膜触发点形成"},
        {"aspect": "病理机制", "tcm": "清阳不升，浊阴不降，湿浊上蒙", "western": "颅周肌肉缺血+致痛物质释放→中枢敏化"},
    ], "syndrome_033")

add_comparison("刺痛固定不移", "固定性锐痛/神经卡压性疼痛 (Fixed Sharp Pain)",
    "症状", [
        {"aspect": "病因", "tcm": "瘀血内停，经络阻滞", "western": "局部组织缺血、神经卡压、代谢产物堆积"},
        {"aspect": "病理机制", "tcm": "血行不畅，离经之血停积", "western": "微循环障碍、血小板聚集、炎症介质释放"},
    ], "syndrome_008")

add_comparison("胀痛走窜", "游走性胀痛/功能性疼痛 (Migratory Distending Pain)",
    "症状", [
        {"aspect": "病因", "tcm": "气机郁滞，气行不畅", "western": "平滑肌痉挛、胃肠蠕动异常"},
        {"aspect": "病理机制", "tcm": "肝气郁结，气滞不通则痛", "western": "平滑肌异常收缩导致管腔压力增高"},
    ], "syndrome_004")

add_comparison("冷痛得热则减", "遇冷加重遇热缓解的冷痛 (Cold-aggravated Pain)",
    "症状", [
        {"aspect": "病因", "tcm": "寒邪凝滞，阳气被遏", "western": "低温导致血管收缩、局部血流减少"},
        {"aspect": "病理机制", "tcm": "寒主收引，气血凝涩", "western": "血管痉挛导致缺血性疼痛（雷诺综合征）"},
    ], "syndrome_028")

add_comparison("胸痛彻背", "放射至背部的胸痛 (Chest Pain Radiating to Back)",
    "症状", [
        {"aspect": "病因", "tcm": "胸阳不振，痰瘀痹阻", "western": "心肌缺血导致的内脏牵涉痛"},
        {"aspect": "病理机制", "tcm": "心脉痹阻，不通则痛", "western": "冠脉狭窄导致心肌供氧不足，通过脊髓节段放射至背部"},
    ], "syndrome_029")

add_comparison("口苦咽干", "口苦口干 (Bitter Taste & Dry Throat)",
    "症状", [
        {"aspect": "病因", "tcm": "少阳胆火上炎，灼伤津液", "western": "胆汁反流、口腔菌群失衡、唾液分泌减少"},
        {"aspect": "病理机制", "tcm": "胆气上逆，胆汁味苦", "western": "胆汁酸反流至口腔或药物副作用导致味觉异常"},
    ], "syndrome_020")

# ---- 疾病/证型类（只保留 病因+病理+症状） ----
add_comparison("风寒感冒", "普通感冒 (Common Cold)",
    "疾病", [
        {"aspect": "病因", "tcm": "风寒之邪外束肌表，卫阳被郁", "western": "鼻病毒(Rhinovirus)、冠状病毒(Coronavirus)等上呼吸道病毒感染"},
        {"aspect": "病理", "tcm": "风寒束表，肺气失宣，腠理闭塞", "western": "病毒侵入上呼吸道黏膜上皮细胞，引发局部炎症反应"},
        {"aspect": "症状", "tcm": "恶寒重发热轻，无汗，头痛身痛，鼻塞流清涕", "western": "畏寒、低热(<38.5℃)、肌痛、鼻塞、水样鼻涕"},
    ], "syndrome_001")

add_comparison("风热感冒", "流感/急性咽喉炎 (Influenza / Acute Pharyngitis)",
    "疾病", [
        {"aspect": "病因", "tcm": "风热之邪侵袭肺卫", "western": "流感病毒(Influenza virus)、腺病毒等感染"},
        {"aspect": "病理", "tcm": "风热上受，首先犯肺，热邪内郁", "western": "病毒引起强烈免疫应答，释放大量炎症因子"},
        {"aspect": "症状", "tcm": "发热重恶寒轻，汗出，咽红肿痛，黄涕黄痰", "western": "高热(>39℃)、咽痛充血、脓涕、全身肌痛"},
    ], "syndrome_002")

add_comparison("脾胃虚弱", "功能性消化不良 (Functional Dyspepsia)",
    "疾病", [
        {"aspect": "病因", "tcm": "饮食不节、劳倦过度、思虑伤脾", "western": "胃肠动力障碍、内脏高敏感性、精神心理因素"},
        {"aspect": "病理", "tcm": "脾气虚弱，运化失职，升降失常", "western": "胃排空延迟、胃容受性舒张障碍、十二指肠炎症"},
        {"aspect": "症状", "tcm": "食少腹胀、便溏、倦怠乏力、面色萎黄", "western": "餐后饱胀、早饱、上腹痛/烧灼感、恶心"},
    ], "syndrome_003")

add_comparison("肝郁气滞", "焦虑/躯体化障碍 (Anxiety / Somatization Disorder)",
    "疾病", [
        {"aspect": "病因", "tcm": "情志抑郁、怒伤肝、气机郁滞", "western": "慢性应激、神经递质失衡（5-HT、NE）、心理社会因素"},
        {"aspect": "病理", "tcm": "肝失疏泄，气机郁结，横逆犯脾", "western": "HPA轴过度激活、自主神经功能紊乱、内脏高敏"},
        {"aspect": "症状", "tcm": "胸胁胀痛、善太息、烦躁易怒、月经不调", "western": "胸闷心悸、过度换气、肠易激、经前期综合征"},
    ], "syndrome_004")

add_comparison("肾阳虚", "肾上腺皮质功能减退/性腺功能低下 (Adrenal/Gonadal Insufficiency)",
    "疾病", [
        {"aspect": "病因", "tcm": "先天不足、房劳过度、久病伤阳", "western": "肾上腺皮质功能减退、性腺功能低下（睾酮下降）"},
        {"aspect": "病理", "tcm": "肾阳不足，温煦失职，气化无权", "western": "皮质醇/醛固酮分泌不足致代谢率下降；雄激素下降"},
        {"aspect": "症状", "tcm": "畏寒肢冷、腰膝酸软、夜尿多、阳痿早泄", "western": "怕冷、乏力、低血压、性欲减退、夜尿增多"},
    ], "syndrome_005")

add_comparison("阴虚火旺", "更年期综合征/自主神经紊乱 (Menopausal Syndrome)",
    "疾病", [
        {"aspect": "病因", "tcm": "阴液亏损，阴不制阳，虚火上炎", "western": "雌激素水平急剧下降，下丘脑-垂体-卵巢轴失衡"},
        {"aspect": "病理", "tcm": "阴虚生内热，虚火扰动心神", "western": "雌激素撤退导致血管舒缩不稳定、5-HT波动"},
        {"aspect": "症状", "tcm": "潮热盗汗、五心烦热、口干咽燥、失眠多梦", "western": "潮热(Hot Flashes)、夜间出汗、心悸、情绪波动"},
    ], "syndrome_009")

add_comparison("痰湿内阻", "代谢综合征 (Metabolic Syndrome)",
    "疾病", [
        {"aspect": "病因", "tcm": "饮食不节、过食肥甘、脾失运化", "western": "能量摄入过剩、缺乏运动、遗传因素"},
        {"aspect": "病理", "tcm": "脾虚生湿，湿聚成痰，痰湿困脾", "western": "胰岛素抵抗、内脏脂肪堆积、慢性低度炎症"},
        {"aspect": "症状", "tcm": "形体肥胖、胸闷痰多、肢体困重、舌苔白腻", "western": "腹型肥胖、高血压、高血糖、血脂异常"},
    ], "syndrome_007")

add_comparison("血瘀证", "微循环障碍/高凝状态 (Microcirculatory Disorder/Hypercoagulability)",
    "疾病", [
        {"aspect": "病因", "tcm": "气滞、寒凝、气虚、外伤导致血行不畅", "western": "血管内皮损伤、血液流变学异常、凝血功能亢进"},
        {"aspect": "病理", "tcm": "离经之血停积，脉道不利", "western": "血小板聚集增多、纤维蛋白溶解减少、血液黏度增高"},
        {"aspect": "症状", "tcm": "舌紫暗瘀斑、肌肤甲错、脉涩、刺痛固定不移", "western": "皮肤紫癜、微循环显微镜下血流缓慢停滞、局部缺血性疼痛"},
    ], "syndrome_008")

add_comparison("阳明腑实证", "肠梗阻/急性腹症 (Intestinal Obstruction/Acute Abdomen)",
    "疾病", [
        {"aspect": "病因", "tcm": "热邪入里，与肠中糟粕相结", "western": "机械性肠梗阻、麻痹性肠梗阻、腹腔感染"},
        {"aspect": "病理", "tcm": "阳明腑实，燥屎内结，气机不通", "western": "肠管扩张、肠壁水肿、肠蠕动减弱或消失"},
        {"aspect": "症状", "tcm": "日晡潮热、大便秘结、腹胀满痛拒按、谵语", "western": "腹痛腹胀、停止排气排便、呕吐、发热"},
    ], "syndrome_019")

add_comparison("黄疸", "黄疸/高胆红素血症 (Jaundice/Hyperbilirubinemia)",
    "疾病", [
        {"aspect": "病因", "tcm": "湿热蕴结肝胆，胆汁外溢肌肤", "western": "肝细胞损伤、胆道梗阻、溶血导致胆红素代谢异常"},
        {"aspect": "病理", "tcm": "湿热交蒸，胆汁不循常道，溢于肌肤", "western": "肝细胞处理胆红素能力下降或胆道排泄障碍"},
        {"aspect": "症状", "tcm": "目黄、身黄、小便黄", "western": "巩膜黄染(Scleral Icterus)、皮肤黄染、尿胆红素↑"},
    ], "syndrome_030")

# ---- 心理类（只保留 病因+机制） ----
add_comparison("烦躁", "烦躁不安 (Agitation/Restlessness)",
    "心理", [
        {"aspect": "病因", "tcm": "热扰心神、肝郁化火、阴虚火旺", "western": "神经递质失衡（NE↑、GABA↓）、急性应激反应"},
        {"aspect": "机制", "tcm": "心主神明功能失常", "western": "交感神经过度激活、杏仁核过度反应"},
    ])

add_comparison("惊悸", "心悸/惊恐发作 (Palpitations/Panic Attack)",
    "心理", [
        {"aspect": "病因", "tcm": "心胆气虚、心脾两虚、水饮凌心", "western": "心律失常、焦虑障碍、二尖瓣脱垂"},
        {"aspect": "机制", "tcm": "心神不宁，惊则气乱", "western": "交感神经骤然兴奋→心率加快、过度换气→恐慌循环"},
    ], "syndrome_013")

add_comparison("抑郁寡欢", "抑郁状态 (Depression)",
    "心理", [
        {"aspect": "病因", "tcm": "肝气郁结，气机不畅，久郁伤神", "western": "5-HT/NE/DA神经递质不足、慢性应激、遗传易感性"},
        {"aspect": "症状", "tcm": "情绪低落、兴趣减退、善太息、不思饮食", "western": "快感缺失(Anhedonia)、食欲减退、睡眠障碍、疲乏"},
    ], "syndrome_004")

# ====================
# Save modern_mapping.json
# ====================
with open(f"{data_dir}/modern_mapping.json", "w", encoding="utf-8") as f:
    json.dump(new_mappings, f, ensure_ascii=False, indent=2)

print(f"✅ modern_mapping.json: {len(new_mappings)} 条对照数据（仅症状+病因病机）")
cats = {}
for m in new_mappings:
    c = m['category']
    cats[c] = cats.get(c, 0) + 1
for c, n in sorted(cats.items()):
    print(f"  {c}: {n} 条")

# ====================
# Part 2: Add comparison to syndromes（只保留 病因+病理+核心症状）
# ====================
with open(f"{data_dir}/syndromes.json", encoding="utf-8") as f:
    syndromes = json.load(f)

comparison_map = {
    "syndrome_001": [
        {"aspect": "病因", "tcm": "风寒之邪外束肌表，卫阳被郁", "western": "鼻病毒(Rhinovirus)、冠状病毒等上呼吸道病毒感染"},
        {"aspect": "病理", "tcm": "风寒束表，肺气失宣，腠理闭塞", "western": "病毒侵入上呼吸道黏膜上皮细胞，引发局部炎症反应和免疫应答"},
        {"aspect": "核心症状", "tcm": "恶寒重发热轻、无汗、头身疼痛、鼻塞流清涕", "western": "畏寒、低热(<38.5℃)、肌痛(Myalgia)、鼻塞、水样鼻涕(Rhinorrhea)"},
    ],
    "syndrome_002": [
        {"aspect": "病因", "tcm": "风热之邪侵袭肺卫", "western": "流感病毒(Influenza virus)、腺病毒(Adenovirus)等"},
        {"aspect": "病理", "tcm": "风热上受，首先犯肺，热邪内郁", "western": "病毒诱发强烈免疫应答，炎症因子风暴(Cytokine Storm)"},
        {"aspect": "核心症状", "tcm": "发热重恶寒轻、汗出、咽喉红肿痛、黄涕黄痰", "western": "高热>39℃、咽部充血(Hyperemia)、脓涕、全身肌痛"},
    ],
    "syndrome_003": [
        {"aspect": "病因", "tcm": "饮食不节、劳倦过度、思虑伤脾", "western": "胃肠动力障碍、内脏高敏感性、HPA轴失调"},
        {"aspect": "病理", "tcm": "脾气虚弱，运化失职，升降失常", "western": "胃排空延迟(Delayed Gastric Emptying)、胃容受性舒张障碍"},
        {"aspect": "核心症状", "tcm": "食少腹胀、便溏、倦怠乏力、面色萎黄", "western": "餐后饱胀(Postprandial Fullness)、早饱(Early Satiety)、上腹痛"},
    ],
    "syndrome_004": [
        {"aspect": "病因", "tcm": "情志抑郁、怒伤肝、气机郁滞", "western": "慢性应激、5-HT/NE失衡、心理社会因素"},
        {"aspect": "病理", "tcm": "肝失疏泄，气机郁结，横逆犯脾", "western": "HPA轴过度激活(Hypercortisolism)、自主神经功能紊乱(Autonomic Dysfunction)"},
        {"aspect": "核心症状", "tcm": "胸胁胀痛、善太息、烦躁易怒、月经不调", "western": "胸闷心悸、过度换气(Hyperventilation)、肠易激(IBS)、PMS"},
    ],
    "syndrome_005": [
        {"aspect": "病因", "tcm": "先天不足、房劳过度、久病伤阳", "western": "下丘脑-垂体-肾上腺/性腺轴功能减退"},
        {"aspect": "病理", "tcm": "肾阳不足，温煦失职，气化无权", "western": "皮质醇↓/醛固酮↓→代谢率下降；睾酮↓→性功能减退"},
        {"aspect": "核心症状", "tcm": "畏寒肢冷、腰膝酸软、夜尿多、阳痿早泄", "western": "怕冷、乏力(Fatigue)、低血压、性欲减退(Libido↓)、夜尿(Nocturia)"},
    ],
    "syndrome_007": [
        {"aspect": "病因", "tcm": "饮食不节、过食肥甘、脾失运化", "western": "能量摄入过剩、久坐、遗传(Genetic Predisposition)"},
        {"aspect": "病理", "tcm": "脾虚生湿，湿聚成痰，痰湿困脾", "western": "胰岛素抵抗(Insulin Resistance)、内脏脂肪堆积、慢性低度炎症"},
        {"aspect": "核心症状", "tcm": "形体肥胖、胸闷痰多、肢体困重", "western": "腹型肥胖(Central Obesity)、高血压、高血糖、血脂异常(Dyslipidemia)"},
    ],
    "syndrome_008": [
        {"aspect": "病因", "tcm": "气滞、寒凝、气虚、外伤致血行不畅", "western": "血管内皮损伤(Endothelial Injury)、血液流变学异常"},
        {"aspect": "病理", "tcm": "离经之血停积，脉道不利", "western": "血小板聚集(Platelet Aggregation)、纤维蛋白溶解↓、血液黏度↑"},
        {"aspect": "核心症状", "tcm": "舌紫暗瘀斑、肌肤甲错、脉涩、刺痛固定不移", "western": "微循环障碍、皮肤瘀斑(Ecchymosis)或紫癜(Purpura)、局部缺血性疼痛"},
    ],
    "syndrome_009": [
        {"aspect": "病因", "tcm": "阴液亏损，阴不制阳，虚火上炎", "western": "雌激素水平急剧下降(Estrogen Withdrawal)"},
        {"aspect": "病理", "tcm": "阴虚生内热，虚火扰动心神", "western": "血管舒缩不稳定(Vasomotor Instability)、5-HT波动"},
        {"aspect": "核心症状", "tcm": "潮热盗汗、五心烦热、口干咽燥", "western": "潮热(Hot Flashes)、夜间出汗、心悸(Palpitations)"},
    ],
    "syndrome_019": [
        {"aspect": "病因", "tcm": "热邪入里，与肠中糟粕相结", "western": "肠梗阻(Intestinal Obstruction)、严重腹腔感染"},
        {"aspect": "病理", "tcm": "阳明腑实，燥屎内结，气机不通", "western": "肠管扩张、肠壁水肿、蠕动减弱或消失"},
        {"aspect": "核心症状", "tcm": "日晡潮热、便秘、腹满痛拒按", "western": "腹痛腹胀、停止排气排便、呕吐、发热>38.5℃"},
    ],
    "syndrome_029": [
        {"aspect": "病因", "tcm": "胸阳不振，痰瘀痹阻心脉", "western": "冠状动脉粥样硬化(Atherosclerosis)→管腔狭窄"},
        {"aspect": "病理", "tcm": "心脉痹阻，不通则痛", "western": "心肌氧供需失衡→缺血→代谢产物堆积刺激神经末梢"},
        {"aspect": "核心症状", "tcm": "胸痛彻背、胸闷气短、心悸", "western": "胸骨后压榨性疼痛放射至左肩/背(Angina Pectoris)"},
    ],
    "syndrome_030": [
        {"aspect": "病因", "tcm": "湿热蕴结肝胆，胆汁外溢", "western": "肝细胞损伤/胆道梗阻→胆红素代谢异常(Hyperbilirubinemia)"},
        {"aspect": "病理", "tcm": "湿热交蒸，胆汁不循常道，溢于肌肤", "western": "肝细胞处理胆红素能力下降或胆道排泄障碍"},
        {"aspect": "核心症状", "tcm": "目黄、身黄、小便黄", "western": "巩膜黄染(Scleral Icterus)、皮肤黄染、尿胆红素↑"},
    ],
    "syndrome_033": [
        {"aspect": "病因", "tcm": "暑湿外袭，湿困肌表", "western": "高温高湿环境导致体温调节障碍"},
        {"aspect": "病理", "tcm": "湿性重浊黏滞，困阻清阳", "western": "脱水+电解质紊乱→肌肉痉挛、头痛、乏力"},
    ],
}

for s in syndromes:
    sid = s["id"]
    if sid in comparison_map:
        s["comparison"] = comparison_map[sid]
    # 对于不在 comparison_map 中的证型：保留已有的 comparison（由 enrich_data.py 添加的），
    # 只删除确实没有 comparison 的条目
    elif "comparison" not in s or not s.get("comparison"):
        s.pop("comparison", None)
    s.pop("modern_explanation", None)

with open(f"{data_dir}/syndromes.json", "w", encoding="utf-8") as f:
    json.dump(syndromes, f, ensure_ascii=False, indent=2)

print(f"\n✅ syndromes.json: {len(syndromes)} 条，已为 {len(comparison_map)} 条添加 症状+病因病机 对照")
print("完成！")
