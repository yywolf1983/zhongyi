#!/usr/bin/env python3
"""完善辨证分类+扩展证型：增加卫气营血/三焦/气血津液/经络辨证分类及新证型"""
import json, os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'data')

with open(os.path.join(DATA_DIR, 'syndromes.json')) as f:
    existing = json.load(f)

# 更新现有证型的分类，添加更细致的辨证分类标签
# 映射：syndrome_id -> 新增分类标签
classification_updates = {
    "syndrome_001": ["六淫辨证", "经络辨证"],  # 风寒感冒
    "syndrome_002": ["六淫辨证"],  # 风热感冒
    "syndrome_007": ["气血津液辨证"],  # 痰湿内阻
    "syndrome_008": ["气血津液辨证"],  # 气滞血瘀
    "syndrome_009": ["气血津液辨证"],  # 阴虚火旺
    "syndrome_010": ["气血津液辨证"],  # 血虚
    "syndrome_015": ["气血津液辨证"],  # 气虚血瘀
    "syndrome_027": ["经络辨证"],  # 行痹
    "syndrome_028": ["经络辨证"],  # 痛痹
    "syndrome_031": ["三焦辨证"],  # 水肿·风水
    "syndrome_034": ["三焦辨证"],  # 消渴·上消
    "syndrome_035": ["经络辨证"],  # 中风·中经络
    "syndrome_036": ["六淫辨证"],  # 咳嗽·风寒
    "syndrome_037": ["六淫辨证"],  # 咳嗽·痰热
    "syndrome_042": ["六淫辨证", "经络辨证"],  # 头痛·风寒
    "syndrome_043": ["经络辨证"],  # 头痛·肝阳
    "syndrome_044": ["六淫辨证", "经络辨证"],  # 腰痛·寒湿
    "syndrome_047": ["三焦辨证"],  # 淋证·热淋
    "syndrome_048": ["经络辨证"],  # 痿证
    "syndrome_049": ["六淫辨证"],  # 哮病·冷哮
}

for s in existing:
    sid = s['id']
    if sid in classification_updates:
        for cat in classification_updates[sid]:
            if cat not in s['category']:
                s['category'].append(cat)

# 新增证型：卫气营血辨证 + 三焦辨证 + 更多脏腑/经络辨证
max_id = max(int(s['id'].replace('syndrome_', '')) for s in existing)
sid = max_id

new_syndromes = []

def add_syndrome(name, pinyin, category, classification, diagnosis, pathogenesis, modern_med, modern_exp, formulas, needles, treatments, effects):
    global sid
    sid += 1
    return {
        "id": f"syndrome_{sid:03d}",
        "name": name, "pinyin": pinyin,
        "category": category,
        "classification": classification,
        "diagnosis_points": diagnosis,
        "pathogenesis": pathogenesis,
        "modern_medicine": modern_med,
        "modern_explanation": modern_exp,
        "related_formulas": formulas,
        "related_needle": needles,
        "related_treatments": treatments,
        "related_effects": effects
    }

