#!/usr/bin/env python3
"""
中医数据全面丰富脚本
1. 交叉引用逆查补全（effect↔medicine, effect↔formula, effect↔syndrome）
2. 经络补全 related_acupoints
3. 治法补全 related_needle
4. 效果描述优化
5. 治法 related_formulas 逆查补全
"""

import json
import os
import shutil

DATA_DIR = "assets/data"
BACKUP_DIR = "assets/data_backup"

def load_json(filename):
    with open(os.path.join(DATA_DIR, filename), 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filename, data):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def backup():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    for f in os.listdir(DATA_DIR):
        if f.endswith('.json'):
            shutil.copy2(os.path.join(DATA_DIR, f), os.path.join(BACKUP_DIR, f))
    print("✅ 数据已备份到 assets/data_backup/")

def main():
    backup()

    # ============ 加载所有数据 ============
    effects = load_json("effects.json")
    medicines = load_json("medicines.json")
    formulas = load_json("formulas.json")
    syndromes = load_json("syndromes.json")
    meridians = load_json("meridians.json")
    treatments = load_json("treatments.json")
    acupoints = load_json("acupoints.json")
    needle_prescriptions = load_json("needle_prescriptions.json")

    # 建立索引
    effect_index = {e['name']: e for e in effects}
    effect_id_index = {e['id']: e for e in effects}
    medicine_index = {m['name']: m for m in medicines}
    medicine_id_index = {m['id']: m for m in medicines}
    formula_id_index = {f['id']: f for f in formulas}
    syndrome_id_index = {s['id']: s for s in syndromes}
    meridian_id_index = {m['id']: m for m in meridians}
    treatment_id_index = {t['id']: t for t in treatments}
    acupoint_id_index = {a['id']: a for a in acupoints}
    needle_id_index = {n['id']: n for n in needle_prescriptions}

    changes = {"effects_related": 0, "meridians": 0, "treatments": 0, "effects_desc": 0}

    # =====================================================
    # 1. 效果 ↔ 中药 交叉补全
    # =====================================================
    print("\n📦 补全效果↔中药交叉引用...")
    for effect in effects:
        effect_name = effect['name']
        matched_medicines = set(effect['related_medicines'])

        # 从中药 effects 字段逆查
        for med in medicines:
            if effect_name in med.get('effects', []):
                matched_medicines.add(med['id'])

        # 从中药 indications 逆查
        for ind in effect.get('indications', []):
            if ind == '适应证':
                continue
            for med in medicines:
                med_inds = ' '.join(med.get('indications', []))
                med_effs = ' '.join(med.get('effects', []))
                if ind in med_inds or ind in med_effs:
                    matched_medicines.add(med['id'])

        before = len(effect['related_medicines'])
        effect['related_medicines'] = sorted(matched_medicines)
        if len(effect['related_medicines']) > before:
            changes["effects_related"] += 1

    print(f"   关联补全: {changes['effects_related']} 条效果")

    # =====================================================
    # 2. 效果 ↔ 方剂 交叉补全
    # =====================================================
    print("\n📦 补全效果↔方剂交叉引用...")
    e2f_count = 0
    for effect in effects:
        effect_name = effect['name']
        matched = set(effect['related_formulas'])
        for f in formulas:
            if effect_name in f.get('effects', []):
                matched.add(f['id'])
        before = len(effect['related_formulas'])
        effect['related_formulas'] = sorted(matched)
        if len(effect['related_formulas']) > before:
            e2f_count += 1
    print(f"   方剂关联补全: {e2f_count} 条效果")

    # =====================================================
    # 3. 效果 ↔ 证型 交叉补全
    # =====================================================
    print("\n📦 补全效果↔证型交叉引用...")
    e2s_count = 0
    for effect in effects:
        matched = set(effect['related_syndromes'])
        for s in syndromes:
            if effect['id'] in s.get('related_effects', []):
                matched.add(s['id'])
        before = len(effect['related_syndromes'])
        effect['related_syndromes'] = sorted(matched)
        if len(effect['related_syndromes']) > before:
            e2s_count += 1
    print(f"   证型关联补全: {e2s_count} 条效果")

    # =====================================================
    # 4. 经络补全 related_acupoints
    # =====================================================
    print("\n📦 补全经络 related_acupoints...")
    for meridian in meridians:
        # 从穴位数据中找出属于该经络的所有穴位ID
        matched_ids = sorted([
            a['id'] for a in acupoints
            if a.get('meridian_id') == meridian['id']
        ])
        before = len(meridian.get('related_acupoints', []))
        meridian['related_acupoints'] = matched_ids
        if len(matched_ids) > before:
            changes["meridians"] += 1
            print(f"   {meridian['name']}: {before} → {len(matched_ids)} 穴")
    print(f"   经络补全: {changes['meridians']} 条")

    # =====================================================
    # 5. 治法补全 related_needle（从关联证型逆查）
    # =====================================================
    print("\n📦 补全治法 related_needle...")
    for treatment in treatments:
        matched = set(treatment.get('related_needle', []))
        for sid in treatment.get('related_syndromes', []):
            syndrome = syndrome_id_index.get(sid)
            if syndrome:
                for nid in syndrome.get('related_needle', []):
                    if nid in needle_id_index:
                        matched.add(nid)
        before = len(treatment.get('related_needle', []))
        treatment['related_needle'] = sorted(matched)
        if len(treatment['related_needle']) > before:
            changes["treatments"] += 1
            print(f"   {treatment['name']}: 针方 {before} → {len(treatment['related_needle'])}")
    print(f"   治法补全: {changes['treatments']} 条")

    # =====================================================
    # 6. 效果描述优化（替换泛化描述）
    # =====================================================
    print("\n📦 优化效果描述...")
    description_map = {
        "滋阴降火": "通过甘寒滋阴药物深层次填补阴液，配合清降药物抑制虚火亢盛，达到阴阳平衡的治疗作用",
        "活血化瘀": "通过活血化瘀药物改善血液循环、消除血液瘀滞，抗血小板聚集，调节微循环的治疗作用",
        "补气活血": "通过补气药物增强元气推动力，配合活血化瘀药物改善血液循环，标本兼顾的治疗作用",
        "益气健脾": "通过补益药物增强脾胃运化功能，促进气血生化之源，改善消化吸收的治疗作用",
        "燥湿化痰": "通过温热燥湿药物燥化体内湿浊，配合化痰药物溶解排除痰饮，恢复脾胃运化的治疗作用",
        "养阴润肺": "通过甘润药物滋养肺阴，清除虚热，缓解燥咳，改善呼吸道黏膜功能的治疗作用",
        "活血祛瘀": "通过活血化瘀与逐瘀药物，改善血液循环，消除陈旧瘀血，促进组织修复的治疗作用",
        "疏风清热": "通过辛凉疏风药物疏散外风，配合清热药物清除体内热邪，解表清里的复合治疗作用",
        "益气养血": "通过补气药物增强元气和脏腑功能，配合滋阴养血药物双补气血的治疗作用",
        "养心安神": "通过滋养心血、安定心神的药物，调节中枢神经系统功能，改善睡眠质量的治疗作用",
        "清心泻火": "通过苦寒药物清泻心经火邪，配合安神药物安定心神，治疗心火亢盛的治疗作用",
        "益气固表": "通过补气药物增强卫外功能，固护肌表防御，调节免疫功能的治疗作用",
        "平肝息风": "通过平肝潜阳药物配合息风止痉药物，降低血压、镇静安神，防治脑血管意外的治疗作用",
        "和解少阳": "通过柴胡、黄芩等药物疏解半表半里之邪，调和枢机，调节自主神经和免疫功能的治疗作用",
        "温中散寒": "通过辛温药物温暖中焦脾胃，驱散寒邪，改善消化道血液循环和消化功能的治疗作用",
        "回阳救逆": "通过大辛大热药物强力温补，挽回衰微阳气，强心升压改善休克的急救治疗作用",
        "通腑泻热": "通过攻下药物通利肠道、排除热结燥屎，促进肠蠕动，治疗肠梗阻和发热的治疗作用",
        "利水渗湿": "通过渗利药物使水湿从小便排出，促进肾脏排尿、调节水盐代谢的治疗作用",
        "祛风除湿": "通过辛散药物祛除关节经络之风寒湿邪，抗炎镇痛、改善关节功能的治疗作用",
        "清热退黄": "通过苦寒清热与利湿药物，疏利肝胆，促进胆红素排泄，治疗黄疸性肝炎的治疗作用",
        "宽胸化痰": "通过辛开苦降药物调畅胸中气机，化散痰浊，扩张冠脉、改善心肌供血的治疗作用",
        "消食化积": "通过消导药物促进消化酶活性、增强胃肠蠕动、调节肠道菌群来消除食积的治疗作用",
        "清营凉血": "通过苦寒药物清泄营分热邪，凉散血分瘀热，抗炎降体温、防止DIC的治疗作用",
        "镇肝熄风": "通过重镇平肝药物配合息风药物，降血压、改善脑循环，防治中风的治疗作用",
        "祛风胜湿": "通过辛散祛风配合利湿药物，抗炎镇痛、调节免疫来治疗风湿类疾病的治疗作用",
        "豁痰开窍": "通过化痰与芳香开窍药物，清除痰浊蒙蔽，保护脑细胞、抗惊厥的治疗作用",
        "健脾利湿": "通过健脾药物增强运化，配合利湿药物使水湿排出，调节水盐代谢的治疗作用",
        "活血通窍": "通过活血化瘀药物配合通窍药物，改善头部微循环、促进神经修复的治疗作用",
        "涩精止遗": "通过收涩药物增强肾气封藏功能，防止精液滑泄和遗尿的治疗作用",
        "清暑利湿": "通过清热解暑药物配合利湿药物，清除暑湿之邪，调节体温和水盐代谢的治疗作用",
        "补益肝肾": "通过补益肝肾药物，增强肝肾功能，改善精血亏虚，强壮筋骨的治疗作用",
        "养阴清热": "通过甘润养阴药物填补阴液，配合寒凉清热药物清除虚热，调节内分泌的治疗作用",
        "生津润燥": "通过甘润药物促进津液生成，濡养干燥组织，缓解口干咽燥和便秘的治疗作用",
        "化痰止咳": "通过化痰药物溶解排除痰液，配合止咳药物缓解咳嗽，改善呼吸道功能的治疗作用",
        "清热解毒": "通过苦寒清热药物清除热毒，抗菌抗炎、增强免疫功能的治疗作用",
        "发汗解表": "通过辛温发散药物促进汗腺分泌，使汗液排出以发散表邪，解除表证的治疗作用",
        "温补肾阳": "通过温热药物补充肾脏阳气，增强温煦气化功能，调节内分泌和能量代谢的治疗作用",
        "补血养血": "通过补血药物促进造血功能，改善微循环，调节营养代谢的治疗作用",
        "清热利湿": "通过苦寒清热药物配合利湿药物，抗菌抗炎、促进尿液排出的治疗作用",
        "宣肺平喘": "通过宣散药物恢复肺气宣发肃降，配合平喘药物缓解咳喘的治疗作用",
        "固肾涩精": "通过收涩药物增强肾气封藏功能，固摄精关，防止精气滑脱的治疗作用",
        "消痈散结": "通过清热解毒与活血散结药物，消除痈肿、消散结块，抗菌抗炎的治疗作用",
        "升阳举陷": "通过补气兼升提药物，将下陷之气提升复位，治疗内脏下垂的治疗作用",
        "熄风止痉": "通过平肝息风药物镇静安神，制止肝风内动所致的抽搐痉挛的治疗作用",
        "交通心肾": "通过药物配伍调和心肾功能，使心火下温肾水、肾水上济心火的治疗作用",
        "润肠通便": "通过润滑肠道药物缓解肠燥，配合泻下或润肠药物通导大便的治疗作用",
        "活血止痛": "通过活血化瘀配合止痛药物，改善局部循环，消除瘀血阻滞所致疼痛的治疗作用",
        "理气化痰": "通过行气药物配合化痰药物，调畅气机并消除痰浊，改善胸闷咳喘的治疗作用",
        "疏肝解郁": "通过疏肝理气药物缓解肝气郁结，调和气血运行，改善情绪和躯体症状的治疗作用",
        "行气止痛": "通过辛香行气药物促进气机运行，配合理气活血药物缓解各种疼痛的治疗作用",
    }

    for effect in effects:
        name = effect['name']
        if name in description_map:
            old_desc = effect.get('description', '')
            if '通过相关药物的配伍，发挥' in old_desc or len(old_desc) < 15:
                effect['description'] = description_map[name]
                changes["effects_desc"] += 1

    print(f"   描述优化: {changes['effects_desc']} 条效果")

    # =====================================================
    # 7. 效果 mechanism 优化
    # =====================================================
    print("\n📦 优化效果机制描述...")
    m_count = 0
    for effect in effects:
        name = effect['name']
        if name in description_map and effect.get('mechanism', '').startswith('通过相关药物的配伍，发挥'):
            effect['mechanism'] = description_map[name]
            m_count += 1
    print(f"   机制描述优化: {m_count} 条效果")

    # =====================================================
    # 8. 证型 related_effects 逆查补全
    # =====================================================
    print("\n📦 补全证型 related_effects (从方剂逆查)...")
    s_count = 0
    for syndrome in syndromes:
        matched = set(syndrome.get('related_effects', []))
        for fid in syndrome.get('related_formulas', []):
            f = formula_id_index.get(fid)
            if f:
                for eid in f.get('effect_ids', []):
                    if eid in effect_id_index:
                        matched.add(eid)
        before = len(syndrome.get('related_effects', []))
        syndrome['related_effects'] = sorted(matched)
        if len(syndrome['related_effects']) > before:
            s_count += 1
    print(f"   证型补全: {s_count} 条")

    # =====================================================
    # 9. 治法 related_formulas 从关联证型逆查
    # =====================================================
    print("\n📦 补全治法 related_formulas...")
    t_count = 0
    for treatment in treatments:
        matched = set(treatment.get('related_formulas', []))
        for sid in treatment.get('related_syndromes', []):
            syndrome = syndrome_id_index.get(sid)
            if syndrome:
                for fid in syndrome.get('related_formulas', []):
                    if fid in formula_id_index:
                        matched.add(fid)
        before = len(treatment.get('related_formulas', []))
        treatment['related_formulas'] = sorted(matched)
        if len(treatment['related_formulas']) > before:
            t_count += 1
    print(f"   治法方剂补全: {t_count} 条")

    # =====================================================
    # 10. 补全 effects indications 的「适应证」占位
    # =====================================================
    print("\n📦 优化效果 indications 占位...")
    ind_count = 0
    for effect in effects:
        inds = effect.get('indications', [])
        if len(inds) == 1 and inds[0] == '适应证':
            # 从中药/方剂关联中推导 indications
            derived = set()
            name = effect['name']
            for med_id in effect.get('related_medicines', []):
                med = medicine_id_index.get(med_id)
                if med:
                    for ind in med.get('indications', [])[:3]:
                        if len(ind) < 20:
                            derived.add(ind)
            for fid in effect.get('related_formulas', []):
                f = formula_id_index.get(fid)
                if f:
                    for ind in f.get('effects', [])[:3]:
                        derived.add(ind)
            if derived:
                effect['indications'] = sorted(derived)
                ind_count += 1
    print(f"   适应证优化: {ind_count} 条效果")

    # ============ 保存所有数据 ============
    print("\n💾 保存数据...")
    save_json("effects.json", effects)
    save_json("meridians.json", meridians)
    save_json("treatments.json", treatments)
    save_json("syndromes.json", syndromes)

    # ============ 最终统计 ============
    print("\n" + "="*50)
    print("📊 最终统计")
    print("="*50)

    for fname in ["effects.json", "meridians.json", "treatments.json", "syndromes.json"]:
        data = load_json(fname)
        empty_count = sum(1 for item in data for k,v in item.items() if isinstance(v, list) and len(v) == 0)
        print(f"   {fname}: {len(data)}条, 空数组 {empty_count}个")

    print("\n✅ 数据丰富完成！")

if __name__ == "__main__":
    main()
