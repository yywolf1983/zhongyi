#!/usr/bin/env python3
"""替换方剂中的注射液，新增伤寒杂病经典方剂"""
import json

with open('/Users/yy/pro-test/zhongyi/assets/data/formulas.json', 'r', encoding='utf-8') as f:
    formulas = json.load(f)

# 移除两个注射液配方 (formula_089, formula_090)
formulas = [f for f in formulas if f['id'] not in ('formula_089', 'formula_090')]

# 新增方剂，替换成伤寒杂病经典方
new_formulas = [
    # formula_089 -> 小青龙汤
    {
        "id": "formula_089",
        "name": "小青龙汤",
        "pinyin": "Xiao Qing Long Tang",
        "category": "解表剂",
        "subcategory": "解表化饮",
        "source": "《伤寒论》",
        "author": "张仲景",
        "ingredients": [
            {"medicine_id": "medicine_001", "name": "麻黄", "quantity": "9g", "role": "君"},
            {"medicine_id": "medicine_002", "name": "桂枝", "quantity": "6g", "role": "臣"},
            {"medicine_id": "medicine_073", "name": "甘草", "quantity": "6g", "role": "佐"},
            {"medicine_id": "medicine_065", "name": "杏仁", "quantity": "6g", "role": "佐"},
        ],
        "effects": ["解表散寒", "温肺化饮"],
        "indications": ["外寒内饮证：恶寒发热无汗，咳喘痰多清稀"],
        "usage": "水煎服，每日1剂，分两次服",
        "modern_applications": ["支气管哮喘", "慢性支气管炎急性发作", "过敏性鼻炎"],
        "pharmacological_effect": "具有解热、抗炎、平喘、抗过敏等作用",
        "syndrome_ids": ["syndrome_017", "syndrome_049"],
        "effect_ids": ["effect_001", "effect_006"],
        "beginner_note": "初学者：注意恶寒无汗咳喘痰稀白为辨证要点。",
        "advanced_clinical_note": "高级要点：麻黄用量宜灵活，表寒重者宜大，内饮重者宜小；注意勿久服免伤阴液。"
    },
    # formula_090 -> 葛根汤
    {
        "id": "formula_090",
        "name": "葛根汤",
        "pinyin": "Ge Gen Tang",
        "category": "解表剂",
        "subcategory": "辛温解表",
        "source": "《伤寒论》",
        "author": "张仲景",
        "ingredients": [
            {"medicine_id": "medicine_035", "name": "葛根", "quantity": "12g", "role": "君"},
            {"medicine_id": "medicine_001", "name": "麻黄", "quantity": "9g", "role": "臣"},
            {"medicine_id": "medicine_002", "name": "桂枝", "quantity": "6g", "role": "臣"},
            {"medicine_id": "medicine_073", "name": "甘草", "quantity": "6g", "role": "佐"},
        ],
        "effects": ["解肌发表", "升津舒筋"],
        "indications": ["太阳病项背强急，无汗恶风"],
        "usage": "水煎服，每日1剂，分两次服",
        "modern_applications": ["感冒", "颈椎病", "肩周炎", "面神经麻痹"],
        "pharmacological_effect": "具有解热、镇痛、改善颈部循环等作用",
        "syndrome_ids": ["syndrome_017", "syndrome_027"],
        "effect_ids": ["effect_021", "effect_001"],
        "beginner_note": "初学者：项背强急为葛根汤的辨证要点。",
        "advanced_clinical_note": "高级要点：葛根解肌升津，治项背强急效果显著；麻黄辛温解表，合用善于治疗项背挛急之外感证。"
    },
    # 再新增一批补充方剂
    {
        "id": "formula_091",
        "name": "桃核承气汤",
        "pinyin": "Tao He Cheng Qi Tang",
        "category": "理血剂",
        "subcategory": "活血化瘀",
        "source": "《伤寒论》",
        "author": "张仲景",
        "ingredients": [
            {"medicine_id": "medicine_042", "name": "桃仁", "quantity": "12g", "role": "君"},
            {"medicine_id": "medicine_016", "name": "大黄", "quantity": "9g", "role": "臣"},
            {"medicine_id": "medicine_002", "name": "桂枝", "quantity": "6g", "role": "佐"},
            {"medicine_id": "medicine_073", "name": "甘草", "quantity": "6g", "role": "使"},
        ],
        "effects": ["破血下瘀", "通便泻热"],
        "indications": ["下焦蓄血证：少腹急结硬满，其人如狂"],
        "usage": "水煎服，每日1剂，分两次服",
        "modern_applications": ["急性盆腔炎", "胎盘滞留", "痛经"],
        "pharmacological_effect": "具有改善微循环、抗炎、促进子宫收缩等作用",
        "syndrome_ids": ["syndrome_008"],
        "effect_ids": ["effect_009"],
        "beginner_note": "初学者：少腹急结如狂为下焦蓄血的辨证要点。",
        "advanced_clinical_note": "高级要点：桃仁破血祛瘀，大黄攻下瘀热，合用为破下活血要方。"
    },
    {
        "id": "formula_092",
        "name": "栀子豉汤",
        "pinyin": "Zhi Zi Chi Tang",
        "category": "清热剂",
        "subcategory": "清热除烦",
        "source": "《伤寒论》",
        "author": "张仲景",
        "ingredients": [
            {"medicine_id": "medicine_089", "name": "栀子", "quantity": "9g", "role": "君"},
            {"medicine_id": "medicine_090", "name": "淡豆豉", "quantity": "9g", "role": "臣"}
        ],
        "effects": ["清热除烦", "宣透郁热"],
        "indications": ["热郁胸膈证：心中懊憹，烦热不眠"],
        "usage": "水煎服，每日1剂",
        "modern_applications": ["神经官能症", "失眠", "胃炎"],
        "pharmacological_effect": "具有解热、镇静、抗炎等作用",
        "syndrome_ids": ["syndrome_020"],
        "effect_ids": ["effect_002", "effect_014"],
        "beginner_note": "初学者：心中懊憹烦热不眠为用方要点。",
        "advanced_clinical_note": "高级要点：栀子清透郁热，淡豆豉宣散郁火，清宣并用而不伤正。"
    },
    {
        "id": "formula_093",
        "name": "白虎加人参汤",
        "pinyin": "Bai Hu Jia Ren Shen Tang",
        "category": "清热剂",
        "subcategory": "清气分热",
        "source": "《伤寒论》",
        "author": "张仲景",
        "ingredients": [
            {"medicine_id": "medicine_008", "name": "石膏", "quantity": "30g", "role": "君"},
            {"medicine_id": "medicine_003", "name": "知母", "quantity": "12g", "role": "臣"},
            {"medicine_id": "medicine_073", "name": "甘草", "quantity": "6g", "role": "佐"},
            {"medicine_id": "medicine_004", "name": "人参", "quantity": "9g", "role": "佐"},
        ],
        "effects": ["清热生津", "益气养阴"],
        "indications": ["阳明热盛，气津两伤：大热大渴，脉洪大而芤"],
        "usage": "水煎服，每日1剂，分两次服",
        "modern_applications": ["糖尿病", "高热", "中暑", "甲状腺功能亢进"],
        "pharmacological_effect": "具有解热、降糖、改善口渴等作用",
        "syndrome_ids": ["syndrome_018", "syndrome_034"],
        "effect_ids": ["effect_002"],
        "beginner_note": "初学者：大热大渴汗出脉洪大，兼有气阴两伤为辨证要点。",
        "advanced_clinical_note": "高级要点：石膏清热力强；人参益气生津。气津两伤者用之尤宜。"
    },
    {
        "id": "formula_094",
        "name": "竹叶石膏汤",
        "pinyin": "Zhu Ye Shi Gao Tang",
        "category": "清热剂",
        "subcategory": "清热生津",
        "source": "《伤寒论》",
        "author": "张仲景",
        "ingredients": [
            {"medicine_id": "medicine_091", "name": "竹叶", "quantity": "9g", "role": "君"},
            {"medicine_id": "medicine_008", "name": "石膏", "quantity": "15g", "role": "臣"},
            {"medicine_id": "medicine_011", "name": "麦冬", "quantity": "12g", "role": "佐"},
            {"medicine_id": "medicine_073", "name": "甘草", "quantity": "6g", "role": "使"},
        ],
        "effects": ["清热生津", "益气和胃"],
        "indications": ["伤寒解后，余热未清：虚羸少气，气逆欲吐"],
        "usage": "水煎服，每日1剂，分两次服",
        "modern_applications": ["热病恢复期", "慢性胃炎", "糖尿病"],
        "pharmacological_effect": "具有解热、保护胃黏膜、促进恢复等作用",
        "syndrome_ids": ["syndrome_018", "syndrome_020"],
        "effect_ids": ["effect_002", "effect_003"],
        "beginner_note": "初学者：热病后期身热不退、口渴欲呕为用方要点。",
        "advanced_clinical_note": "高级要点：竹叶石膏善清解余热而不伤正，为热病后期调理要方。"
    },
    {
        "id": "formula_095",
        "name": "旋覆代赭汤",
        "pinyin": "Xuan Fu Dai Zhe Tang",
        "category": "理气剂",
        "subcategory": "降逆止呕",
        "source": "《伤寒论》",
        "author": "张仲景",
        "ingredients": [
            {"medicine_id": "medicine_092", "name": "旋覆花", "quantity": "9g", "role": "君"},
            {"medicine_id": "medicine_093", "name": "代赭石", "quantity": "15g", "role": "臣"},
            {"medicine_id": "medicine_007", "name": "半夏", "quantity": "9g", "role": "臣"},
            {"medicine_id": "medicine_004", "name": "人参", "quantity": "6g", "role": "佐"},
            {"medicine_id": "medicine_073", "name": "甘草", "quantity": "6g", "role": "使"},
        ],
        "effects": ["降逆化痰", "益气和胃"],
        "indications": ["胃虚痰阻气逆：心下痞硬，噫气不除"],
        "usage": "水煎服，每日1剂，分两次服",
        "modern_applications": ["慢性胃炎", "胃食管反流", "神经性呕吐"],
        "pharmacological_effect": "具有促进胃肠蠕动、抑制反流等作用",
        "syndrome_ids": ["syndrome_003", "syndrome_026"],
        "effect_ids": ["effect_003"],
        "beginner_note": "初学者：嗳气不除、心下痞硬为辨证要点。",
        "advanced_clinical_note": "高级要点：旋覆花降气化痰，代赭石重镇降逆，合为止呕降气要方。"
    },
    {
        "id": "formula_096",
        "name": "理中汤",
        "pinyin": "Li Zhong Tang",
        "category": "温里剂",
        "subcategory": "温中祛寒",
        "source": "《伤寒论》",
        "author": "张仲景",
        "ingredients": [
            {"medicine_id": "medicine_004", "name": "人参", "quantity": "9g", "role": "君"},
            {"medicine_id": "medicine_010", "name": "干姜", "quantity": "9g", "role": "君"},
            {"medicine_id": "medicine_022", "name": "白术", "quantity": "9g", "role": "臣"},
            {"medicine_id": "medicine_073", "name": "甘草", "quantity": "6g", "role": "使"},
        ],
        "effects": ["温中祛寒", "补气健脾"],
        "indications": ["脾胃虚寒证：腹满时痛，呕吐泄泻，手足不温"],
        "usage": "炼蜜为丸，或水煎服，每日1剂",
        "modern_applications": ["慢性胃肠炎", "消化性溃疡", "功能性消化不良"],
        "pharmacological_effect": "具有促进消化、抗溃疡、调节免疫等作用",
        "syndrome_ids": ["syndrome_021", "syndrome_003"],
        "effect_ids": ["effect_018", "effect_003"],
        "beginner_note": "初学者：吐利腹满手足不温，舌淡苔白为用方要点。",
        "advanced_clinical_note": "高级要点：姜参术草四药相配，温中有补，补中有温，为太阴虚寒代表方。"
    },
    {
        "id": "formula_097",
        "name": "吴茱萸汤",
        "pinyin": "Wu Zhu Yu Tang",
        "category": "温里剂",
        "subcategory": "温肝暖胃",
        "source": "《伤寒论》",
        "author": "张仲景",
        "ingredients": [
            {"medicine_id": "medicine_094", "name": "吴茱萸", "quantity": "6g", "role": "君"},
            {"medicine_id": "medicine_004", "name": "人参", "quantity": "9g", "role": "臣"},
            {"medicine_id": "medicine_073", "name": "甘草", "quantity": "6g", "role": "佐"},
        ],
        "effects": ["温肝暖胃", "降逆止呕"],
        "indications": ["肝胃虚寒，浊阴上逆：食后欲呕，巅顶头痛"],
        "usage": "水煎服，每日1剂，分两次服",
        "modern_applications": ["慢性胃炎", "偏头痛", "梅尼埃病"],
        "pharmacological_effect": "具有止呕、止痛、抗炎等作用",
        "syndrome_ids": ["syndrome_024", "syndrome_039"],
        "effect_ids": ["effect_018"],
        "beginner_note": "初学者：巅顶头痛、食后欲呕为用方要点。",
        "advanced_clinical_note": "高级要点：吴茱萸辛热暖肝；用人参温补中气。"
    },
    {
        "id": "formula_098",
        "name": "乌梅丸",
        "pinyin": "Wu Mei Wan",
        "category": "驱虫剂",
        "subcategory": "安蛔驱虫",
        "source": "《伤寒论》",
        "author": "张仲景",
        "ingredients": [
            {"medicine_id": "medicine_095", "name": "乌梅", "quantity": "15g", "role": "君"},
            {"medicine_id": "medicine_010", "name": "干姜", "quantity": "6g", "role": "臣"},
            {"medicine_id": "medicine_004", "name": "人参", "quantity": "6g", "role": "佐"},
            {"medicine_id": "medicine_022", "name": "白术", "quantity": "9g", "role": "佐"},
        ],
        "effects": ["安蛔止痛", "寒热并调"],
        "indications": ["蛔厥证：腹痛时作时止，手足厥冷"],
        "usage": "炼蜜为丸，或水煎服，每日1剂",
        "modern_applications": ["胆道蛔虫症", "慢性肠炎", "溃疡性结肠炎"],
        "pharmacological_effect": "具有驱虫、解痉、抗炎等作用",
        "syndrome_ids": ["syndrome_024"],
        "effect_ids": ["effect_026"],
        "beginner_note": "初学者：腹痛时作时止、得食痛作、有吐蛔史为要点。",
        "advanced_clinical_note": "高级要点：酸苦辛合法，乌梅酸能安蛔，配合清热温中，寒热错杂证通用。"
    },
    {
        "id": "formula_099",
        "name": "黄芪桂枝五物汤",
        "pinyin": "Huang Qi Gui Zhi Wu Wu Tang",
        "category": "补益剂",
        "subcategory": "益气通络",
        "source": "《金匮要略》",
        "author": "张仲景",
        "ingredients": [
            {"medicine_id": "medicine_096", "name": "黄芪", "quantity": "15g", "role": "君"},
            {"medicine_id": "medicine_002", "name": "桂枝", "quantity": "9g", "role": "臣"},
            {"medicine_id": "medicine_073", "name": "甘草", "quantity": "6g", "role": "使"},
        ],
        "effects": ["益气通络", "调和营卫"],
        "indications": ["血痹证：肌肤麻木不仁，肢节疼痛"],
        "usage": "水煎服，每日1剂，分两次服",
        "modern_applications": ["末梢神经炎", "颈椎病", "糖尿病周围神经病变"],
        "pharmacological_effect": "具有改善微循环、保护神经等作用",
        "syndrome_ids": ["syndrome_015", "syndrome_027"],
        "effect_ids": ["effect_003", "effect_016"],
        "beginner_note": "初学者：肢体麻木疼痛、恶风为用方要点。",
        "advanced_clinical_note": "高级要点：黄芪补气行血，桂枝温通经络，气血通则麻木除。"
    },
    {
        "id": "formula_100",
        "name": "麦门冬汤",
        "pinyin": "Mai Men Dong Tang",
        "category": "补益剂",
        "subcategory": "滋阴润肺",
        "source": "《金匮要略》",
        "author": "张仲景",
        "ingredients": [
            {"medicine_id": "medicine_011", "name": "麦冬", "quantity": "15g", "role": "君"},
            {"medicine_id": "medicine_007", "name": "半夏", "quantity": "6g", "role": "臣"},
            {"medicine_id": "medicine_004", "name": "人参", "quantity": "6g", "role": "佐"},
            {"medicine_id": "medicine_073", "name": "甘草", "quantity": "6g", "role": "使"},
        ],
        "effects": ["滋养肺胃", "降逆下气"],
        "indications": ["肺胃阴虚，虚火上炎：咳逆上气，咽喉不利"],
        "usage": "水煎服，每日1剂，分两次服",
        "modern_applications": ["慢性咽炎", "慢性支气管炎", "胃食管反流"],
        "pharmacological_effect": "具有润肺、抗炎、保护黏膜等作用",
        "syndrome_ids": ["syndrome_006", "syndrome_023"],
        "effect_ids": ["effect_007", "effect_003"],
        "beginner_note": "初学者：咳逆上气，咽喉不利，口干为辨证要点。",
        "advanced_clinical_note": "高级要点：麦冬养阴润肺，半夏降逆化痰，一润一降配伍精妙。"
    },
]

# 合并所有方剂
all_formulas = formulas + new_formulas

with open('/Users/yy/pro-test/zhongyi/assets/data/formulas.json', 'w', encoding='utf-8') as f:
    json.dump(all_formulas, f, ensure_ascii=False, indent=2)

print(f"Done! Removed 2 injection formulas, added {len(new_formulas)} new classic formulas.")
print(f"Total formulas: {len(all_formulas)}")