# === 卫气营血辨证 ===
new_syndromes.append(add_syndrome(
    "卫分证", "Wei Fen Zheng",
    ["卫气营血辨证"], ["表证", "热证"],
    ["发热", "微恶风寒", "头痛", "无汗或少汗", "咳嗽", "咽痛", "舌边尖红", "脉浮数"],
    "温邪袭表，卫气被郁，肺失宣降",
    ["上呼吸道感染", "急性扁桃体炎", "流行性感冒初期"],
    "卫分证是温病初起，邪在肺卫的病理阶段，与现代医学中的急性上呼吸道感染早期相似",
    ["formula_003", "formula_004"], ["needle_002"], ["treatment_002"], ["effect_002"]
))
new_syndromes.append(add_syndrome(
    "气分证", "Qi Fen Zheng",
    ["卫气营血辨证"], ["里证", "热证", "实证"],
    ["大热", "大汗", "大渴", "脉洪大", "面赤心烦", "舌红苔黄燥"],
    "温邪由表入里，邪正剧争，热炽气分",
    ["重症感染高热期", "中暑", "败血症"],
    "气分证是热邪入里的高热阶段，与现代医学中的严重感染高热期相似",
    ["formula_006", "formula_005"], ["needle_019"], ["treatment_019"], ["effect_020"]
))
new_syndromes.append(add_syndrome(
    "营分证", "Ying Fen Zheng",
    ["卫气营血辨证"], ["里证", "热证"],
    ["身热夜甚", "心烦不寐", "斑疹隐隐", "时有谵语", "舌绛", "脉细数"],
    "热邪深入营分，灼伤营阴，扰乱心神",
    ["败血症", "感染性休克早期", "重症传染性疾病"],
    "营分证是热邪深入营阴的危重阶段，与现代医学中的败血症相似",
    ["formula_003"], ["needle_002", "needle_019"], ["treatment_009"], ["effect_002", "effect_010"]
))
new_syndromes.append(add_syndrome(
    "血分证", "Xue Fen Zheng",
    ["卫气营血辨证"], ["里证", "热证", "实证"],
    ["持续高热", "躁扰如狂", "斑疹透露", "吐血衄血", "便血尿血", "舌深绛", "脉弦数"],
    "热入血分，迫血妄行，心神被扰",
    ["弥散性血管内凝血", "脑炎脑膜炎", "败血症晚期"],
    "血分证是温病最深重的阶段，与现代医学中的DIC、重症感染末期相似",
    ["formula_014"], ["needle_019", "needle_012"], ["treatment_019"], ["effect_020", "effect_009"]
))

# === 三焦辨证 ===
new_syndromes.append(add_syndrome(
    "上焦湿热", "Shang Jiao Shi Re",
    ["三焦辨证"], ["表证", "实证", "热证"],
    ["恶寒发热", "身热不扬", "头身重痛", "胸闷脘痞", "不渴", "舌苔白腻", "脉濡缓"],
    "湿热之邪郁遏上焦，卫阳不宣",
    ["夏秋季感冒", "胃肠型感冒", "流行性感冒"],
    "上焦湿热证与现代医学中的夏秋季上呼吸道感染、胃肠型感冒相似",
    ["formula_003", "formula_019"], ["needle_002", "needle_007"], ["treatment_007"], ["effect_001", "effect_012"]
))
new_syndromes.append(add_syndrome(
    "中焦湿热", "Zhong Jiao Shi Re",
    ["三焦辨证"], ["里证", "实证", "热证"],
    ["身热不扬", "脘痞呕恶", "口干不欲饮", "大便溏泄", "小便短黄", "舌苔黄腻", "脉滑数"],
    "湿热困阻中焦脾胃，升降失常",
    ["急性胃肠炎", "肠伤寒", "胆囊炎"],
    "中焦湿热与现代医学中的急性胃肠炎、肝胆系统感染相似",
    ["formula_029", "formula_073"], ["needle_003", "needle_011"], ["treatment_003"], ["effect_012", "effect_003"]
))
new_syndromes.append(add_syndrome(
    "下焦湿热", "Xia Jiao Shi Re",
    ["三焦辨证"], ["里证", "实证", "热证"],
    ["小腹胀满", "小便频数涩痛", "大便不畅", "口苦口干", "阴部潮湿瘙痒", "舌苔黄腻", "脉滑数"],
    "湿热下注膀胱大肠，气化不利，传导失常",
    ["泌尿系感染", "前列腺炎", "阴道炎", "痔疮发作"],
    "下焦湿热与现代医学中的泌尿生殖系统感染相似",
    ["formula_075", "formula_016"], ["needle_011", "needle_003"], ["treatment_011"], ["effect_012"]
))

