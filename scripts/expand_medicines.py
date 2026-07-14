#!/usr/bin/env python3
"""扩展药材：覆盖新增方剂所需的药物"""
import json, os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'data')

with open(os.path.join(DATA_DIR, 'medicines.json')) as f:
    existing = json.load(f)

existing_names = {m['name'] for m in existing}
max_id = max(int(m['id'].replace('medicine_', '')) for m in existing)

# 定义新增药材（聚焦于新增方剂中新引入的药物）
new_medicines_data = [
    # 补虚药
    {"name": "龟甲胶", "pinyin": "Gui Jia Jiao", "latin_name": "Testudinis Carapacis Et Plastri Colla",
     "nature": "微寒", "flavor": ["甘", "咸"], "meridian": ["肝经", "肾经"],
     "effects": ["滋阴潜阳", "益肾健骨", "养血补心"],
     "indications": ["阴虚潮热", "骨蒸盗汗", "腰膝酸软", "心虚惊悸"], "usage": "烊化兑服，3-9g",
     "contraindications": ["脾胃虚寒者慎用"], "category": "补虚药", "subcategory": "补阴药"},
    {"name": "鹿角胶", "pinyin": "Lu Jiao Jiao", "latin_name": "Cervi Cornus Colla",
     "nature": "温", "flavor": ["甘", "咸"], "meridian": ["肝经", "肾经"],
     "effects": ["温补肝肾", "益精养血"],
     "indications": ["肾阳不足", "阳痿滑精", "虚寒崩漏", "骨弱筋软"], "usage": "烊化兑服，3-6g",
     "contraindications": ["阴虚阳亢者禁用"], "category": "补虚药", "subcategory": "补阳药"},
    {"name": "沙苑子", "pinyin": "Sha Yuan Zi", "latin_name": "Astragali Complanati Semen",
     "nature": "温", "flavor": ["甘"], "meridian": ["肝经", "肾经"],
     "effects": ["补肾固精", "养肝明目"],
     "indications": ["肾虚腰痛", "遗精早泄", "头晕目眩", "视力减退"], "usage": "煎服，9-15g",
     "contraindications": ["阴虚火旺者慎用"], "category": "补虚药", "subcategory": "补阳药"},
    {"name": "太子参", "pinyin": "Tai Zi Shen", "latin_name": "Pseudostellariae Radix",
     "nature": "平", "flavor": ["甘", "微苦"], "meridian": ["脾经", "肺经"],
     "effects": ["益气健脾", "生津润肺"],
     "indications": ["脾虚体倦", "食欲不振", "病后虚弱", "气阴不足"], "usage": "煎服，9-30g",
     "contraindications": [], "category": "补虚药", "subcategory": "补气药"},

    # 清热药
    {"name": "水牛角", "pinyin": "Shui Niu Jiao", "latin_name": "Bubali Cornu",
     "nature": "寒", "flavor": ["苦"], "meridian": ["心经", "肝经"],
     "effects": ["清热凉血", "解毒定惊"],
     "indications": ["高热神昏", "斑疹吐衄", "惊风癫狂"], "usage": "煎服，15-30g，先煎3小时以上",
     "contraindications": ["脾胃虚寒者慎用"], "category": "清热药", "subcategory": "清热凉血药"},
    {"name": "生地黄", "pinyin": "Sheng Di Huang", "latin_name": "Rehmanniae Radix",
     "nature": "寒", "flavor": ["甘", "苦"], "meridian": ["心经", "肝经", "肾经"],
     "effects": ["清热凉血", "养阴生津"],
     "indications": ["热入营血", "吐血衄血", "阴虚发热", "消渴"], "usage": "煎服，10-30g",
     "contraindications": ["脾虚湿滞者慎用"], "category": "清热药", "subcategory": "清热凉血药"},
    {"name": "牡丹皮", "pinyin": "Mu Dan Pi", "latin_name": "Moutan Cortex",
     "nature": "微寒", "flavor": ["苦", "辛"], "meridian": ["心经", "肝经", "肾经"],
     "effects": ["清热凉血", "活血散瘀"],
     "indications": ["热入血分", "吐血衄血", "瘀血闭经", "疮疡肿毒"], "usage": "煎服，6-12g",
     "contraindications": ["孕妇慎用", "月经过多者慎用"], "category": "清热药", "subcategory": "清热凉血药"},
    {"name": "淡竹叶", "pinyin": "Dan Zhu Ye", "latin_name": "Lophatheri Herba",
     "nature": "寒", "flavor": ["甘", "淡"], "meridian": ["心经", "胃经", "小肠经"],
     "effects": ["清热泻火", "除烦止渴", "利尿通淋"],
     "indications": ["热病烦渴", "小便赤涩淋痛", "口舌生疮"], "usage": "煎服，6-9g",
     "contraindications": [], "category": "清热药", "subcategory": "清热泻火药"},

    # 活血化瘀药
    {"name": "五灵脂", "pinyin": "Wu Ling Zhi", "latin_name": "Trogopterori Faeces",
     "nature": "温", "flavor": ["苦", "甘"], "meridian": ["肝经"],
     "effects": ["活血止痛", "化瘀止血"],
     "indications": ["瘀血阻滞诸痛", "痛经", "产后恶露不行", "瘀血崩漏"], "usage": "煎服，3-10g，包煎",
     "contraindications": ["孕妇慎用", "人参畏五灵脂"], "category": "活血化瘀药", "subcategory": "活血止痛药"},
    {"name": "皂角刺", "pinyin": "Zao Jiao Ci", "latin_name": "Gleditsiae Spina",
     "nature": "温", "flavor": ["辛"], "meridian": ["肝经", "胃经"],
     "effects": ["消肿托毒", "排脓杀虫"],
     "indications": ["痈疽疮毒初起", "脓成未溃", "疥癣麻风"], "usage": "煎服，3-10g",
     "contraindications": ["孕妇慎用", "痈疽已溃者忌用"], "category": "活血化瘀药", "subcategory": "破血消癥药"},

    # 收涩药
    {"name": "芡实", "pinyin": "Qian Shi", "latin_name": "Euryales Semen",
     "nature": "平", "flavor": ["甘", "涩"], "meridian": ["脾经", "肾经"],
     "effects": ["益肾固精", "健脾止泻", "除湿止带"],
     "indications": ["遗精滑精", "脾虚久泻", "带下", "小便不禁"], "usage": "煎服，10-15g",
     "contraindications": [], "category": "收涩药", "subcategory": "固精缩尿止带药"},
    {"name": "莲须", "pinyin": "Lian Xu", "latin_name": "Nelumbinis Stamen",
     "nature": "平", "flavor": ["甘", "涩"], "meridian": ["心经", "肾经"],
     "effects": ["固肾涩精"],
     "indications": ["遗精滑精", "带下", "尿频"], "usage": "煎服，3-5g",
     "contraindications": ["小便不利者慎用"], "category": "收涩药", "subcategory": "固精缩尿止带药"},

    # 开窍药
    {"name": "石菖蒲", "pinyin": "Shi Chang Pu", "latin_name": "Acori Tatarinowii Rhizoma",
     "nature": "温", "flavor": ["辛", "苦"], "meridian": ["心经", "胃经"],
     "effects": ["开窍豁痰", "醒神益智", "化湿和胃"],
     "indications": ["神昏癫痫", "健忘失眠", "耳鸣耳聋", "脘痞不饥"], "usage": "煎服，3-9g",
     "contraindications": [], "category": "开窍药", "subcategory": ""},
    {"name": "冰片", "pinyin": "Bing Pian", "latin_name": "Borneolum Syntheticum",
     "nature": "微寒", "flavor": ["辛", "苦"], "meridian": ["心经", "脾经", "肺经"],
     "effects": ["开窍醒神", "清热止痛"],
     "indications": ["闭证神昏", "目赤肿痛", "喉痹口疮", "疮疡肿痛"], "usage": "入丸散，0.15-0.3g",
     "contraindications": ["孕妇慎用"], "category": "开窍药", "subcategory": ""},

    # 祛风湿药
    {"name": "白豆蔻", "pinyin": "Bai Dou Kou", "latin_name": "Amomi Fructus Rotundus",
     "nature": "温", "flavor": ["辛"], "meridian": ["肺经", "脾经", "胃经"],
     "effects": ["化湿行气", "温中止呕"],
     "indications": ["湿阻中焦", "脘腹胀满", "呕吐", "不思饮食"], "usage": "煎服，3-6g，后下",
     "contraindications": [], "category": "化湿药", "subcategory": ""},

    # 治风药
    {"name": "代赭石", "pinyin": "Dai Zhe Shi", "latin_name": "Haematitum",
     "nature": "寒", "flavor": ["苦"], "meridian": ["肝经", "心经", "肺经", "胃经"],
     "effects": ["平肝潜阳", "重镇降逆", "凉血止血"],
     "indications": ["肝阳上亢眩晕", "嗳气呃逆", "呕吐", "气逆喘息"], "usage": "煎服，9-30g，先煎",
     "contraindications": ["孕妇慎用"], "category": "平肝熄风药", "subcategory": "平抑肝阳药"},
    {"name": "磁石", "pinyin": "Ci Shi", "latin_name": "Magnetitum",
     "nature": "寒", "flavor": ["咸"], "meridian": ["肝经", "心经", "肾经"],
     "effects": ["镇惊安神", "平肝潜阳", "聪耳明目", "纳气定喘"],
     "indications": ["心神不宁惊悸", "癫痫", "头晕目眩", "耳鸣耳聋"], "usage": "煎服，9-30g，先煎",
     "contraindications": ["脾胃虚弱者慎用"], "category": "安神药", "subcategory": "重镇安神药"},

    # 化痰止咳平喘药
    {"name": "川贝母", "pinyin": "Chuan Bei Mu", "latin_name": "Fritillariae Cirrhosae Bulbus",
     "nature": "微寒", "flavor": ["苦", "甘"], "meridian": ["肺经", "心经"],
     "effects": ["清热润肺", "化痰止咳", "散结消痈"],
     "indications": ["肺热燥咳", "干咳少痰", "阴虚劳嗽", "瘰疬痈肿"], "usage": "煎服，3-9g；研末冲服，1-2g",
     "contraindications": ["湿痰、寒痰者慎用"], "category": "化痰止咳平喘药", "subcategory": "清化热痰药"},
    {"name": "白芥子", "pinyin": "Bai Jie Zi", "latin_name": "Sinapis Semen",
     "nature": "温", "flavor": ["辛"], "meridian": ["肺经"],
     "effects": ["温肺豁痰利气", "散结通络止痛"],
     "indications": ["寒痰咳嗽", "胸胁悬饮", "阴疽流注", "关节麻木疼痛"], "usage": "煎服，3-9g",
     "contraindications": ["肺虚久咳者慎用", "消化道溃疡慎用"], "category": "化痰止咳平喘药", "subcategory": "温化寒痰药"},

    # 利水渗湿药
    {"name": "萹蓄", "pinyin": "Bian Xu", "latin_name": "Polygoni Avicularis Herba",
     "nature": "微寒", "flavor": ["苦"], "meridian": ["膀胱经"],
     "effects": ["利尿通淋", "杀虫止痒"],
     "indications": ["热淋涩痛", "小便短赤", "皮肤湿疹", "阴痒带下"], "usage": "煎服，9-15g",
     "contraindications": ["脾虚者慎用"], "category": "利水渗湿药", "subcategory": "利尿通淋药"},
    {"name": "瞿麦", "pinyin": "Qu Mai", "latin_name": "Dianthi Herba",
     "nature": "寒", "flavor": ["苦"], "meridian": ["心经", "小肠经", "膀胱经"],
     "effects": ["利尿通淋", "活血通经"],
     "indications": ["热淋", "血淋", "石淋", "小便不通"], "usage": "煎服，9-15g",
     "contraindications": ["孕妇慎用"], "category": "利水渗湿药", "subcategory": "利尿通淋药"},
    {"name": "冬瓜皮", "pinyin": "Dong Gua Pi", "latin_name": "Benincasae Exocarpium",
     "nature": "微寒", "flavor": ["甘"], "meridian": ["脾经", "小肠经"],
     "effects": ["利尿消肿"],
     "indications": ["水肿胀满", "小便不利", "暑热口渴"], "usage": "煎服，9-30g",
     "contraindications": [], "category": "利水渗湿药", "subcategory": "利水消肿药"},

    # 涌吐药
    {"name": "瓜蒂", "pinyin": "Gua Di", "latin_name": "Cucumis Melo Pedicellus",
     "nature": "寒", "flavor": ["苦"], "meridian": ["胃经"],
     "effects": ["涌吐痰食", "祛湿退黄"],
     "indications": ["食积胃脘", "痰涎壅盛", "急黄", "湿热黄疸"], "usage": "煎服，2.5-5g；入丸散0.3-1g",
     "contraindications": ["体虚、吐血、咯血者禁用"], "category": "涌吐药", "subcategory": ""},
]

# 创建新条目
new_medicines = []
current_max = max_id
for md in new_medicines_data:
    if md['name'] in existing_names:
        continue  # 药物已存在则跳过
    current_max += 1
    entry = {"id": f"medicine_{current_max:03d}"}
    entry.update(md)
    if not entry.get('subcategory'):
        entry['subcategory'] = ''
    new_medicines.append(entry)
    existing_names.add(md['name'])

all_medicines = existing + new_medicines
for i, m in enumerate(all_medicines, 1):
    m['id'] = f"medicine_{i:03d}"

with open(os.path.join(DATA_DIR, 'medicines.json'), 'w', encoding='utf-8') as f:
    json.dump(all_medicines, f, ensure_ascii=False, indent=2)

print(f"药材：{len(existing)} → {len(all_medicines)}（新增 {len(new_medicines)} 条）")

from collections import Counter
cats = Counter(m.get('category','') for m in all_medicines)
print("\n分类分布（前15）：")
for c, cnt in cats.most_common(15):
    print(f"  {c}: {cnt}")
