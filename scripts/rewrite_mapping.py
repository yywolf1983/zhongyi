#!/usr/bin/env python3
"""重写中西医对照：古代术语 ↔ 现代症状的精细映射"""
import json

# 基于症状/体征层面的古今对照，而非简单的病名对应
mappings = [
    # === 发热与热象 ===
    {
        "id": "mapping_001",
        "chinese_term": "恶寒发热",
        "modern_term": "畏寒伴体温升高",
        "category": "症状",
        "explanation": "恶寒发热是外感表证的典型表现，「有一分恶寒便有一分表证」。现代医学中常见于感染性疾病的寒战发热期，机体通过骨骼肌收缩（寒战）产热以升高体温的免疫反应。",
        "related_syndrome": "syndrome_001"
    },
    {
        "id": "mapping_002",
        "chinese_term": "寒热往来",
        "modern_term": "间歇性发热/弛张热",
        "category": "症状",
        "explanation": "寒热往来是少阳病特征，病人自觉忽冷忽热。现代医学对应疟疾的间歇热、胆道感染的弛张热等，反映了病原体在体内周期性增殖释放导致的体温波动。",
        "related_syndrome": "syndrome_020"
    },
    {
        "id": "mapping_003",
        "chinese_term": "日晡潮热",
        "modern_term": "午后高热/弛张热高峰",
        "category": "症状",
        "explanation": "下午定时高热如潮，为阳明腑实的特征。现代常见于肠梗阻合并感染、严重腹腔感染等，下午体温高峰与机体生理节律相关。",
        "related_syndrome": "syndrome_019"
    },
    {
        "id": "mapping_004",
        "chinese_term": "身热不扬",
        "modern_term": "低热不退/慢性低热",
        "category": "症状",
        "explanation": "体温虽高但自觉热不显著，扪之肌肤灼手但不甚热。常见于湿温病，现代医学对应结核、慢性感染、肿瘤等引起的持续低热。",
        "related_syndrome": "syndrome_007"
    },
    {
        "id": "mapping_005",
        "chinese_term": "五心烦热",
        "modern_term": "手足心及胸口发热感/植物神经功能紊乱",
        "category": "症状",
        "explanation": "手足心和心胸部自觉发热，为阴虚内热的标志。现代常见于更年期综合征、焦虑症、甲亢等自主神经功能紊乱，体温可正常。",
        "related_syndrome": "syndrome_009"
    },

    # === 出汗与体液 ===
    {
        "id": "mapping_006",
        "chinese_term": "自汗",
        "modern_term": "白天不活动即出汗/多汗症",
        "category": "症状",
        "explanation": "白昼不因劳动、炎热即汗出，动则加重。中医认为表虚卫气不固。现代医学对应多汗症、甲亢、低血糖等导致的自主神经系统功能失调。",
        "related_syndrome": "syndrome_003"
    },
    {
        "id": "mapping_007",
        "chinese_term": "盗汗",
        "modern_term": "夜间睡眠时出汗/夜间多汗",
        "category": "症状",
        "explanation": "入睡汗出、醒来汗止，为阴虚内热的典型症状。现代对应结核病、淋巴瘤、艾滋病等感染消耗性疾病，以及更年期综合征的潮热出汗。",
        "related_syndrome": "syndrome_009"
    },
    {
        "id": "mapping_008",
        "chinese_term": "但头汗出",
        "modern_term": "仅头面部出汗/自主神经功能紊乱",
        "category": "症状",
        "explanation": "仅头部或头颈出汗，或伴心胸烦热。现代常见于更年期、焦虑发作、低血糖等导致的局限性多汗，也见于心衰危重症的头面出汗。",
        "related_syndrome": "syndrome_023"
    },

    # === 疼痛 ===
    {
        "id": "mapping_009",
        "chinese_term": "头痛如裹",
        "modern_term": "压迫性头痛/紧张性头痛",
        "category": "症状",
        "explanation": "头痛沉重如被布裹，伴肢体困重。现代对应紧张性头痛、鼻窦炎头痛，因颈肌和颅周肌肉持续紧张导致压迫感。",
        "related_syndrome": "syndrome_033"
    },
    {
        "id": "mapping_010",
        "chinese_term": "刺痛固定不移",
        "modern_term": "固定性锐痛/局部缺血性疼痛",
        "category": "症状",
        "explanation": "疼痛部位固定如针刺，拒按，夜间甚。这是瘀血的典型表现。现代对应缺血性疼痛、神经卡压综合征等，因局部血液循环障碍和代谢产物堆积导致。",
        "related_syndrome": "syndrome_008"
    },
    {
        "id": "mapping_011",
        "chinese_term": "胀痛走窜",
        "modern_term": "游走性胀痛/气机障碍性疼痛",
        "category": "症状",
        "explanation": "疼痛部位不固定，呈胀闷走窜性质。为气滞的典型特征。现代对应肠胀气疼痛、肋间神经痛等。",
        "related_syndrome": "syndrome_004"
    },
    {
        "id": "mapping_012",
        "chinese_term": "冷痛得热则减",
        "modern_term": "遇冷加重遇热缓解的疼痛",
        "category": "症状",
        "explanation": "冷痛是寒证的疼痛特征，得温痛减提示局部血液循环不佳。现代对应雷诺综合征、关节退行性病变等，温热可扩张血管缓解疼痛。",
        "related_syndrome": "syndrome_028"
    },
    {
        "id": "mapping_013",
        "chinese_term": "胸痛彻背",
        "modern_term": "放射至背部的胸痛/心绞痛",
        "category": "症状",
        "explanation": "胸痛向后背放射，喘息咳唾。这是胸痹的典型表现。现代医学对应心绞痛、心肌梗死，因冠脉供血不足导致心肌缺血缺氧。",
        "related_syndrome": "syndrome_029"
    },
    {
        "id": "mapping_014",
        "chinese_term": "少腹急结",
        "modern_term": "下腹部痉挛性疼痛/急腹症",
        "category": "症状",
        "explanation": "下腹部痉挛拘急硬满疼痛，这是下焦蓄血的体征。现代对应宫外孕破裂、盆腔炎、肠梗阻等引起的腹膜刺激征。",
        "related_syndrome": "syndrome_025"
    },

    # === 消化症状 ===
    {
        "id": "mapping_015",
        "chinese_term": "纳呆食少",
        "modern_term": "食欲减退/厌食",
        "category": "症状",
        "explanation": "食欲不振、食量减少，中医多责之脾胃虚弱。现代常见于慢性胃炎、抑郁症、恶性肿瘤等导致的食欲下降。",
        "related_syndrome": "syndrome_003"
    },
    {
        "id": "mapping_016",
        "chinese_term": "恶闻食臭",
        "modern_term": "厌恶食物气味/嗅觉过敏伴厌食",
        "category": "症状",
        "explanation": "闻到食物气味即恶心想呕。见于少阳病及肝胆疾病。现代对应肝炎、胆囊炎、早孕反应等的厌食油腻表现。",
        "related_syndrome": "syndrome_020"
    },
    {
        "id": "mapping_017",
        "chinese_term": "嗳腐吞酸",
        "modern_term": "胃食管反流/消化不良伴反酸",
        "category": "症状",
        "explanation": "嗳气带酸腐味、泛酸水，为食积停滞标志。现代对应胃食管反流病、功能性消化不良，食物在胃内过久停留发酵。",
        "related_syndrome": "syndrome_014"
    },
    {
        "id": "mapping_018",
        "chinese_term": "呕吐清稀",
        "modern_term": "呕吐水样清稀物",
        "category": "症状",
        "explanation": "呕吐物清稀不臭，为寒邪犯胃之象。现代见于急性胃肠炎、神经性呕吐的早期阶段。",
        "related_syndrome": "syndrome_039"
    },
    {
        "id": "mapping_019",
        "chinese_term": "呕吐酸腐",
        "modern_term": "呕吐酸臭腐败物/急性胃炎",
        "category": "症状",
        "explanation": "呕吐物酸腐难闻，为食积或湿热内蕴。现代见于急性胃炎、食物中毒的呕吐。",
        "related_syndrome": "syndrome_014"
    },
    {
        "id": "mapping_020",
        "chinese_term": "下利清谷",
        "modern_term": "水样便含不消化物/严重腹泻",
        "category": "症状",
        "explanation": "腹泻排出未经消化的食物残渣，为脾肾阳虚的标志。现代对应吸收不良综合征、严重肠炎、短肠综合征等。",
        "related_syndrome": "syndrome_022"
    },

    # === 口渴与津液 ===
    {
        "id": "mapping_021",
        "chinese_term": "烦渴引饮",
        "modern_term": "剧烈口渴多饮/高渗性脱水",
        "category": "症状",
        "explanation": "极度口渴大量饮水，为阳明热盛伤津或消渴病的典型表现。现代对应糖尿病酮症、高钙血症、严重脱水等引起的渗透性利尿和口渴中枢兴奋。",
        "related_syndrome": "syndrome_034"
    },
    {
        "id": "mapping_022",
        "chinese_term": "渴不欲饮",
        "modern_term": "口渴但不想喝水/湿阻中焦",
        "category": "症状",
        "explanation": "自觉口渴但不愿意喝水，或喝后不适。这是湿邪内阻的特征，现代见于胃肠功能减退、心衰水肿病人等体内并不缺水但津液输布障碍。",
        "related_syndrome": "syndrome_007"
    },
    {
        "id": "mapping_023",
        "chinese_term": "口不渴",
        "modern_term": "无口渴感/寒证或阳虚",
        "category": "症状",
        "explanation": "即使发热也不觉口渴，为寒证或阳虚的标志。现代见于急性感染早期、甲状腺功能减退等代谢低下状态。",
        "related_syndrome": "syndrome_017"
    },

    # === 二便 ===
    {
        "id": "mapping_024",
        "chinese_term": "小便清长",
        "modern_term": "尿量增多且色清/多尿症",
        "category": "症状",
        "explanation": "小便量多色清，为阳虚水气不化的特征。现代对应尿崩症、糖尿病多尿期、慢性肾病早期等。",
        "related_syndrome": "syndrome_005"
    },
    {
        "id": "mapping_025",
        "chinese_term": "小便短赤涩痛",
        "modern_term": "尿频尿急尿痛/尿路感染三联征",
        "category": "症状",
        "explanation": "小便量少色深、灼热疼痛，为湿热下注的表现。现代医学直接对应急性膀胱炎、尿道炎等下尿路感染的典型症状。",
        "related_syndrome": "syndrome_047"
    },
    {
        "id": "mapping_026",
        "chinese_term": "大便秘结如羊屎",
        "modern_term": "干硬球状便秘/慢传输型便秘",
        "category": "症状",
        "explanation": "大便干结如羊粪粒状，燥热内结的标志。现代对应慢传输型便秘，因肠道蠕动减慢、水分过度吸收导致粪便干硬。",
        "related_syndrome": "syndrome_041"
    },
    {
        "id": "mapping_027",
        "chinese_term": "大便黏腻不爽",
        "modern_term": "排便不尽感/大便黏滞",
        "category": "症状",
        "explanation": "大便黏滞不爽、里急后重感，为湿热蕴结的体征。现代对应肠易激综合征（腹泻型）、慢性结肠炎的功能紊乱。",
        "related_syndrome": "syndrome_011"
    },
    {
        "id": "mapping_028",
        "chinese_term": "里急后重",
        "modern_term": "急迫便意但排便困难/直肠刺激征",
        "category": "症状",
        "explanation": "紧急便意但排便不畅。现代医学对应细菌性痢疾、溃疡性结肠炎的直肠刺激表现。",
        "related_syndrome": "syndrome_011"
    },

    # === 神志与睡眠 ===
    {
        "id": "mapping_029",
        "chinese_term": "但欲寐",
        "modern_term": "嗜睡/精神状态低下",
        "category": "症状",
        "explanation": "终日昏昏欲睡、精神不振，为少阴病阳气衰微的标志。现代对应甲状腺功能减退（甲减）、抑郁症、慢性疲劳综合征的精神萎靡状态。",
        "related_syndrome": "syndrome_022"
    },
    {
        "id": "mapping_030",
        "chinese_term": "虚烦不眠",
        "modern_term": "烦躁性失眠/入睡困难伴焦虑",
        "category": "症状",
        "explanation": "心中烦乱、入睡困难，躺下后思绪万千。为阴虚火旺、热扰胸膈之象。现代对应焦虑性失眠、更年期失眠等。",
        "related_syndrome": "syndrome_023"
    },
    {
        "id": "mapping_031",
        "chinese_term": "谵语妄言",
        "modern_term": "谵妄/意识障碍伴胡言乱语",
        "category": "症状",
        "explanation": "神志不清、胡言乱语、声高有力，为阳明腑实热扰心神的危重表现。现代对应感染中毒性脑病、肝性脑病等导致的谵妄状态。",
        "related_syndrome": "syndrome_019"
    },
    {
        "id": "mapping_032",
        "chinese_term": "多梦易醒",
        "modern_term": "睡眠片段化/睡眠维持障碍",
        "category": "症状",
        "explanation": "入睡后多梦、频繁醒来，为心脾两虚证候。现代对应抑郁/焦虑相关的睡眠结构紊乱，REM睡眠异常增多。",
        "related_syndrome": "syndrome_045"
    },
    {
        "id": "mapping_033",
        "chinese_term": "善太息",
        "modern_term": "频繁叹气/胸闷伴深呼吸需求",
        "category": "症状",
        "explanation": "经常不自觉地长叹一声，叹后稍舒。这是肝气郁结的特征性表现。现代对应急性焦虑、换气过度综合征等导致的胸部憋闷感。",
        "related_syndrome": "syndrome_046"
    },

    # === 感觉与体表 ===
    {
        "id": "mapping_035",
        "chinese_term": "项背强急",
        "modern_term": "颈项背部僵硬/颈肌张力增高",
        "category": "症状",
        "explanation": "颈项及背部僵硬拘急、活动受限。中医责之太阳经气不舒。现代对应颈椎病、颈肌痉挛、脑膜刺激征的颈项强直等。",
        "related_syndrome": "syndrome_017"
    },
    {
        "id": "mapping_036",
        "chinese_term": "肢体困重",
        "modern_term": "身体沉重感/疲劳综合征",
        "category": "症状",
        "explanation": "自觉身体沉重、行动不便，如负百斤。为湿邪困阻的特征。现代对应慢性疲劳综合征、纤维肌痛、甲状腺功能减退等导致的乏力沉重感。",
        "related_syndrome": "syndrome_007"
    },
    {
        "id": "mapping_037",
        "chinese_term": "肌肤甲错",
        "modern_term": "皮肤干燥粗糙鳞屑化/鱼鳞病样改变",
        "category": "症状",
        "explanation": "皮肤干燥粗糙如鱼鳞片，为瘀血内阻、肌肤失养的表现。现代对应鱼鳞病、糖尿病周围血管病变、慢性消耗性疾病的皮肤营养障碍。",
        "related_syndrome": "syndrome_008"
    },
    {
        "id": "mapping_038",
        "chinese_term": "面色黧黑",
        "modern_term": "面部色素沉着/慢性肝病面容",
        "category": "症状",
        "explanation": "面色晦暗发黑，为瘀血或肾虚的体征。现代对应慢性肝病的肝病面容（色素沉着）、慢性肾功能不全的肾性面容等。",
        "related_syndrome": "syndrome_008"
    },
    {
        "id": "mapping_039",
        "chinese_term": "目黄身黄",
        "modern_term": "巩膜及皮肤黄染/黄疸",
        "category": "症状",
        "explanation": "眼白及皮肤发黄，小便赤黄。为黄疸的核心体征。现代医学的黄疸由胆红素代谢障碍引起，病因包括肝炎、胆道梗阻、溶血等。",
        "related_syndrome": "syndrome_030"
    },
    {
        "id": "mapping_040",
        "chinese_term": "口眼歪斜",
        "modern_term": "面瘫/面神经麻痹",
        "category": "症状",
        "explanation": "口角向一侧歪斜、眼睑闭合不全。风中经络或中风的体征。现代对应周围性面神经麻痹（Bell面瘫）或中枢性面瘫（脑血管病变）。",
        "related_syndrome": "syndrome_035"
    },

    # === 水肿 ===
    {
        "id": "mapping_041",
        "chinese_term": "目窠上微肿",
        "modern_term": "眼睑水肿/晨起眼皮浮肿",
        "category": "症状",
        "explanation": "早晨起床眼睑浮肿，是风水水肿的早期表现。现代对应急性肾小球肾炎的早期症状，因肾小球滤过率下降致水钠潴留。",
        "related_syndrome": "syndrome_031"
    },
    {
        "id": "mapping_042",
        "chinese_term": "腰以下肿甚",
        "modern_term": "下肢凹陷性水肿/体位性水肿",
        "category": "症状",
        "explanation": "水肿从下半身开始，按之凹陷不起。为肾阳虚水湿内停。现代对应慢性心力衰竭、肾病综合征、低蛋白血症等的体位性水肿。",
        "related_syndrome": "syndrome_005"
    },

    # === 舌脉 ===
    {
        "id": "mapping_043",
        "chinese_term": "舌紫暗有瘀斑",
        "modern_term": "舌质瘀暗/微循环障碍舌象",
        "category": "体征",
        "explanation": "舌色紫暗、有瘀点瘀斑，为瘀血证的客观指征。现代对应微循环障碍、高黏血症、心脏病、肝病等的舌象改变，与血液流变学异常相关。",
        "related_syndrome": "syndrome_008"
    },
    {
        "id": "mapping_044",
        "chinese_term": "苔黄燥",
        "modern_term": "舌苔黄干/脱水及胃肠积热",
        "category": "体征",
        "explanation": "舌苔黄而干糙，为里热伤津的标志。现代对应高热脱水、抗生素相关性念珠菌舌苔改变等。",
        "related_syndrome": "syndrome_018"
    },
    {
        "id": "mapping_045",
        "chinese_term": "苔白腻",
        "modern_term": "舌苔白厚腻/消化功能减退",
        "category": "体征",
        "explanation": "舌苔白而厚腻如糊，为湿浊内停的体征。现代对应胃肠道功能减退、口腔菌群失调导致的丝状乳头过度角化。",
        "related_syndrome": "syndrome_007"
    },

    # === 脉象 ===
    {
        "id": "mapping_046",
        "chinese_term": "脉浮紧",
        "modern_term": "浮紧脉/交感神经紧张状态",
        "category": "体征",
        "explanation": "轻取即得、紧张有力，为风寒表证的脉象。现代对应交感神经兴奋状态：心输出量增加+外周血管收缩，常见于感冒发热早期。",
        "related_syndrome": "syndrome_017"
    },
    {
        "id": "mapping_047",
        "chinese_term": "脉弦",
        "modern_term": "弦脉/动脉硬化和焦虑状态",
        "category": "体征",
        "explanation": "脉管硬如弓弦，为肝郁或疼痛的脉象。现代对应高血压动脉硬化、焦虑/紧张状态导致的血管平滑肌张力增高。",
        "related_syndrome": "syndrome_004"
    },
    {
        "id": "mapping_048",
        "chinese_term": "脉微细",
        "modern_term": "微细脉/低血容量或心衰状态",
        "category": "体征",
        "explanation": "脉搏极细弱无力，似有似无，为少阴病心肾阳衰的脉象。现代对应低血容量性休克、心力衰竭等导致的心输出量严重不足。",
        "related_syndrome": "syndrome_022"
    },
    {
        "id": "mapping_049",
        "chinese_term": "脉滑",
        "modern_term": "滑脉/血流加速状态",
        "category": "体征",
        "explanation": "脉来流利圆滑如珠滚，为痰湿或食积的脉象。现代对应血容量充足+血流加速状态，见于发热、妊娠、胃肠功能亢进等。",
        "related_syndrome": "syndrome_007"
    },

    # === 心理情绪 ===
    {
        "id": "mapping_050",
        "chinese_term": "烦躁",
        "modern_term": "烦躁不安/激越状态",
        "category": "心理",
        "explanation": "心烦意乱、躁动不安，为热扰心神的表现。现代对应焦虑激越、急性应激反应、甲亢等的烦躁状态。",
        "related_syndrome": "syndrome_013"
    },
    {
        "id": "mapping_051",
        "chinese_term": "默默不语",
        "modern_term": "社交退缩/情绪低落伴沉默",
        "category": "心理",
        "explanation": "沉默寡言、不愿与人交往，为少阳病或抑郁的表现。现代对应抑郁症的核心症状——社交退缩和兴趣丧失。",
        "related_syndrome": "syndrome_046"
    },
    {
        "id": "mapping_052",
        "chinese_term": "惊悸怔忡",
        "modern_term": "心悸惊恐/焦虑障碍躯体化",
        "category": "心理",
        "explanation": "心悸惊恐、坐卧不安，为心神不宁的表现。现代对应惊恐发作、广泛性焦虑障碍的心悸表现，常伴植物神经症状。",
        "related_syndrome": "syndrome_032"
    },
    {
        "id": "mapping_053",
        "chinese_term": "健忘",
        "modern_term": "记忆力下降/认知功能减退",
        "category": "心理",
        "explanation": "记忆力明显下降、转瞬即忘，为心脾两虚或髓海不足的表现。现代对应轻度认知障碍、早期痴呆、慢性疲劳的注意力和记忆损害。",
        "related_syndrome": "syndrome_045"
    },

    # === 病证层面 ===
    {
        "id": "mapping_054",
        "chinese_term": "半身不遂",
        "modern_term": "偏瘫/脑卒中后遗症",
        "category": "体征",
        "explanation": "一侧上下肢不能自主运动，为中风后经络瘀阻的主症。现代医学直接对应脑血管意外（脑梗死或脑出血）导致的偏瘫。",
        "related_syndrome": "syndrome_035"
    },
    {
        "id": "mapping_055",
        "chinese_term": "喉中哮鸣",
        "modern_term": "哮鸣音/支气管哮喘发作",
        "category": "症状",
        "explanation": "呼吸时喉中发出哮鸣声，为哮病发作的标志。现代医学的哮鸣音由气道痉挛和狭窄所致，是支气管哮喘急性发作的听诊特征。",
        "related_syndrome": "syndrome_049"
    },
    {
        "id": "mapping_056",
        "chinese_term": "消谷善饥",
        "modern_term": "多食易饥/代谢亢进",
        "category": "症状",
        "explanation": "食量增多仍易饥饿，为胃火炽盛或消渴的表现。现代对应甲亢的高代谢状态、1型糖尿病的多食表现。",
        "related_syndrome": "syndrome_034"
    },
    {
        "id": "mapping_057",
        "chinese_term": "肌肉萎软",
        "modern_term": "肌萎缩/神经肌肉疾病",
        "category": "体征",
        "explanation": "肌肉萎缩无力、不能随意运动，为痿证的核心体征。现代对应肌营养不良、运动神经元病、重症肌无力等导致的进行性肌肉萎缩。",
        "related_syndrome": "syndrome_048"
    },
    {
        "id": "mapping_058",
        "chinese_term": "关节肿大变形",
        "modern_term": "关节肿胀畸形/类风湿关节炎",
        "category": "体征",
        "explanation": "关节肿胀变形、屈伸不利，为痹证日久不愈。现代对应类风湿关节炎晚期、骨关节炎重度的关节结构改变。",
        "related_syndrome": "syndrome_027"
    },
    {
        "id": "mapping_059",
        "chinese_term": "爪甲青紫",
        "modern_term": "发绀/组织缺氧",
        "category": "体征",
        "explanation": "指甲口唇青紫，为瘀血或阳虚不能温运的标志。现代医学的发绀由血氧饱和度下降引起，见于心力衰竭、呼吸衰竭、休克等。",
        "related_syndrome": "syndrome_022"
    },
    {
        "id": "mapping_060",
        "chinese_term": "气上冲胸",
        "modern_term": "胃食管反流感/功能性胸闷",
        "category": "症状",
        "explanation": "自觉有气向上冲至心胸，伴心悸感。为奔豚气或气逆的典型描述。现代对应胃食管反流、功能性胸闷、焦虑躯体化的嗳气和胸闷。",
        "related_syndrome": "syndrome_024"
    },
]

with open('/Users/yy/pro-test/zhongyi/assets/data/modern_mapping.json', 'w', encoding='utf-8') as f:
    json.dump(mappings, f, ensure_ascii=False, indent=2)

print(f"Done! Modern mapping entries: {len(mappings)}")
print("Categories breakdown:")
cats = {}
for m in mappings:
    c = m['category']
    cats[c] = cats.get(c, 0) + 1
for c, n in sorted(cats.items()):
    print(f"  {c}: {n}")