# === 气血津液辨证新证型 ===
new_syndromes.append(add_syndrome(
    "气滞证", "Qi Zhi Zheng",
    ["气血津液辨证"], ["里证", "实证"],
    ["局部或全身胀痛窜痛", "时轻时重", "嗳气或矢气则舒", "胸闷", "善太息", "舌淡暗", "脉弦"],
    "情志不畅或邪气阻滞，气机运行不畅",
    ["功能性消化不良", "经前期综合征", "肠痉挛"],
    "气滞证以'胀痛窜痛'为特征，与现代医学中的平滑肌痉挛、胃肠功能紊乱相似",
    ["formula_021", "formula_052"], ["needle_004"], ["treatment_004"], ["effect_004"]
))
new_syndromes.append(add_syndrome(
    "气虚证", "Qi Xu Zheng",
    ["气血津液辨证", "八纲辨证"], ["里证", "虚证"],
    ["神疲乏力", "少气懒言", "动则气短", "食欲不振", "自汗", "面色㿠白", "舌淡苔白", "脉弱"],
    "先天不足或后天失养，元气亏虚，脏腑功能减退",
    ["慢性疲劳综合征", "免疫功能低下", "贫血", "病后体虚"],
    "气虚证表现为全身性功能低下，与现代医学中的免疫功能低下、代谢减退相似",
    ["formula_030", "formula_031"], ["needle_003", "needle_015"], ["treatment_003"], ["effect_003"]
))
new_syndromes.append(add_syndrome(
    "血瘀证", "Xue Yu Zheng",
    ["气血津液辨证"], ["里证", "实证"],
    ["刺痛固定不移", "拒按", "夜间加重", "面色黧黑", "肌肤甲错", "舌紫暗瘀斑", "脉涩"],
    "血液运行不畅或离经之血停积，形成瘀血",
    ["血栓性疾病", "动脉粥样硬化", "慢性肝炎肝纤维化", "痛经"],
    "血瘀证与现代医学中的微循环障碍、血栓形成、纤维化等病理改变相关",
    ["formula_055", "formula_056"], ["needle_008"], ["treatment_008"], ["effect_009"]
))

# === 经络辨证新证型 ===
new_syndromes.append(add_syndrome(
    "手太阴肺经病证", "Shou Tai Yin Fei Jing Bing Zheng",
    ["经络辨证", "脏腑辨证"], ["经证"],
    ["胸部胀满", "哮喘", "咳嗽", "缺盆中痛", "肩背痛", "手掌心热", "小便频数"],
    "外邪侵袭或内伤损及肺经，经气不利",
    ["肋间神经痛", "胸部软组织损伤", "肩关节周围炎"],
    "肺经循行路线上的症状，与现代医学中的胸部及上肢神经肌肉疾病相关",
    ["formula_001", "formula_005"], ["needle_001", "needle_006"], ["treatment_001"], ["effect_006"]
))
new_syndromes.append(add_syndrome(
    "手阳明大肠经病证", "Shou Yang Ming Da Chang Jing Bing Zheng",
    ["经络辨证", "脏腑辨证"], ["经证"],
    ["齿痛", "颈肿", "鼻衄", "咽喉肿痛", "肩前臑痛", "食指不用"],
    "大肠经经气运行不畅，循行部位出现症状",
    ["牙周炎", "颈淋巴结炎", "上肢周围神经炎"],
    "大肠经循行路线上的症状，与现代医学中的头面及上肢疾病相关",
    ["formula_003", "formula_017"], ["needle_002"], ["treatment_002"], ["effect_002"]
))
new_syndromes.append(add_syndrome(
    "足阳明胃经病证", "Zu Yang Ming Wei Jing Bing Zheng",
    ["经络辨证", "脏腑辨证"], ["经证"],
    ["发热汗出", "口唇生疮", "咽喉肿痛", "鼻痛", "齿痛", "颈肿", "下肢前侧疼痛"],
    "胃经经气不畅，气血壅滞",
    ["鼻窦炎", "牙龈炎", "下肢坐骨神经痛（前侧）", "甲状腺功能亢进"],
    "足阳明胃经病证与现代医学中的鼻窦炎、牙龈炎等头面及下肢前侧病变相关",
    ["formula_006", "formula_007"], ["needle_019"], ["treatment_019"], ["effect_020"]
))
new_syndromes.append(add_syndrome(
    "足太阳膀胱经病证", "Zu Tai Yang Pang Guang Jing Bing Zheng",
    ["经络辨证"], ["经证"],
    ["头痛项强", "目痛如脱", "脊背痛", "腰痛如折", "髋关节不利", "腘窝疼痛", "足小趾不用"],
    "风寒湿邪侵袭膀胱经，经气痹阻不通",
    ["颈椎病", "腰椎间盘突出", "坐骨神经痛", "腓肠肌痉挛"],
    "膀胱经循行人体背部最长经络，循经出现的症状与现代医学中的颈腰椎疾病相关",
    ["formula_077", "formula_078"], ["needle_001", "needle_005"], ["treatment_007"], ["effect_023"]
))

