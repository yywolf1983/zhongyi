#!/usr/bin/env python3
"""
中医辨证论治知识库 - 数据汇总 Markdown 生成器
读取所有 JSON 数据，生成全面的学习参考文档
"""

import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE, "assets", "data")

def load_json(name):
    with open(os.path.join(DATA_DIR, name), 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    medicines = load_json("medicines.json")
    acupoints = load_json("acupoints.json")
    formulas = load_json("formulas.json")
    acu_prescriptions = load_json("acupuncture_prescriptions.json")
    needle_prescriptions = load_json("needle_prescriptions.json")
    meridians = load_json("meridians.json")
    syndromes = load_json("syndromes.json")
    treatments = load_json("treatments.json")
    effects = load_json("effects.json")
    modern_mapping = load_json("modern_mapping.json")

    # Build lookup maps & save counts
    med_map = {m['id']: m for m in medicines}
    acu_map = {a['id']: a for a in acupoints}
    fm_map = {f['id']: f for f in formulas}
    syn_map = {s['id']: s for s in syndromes}
    treat_map = {t['id']: t for t in treatments}

    n_medicines = len(medicines)
    n_acupoints = len(acupoints)
    n_formulas = len(formulas)
    n_syndromes = len(syndromes)
    n_treatments = len(treatments)
    n_effects = len(effects)
    n_acu_presc = len(acu_prescriptions)
    n_needle_presc = len(needle_prescriptions)
    n_meridians = len(meridians)
    n_mappings = len(modern_mapping)

    # ============ 常用药材精简 ============
    # 核心常用药材关键词（高频使用、经典教材必学）
    CORE_HERBS = {
        "解表药": ["麻黄","桂枝","紫苏","生姜","荆芥","防风","羌活","白芷","细辛","薄荷","牛蒡子","蝉蜕","桑叶","菊花","柴胡","升麻","葛根","淡豆豉"],
        "清热药": ["石膏","知母","芦根","天花粉","淡竹叶","栀子","夏枯草","决明子","黄芩","黄连","黄柏","龙胆","苦参","金银花","连翘","板蓝根","蒲公英","紫花地丁","鱼腥草","射干","白头翁","大血藤","败酱草","生地黄","玄参","牡丹皮","赤芍","青蒿","地骨皮"],
        "泻下药": ["大黄","芒硝","火麻仁","甘遂","巴豆"],
        "祛风湿药": ["独活","威灵仙","防己","秦艽","木瓜","桑寄生","五加皮","狗脊","苍术","络石藤"],
        "化湿药": ["藿香","佩兰","苍术","厚朴","砂仁","豆蔻"],
        "利水渗湿药": ["茯苓","猪苓","泽泻","车前子","滑石","薏苡仁","茵陈","金钱草","海金沙","石韦"],
        "温里药": ["附子","干姜","肉桂","吴茱萸","丁香","小茴香"],
        "理气药": ["陈皮","青皮","枳实","木香","香附","乌药","沉香","川楝子","佛手"],
        "消食药": ["山楂","神曲","麦芽","谷芽","莱菔子","鸡内金"],
        "驱虫药": ["使君子","槟榔","苦楝皮"],
        "止血药": ["小蓟","大蓟","地榆","槐花","白茅根","三七","茜草","蒲黄","艾叶","炮姜"],
        "活血化瘀药": ["川芎","延胡索","郁金","姜黄","乳香","没药","五灵脂","丹参","红花","桃仁","益母草","牛膝","鸡血藤","土鳖虫","水蛭","莪术","三棱"],
        "化痰止咳平喘药": ["半夏","天南星","旋覆花","白前","前胡","桔梗","川贝母","浙贝母","瓜蒌","竹茹","苦杏仁","紫苏子","百部","紫菀","款冬花","马兜铃","枇杷叶","桑白皮","葶苈子"],
        "安神药": ["朱砂","磁石","龙骨","琥珀","酸枣仁","柏子仁","远志","合欢皮"],
        "平肝熄风药": ["石决明","牡蛎","代赭石","羚羊角","牛黄","天麻","钩藤","地龙","全蝎","僵蚕"],
        "开窍药": ["麝香","冰片","石菖蒲","苏合香"],
        "补虚药": ["人参","西洋参","党参","黄芪","白术","山药","甘草","大枣","当归","熟地黄","白芍","阿胶","何首乌","龙眼肉","北沙参","南沙参","麦冬","天冬","石斛","玉竹","枸杞子","墨旱莲","女贞子","龟甲","鳖甲","鹿茸","巴戟天","淫羊藿","杜仲","续断","补骨脂","菟丝子","蛤蚧","冬虫夏草","紫河车"],
        "收涩药": ["五味子","乌梅","肉豆蔻","山茱萸","莲子","芡实","海螵蛸","桑螵蛸","金樱子"],
        "涌吐药": ["常山"],
        "解毒杀虫燥湿止痒药": ["雄黄","硫黄","白矾","蛇床子"],
        "拔毒化腐生肌药": ["升药","砒石","炉甘石","硼砂"],
    }

    # 常用药材ID列表
    common_ids = set()
    common_meds = []
    for m in medicines:
        cat = m['category']
        if cat in CORE_HERBS and m['name'] in CORE_HERBS[cat]:
            common_ids.add(m['id'])
            common_meds.append(m)

    # ============ 按类别整理的药材分组 ============
    med_by_category = {}
    for m in common_meds:
        cat = m['category']
        if cat not in med_by_category:
            med_by_category[cat] = []
        med_by_category[cat].append(m)

    # ============ 按类别整理的方剂分组 ============
    fm_by_category = {}
    for fm in formulas:
        cat = fm['category']
        if cat not in fm_by_category:
            fm_by_category[cat] = []
        fm_by_category[cat].append(fm)

    # ============ 证型链接关系 ============
    syn_relations = {}
    for s in syndromes:
        syn_relations[s['id']] = {
            'syndrome': s,
            'formulas': [fm_map[fid] for fid in s.get('related_formulas', []) if fid in fm_map],
            'treatments': [treat_map[tid] for tid in s.get('related_treatments', []) if tid in treat_map],
            'needles': [np for np in needle_prescriptions if s['id'] in np.get('related_syndromes', [])],
            'effects': [e for e in effects if s['id'] in e.get('related_syndromes', [])],
        }

    # ============ 中西医对照 ============
    mappings = {}
    for mm in modern_mapping:
        cat = mm['category']
        if cat not in mappings:
            mappings[cat] = []
        mappings[cat].append(mm)

    # ============ 生成 Markdown ============
    md = []
    md.append("# 中医辨证论治知识库 · 数据汇总\n")
    md.append("> 本文件汇总了中医辨证论治系统的全部核心数据，涵盖常用药材、穴位、经典方剂、证型、治法、功效及中西医对照。\n")
    md.append("> 生成时间：自动生成\n")

    # ── 目录 ──
    md.append("## 目录\n")
    md.append("1. [常用药材分类](#一常用药材分类)")
    md.append("2. [经络与穴位](#二经络与穴位)")
    md.append("3. [经典方剂](#三经典方剂)")
    md.append("4. [辨证论治体系](#四辨证论治体系)")
    md.append("5. [治法治则](#五治法治则)")
    md.append("6. [针灸处方](#六针灸处方)")
    md.append("7. [中西医对照](#七中西医对照)")
    md.append("8. [数据关联总览](#八数据关联总览)\n")

    # ════════════════════════════════════════
    # 一、常用药材
    # ════════════════════════════════════════
    md.append("## 一、常用药材分类\n")
    md.append(f"本系统收录药材 {len(medicines)} 味，其中**常用药材** {len(common_meds)} 味，分布于 {len(med_by_category)} 个大类。\n")

    for cat in sorted(med_by_category.keys()):
        meds_in_cat = sorted(med_by_category[cat], key=lambda x: x['name'])
        md.append(f"### {cat} ({len(meds_in_cat)}味)\n")
        md.append("| 药材 | 拼音 | 性味 | 归经 | 功效 | 用法用量 |")
        md.append("|------|------|------|------|------|----------|")
        for m in meds_in_cat:
            nature = m['nature']
            flavor = ''.join(m['flavor'])
            meridian = '、'.join(m['meridian'])
            eff_str = '、'.join(m['effects'][:3])
            usage = m.get('usage', '')
            md.append(f"| {m['name']} | {m['pinyin']} | {nature}/{flavor} | {meridian} | {eff_str} | {usage} |")
        md.append("")

    # ════════════════════════════════════════
    # 二、经络与穴位
    # ════════════════════════════════════════
    md.append("## 二、经络与穴位\n")
    md.append(f"本系统收录 {len(meridians)} 条经络（十四正经+经外奇穴），共 {len(acupoints)} 个穴位。\n")

    for mer in meridians:
        md.append(f"### {mer['name']}\n")
        md.append(f"- **拼音**: {mer['pinyin']}")
        if mer.get('yin_yang'):
            md.append(f"- **阴阳**: {mer['yin_yang']}")
        if mer.get('element'):
            md.append(f"- **五行**: {mer['element']}")
        md.append(f"- **循行**: {mer['path']}")
        md.append(f"- **主治**: {'、'.join(mer.get('indications', []))}")
        md.append(f"- **穴位**: {', '.join(mer.get('main_points', []))}")
        related_acu_ids = mer.get('related_acupoints', [])
        if related_acu_ids:
            md.append(f"- **关联穴位ID**: {', '.join(related_acu_ids)}")
        md.append("")

    # ════════════════════════════════════════
    # 三、经典方剂
    # ════════════════════════════════════════
    md.append("## 三、经典方剂\n")
    md.append(f"本系统收录经典方剂 {len(formulas)} 首，分为 {len(fm_by_category)} 个类别。\n")

    for cat in sorted(fm_by_category.keys()):
        fms_in_cat = sorted(fm_by_category[cat], key=lambda x: x['name'])
        md.append(f"### {cat} ({len(fms_in_cat)}首)\n")
        for fm in fms_in_cat:
            md.append(f"#### {fm['name']} `{fm['pinyin']}`\n")
            md.append(f"- **来源**: {fm.get('source', '未知')} · {fm.get('author', '佚名')}")
            md.append(f"- **分类**: {fm['subcategory']}")
            md.append(f"- **功效**: {'、'.join(fm['effects'])}")
            md.append(f"- **主治**: {'；'.join(fm['indications'])}")
            # 组成
            ings = fm.get('ingredients', [])
            ing_strs = []
            for i in ings:
                role_tag = {'君':'君💎','臣':'臣🔶','佐':'佐📎','使':'使📨'}.get(i['role'], i['role'])
                ing_strs.append(f"{i['name']}({i['quantity']})·{role_tag}")
            md.append(f"- **组成**: {', '.join(ing_strs)}")
            md.append(f"- **用法**: {fm.get('usage', '')}")
            if fm.get('modern_applications'):
                md.append(f"- **现代应用**: {'、'.join(fm['modern_applications'])}")
            if fm.get('beginner_note'):
                md.append(f"- **📖 初学者**: {fm['beginner_note']}")
            if fm.get('advanced_clinical_note'):
                md.append(f"- **🎯 进阶要点**: {fm['advanced_clinical_note']}")
            # 关联证型
            syn_ids = fm.get('syndrome_ids', [])
            if syn_ids:
                syn_names = [syn_map[sid]['name'] for sid in syn_ids if sid in syn_map]
                md.append(f"- **关联证型**: {'、'.join(syn_names)}")
            md.append("")

    # ════════════════════════════════════════
    # 四、辨证论治体系
    # ════════════════════════════════════════
    md.append("## 四、辨证论治体系\n")
    md.append("### 4.1 辨证方法概述\n")
    md.append("中医辨证论治体系包括多种辨证方法，各有侧重，相辅相成：\n")
    md.append("| 辨证方法 | 核心内容 | 适用范围 |")
    md.append("|----------|----------|----------|")
    md.append("| **八纲辨证** | 表里、寒热、虚实、阴阳 | 所有疾病的纲领性辨证 |")
    md.append("| **脏腑辨证** | 五脏六腑的功能失调 | 内伤杂病 |")
    md.append("| **病因辨证** | 外感六淫、内伤七情、饮食劳逸 | 病因分析 |")
    md.append("| **气血津液辨证** | 气血津液的盈虚通滞 | 气血津液病变 |")
    md.append("| **六经辨证** | 太阳、阳明、少阳、太阴、少阴、厥阴 | 外感伤寒 |")
    md.append("| **卫气营血辨证** | 卫分、气分、营分、血分 | 温病 |")
    md.append("| **三焦辨证** | 上焦、中焦、下焦 | 温病传变 |")
    md.append("| **经络辨证** | 十二经脉、奇经八脉 | 经络病证 |")

    md.append("\n### 4.2 病因总论\n")
    md.append("#### 4.2.1 外感病因（六淫）\n")
    md.append("| 六淫 | 性质 | 致病特点 | 常见病证 |")
    md.append("|------|------|----------|----------|")
    md.append("| **风** | 风为阳邪，其性开泄，易袭阳位；善行而数变；风为百病之长 | 发病急、传变快、游走性疼痛、皮肤瘙痒、头痛、恶风 | 风寒感冒、风热感冒、风疹、行痹（风湿关节痛） |")
    md.append("| **寒** | 寒为阴邪，易伤阳气；寒性凝滞；寒性收引 | 阳气受损→恶寒怕冷、四肢不温；气血凝滞→疼痛固定；经脉收缩→肢体拘挛 | 风寒感冒、寒痹（关节冷痛）、胃寒腹痛、寒凝痛经 |")
    md.append("| **暑** | 暑为阳邪，其性炎热；暑性升散，易伤津耗气；暑多挟湿 | 高热、大汗、口渴、气短乏力、头重如裹、胸闷泛恶 | 暑温、中暑、暑热感冒 |")
    md.append("| **湿** | 湿为阴邪，易阻遏气机，损伤阳气；湿性重浊；湿性黏滞；湿性趋下，易袭阴位 | 头身困重、胸闷脘痞、大便溏泄、病程缠绵难愈、下肢水肿带下 | 湿温、泄泻、着痹（湿痹）、水肿、带下病 |")
    md.append("| **燥** | 燥性干涩，易伤津液；燥易伤肺 | 口干舌燥、皮肤干燥、干咳少痰、鼻干咽痛 | 秋燥、燥咳、皮肤干燥症 |")
    md.append("| **火（热）** | 火为阳邪，其性炎上；易扰心神；易伤津耗气；易生风动血；易致肿疡 | 高热、面红目赤、烦躁、出血、疮疡、咽喉肿痛、尿黄便秘 | 热入气分、心火亢盛、肝火上炎、疮痈肿毒 |")

    md.append("\n#### 4.2.2 内伤病因\n")
    md.append("| 内伤类别 | 病机特点 | 常见病证 |")
    md.append("|----------|----------|----------|")
    md.append("| **七情过极** | 怒伤肝→气逆；喜伤心→气缓；思伤脾→气结；悲伤肺→气消；恐伤肾→气下；惊伤心神→气乱 | 肝郁气滞、心悸失眠、脾胃虚弱、肺气耗伤、肾虚 |")
    md.append("| **饮食不节** | 过饱伤脾→食积停滞；过饥→气血亏虚；偏嗜五味→脏腑偏盛偏衰；饮食不洁→损伤脾胃 | 食积、泄泻、胃痛、便秘 |")
    md.append("| **劳逸失度** | 过劳伤气→气虚乏力；房劳伤肾→肾精亏损；过逸伤气→气血运行不畅 | 气虚、肾虚、气滞血瘀 |")

    md.append("\n#### 4.2.3 病理产物性病因\n")
    md.append("| 病理产物 | 形成机制 | 致病特点 |")
    md.append("|----------|----------|----------|")
    md.append("| **痰饮** | 水液代谢障碍，津液停滞而成。稠浊为痰，清稀为饮 | 痰阻气机→胸闷脘痞；痰蒙清窍→头晕目眩；痰扰心神→癫狂；饮停胸胁→悬饮；饮溢肌肤→水肿 |")
    md.append("| **瘀血** | 气滞、气虚、寒凝、热结、外伤等导致血液运行不畅 | 刺痛固定、拒按、面色晦暗、舌紫或瘀斑、脉涩 |")
    md.append("| **结石** | 湿热煎熬、气化失常、饮食不当导致砂石形成 | 疼痛剧烈、排尿困难、黄疸 |")

    md.append("\n### 4.3 病机总论\n")
    md.append("#### 4.3.1 基本病机\n")
    md.append("| 病机类型 | 核心机制 | 具体表现 |")
    md.append("|----------|----------|----------|")
    md.append("| **邪正盛衰** | 邪气与正气的消长变化 | 实证：邪气盛而正气未衰；虚证：正气虚而邪气不盛；虚实夹杂：邪盛正虚并存 |")
    md.append("| **阴阳失调** | 阴阳偏盛、偏衰、互损、格拒、亡失 | 阳盛则热、阴盛则寒、阳虚则寒、阴虚则热；阴损及阳、阳损及阴；亡阴亡阳 |")
    md.append("| **气血失常** | 气血生成不足或运行障碍 | 气虚、气滞、气逆、气陷、气闭、气脱；血虚、血瘀、血热、血寒、出血 |")
    md.append("| **津液代谢失常** | 津液生成不足或输布排泄障碍 | 津液亏损→燥证；津液停滞→痰饮、水肿 |")
    md.append("| **内生五邪** | 内风、内寒、内湿、内燥、内火 | 内风→肝风内动；内寒→阳虚寒生；内湿→脾虚生湿；内燥→津亏液涸；内火→阳盛化火 |")

    md.append("#### 4.3.2 五脏病机\n")
    md.append("| 脏腑 | 主要病机 | 常见证型 |")
    md.append("|------|----------|----------|")
    md.append("| **心** | 心主血脉失常→血行不畅或心神不宁；心主神志失常→神不守舍 | 心气虚、心血虚、心阴虚、心阳虚、心火上炎、痰迷心窍、心血瘀阻 |")
    md.append("| **肺** | 肺主气失常→呼吸不利；肺主宣发肃降失常→咳嗽气喘；肺为娇脏→易受外邪 | 肺气虚、肺阴虚、风寒束肺、风热犯肺、燥邪伤肺、痰湿阻肺、痰热壅肺 |")
    md.append("| **脾** | 脾主运化失常→水谷不化或水湿内停；脾主升清失常→中气下陷；脾统血失常→出血 | 脾气虚、脾阳虚、脾不统血、寒湿困脾、湿热蕴脾 |")
    md.append("| **肝** | 肝主疏泄失常→气机郁滞或疏泄太过；肝藏血失常→血不归经；肝主筋失常→筋脉失养 | 肝气郁结、肝火上炎、肝血虚、肝阴虚、肝阳上亢、肝风内动、寒凝肝脉 |")
    md.append("| **肾** | 肾藏精失常→生长发育、生殖障碍；肾主水失常→水液代谢障碍；肾主纳气失常→气喘 | 肾阳虚、肾阴虚、肾精不足、肾气不固、肾不纳气 |")
    md.append("| **胆** | 胆汁分泌排泄异常；胆主决断失常 | 胆郁痰扰、胆气虚 |")
    md.append("| **胃** | 胃主受纳腐熟失常；胃气上逆 | 胃气虚、胃阴虚、胃寒、胃热（胃火）、食滞胃脘 |")
    md.append("| **小肠** | 受盛化物失常；泌别清浊失常 | 小肠虚寒、小肠实热 |")
    md.append("| **大肠** | 传导失常 | 大肠虚寒、大肠液亏、大肠湿热、肠燥便秘 |")
    md.append("| **膀胱** | 气化失常 | 膀胱湿热、膀胱虚寒 |")
    md.append("| **三焦** | 气化失常，水液运化障碍 | 上焦病、中焦病、下焦病 |")

    # ── 各证型详述 ──
    md.append("\n### 4.4 证型详述\n")
    md.append(f"本系统收录 {len(syndromes)} 个核心证型，每个证型包含辨证要点、病因病机、关联方剂、治法、针方等完整信息。\n")

    for s in syndromes:
        md.append(f"#### ✦ {s['name']} ({s['pinyin']})\n")
        md.append(f"- **辨证分类**: {'、'.join(s.get('classification', []))}")
        md.append(f"- **辨证体系**: {'、'.join(s.get('category', []))}")
        md.append(f"- **辨证要点**: ")
        for dp in s.get('diagnosis_points', []):
            md.append(f"  - {dp}")
        md.append(f"- **病因病机**: {s.get('pathogenesis', '')}")
        # 现代医学对应
        if s.get('modern_medicine'):
            mm_names = s['modern_medicine']
            md.append(f"- **对应现代疾病**: {'、'.join(mm_names)}")
            md.append(f"- **现代医学解释**: {s.get('modern_explanation', '')}")

        # 关联方剂
        rel_fm_ids = s.get('related_formulas', [])
        if rel_fm_ids:
            md.append(f"- **推荐方剂**: ")
            for fid in rel_fm_ids:
                if fid in fm_map:
                    fm = fm_map[fid]
                    md.append(f"  - {fm['name']}（{fm.get('source','')}）：{'、'.join(fm['effects'])}")
                    if fm.get('beginner_note'):
                        md.append(f"    - 💡 {fm['beginner_note']}")

        # 关联治法
        rel_treat_ids = s.get('related_treatments', [])
        if rel_treat_ids:
            md.append(f"- **推荐治法**: ")
            for tid in rel_treat_ids:
                if tid in treat_map:
                    t = treat_map[tid]
                    md.append(f"  - {t['name']}：{t['principle']}")

        # 关联针方
        rel_needle = s.get('related_needle', [])
        if rel_needle:
            md.append(f"- **推荐针方**: ")
            for nid in rel_needle:
                for np in needle_prescriptions:
                    if np['id'] == nid:
                        acu_pts = ', '.join([a['name'] for a in np.get('acupoints', [])])
                        md.append(f"  - {np['name']}：{acu_pts}")

        md.append("")

    # ════════════════════════════════════════
    # 五、治法治则
    # ════════════════════════════════════════
    md.append("## 五、治法治则\n")
    md.append("### 5.1 八法总纲\n")
    md.append("中医治疗八法，源于《黄帝内经》，由清代程钟龄在《医学心悟》中明确归纳：\n")
    md.append("| 治法 | 核心作用 | 代表方 | 适用范围 |")
    md.append("|------|----------|--------|----------|")
    md.append("| **汗法**  | 发汗解表、透邪外出 | 麻黄汤、桂枝汤、银翘散 | 表证：风寒/风热感冒、麻疹初起 |")
    md.append("| **吐法**  | 涌吐痰涎、宿食、毒物 | 瓜蒂散、救急稀涎散 | 痰涎壅盛、食积胃脘、误食毒物 |")
    md.append("| **下法**  | 攻下通便、荡涤实热 | 大承气汤、麻子仁丸 | 胃肠实热、便秘、积滞 |")
    md.append("| **和法**  | 和解少阳、调和肝脾 | 小柴胡汤、逍遥散、半夏泻心汤 | 半表半里、肝脾不和、寒热错杂 |")
    md.append("| **温法**  | 温中散寒、回阳救逆 | 理中汤、四逆汤 | 里寒证、阳虚证 |")
    md.append("| **清法**  | 清热泻火、凉血解毒 | 白虎汤、黄连解毒汤 | 里热证、热毒证 |")
    md.append("| **消法**  | 消食导滞、软坚散结 | 保和丸、桂枝茯苓丸 | 食积、痞块、积聚 |")
    md.append("| **补法**  | 补益气、血、阴、阳 | 四君子汤、四物汤、六味地黄丸 | 虚证：气虚、血虚、阴虚、阳虚 |")

    md.append("\n### 5.2 具体治法\n")
    md.append(f"本系统收录 {len(treatments)} 种具体治法：\n")
    md.append("| 治法 | 类别 | 治则原理 | 适用证型 | 代表方剂 | 针灸配穴 |")
    md.append("|------|------|----------|----------|----------|----------|")
    for t in treatments:
        syn_names = []
        for sid in t.get('related_syndromes', []):
            if sid in syn_map:
                syn_names.append(syn_map[sid]['name'])
        fm_names = []
        for fid in t.get('related_formulas', []):
            if fid in fm_map:
                fm_names.append(fm_map[fid]['name'])
        nd_names = []
        for nid in t.get('related_needle', []):
            for np in needle_prescriptions:
                if np['id'] == nid:
                    nd_names.append(np['name'])
        md.append(f"| {t['name']} | {t['category']} | {t['principle']} | {'、'.join(syn_names)} | {'、'.join(fm_names)} | {'、'.join(nd_names)} |")

    # ════════════════════════════════════════
    # 六、针灸处方
    # ════════════════════════════════════════
    md.append("\n## 六、针灸处方\n")
    md.append(f"### 6.1 针灸处方 ({len(acu_prescriptions)}首)\n")
    for ap in acu_prescriptions:
        md.append(f"#### {ap['name']} `{ap['pinyin']}`\n")
        md.append(f"- **分类**: {ap['category']} / {ap['subcategory']}")
        md.append(f"- **证型**: {ap['syndrome']}")
        acu_list = ap.get('acupoints', [])
        pt_strs = ', '.join([f"{a['name']}({a['method']})" for a in acu_list])
        md.append(f"- **选穴**: {pt_strs}")
        md.append(f"- **功效**: {'、'.join(ap.get('effects', []))}")
        md.append(f"- **主治**: {'、'.join(ap.get('indications', []))}")
        md.append(f"- **刺法**: {ap.get('method', '')}")
        if ap.get('modern_applications'):
            md.append(f"- **现代应用**: {'、'.join(ap['modern_applications'])}")
        if ap.get('beginner_note'):
            md.append(f"- **📖 初学者**: {ap['beginner_note']}")
        if ap.get('advanced_clinical_note'):
            md.append(f"- **🎯 进阶要点**: {ap['advanced_clinical_note']}")
        md.append("")

    md.append(f"### 6.2 针方 ({len(needle_prescriptions)}首)\n")
    for np in needle_prescriptions:
        md.append(f"#### {np['name']}\n")
        md.append(f"- **类别**: {np['category']}")
        acu_list = np.get('acupoints', [])
        pt_strs = ', '.join([f"{a['name']}({a['method']})" for a in acu_list])
        md.append(f"- **选穴**: {pt_strs}")
        md.append(f"- **功效**: {'、'.join(np.get('effects', []))}")
        md.append(f"- **主治**: {'、'.join(np.get('indications', []))}")
        if np.get('modern_applications'):
            md.append(f"- **现代应用**: {'、'.join(np['modern_applications'])}")
        md.append("")

    # ════════════════════════════════════════
    # 七、中西医对照
    # ════════════════════════════════════════
    md.append("## 七、中西医对照\n")
    md.append(f"本系统收录 {len(modern_mapping)} 条中西医术语对照，涵盖疾病、穴位、中药、方剂：\n")
    md.append("| 中医术语 | 现代医学 | 类别 | 说明 |")
    md.append("|----------|----------|------|------|")
    for mm in modern_mapping:
        md.append(f"| {mm['chinese_term']} | {mm['modern_term']} | {mm['category']} | {mm['explanation'][:60]}... |")

    # ════════════════════════════════════════
    # 八、数据关联总览
    # ════════════════════════════════════════
    md.append("\n## 八、数据关联总览\n")
    md.append("### 8.1 数据统计\n")
    md.append(f"| 数据模块 | 条目数 | 关联关系 |")
    md.append(f"|----------|--------|----------|")
    md.append(f"| 药材（Medicines） | {len(medicines)}（常用{len(common_meds)}） | 关联到方剂、功效、证型 |")
    md.append(f"| 穴位（Acupoints） | {len(acupoints)} | 关联到经络、针方、证型 |")
    md.append(f"| 经络（Meridians） | {len(meridians)} | 关联到穴位、证型 |")
    md.append(f"| 方剂（Formulas） | {len(formulas)} | 关联到药材、证型、功效 |")
    md.append(f"| 证型（Syndromes） | {len(syndromes)} | 关联到方剂、治法、针方、功效 |")
    md.append(f"| 治法（Treatments） | {len(treatments)} | 关联到证型、方剂、针方 |")
    md.append(f"| 功效（Effects） | {n_effects} | 关联到药材、方剂、证型 |")
    md.append(f"| 针灸处方 | {len(acu_prescriptions)} | 关联到穴位、证型 |")
    md.append(f"| 针方 | {len(needle_prescriptions)} | 关联到穴位、证型 |")
    md.append(f"| 中西医对照 | {len(modern_mapping)} | 关联到证型/穴位/药材/方剂 |")

    md.append("\n### 8.2 证型-方剂-治法-针方 关联矩阵\n")
    md.append("| 证型 | 推荐方剂 | 推荐治法 | 推荐针方 | 现代疾病 |")
    md.append("|------|----------|----------|----------|----------|")
    for s in syndromes:
        fm_names = [fm_map[fid]['name'] for fid in s.get('related_formulas', []) if fid in fm_map]
        treat_names = [treat_map[tid]['name'] for tid in s.get('related_treatments', []) if tid in treat_map]
        nd_names = []
        for nid in s.get('related_needle', []):
            for np in needle_prescriptions:
                if np['id'] == nid:
                    nd_names.append(np['name'])
        mm_names = s.get('modern_medicine', [])
        md.append(f"| {s['name']} | {'、'.join(fm_names)} | {'、'.join(treat_names)} | {'、'.join(nd_names)} | {'、'.join(mm_names)} |")

    md.append("\n### 8.3 常用药材-方剂关联\n")
    md.append("以下展示常用药材在各经典方剂中的使用情况：\n")
    md.append("| 药材 | 性味 | 归经 | 出现的经典方剂 |")
    md.append("|------|------|------|----------------|")
    for m in sorted(common_meds, key=lambda x: x['name']):
        used_in = []
        for fm in formulas:
            for ing in fm.get('ingredients', []):
                if ing['medicine_id'] == m['id']:
                    used_in.append(f"{fm['name']}({ing.get('role','-')})")
        used_str = '、'.join(used_in[:5])
        if len(used_in) > 5:
            used_str += f' 等{len(used_in)}首'
        nature = m['nature']
        flavor = ''.join(m['flavor'])
        meridian = '、'.join(m['meridian'])
        md.append(f"| {m['name']} | {nature}/{flavor} | {meridian} | {used_str} |")

    # ── 结束 ──
    md.append("\n---\n")
    md.append("*本文档由中医辨证论治知识库自动生成，数据来源于 assets/data/ 目录下的 JSON 数据文件。*\n")

    # 写入文件
    output_path = os.path.join(BASE, "docs", "数据汇总.md")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md))

    print(f"✅ Markdown 已生成: {output_path}")
    print(f"   药材: {n_medicines}条（常用{len(common_meds)}条）")
    print(f"   穴位: {n_acupoints}条")
    print(f"   经络: {n_meridians}条")
    print(f"   方剂: {n_formulas}首")
    print(f"   证型: {n_syndromes}个")
    print(f"   治法: {n_treatments}种")
    print(f"   功效: {n_effects}种")
    print(f"   针灸处方: {n_acu_presc}首")
    print(f"   针方: {n_needle_presc}首")
    print(f"   中西医对照: {n_mappings}条")

if __name__ == '__main__':
    main()
