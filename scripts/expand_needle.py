#!/usr/bin/env python3
"""扩展针方数据：覆盖《针灸甲乙经》+《针灸大成》经典处方"""
import json
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'data')

# 加载现有数据
with open(os.path.join(DATA_DIR, 'needle_prescriptions.json')) as f:
    existing = json.load(f)

# 找到最大编号
max_id = max(int(n['id'].replace('needle_', '')) for n in existing)

# ===== 新增针方（含甲乙经和针灸大成经典） =====
new_needles = [
    # === 《针灸甲乙经》经典处方 ===
    {
        "id": f"needle_{max_id+1:03d}", "name": "外感发热针方（甲乙经）",
        "category": "解表", "source": "《针灸甲乙经》",
        "acupoints": [
            {"acupoint_id": "acupoint_323", "name": "大椎", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_271", "name": "风池", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_015", "name": "合谷", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_022", "name": "曲池", "method": "捻转泻法"}
        ],
        "effects": ["清热解表", "调和营卫"],
        "indications": ["外感发热", "恶寒发热", "头痛身痛", "无汗"],
        "modern_applications": ["上呼吸道感染", "流行性感冒", "急性发热"],
        "related_syndromes": ["syndrome_001", "syndrome_002"]
    },
    {
        "id": f"needle_{max_id+2:03d}", "name": "咳嗽针方（甲乙经）",
        "category": "止咳", "source": "《针灸甲乙经》",
        "acupoints": [
            {"acupoint_id": "acupoint_138", "name": "肺俞", "method": "捻转补法"},
            {"acupoint_id": "acupoint_007", "name": "列缺", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_015", "name": "合谷", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_067", "name": "足三里", "method": "提插补法"}
        ],
        "effects": ["宣肺止咳", "降气化痰"],
        "indications": ["咳嗽", "气喘", "胸闷", "咯痰不爽"],
        "modern_applications": ["急慢性支气管炎", "上呼吸道感染", "咳嗽变异性哮喘"],
        "related_syndromes": ["syndrome_006", "syndrome_007", "syndrome_036"]
    },
    {
        "id": f"needle_{max_id+3:03d}", "name": "胃痛针方（甲乙经）",
        "category": "理气", "source": "《针灸甲乙经》",
        "acupoints": [
            {"acupoint_id": "acupoint_349", "name": "中脘", "method": "提插泻法"},
            {"acupoint_id": "acupoint_225", "name": "内关", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_067", "name": "足三里", "method": "提插补法"},
            {"acupoint_id": "acupoint_329", "name": "百会", "method": "平刺补法"}
        ],
        "effects": ["和胃止痛", "降逆止呕"],
        "indications": ["胃脘痛", "恶心呕吐", "嗳气反酸", "食欲不振"],
        "modern_applications": ["急慢性胃炎", "消化性溃疡", "功能性消化不良"],
        "related_syndromes": ["syndrome_003", "syndrome_014", "syndrome_050"]
    },
    {
        "id": f"needle_{max_id+4:03d}", "name": "头痛针方（甲乙经）",
        "category": "祛风", "source": "《针灸甲乙经》",
        "acupoints": [
            {"acupoint_id": "acupoint_271", "name": "风池", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_329", "name": "百会", "method": "平刺泻法"},
            {"acupoint_id": "acupoint_298", "name": "太冲", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_015", "name": "合谷", "method": "捻转泻法"}
        ],
        "effects": ["祛风止痛", "通络清窍"],
        "indications": ["头痛", "偏头痛", "眩晕", "目眩"],
        "modern_applications": ["偏头痛", "紧张性头痛", "颈椎病头痛", "高血压头痛"],
        "related_syndromes": ["syndrome_012", "syndrome_042", "syndrome_043"]
    },
    {
        "id": f"needle_{max_id+5:03d}", "name": "面瘫针方（甲乙经）",
        "category": "祛风", "source": "《针灸甲乙经》",
        "acupoints": [
            {"acupoint_id": "acupoint_020", "name": "颊车", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_019", "name": "地仓", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_015", "name": "合谷", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_271", "name": "风池", "method": "捻转泻法"}
        ],
        "effects": ["祛风通络", "活血牵正"],
        "indications": ["口眼歪斜", "面肌麻木", "眼睑闭合不全", "口角流涎"],
        "modern_applications": ["面神经麻痹", "面神经炎", "中风后遗症面瘫"],
        "related_syndromes": ["syndrome_035"]
    },
    {
        "id": f"needle_{max_id+6:03d}", "name": "腰痛针方（甲乙经）",
        "category": "祛湿", "source": "《针灸甲乙经》",
        "acupoints": [
            {"acupoint_id": "acupoint_148", "name": "肾俞", "method": "捻转补法"},
            {"acupoint_id": "acupoint_329", "name": "百会", "method": "平刺泻法"},
            {"acupoint_id": "acupoint_186", "name": "委中", "method": "提插泻法"},
            {"acupoint_id": "acupoint_122", "name": "大肠俞", "method": "捻转泻法"}
        ],
        "effects": ["强腰壮肾", "通络止痛"],
        "indications": ["腰痛", "腰膝酸软", "转侧不利", "腰部冷痛"],
        "modern_applications": ["腰椎间盘突出", "腰肌劳损", "腰椎骨关节炎", "肾结石绞痛"],
        "related_syndromes": ["syndrome_005", "syndrome_044"]
    },
    {
        "id": f"needle_{max_id+7:03d}", "name": "痹证针方（甲乙经）",
        "category": "祛风", "source": "《针灸甲乙经》",
        "acupoints": [
            {"acupoint_id": "acupoint_022", "name": "曲池", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_015", "name": "合谷", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_067", "name": "足三里", "method": "提插补法"},
            {"acupoint_id": "acupoint_271", "name": "风池", "method": "捻转泻法"}
        ],
        "effects": ["祛风散寒", "蠲痹通络"],
        "indications": ["关节疼痛", "屈伸不利", "肢体沉重", "筋脉拘挛"],
        "modern_applications": ["风湿性关节炎", "类风湿关节炎", "痛风性关节炎", "骨关节炎"],
        "related_syndromes": ["syndrome_027", "syndrome_028", "syndrome_048"]
    },
    {
        "id": f"needle_{max_id+8:03d}", "name": "心悸怔忡针方（甲乙经）",
        "category": "安神", "source": "《针灸甲乙经》",
        "acupoints": [
            {"acupoint_id": "acupoint_104", "name": "神门", "method": "捻转补法"},
            {"acupoint_id": "acupoint_225", "name": "内关", "method": "捻转补法"},
            {"acupoint_id": "acupoint_154", "name": "心俞", "method": "捻转补法"},
            {"acupoint_id": "acupoint_082", "name": "三阴交", "method": "提插补法"}
        ],
        "effects": ["宁心安神", "定悸止惊"],
        "indications": ["心悸", "怔忡", "惊悸不安", "胸闷气短"],
        "modern_applications": ["心律失常", "心脏神经官能症", "焦虑症", "心脏瓣膜病"],
        "related_syndromes": ["syndrome_029", "syndrome_032", "syndrome_004"]
    },
    {
        "id": f"needle_{max_id+9:03d}", "name": "泄泻痢疾针方（甲乙经）",
        "category": "祛湿", "source": "《针灸甲乙经》",
        "acupoints": [
            {"acupoint_id": "acupoint_349", "name": "中脘", "method": "提插补法"},
            {"acupoint_id": "acupoint_067", "name": "足三里", "method": "提插补法"},
            {"acupoint_id": "acupoint_036", "name": "天枢", "method": "提插补法"},
            {"acupoint_id": "acupoint_145", "name": "脾俞", "method": "捻转补法"}
        ],
        "effects": ["健脾止泻", "清热利湿"],
        "indications": ["泄泻", "痢疾", "腹痛", "里急后重"],
        "modern_applications": ["急慢性肠炎", "肠易激综合征", "细菌性痢疾", "溃疡性结肠炎"],
        "related_syndromes": ["syndrome_003", "syndrome_021", "syndrome_040"]
    },
    {
        "id": f"needle_{max_id+10:03d}", "name": "黄疸针方（甲乙经）",
        "category": "清热", "source": "《针灸甲乙经》",
        "acupoints": [
            {"acupoint_id": "acupoint_143", "name": "肝俞", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_082", "name": "三阴交", "method": "提插泻法"},
            {"acupoint_id": "acupoint_067", "name": "足三里", "method": "提插泻法"},
            {"acupoint_id": "acupoint_349", "name": "中脘", "method": "提插泻法"}
        ],
        "effects": ["清热利湿", "疏肝退黄"],
        "indications": ["黄疸", "身目俱黄", "小便黄赤", "胁痛口苦"],
        "modern_applications": ["急性黄疸型肝炎", "胆囊炎", "胆结石", "溶血性黄疸"],
        "related_syndromes": ["syndrome_030", "syndrome_004", "syndrome_011"]
    },

    # === 《针灸大成》经典处方 ===
    {
        "id": f"needle_{max_id+11:03d}", "name": "中风七穴针方（针灸大成）",
        "category": "祛风", "source": "《针灸大成》",
        "acupoints": [
            {"acupoint_id": "acupoint_329", "name": "百会", "method": "平刺泻法"},
            {"acupoint_id": "acupoint_271", "name": "风池", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_015", "name": "合谷", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_022", "name": "曲池", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_067", "name": "足三里", "method": "提插补法"},
            {"acupoint_id": "acupoint_082", "name": "三阴交", "method": "提插补法"}
        ],
        "effects": ["醒脑开窍", "通经活络"],
        "indications": ["中风", "半身不遂", "口眼歪斜", "言语不利"],
        "modern_applications": ["脑梗死", "脑出血后遗症", "中风恢复期", "面神经麻痹"],
        "related_syndromes": ["syndrome_015", "syndrome_035"]
    },
    {
        "id": f"needle_{max_id+12:03d}", "name": "不寐安神针方（针灸大成）",
        "category": "安神", "source": "《针灸大成》",
        "acupoints": [
            {"acupoint_id": "acupoint_104", "name": "神门", "method": "捻转补法"},
            {"acupoint_id": "acupoint_225", "name": "内关", "method": "捻转补法"},
            {"acupoint_id": "acupoint_082", "name": "三阴交", "method": "提插补法"},
            {"acupoint_id": "acupoint_329", "name": "百会", "method": "平刺补法"}
        ],
        "effects": ["宁心安神", "调和阴阳"],
        "indications": ["失眠", "多梦", "心烦不寐", "健忘"],
        "modern_applications": ["失眠症", "神经衰弱", "焦虑症", "更年期综合征失眠"],
        "related_syndromes": ["syndrome_009", "syndrome_013", "syndrome_023", "syndrome_045"]
    },
    {
        "id": f"needle_{max_id+13:03d}", "name": "眩晕平肝针方（针灸大成）",
        "category": "平肝", "source": "《针灸大成》",
        "acupoints": [
            {"acupoint_id": "acupoint_271", "name": "风池", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_329", "name": "百会", "method": "平刺泻法"},
            {"acupoint_id": "acupoint_298", "name": "太冲", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_225", "name": "内关", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_085", "name": "阴陵泉", "method": "提插泻法"}
        ],
        "effects": ["平肝潜阳", "熄风定眩"],
        "indications": ["眩晕", "头重脚轻", "耳鸣", "恶心呕吐"],
        "modern_applications": ["梅尼埃病", "高血压眩晕", "椎基底动脉供血不足", "前庭功能障碍"],
        "related_syndromes": ["syndrome_012", "syndrome_033", "syndrome_043"]
    },
    {
        "id": f"needle_{max_id+14:03d}", "name": "呕吐降逆针方（针灸大成）",
        "category": "理气", "source": "《针灸大成》",
        "acupoints": [
            {"acupoint_id": "acupoint_225", "name": "内关", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_349", "name": "中脘", "method": "提插补法"},
            {"acupoint_id": "acupoint_067", "name": "足三里", "method": "提插补法"},
            {"acupoint_id": "acupoint_149", "name": "胃俞", "method": "捻转补法"}
        ],
        "effects": ["和胃降逆", "止呕安中"],
        "indications": ["呕吐", "恶心", "呃逆", "嗳气"],
        "modern_applications": ["急慢性胃炎", "神经性呕吐", "化疗后呕吐", "妊娠反应", "手术后呕吐"],
        "related_syndromes": ["syndrome_003", "syndrome_014", "syndrome_039"]
    },
    {
        "id": f"needle_{max_id+15:03d}", "name": "胁痛理气针方（针灸大成）",
        "category": "理气", "source": "《针灸大成》",
        "acupoints": [
            {"acupoint_id": "acupoint_263", "name": "期门", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_143", "name": "肝俞", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_067", "name": "足三里", "method": "提插泻法"},
            {"acupoint_id": "acupoint_082", "name": "三阴交", "method": "提插泻法"}
        ],
        "effects": ["疏肝理气", "活血止痛"],
        "indications": ["胁痛", "胸胁胀满", "嗳气", "口苦"],
        "modern_applications": ["肋间神经痛", "胆囊炎", "慢性肝炎", "胸膜炎"],
        "related_syndromes": ["syndrome_004", "syndrome_020", "syndrome_046"]
    },
    {
        "id": f"needle_{max_id+16:03d}", "name": "水肿利水针方（针灸大成）",
        "category": "祛湿", "source": "《针灸大成》",
        "acupoints": [
            {"acupoint_id": "acupoint_085", "name": "阴陵泉", "method": "提插泻法"},
            {"acupoint_id": "acupoint_082", "name": "三阴交", "method": "提插泻法"},
            {"acupoint_id": "acupoint_148", "name": "肾俞", "method": "捻转补法"},
            {"acupoint_id": "acupoint_349", "name": "中脘", "method": "提插泻法"}
        ],
        "effects": ["健脾利水", "温阳化气"],
        "indications": ["水肿", "小便不利", "腹胀如鼓", "下肢浮肿"],
        "modern_applications": ["肾病综合征", "心力衰竭水肿", "肝硬化腹水", "慢性肾炎"],
        "related_syndromes": ["syndrome_005", "syndrome_031", "syndrome_032"]
    },
    {
        "id": f"needle_{max_id+17:03d}", "name": "疝气止痛针方（针灸大成）",
        "category": "理气", "source": "《针灸大成》",
        "acupoints": [
            {"acupoint_id": "acupoint_341", "name": "关元", "method": "灸法"},
            {"acupoint_id": "acupoint_082", "name": "三阴交", "method": "提插泻法"},
            {"acupoint_id": "acupoint_067", "name": "足三里", "method": "提插补法"},
            {"acupoint_id": "acupoint_143", "name": "肝俞", "method": "捻转泻法"}
        ],
        "effects": ["温经散寒", "行气止痛"],
        "indications": ["疝气疼痛", "少腹坠胀", "睾丸疼痛", "引及腰部"],
        "modern_applications": ["腹股沟疝", "睾丸炎", "附睾炎", "精索静脉曲张"],
        "related_syndromes": ["syndrome_005", "syndrome_008"]
    },
    {
        "id": f"needle_{max_id+18:03d}", "name": "痢疾调中针方（针灸大成）",
        "category": "清热", "source": "《针灸大成》",
        "acupoints": [
            {"acupoint_id": "acupoint_036", "name": "天枢", "method": "提插泻法"},
            {"acupoint_id": "acupoint_067", "name": "足三里", "method": "提插泻法"},
            {"acupoint_id": "acupoint_015", "name": "合谷", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_022", "name": "曲池", "method": "捻转泻法"}
        ],
        "effects": ["清热化湿", "调气和血"],
        "indications": ["痢疾", "腹痛", "里急后重", "下利赤白"],
        "modern_applications": ["细菌性痢疾", "急性肠炎", "溃疡性结肠炎"],
        "related_syndromes": ["syndrome_011", "syndrome_018"]
    },
    {
        "id": f"needle_{max_id+19:03d}", "name": "五更泄针方（针灸大成）",
        "category": "温里", "source": "《针灸大成》",
        "acupoints": [
            {"acupoint_id": "acupoint_341", "name": "关元", "method": "灸法"},
            {"acupoint_id": "acupoint_148", "name": "肾俞", "method": "捻转补法"},
            {"acupoint_id": "acupoint_067", "name": "足三里", "method": "提插补法"},
            {"acupoint_id": "acupoint_082", "name": "三阴交", "method": "提插补法"}
        ],
        "effects": ["温肾暖脾", "固肠止泻"],
        "indications": ["五更泄", "黎明腹泻", "腹痛喜按", "畏寒肢冷"],
        "modern_applications": ["肠易激综合征腹泻型", "慢性肠炎", "慢性结肠炎"],
        "related_syndromes": ["syndrome_005", "syndrome_021", "syndrome_022"]
    },

    # === 针灸通用经典处方（甲乙经/大成通用） ===
    {
        "id": f"needle_{max_id+20:03d}", "name": "耳聋耳鸣针方",
        "category": "祛风", "source": "《针灸甲乙经》《针灸大成》",
        "acupoints": [
            {"acupoint_id": "acupoint_271", "name": "风池", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_304", "name": "听会", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_305", "name": "翳风", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_015", "name": "合谷", "method": "捻转泻法"}
        ],
        "effects": ["通窍聪耳", "疏风清热"],
        "indications": ["耳鸣", "耳聋", "头晕", "耳内如蝉鸣"],
        "modern_applications": ["神经性耳鸣", "突发性耳聋", "梅尼埃病", "中耳炎后遗症"],
        "related_syndromes": ["syndrome_009", "syndrome_012", "syndrome_033"]
    },
    {
        "id": f"needle_{max_id+21:03d}", "name": "目赤肿痛针方",
        "category": "清热", "source": "《针灸大成》",
        "acupoints": [
            {"acupoint_id": "acupoint_298", "name": "太冲", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_271", "name": "风池", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_015", "name": "合谷", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_022", "name": "曲池", "method": "捻转泻法"}
        ],
        "effects": ["清肝明目", "疏风散热"],
        "indications": ["目赤肿痛", "畏光流泪", "视物模糊", "目涩干痒"],
        "modern_applications": ["急性结膜炎", "角膜炎", "干眼症", "视疲劳"],
        "related_syndromes": ["syndrome_002", "syndrome_004", "syndrome_012"]
    },
    {
        "id": f"needle_{max_id+22:03d}", "name": "喉痹咽痛针方",
        "category": "清热", "source": "《针灸甲乙经》",
        "acupoints": [
            {"acupoint_id": "acupoint_022", "name": "曲池", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_015", "name": "合谷", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_323", "name": "大椎", "method": "放血疗法"},
            {"acupoint_id": "acupoint_007", "name": "列缺", "method": "捻转泻法"}
        ],
        "effects": ["清利咽喉", "消肿止痛"],
        "indications": ["咽喉肿痛", "声音嘶哑", "喉痹", "吞咽困难"],
        "modern_applications": ["急性扁桃体炎", "急性咽喉炎", "声带小结", "慢性咽炎"],
        "related_syndromes": ["syndrome_002", "syndrome_006"]
    },
    {
        "id": f"needle_{max_id+23:03d}", "name": "癃闭通利针方",
        "category": "祛湿", "source": "《针灸大成》",
        "acupoints": [
            {"acupoint_id": "acupoint_082", "name": "三阴交", "method": "提插泻法"},
            {"acupoint_id": "acupoint_085", "name": "阴陵泉", "method": "提插泻法"},
            {"acupoint_id": "acupoint_148", "name": "肾俞", "method": "捻转补法"},
            {"acupoint_id": "acupoint_341", "name": "关元", "method": "提插补法"}
        ],
        "effects": ["通利小便", "温阳化气"],
        "indications": ["小便不通", "排尿困难", "小腹胀满", "点滴而下"],
        "modern_applications": ["前列腺增生", "术后尿潴留", "产后尿潴留", "神经性排尿障碍"],
        "related_syndromes": ["syndrome_005", "syndrome_011", "syndrome_047"]
    },
    {
        "id": f"needle_{max_id+24:03d}", "name": "遗尿固摄针方",
        "category": "固涩", "source": "《针灸大成》",
        "acupoints": [
            {"acupoint_id": "acupoint_148", "name": "肾俞", "method": "捻转补法"},
            {"acupoint_id": "acupoint_341", "name": "关元", "method": "灸法"},
            {"acupoint_id": "acupoint_082", "name": "三阴交", "method": "提插补法"},
            {"acupoint_id": "acupoint_104", "name": "神门", "method": "捻转补法"}
        ],
        "effects": ["温肾固摄", "缩尿止遗"],
        "indications": ["遗尿", "夜尿频多", "小便失禁", "尿后余沥"],
        "modern_applications": ["小儿遗尿", "老年性尿失禁", "神经源性膀胱"],
        "related_syndromes": ["syndrome_005", "syndrome_048"]
    },
    {
        "id": f"needle_{max_id+25:03d}", "name": "月经不调针方",
        "category": "理气", "source": "《针灸甲乙经》《针灸大成》",
        "acupoints": [
            {"acupoint_id": "acupoint_082", "name": "三阴交", "method": "提插补法"},
            {"acupoint_id": "acupoint_086", "name": "血海", "method": "提插补法"},
            {"acupoint_id": "acupoint_341", "name": "关元", "method": "提插补法"},
            {"acupoint_id": "acupoint_145", "name": "脾俞", "method": "捻转补法"}
        ],
        "effects": ["调经养血", "理气和血"],
        "indications": ["月经不调", "经期先后不定", "经量异常", "经色异常"],
        "modern_applications": ["月经紊乱", "多囊卵巢综合征", "功能性子宫出血", "围绝经期综合征"],
        "related_syndromes": ["syndrome_004", "syndrome_008", "syndrome_010"]
    },
    {
        "id": f"needle_{max_id+26:03d}", "name": "带下病针方",
        "category": "祛湿", "source": "《针灸大成》",
        "acupoints": [
            {"acupoint_id": "acupoint_082", "name": "三阴交", "method": "提插泻法"},
            {"acupoint_id": "acupoint_085", "name": "阴陵泉", "method": "提插泻法"},
            {"acupoint_id": "acupoint_341", "name": "关元", "method": "提插补法"},
            {"acupoint_id": "acupoint_145", "name": "脾俞", "method": "捻转补法"}
        ],
        "effects": ["清热利湿", "健脾止带"],
        "indications": ["带下过多", "色黄气臭", "外阴瘙痒", "小腹胀痛"],
        "modern_applications": ["细菌性阴道炎", "霉菌性阴道炎", "盆腔炎", "宫颈炎"],
        "related_syndromes": ["syndrome_011", "syndrome_003"]
    },
    {
        "id": f"needle_{max_id+27:03d}", "name": "小儿惊风针方",
        "category": "安神", "source": "《针灸甲乙经》",
        "acupoints": [
            {"acupoint_id": "acupoint_323", "name": "大椎", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_015", "name": "合谷", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_298", "name": "太冲", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_329", "name": "百会", "method": "平刺泻法"}
        ],
        "effects": ["镇惊安神", "熄风定志"],
        "indications": ["小儿惊风", "抽搐", "高热惊厥", "夜啼"],
        "modern_applications": ["小儿高热惊厥", "小儿癫痫", "小儿夜惊症"],
        "related_syndromes": ["syndrome_002", "syndrome_018"]
    },
    {
        "id": f"needle_{max_id+28:03d}", "name": "瘰疬散结针方",
        "category": "清热", "source": "《针灸大成》",
        "acupoints": [
            {"acupoint_id": "acupoint_022", "name": "曲池", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_271", "name": "风池", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_082", "name": "三阴交", "method": "提插泻法"},
            {"acupoint_id": "acupoint_363", "name": "百劳", "method": "捻转泻法"}
        ],
        "effects": ["清热解毒", "化痰散结"],
        "indications": ["瘰疬", "颈部淋巴结肿大", "皮下结节", "按之可移"],
        "modern_applications": ["颈部淋巴结结核", "淋巴结炎", "甲状腺结节"],
        "related_syndromes": ["syndrome_007"]
    },
    {
        "id": f"needle_{max_id+29:03d}", "name": "痫证定痫针方",
        "category": "安神", "source": "《针灸甲乙经》",
        "acupoints": [
            {"acupoint_id": "acupoint_329", "name": "百会", "method": "平刺泻法"},
            {"acupoint_id": "acupoint_298", "name": "太冲", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_271", "name": "风池", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_225", "name": "内关", "method": "捻转泻法"}
        ],
        "effects": ["豁痰开窍", "熄风定痫"],
        "indications": ["痫证", "突然昏倒", "口吐涎沫", "四肢抽搐"],
        "modern_applications": ["癫痫", "癔病性发作", "晕厥"],
        "related_syndromes": ["syndrome_007", "syndrome_012", "syndrome_033"]
    },
    {
        "id": f"needle_{max_id+30:03d}", "name": "郁证解郁针方",
        "category": "理气", "source": "《针灸大成》",
        "acupoints": [
            {"acupoint_id": "acupoint_225", "name": "内关", "method": "捻转补法"},
            {"acupoint_id": "acupoint_104", "name": "神门", "method": "捻转补法"},
            {"acupoint_id": "acupoint_298", "name": "太冲", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_329", "name": "百会", "method": "平刺补法"}
        ],
        "effects": ["疏肝解郁", "宁心安神"],
        "indications": ["郁证", "情绪低落", "善太息", "胸胁胀闷"],
        "modern_applications": ["抑郁症", "焦虑症", "植物神经功能紊乱", "慢性疲劳综合征"],
        "related_syndromes": ["syndrome_004", "syndrome_046"]
    },

    # === 针灸常用经验针方 ===
    {
        "id": f"needle_{max_id+31:03d}", "name": "哮病平喘针方",
        "category": "止咳", "source": "常用经验方",
        "acupoints": [
            {"acupoint_id": "acupoint_138", "name": "肺俞", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_007", "name": "列缺", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_067", "name": "足三里", "method": "提插补法"},
            {"acupoint_id": "acupoint_085", "name": "阴陵泉", "method": "提插泻法"}
        ],
        "effects": ["宣肺平喘", "降气化痰"],
        "indications": ["哮病", "喘促气急", "喉中哮鸣", "胸闷憋气"],
        "modern_applications": ["支气管哮喘", "喘息性支气管炎", "过敏性哮喘"],
        "related_syndromes": ["syndrome_007", "syndrome_038", "syndrome_049"]
    },
    {
        "id": f"needle_{max_id+32:03d}", "name": "消渴降糖针方",
        "category": "补阴", "source": "《针灸大成》",
        "acupoints": [
            {"acupoint_id": "acupoint_148", "name": "肾俞", "method": "捻转补法"},
            {"acupoint_id": "acupoint_349", "name": "中脘", "method": "提插补法"},
            {"acupoint_id": "acupoint_067", "name": "足三里", "method": "提插补法"},
            {"acupoint_id": "acupoint_082", "name": "三阴交", "method": "提插补法"}
        ],
        "effects": ["滋阴清热", "生津止渴"],
        "indications": ["消渴", "口干多饮", "多食易饥", "小便频多"],
        "modern_applications": ["2型糖尿病辅助治疗", "糖尿病前期", "代谢综合征"],
        "related_syndromes": ["syndrome_009", "syndrome_034"]
    },
    {
        "id": f"needle_{max_id+33:03d}", "name": "肩痹通络针方",
        "category": "祛风", "source": "《针灸大成》",
        "acupoints": [
            {"acupoint_id": "acupoint_022", "name": "曲池", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_015", "name": "合谷", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_304", "name": "肩髃", "method": "提插泻法"},
            {"acupoint_id": "acupoint_271", "name": "风池", "method": "捻转泻法"}
        ],
        "effects": ["祛风通络", "舒筋止痛"],
        "indications": ["肩关节疼痛", "活动受限", "手臂上举困难", "夜间痛甚"],
        "modern_applications": ["肩周炎", "肩袖损伤", "肱二头肌长头腱鞘炎"],
        "related_syndromes": ["syndrome_027", "syndrome_028"]
    },
    {
        "id": f"needle_{max_id+34:03d}", "name": "汗证敛汗针方",
        "category": "固涩", "source": "常用经验方",
        "acupoints": [
            {"acupoint_id": "acupoint_015", "name": "合谷", "method": "捻转补法"},
            {"acupoint_id": "acupoint_082", "name": "三阴交", "method": "提插补法"},
            {"acupoint_id": "acupoint_104", "name": "神门", "method": "捻转补法"},
            {"acupoint_id": "acupoint_138", "name": "肺俞", "method": "捻转补法"}
        ],
        "effects": ["益气固表", "敛阴止汗"],
        "indications": ["自汗", "盗汗", "动则汗出", "手足心汗"],
        "modern_applications": ["多汗症", "更年期综合征潮热汗出", "甲亢多汗"],
        "related_syndromes": ["syndrome_009", "syndrome_015", "syndrome_034"]
    },
    {
        "id": f"needle_{max_id+35:03d}", "name": "痿证强壮针方",
        "category": "补益", "source": "《针灸甲乙经》",
        "acupoints": [
            {"acupoint_id": "acupoint_067", "name": "足三里", "method": "提插补法"},
            {"acupoint_id": "acupoint_148", "name": "肾俞", "method": "捻转补法"},
            {"acupoint_id": "acupoint_145", "name": "脾俞", "method": "捻转补法"},
            {"acupoint_id": "acupoint_341", "name": "关元", "method": "灸法"}
        ],
        "effects": ["健脾益气", "强筋健骨"],
        "indications": ["肢体萎软", "肌肉萎缩", "行走无力", "神疲乏力"],
        "modern_applications": ["重症肌无力", "运动神经元病", "多发性肌炎", "脊髓损伤康复"],
        "related_syndromes": ["syndrome_003", "syndrome_005", "syndrome_048"]
    },
    {
        "id": f"needle_{max_id+36:03d}", "name": "积聚消癥针方",
        "category": "活血", "source": "《针灸大成》",
        "acupoints": [
            {"acupoint_id": "acupoint_143", "name": "肝俞", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_082", "name": "三阴交", "method": "提插泻法"},
            {"acupoint_id": "acupoint_067", "name": "足三里", "method": "提插泻法"},
            {"acupoint_id": "acupoint_271", "name": "风池", "method": "捻转泻法"}
        ],
        "effects": ["活血化瘀", "软坚散结"],
        "indications": ["腹部肿块", "痞块", "肝脾肿大", "刺痛拒按"],
        "modern_applications": ["肝脾肿大", "肝硬化", "子宫肌瘤", "腹腔肿瘤辅助"],
        "related_syndromes": ["syndrome_008", "syndrome_015"]
    },
    {
        "id": f"needle_{max_id+37:03d}", "name": "鼻渊通窍针方",
        "category": "祛风", "source": "《针灸甲乙经》",
        "acupoints": [
            {"acupoint_id": "acupoint_007", "name": "列缺", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_015", "name": "合谷", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_271", "name": "风池", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_323", "name": "大椎", "method": "捻转泻法"}
        ],
        "effects": ["宣肺通窍", "清热化浊"],
        "indications": ["鼻塞", "流涕", "嗅觉减退", "头痛"],
        "modern_applications": ["慢性鼻炎", "鼻窦炎", "过敏性鼻炎"],
        "related_syndromes": ["syndrome_001", "syndrome_002"]
    },
    {
        "id": f"needle_{max_id+38:03d}", "name": "遗精固肾针方",
        "category": "固涩", "source": "《针灸大成》",
        "acupoints": [
            {"acupoint_id": "acupoint_341", "name": "关元", "method": "灸法"},
            {"acupoint_id": "acupoint_148", "name": "肾俞", "method": "捻转补法"},
            {"acupoint_id": "acupoint_082", "name": "三阴交", "method": "提插补法"},
            {"acupoint_id": "acupoint_104", "name": "神门", "method": "捻转补法"}
        ],
        "effects": ["补肾固精", "安神定志"],
        "indications": ["遗精", "滑精", "夜梦纷纭", "腰膝酸软"],
        "modern_applications": ["前列腺炎", "性神经官能症", "男性功能障碍"],
        "related_syndromes": ["syndrome_005", "syndrome_009"]
    },
    {
        "id": f"needle_{max_id+39:03d}", "name": "疟疾截疟针方",
        "category": "和解", "source": "《针灸甲乙经》",
        "acupoints": [
            {"acupoint_id": "acupoint_323", "name": "大椎", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_271", "name": "风池", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_015", "name": "合谷", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_022", "name": "曲池", "method": "捻转泻法"}
        ],
        "effects": ["和解少阳", "截疟祛邪"],
        "indications": ["疟疾", "寒战高热", "定时发作", "头痛欲裂"],
        "modern_applications": ["疟疾辅助治疗", "不明原因周期性发热"],
        "related_syndromes": ["syndrome_020"]
    },
    {
        "id": f"needle_{max_id+40:03d}", "name": "狂证安神针方",
        "category": "安神", "source": "《针灸甲乙经》",
        "acupoints": [
            {"acupoint_id": "acupoint_349", "name": "中脘", "method": "提插泻法"},
            {"acupoint_id": "acupoint_104", "name": "神门", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_298", "name": "太冲", "method": "捻转泻法"},
            {"acupoint_id": "acupoint_225", "name": "内关", "method": "捻转泻法"}
        ],
        "effects": ["清心泻火", "镇静安神"],
        "indications": ["狂证", "躁扰不宁", "胡言乱语", "哭笑无常"],
        "modern_applications": ["躁狂发作", "精神分裂症躁动", "急性应激障碍"],
        "related_syndromes": ["syndrome_013", "syndrome_018"]
    },
]

# 合并数据
all_needles = existing + new_needles

# 重新编号确保ID连续
for i, n in enumerate(all_needles, 1):
    n['id'] = f"needle_{i:03d}"

with open(os.path.join(DATA_DIR, 'needle_prescriptions.json'), 'w', encoding='utf-8') as f:
    json.dump(all_needles, f, ensure_ascii=False, indent=2)

print(f"针方：{len(existing)} → {len(all_needles)}（新增 {len(new_needles)} 条）")
print(f"  其中《针灸甲乙经》: {sum(1 for n in all_needles if '甲乙经' in n.get('source',''))} 条")
print(f"  其中《针灸大成》: {sum(1 for n in all_needles if '针灸大成' in n.get('source',''))} 条")

# 统计来源
from collections import Counter
sources = Counter(n.get('source','-') for n in all_needles)
for s, c in sources.most_common():
    print(f"  {s}: {c}")