# === 脏腑辨证新证型 ===
new_syndromes.append(add_syndrome(
    "心阳虚", "Xin Yang Xu",
    ["脏腑辨证", "八纲辨证"], ["里证", "虚证", "寒证"],
    ["心悸怔忡", "胸闷气短", "形寒肢冷", "畏寒", "自汗", "舌淡胖", "脉迟或结代"],
    "心阳亏虚，鼓动无力，温煦失常",
    ["慢性心力衰竭", "缓慢型心律失常", "低血压"],
    "心阳虚与现代医学中的心功能减退、窦房结功能低下相似",
    ["formula_025", "formula_026"], ["needle_018", "needle_020"], ["treatment_018"], ["effect_019"]
))
new_syndromes.append(add_syndrome(
    "肝血虚", "Gan Xue Xu",
    ["脏腑辨证", "气血津液辨证"], ["里证", "虚证"],
    ["头晕眼花", "面色萎黄", "视物模糊", "肢体麻木", "筋脉拘挛", "月经量少色淡", "舌淡", "脉细"],
    "肝脏血液亏虚，筋目失于濡养",
    ["缺铁性贫血", "维生素A缺乏", "慢性肝病", "干眼症"],
    "肝血虚与现代医学中的缺铁性贫血、维生素A缺乏症等营养代谢性疾病相似",
    ["formula_035", "formula_036"], ["needle_010"], ["treatment_010"], ["effect_011"]
))
new_syndromes.append(add_syndrome(
    "肺气虚", "Fei Qi Xu",
    ["脏腑辨证", "八纲辨证"], ["里证", "虚证"],
    ["咳嗽无力", "气短懒言", "声音低微", "自汗畏风", "易感冒", "面色㿠白", "舌淡苔白", "脉虚"],
    "肺气不足，宣降无力，卫外不固",
    ["慢性支气管炎", "肺气肿", "免疫功能低下"],
    "肺气虚与现代医学中的呼吸功能减退、免疫功能低下相关",
    ["formula_041", "formula_030"], ["needle_006"], ["treatment_006"], ["effect_007"]
))

# === 外伤及特殊证型 ===
new_syndromes.append(add_syndrome(
    "跌打损伤", "Die Da Sun Shang",
    ["病因辨证"], ["实证"],
    ["局部疼痛", "肿胀青紫", "瘀斑", "活动受限", "压痛明显"],
    "外力致伤，经脉破损，血溢脉外，瘀血停滞",
    ["软组织挫伤", "骨折", "关节脱位", "肌肉拉伤"],
    "跌打损伤与现代医学中的急性软组织损伤完全对应",
    ["formula_055", "formula_056"], ["needle_008"], ["treatment_008"], ["effect_009"]
))
new_syndromes.append(add_syndrome(
    "暑湿感冒", "Shu Shi Gan Mao",
    ["病因辨证", "八纲辨证"], ["表证", "实证"],
    ["身热汗出不解", "微恶风", "头昏重胀痛", "胸闷脘痞", "心烦口渴", "小便短赤", "舌苔黄腻", "脉濡数"],
    "暑湿之邪侵袭肌表，暑热内盛，湿邪困脾",
    ["夏季感冒", "热射病先兆", "急性胃肠炎"],
    "暑湿感冒与现代医学中的夏季病毒性感染、中暑前兆状态相似",
    ["formula_003", "formula_004"], ["needle_002", "needle_019"], ["treatment_002"], ["effect_002"]
))

# 合并
all_syndromes = existing + new_syndromes
for i, s in enumerate(all_syndromes, 1):
    s['id'] = f"syndrome_{i:03d}"

with open(os.path.join(DATA_DIR, 'syndromes.json'), 'w', encoding='utf-8') as f:
    json.dump(all_syndromes, f, ensure_ascii=False, indent=2)

# 统计
from collections import Counter
all_cats = []
for s in all_syndromes:
    all_cats.extend(s.get('category', []))
cat_counts = Counter(all_cats)

print(f"证型：{len(existing)} → {len(all_syndromes)}（新增 {len(new_syndromes)} 条）")
print("\n辨证分类覆盖：")
for c, cnt in cat_counts.most_common(20):
    print(f"  {c}: {cnt}个证型")
