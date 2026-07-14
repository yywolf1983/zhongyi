#!/usr/bin/env python3
"""补充缺失中药数据到500味"""
import json

# 完整的补充药物数据
missing_herbs = [
    # ====== 安神药 ======
    {"name": "朱砂", "pinyin": "Zhu Sha", "latin_name": "Cinnabaris", "nature": "微寒", "flavor": ["甘"], "meridian": ["心经"], "effects": ["清心镇惊", "安神解毒"], "indications": ["心悸易惊", "失眠多梦"], "usage": "0.1-0.5g，入丸散", "contraindications": ["孕妇慎用"], "category": "安神药", "subcategory": "重镇安神药"},
    {"name": "磁石", "pinyin": "Ci Shi", "latin_name": "Magnetitum", "nature": "寒", "flavor": ["咸"], "meridian": ["心经", "肝经", "肾经"], "effects": ["镇惊安神", "平肝潜阳"], "indications": ["心悸失眠", "头晕目眩"], "usage": "煎服，9-30g", "contraindications": [], "category": "安神药", "subcategory": "重镇安神药"},
    {"name": "龙骨", "pinyin": "Long Gu", "latin_name": "Os Draconis", "nature": "平", "flavor": ["甘", "涩"], "meridian": ["心经", "肝经", "肾经"], "effects": ["镇惊安神", "平肝潜阳", "收敛固涩"], "indications": ["心悸失眠", "眩晕", "遗精带下"], "usage": "煎服，15-30g", "contraindications": [], "category": "安神药", "subcategory": "重镇安神药"},
    {"name": "柏子仁", "pinyin": "Bai Zi Ren", "latin_name": "Platycladi Semen", "nature": "平", "flavor": ["甘"], "meridian": ["心经", "肾经", "大肠经"], "effects": ["养心安神", "润肠通便"], "indications": ["心悸失眠", "肠燥便秘"], "usage": "煎服，3-10g", "contraindications": [], "category": "安神药", "subcategory": "养心安神药"},
    {"name": "合欢皮", "pinyin": "He Huan Pi", "latin_name": "Albiziae Cortex", "nature": "平", "flavor": ["甘"], "meridian": ["心经", "肝经"], "effects": ["解郁安神", "活血消肿"], "indications": ["心神不安", "忧郁失眠"], "usage": "煎服，6-12g", "contraindications": [], "category": "安神药", "subcategory": "养心安神药"},
    {"name": "灵芝", "pinyin": "Ling Zhi", "latin_name": "Ganoderma", "nature": "平", "flavor": ["甘"], "meridian": ["心经", "肺经", "肝经", "肾经"], "effects": ["补气安神", "止咳平喘"], "indications": ["心神不宁", "虚劳咳喘"], "usage": "煎服，6-12g", "contraindications": [], "category": "安神药", "subcategory": "养心安神药"},
    {"name": "首乌藤", "pinyin": "Shou Wu Teng", "latin_name": "Polygoni Multiflori Caulis", "nature": "平", "flavor": ["甘"], "meridian": ["心经", "肝经"], "effects": ["养血安神", "祛风通络"], "indications": ["失眠多梦", "血虚身痛"], "usage": "煎服，9-15g", "contraindications": [], "category": "安神药", "subcategory": "养心安神药"},
    
    # ====== 平肝熄风药 ======
    {"name": "石决明", "pinyin": "Shi Jue Ming", "latin_name": "Haliotidis Concha", "nature": "寒", "flavor": ["咸"], "meridian": ["肝经"], "effects": ["平肝潜阳", "清肝明目"], "indications": ["头痛眩晕", "目赤肿痛"], "usage": "煎服，6-20g，先煎", "contraindications": [], "category": "平肝熄风药", "subcategory": ""},
    {"name": "珍珠母", "pinyin": "Zhen Zhu Mu", "latin_name": "Margaritifera Concha", "nature": "寒", "flavor": ["咸"], "meridian": ["肝经", "心经"], "effects": ["平肝潜阳", "安神定惊"], "indications": ["头痛眩晕", "心悸失眠"], "usage": "煎服，10-25g", "contraindications": [], "category": "平肝熄风药", "subcategory": ""},
    {"name": "蒺藜", "pinyin": "Ji Li", "latin_name": "Tribuli Fructus", "nature": "平", "flavor": ["辛", "苦"], "meridian": ["肝经"], "effects": ["平肝解郁", "活血祛风", "明目"], "indications": ["头痛眩晕", "胸胁胀痛"], "usage": "煎服，6-9g", "contraindications": [], "category": "平肝熄风药", "subcategory": ""},
    {"name": "罗布麻", "pinyin": "Luo Bu Ma", "latin_name": "Apocyni Veneti Folium", "nature": "凉", "flavor": ["甘", "苦"], "meridian": ["肝经"], "effects": ["平抑肝阳", "清热利尿"], "indications": ["头晕目眩", "水肿"], "usage": "煎服，6-12g", "contraindications": [], "category": "平肝熄风药", "subcategory": ""},
    {"name": "僵蚕", "pinyin": "Jiang Can", "latin_name": "Bombyx Batryticatus", "nature": "平", "flavor": ["咸", "辛"], "meridian": ["肝经", "肺经"], "effects": ["息风止痉", "祛风止痛", "化痰散结"], "indications": ["惊痫抽搐", "头痛", "瘰疬"], "usage": "煎服，5-10g", "contraindications": [], "category": "平肝熄风药", "subcategory": ""},
    {"name": "全蝎", "pinyin": "Quan Xie", "latin_name": "Scorpio", "nature": "平", "flavor": ["辛"], "meridian": ["肝经"], "effects": ["息风镇痉", "通络止痛", "攻毒散结"], "indications": ["痉挛抽搐", "风湿顽痹"], "usage": "煎服，3-6g", "contraindications": ["孕妇禁用"], "category": "平肝熄风药", "subcategory": ""},
    {"name": "蜈蚣", "pinyin": "Wu Gong", "latin_name": "Scolopendra", "nature": "温", "flavor": ["辛"], "meridian": ["肝经"], "effects": ["息风镇痉", "通络止痛", "攻毒散结"], "indications": ["痉挛抽搐", "风湿顽痹"], "usage": "煎服，3-5g", "contraindications": ["孕妇禁用"], "category": "平肝熄风药", "subcategory": ""},
    {"name": "地龙", "pinyin": "Di Long", "latin_name": "Pheretima", "nature": "寒", "flavor": ["咸"], "meridian": ["肝经", "脾经", "膀胱经"], "effects": ["清热定惊", "通络", "平喘", "利尿"], "indications": ["高热惊痫", "半身不遂", "痹痛"], "usage": "煎服，4.5-9g", "contraindications": [], "category": "平肝熄风药", "subcategory": ""},
    
    # ====== 开窍药 ======
    {"name": "冰片", "pinyin": "Bing Pian", "latin_name": "Borneolum", "nature": "微寒", "flavor": ["辛", "苦"], "meridian": ["心经", "脾经", "肺经"], "effects": ["开窍醒神", "清热止痛"], "indications": ["闭证神昏", "目赤肿痛"], "usage": "0.15-0.3g，入丸散", "contraindications": ["孕妇慎用"], "category": "开窍药", "subcategory": ""},
    {"name": "苏合香", "pinyin": "Su He Xiang", "latin_name": "Styrax", "nature": "温", "flavor": ["辛"], "meridian": ["心经", "脾经"], "effects": ["开窍醒神", "辟秽止痛"], "indications": ["寒闭神昏", "胸腹冷痛"], "usage": "0.3-1g，入丸散", "contraindications": [], "category": "开窍药", "subcategory": ""},
    {"name": "蟾酥", "pinyin": "Chan Su", "latin_name": "Bufonis Venenum", "nature": "温", "flavor": ["辛"], "meridian": ["心经"], "effects": ["开窍醒神", "解毒止痛"], "indications": ["闭证神昏", "疮疡肿痛"], "usage": "0.015-0.03g，入丸散", "contraindications": ["孕妇禁用"], "category": "开窍药", "subcategory": ""},
    
    # ====== 收涩药 ======
    {"name": "五味子", "pinyin": "Wu Wei Zi", "latin_name": "Schisandrae Chinensis Fructus", "nature": "温", "flavor": ["酸", "甘"], "meridian": ["肺经", "心经", "肾经"], "effects": ["收敛固涩", "益气生津", "补肾宁心"], "indications": ["久咳虚喘", "梦遗滑精", "久泻不止"], "usage": "煎服，1.5-6g", "contraindications": [], "category": "收涩药", "subcategory": ""},
    {"name": "山茱萸", "pinyin": "Shan Zhu Yu", "latin_name": "Corni Fructus", "nature": "微温", "flavor": ["酸", "甘"], "meridian": ["肝经", "肾经"], "effects": ["补益肝肾", "收涩固脱"], "indications": ["眩晕耳鸣", "腰膝酸痛", "遗精滑精"], "usage": "煎服，6-12g", "contraindications": [], "category": "收涩药", "subcategory": ""},
    {"name": "乌梅", "pinyin": "Wu Mei", "latin_name": "Mume Fructus", "nature": "平", "flavor": ["酸", "涩"], "meridian": ["肝经", "脾经", "肺经", "大肠经"], "effects": ["敛肺涩肠", "生津安蛔"], "indications": ["久咳", "久泻", "蛔厥腹痛"], "usage": "煎服，6-12g", "contraindications": [], "category": "收涩药", "subcategory": ""},
    {"name": "诃子", "pinyin": "He Zi", "latin_name": "Chebulae Fructus", "nature": "平", "flavor": ["苦", "酸", "涩"], "meridian": ["肺经", "大肠经"], "effects": ["涩肠止泻", "敛肺止咳"], "indications": ["久泻久痢", "久咳失音"], "usage": "煎服，3-10g", "contraindications": [], "category": "收涩药", "subcategory": ""},
    {"name": "肉豆蔻", "pinyin": "Rou Dou Kou", "latin_name": "Myristicae Semen", "nature": "温", "flavor": ["辛"], "meridian": ["脾经", "胃经", "大肠经"], "effects": ["涩肠止泻", "温中行气"], "indications": ["久泻不止", "脘腹胀痛"], "usage": "煎服，3-9g", "contraindications": [], "category": "收涩药", "subcategory": ""},
    {"name": "赤石脂", "pinyin": "Chi Shi Zhi", "latin_name": "Halloysitum Rubrum", "nature": "温", "flavor": ["甘", "涩"], "meridian": ["大肠经", "胃经"], "effects": ["涩肠止泻", "收敛止血", "敛疮生肌"], "indications": ["久泻久痢", "崩漏便血"], "usage": "煎服，9-12g", "contraindications": [], "category": "收涩药", "subcategory": ""},
    {"name": "莲子", "pinyin": "Lian Zi", "latin_name": "Nelumbinis Semen", "nature": "平", "flavor": ["甘", "涩"], "meridian": ["脾经", "肾经", "心经"], "effects": ["补脾止泻", "益肾固精", "养心安神"], "indications": ["脾虚泄泻", "遗精滑精", "心悸失眠"], "usage": "煎服，6-15g", "contraindications": [], "category": "收涩药", "subcategory": ""},
    {"name": "芡实", "pinyin": "Qian Shi", "latin_name": "Euryales Semen", "nature": "平", "flavor": ["甘", "涩"], "meridian": ["脾经", "肾经"], "effects": ["益肾固精", "健脾止泻", "除湿止带"], "indications": ["遗精滑精", "脾虚久泻", "带下"], "usage": "煎服，9-15g", "contraindications": [], "category": "收涩药", "subcategory": ""},
    {"name": "海螵蛸", "pinyin": "Hai Piao Xiao", "latin_name": "Sepiae Endoconcha", "nature": "微温", "flavor": ["咸", "涩"], "meridian": ["肝经", "肾经"], "effects": ["固精止带", "收敛止血", "制酸止痛"], "indications": ["遗精带下", "崩漏", "胃痛泛酸"], "usage": "煎服，5-10g", "contraindications": [], "category": "收涩药", "subcategory": ""},
    {"name": "金樱子", "pinyin": "Jin Ying Zi", "latin_name": "Rosae Laevigatae Fructus", "nature": "平", "flavor": ["酸", "甘", "涩"], "meridian": ["肾经", "膀胱经", "大肠经"], "effects": ["固精缩尿", "涩肠止泻"], "indications": ["遗精滑精", "遗尿", "久泻"], "usage": "煎服，6-12g", "contraindications": [], "category": "收涩药", "subcategory": ""},
    {"name": "桑螵蛸", "pinyin": "Sang Piao Xiao", "latin_name": "Mantidis Ootheca", "nature": "平", "flavor": ["甘", "咸"], "meridian": ["肝经", "肾经"], "effects": ["固精缩尿", "补肾助阳"], "indications": ["遗精滑精", "遗尿", "阳痿"], "usage": "煎服，5-10g", "contraindications": [], "category": "收涩药", "subcategory": ""},
    {"name": "覆盆子", "pinyin": "Fu Pen Zi", "latin_name": "Rubi Fructus", "nature": "温", "flavor": ["甘", "酸"], "meridian": ["肝经", "肾经", "膀胱经"], "effects": ["益肾固精缩尿", "养肝明目"], "indications": ["遗精滑精", "遗尿", "目暗不明"], "usage": "煎服，6-12g", "contraindications": [], "category": "收涩药", "subcategory": ""},
    
    # ====== 温里药补充 ======
    {"name": "小茴香", "pinyin": "Xiao Hui Xiang", "latin_name": "Foeniculi Fructus", "nature": "温", "flavor": ["辛"], "meridian": ["肝经", "肾经", "脾经", "胃经"], "effects": ["散寒止痛", "理气和胃"], "indications": ["寒疝腹痛", "脘腹胀痛"], "usage": "煎服，3-6g", "contraindications": [], "category": "温里药", "subcategory": ""},
    {"name": "荜茇", "pinyin": "Bi Ba", "latin_name": "Piperis Longi Fructus", "nature": "热", "flavor": ["辛"], "meridian": ["胃经", "大肠经"], "effects": ["温中散寒", "下气止痛"], "indications": ["脘腹冷痛", "呕吐泄泻"], "usage": "煎服，1-3g", "contraindications": [], "category": "温里药", "subcategory": ""},
    {"name": "荜澄茄", "pinyin": "Bi Cheng Qie", "latin_name": "Litseae Fructus", "nature": "温", "flavor": ["辛"], "meridian": ["脾经", "胃经", "肾经", "膀胱经"], "effects": ["温中散寒", "行气止痛"], "indications": ["胃寒腹痛", "呕吐"], "usage": "煎服，1.5-3g", "contraindications": [], "category": "温里药", "subcategory": ""},
    
    # ====== 补虚药大量补充 ======
    {"name": "西洋参", "pinyin": "Xi Yang Shen", "latin_name": "Panacis Quinquefolii Radix", "nature": "凉", "flavor": ["甘", "微苦"], "meridian": ["心经", "肺经", "肾经"], "effects": ["补气养阴", "清热生津"], "indications": ["气阴两虚", "虚热烦倦"], "usage": "煎服，3-6g", "contraindications": [], "category": "补虚药", "subcategory": "补气药"},
    {"name": "太子参", "pinyin": "Tai Zi Shen", "latin_name": "Pseudostellariae Radix", "nature": "平", "flavor": ["甘", "微苦"], "meridian": ["脾经", "肺经"], "effects": ["益气健脾", "生津润肺"], "indications": ["脾虚体倦", "病后虚弱"], "usage": "煎服，9-30g", "contraindications": [], "category": "补虚药", "subcategory": "补气药"},
    {"name": "白扁豆", "pinyin": "Bai Bian Dou", "latin_name": "Lablab Semen Album", "nature": "微温", "flavor": ["甘"], "meridian": ["脾经", "胃经"], "effects": ["健脾化湿", "和中消暑"], "indications": ["脾虚泄泻", "暑湿吐泻"], "usage": "煎服，9-15g", "contraindications": [], "category": "补虚药", "subcategory": "补气药"},
    {"name": "饴糖", "pinyin": "Yi Tang", "latin_name": "Maltosum", "nature": "温", "flavor": ["甘"], "meridian": ["脾经", "胃经", "肺经"], "effects": ["补中益气", "缓急止痛", "润肺止咳"], "indications": ["脾胃虚寒", "虚寒腹痛", "肺燥咳嗽"], "usage": "烊化冲服，15-30g", "contraindications": [], "category": "补虚药", "subcategory": "补气药"},
    {"name": "蜂蜜", "pinyin": "Feng Mi", "latin_name": "Mel", "nature": "平", "flavor": ["甘"], "meridian": ["肺经", "脾经", "大肠经"], "effects": ["补中润燥", "止痛解毒"], "indications": ["脘腹虚痛", "肺燥干咳", "肠燥便秘"], "usage": "冲服，15-30g", "contraindications": [], "category": "补虚药", "subcategory": "补气药"},
    
    {"name": "阿胶", "pinyin": "E Jiao", "latin_name": "Asini Corii Colla", "nature": "平", "flavor": ["甘"], "meridian": ["肺经", "肝经", "肾经"], "effects": ["补血止血", "滋阴润燥"], "indications": ["血虚萎黄", "出血证"], "usage": "3-9g，烊化冲服", "contraindications": [], "category": "补虚药", "subcategory": "补血药"},
    {"name": "何首乌", "pinyin": "He Shou Wu", "latin_name": "Polygoni Multiflori Radix", "nature": "温", "flavor": ["苦", "甘", "涩"], "meridian": ["肝经", "肾经"], "effects": ["补肝肾", "益精血", "乌须发"], "indications": ["血虚萎黄", "须发早白"], "usage": "煎服，6-12g", "contraindications": [], "category": "补虚药", "subcategory": "补血药"},
    {"name": "龙眼肉", "pinyin": "Long Yan Rou", "latin_name": "Longan Arillus", "nature": "温", "flavor": ["甘"], "meridian": ["心经", "脾经"], "effects": ["补益心脾", "养血安神"], "indications": ["气血不足", "心悸失眠", "健忘"], "usage": "煎服，9-15g", "contraindications": [], "category": "补虚药", "subcategory": "补血药"},
    
    {"name": "百合", "pinyin": "Bai He", "latin_name": "Lilii Bulbus", "nature": "寒", "flavor": ["甘"], "meridian": ["心经", "肺经"], "effects": ["养阴润肺", "清心安神"], "indications": ["阴虚燥咳", "虚烦惊悸"], "usage": "煎服，6-12g", "contraindications": [], "category": "补虚药", "subcategory": "补阴药"},
    {"name": "玉竹", "pinyin": "Yu Zhu", "latin_name": "Polygonati Odorati Rhizoma", "nature": "微寒", "flavor": ["甘"], "meridian": ["肺经", "胃经"], "effects": ["养阴润燥", "生津止渴"], "indications": ["肺胃阴伤", "燥热咳嗽"], "usage": "煎服，6-12g", "contraindications": [], "category": "补虚药", "subcategory": "补阴药"},
    {"name": "石斛", "pinyin": "Shi Hu", "latin_name": "Dendrobii Caulis", "nature": "微寒", "flavor": ["甘"], "meridian": ["胃经", "肾经"], "effects": ["益胃生津", "滋阴清热"], "indications": ["胃阴不足", "阴虚发热"], "usage": "煎服，6-12g", "contraindications": [], "category": "补虚药", "subcategory": "补阴药"},
    {"name": "黄精", "pinyin": "Huang Jing", "latin_name": "Polygonati Rhizoma", "nature": "平", "flavor": ["甘"], "meridian": ["脾经", "肺经", "肾经"], "effects": ["补气养阴", "健脾润肺益肾"], "indications": ["脾胃气虚", "肺虚燥咳", "肾虚腰酸"], "usage": "煎服，9-15g", "contraindications": [], "category": "补虚药", "subcategory": "补阴药"},
    {"name": "女贞子", "pinyin": "Nv Zhen Zi", "latin_name": "Ligustri Lucidi Fructus", "nature": "凉", "flavor": ["甘", "苦"], "meridian": ["肝经", "肾经"], "effects": ["滋补肝肾", "乌须明目"], "indications": ["肝肾阴虚", "须发早白"], "usage": "煎服，6-12g", "contraindications": [], "category": "补虚药", "subcategory": "补阴药"},
    {"name": "墨旱莲", "pinyin": "Mo Han Lian", "latin_name": "Ecliptae Herba", "nature": "寒", "flavor": ["甘", "酸"], "meridian": ["肝经", "肾经"], "effects": ["滋补肝肾", "凉血止血"], "indications": ["肝肾阴虚", "须发早白", "出血"], "usage": "煎服，6-12g", "contraindications": [], "category": "补虚药", "subcategory": "补阴药"},
    {"name": "龟甲", "pinyin": "Gui Jia", "latin_name": "Testudinis Carapax", "nature": "寒", "flavor": ["甘", "咸"], "meridian": ["肝经", "肾经", "心经"], "effects": ["滋阴潜阳", "益肾强骨", "养血补心"], "indications": ["阴虚潮热", "骨蒸盗汗", "腰膝酸软"], "usage": "煎服，9-24g", "contraindications": [], "category": "补虚药", "subcategory": "补阴药"},
    {"name": "天冬", "pinyin": "Tian Dong", "latin_name": "Asparagi Radix", "nature": "寒", "flavor": ["甘", "苦"], "meridian": ["肺经", "肾经"], "effects": ["养阴润燥", "清肺生津"], "indications": ["肺燥干咳", "咽干口渴"], "usage": "煎服，6-12g", "contraindications": [], "category": "补虚药", "subcategory": "补阴药"},
    {"name": "南沙参", "pinyin": "Nan Sha Shen", "latin_name": "Adenophorae Radix", "nature": "微寒", "flavor": ["甘"], "meridian": ["肺经", "胃经"], "effects": ["养阴清肺", "益胃生津", "化痰益气"], "indications": ["肺热燥咳", "胃阴不足"], "usage": "煎服，9-15g", "contraindications": [], "category": "补虚药", "subcategory": "补阴药"},
    
    {"name": "巴戟天", "pinyin": "Ba Ji Tian", "latin_name": "Morindae Officinalis Radix", "nature": "微温", "flavor": ["辛", "甘"], "meridian": ["肝经", "肾经"], "effects": ["补肾助阳", "祛风除湿"], "indications": ["阳痿", "宫冷", "风湿痹痛"], "usage": "煎服，3-10g", "contraindications": [], "category": "补虚药", "subcategory": "补阳药"},
    {"name": "续断", "pinyin": "Xu Duan", "latin_name": "Dipsaci Radix", "nature": "微温", "flavor": ["苦", "辛"], "meridian": ["肝经", "肾经"], "effects": ["补肝肾", "强筋骨", "续折伤", "安胎"], "indications": ["腰膝酸软", "跌打损伤", "胎动不安"], "usage": "煎服，9-15g", "contraindications": [], "category": "补虚药", "subcategory": "补阳药"},
    {"name": "补骨脂", "pinyin": "Bu Gu Zhi", "latin_name": "Psoraleae Fructus", "nature": "温", "flavor": ["辛", "苦"], "meridian": ["肾经", "脾经"], "effects": ["补肾壮阳", "固精缩尿", "温脾止泻"], "indications": ["肾虚阳痿", "遗精遗尿", "虚寒泄泻"], "usage": "煎服，6-10g", "contraindications": [], "category": "补虚药", "subcategory": "补阳药"},
    {"name": "益智仁", "pinyin": "Yi Zhi Ren", "latin_name": "Alpiniae Oxyphyllae Fructus", "nature": "温", "flavor": ["辛"], "meridian": ["肾经", "脾经"], "effects": ["暖肾固精缩尿", "温脾止泻摄唾"], "indications": ["遗尿", "遗精", "脾寒泄泻"], "usage": "煎服，3-10g", "contraindications": [], "category": "补虚药", "subcategory": "补阳药"},
    {"name": "菟丝子", "pinyin": "Tu Si Zi", "latin_name": "Cuscutae Semen", "nature": "平", "flavor": ["辛", "甘"], "meridian": ["肝经", "肾经", "脾经"], "effects": ["补肾益精", "养肝明目", "安胎"], "indications": ["肾虚阳痿", "腰膝酸软", "胎动不安"], "usage": "煎服，6-12g", "contraindications": [], "category": "补虚药", "subcategory": "补阳药"},
    {"name": "沙苑子", "pinyin": "Sha Yuan Zi", "latin_name": "Astragali Complanati Semen", "nature": "温", "flavor": ["甘"], "meridian": ["肝经", "肾经"], "effects": ["补肾固精", "养肝明目"], "indications": ["肾虚阳痿", "遗精早泄", "目昏"], "usage": "煎服，9-15g", "contraindications": [], "category": "补虚药", "subcategory": "补阳药"},
    {"name": "冬虫夏草", "pinyin": "Dong Chong Xia Cao", "latin_name": "Cordyceps", "nature": "平", "flavor": ["甘"], "meridian": ["肺经", "肾经"], "effects": ["补肾益肺", "止血化痰"], "indications": ["阳痿遗精", "久咳虚喘"], "usage": "煎服，3-9g", "contraindications": [], "category": "补虚药", "subcategory": "补阳药"},
    {"name": "蛤蚧", "pinyin": "Ge Jie", "latin_name": "Gecko", "nature": "平", "flavor": ["咸"], "meridian": ["肺经", "肾经"], "effects": ["补肺益肾", "纳气定喘", "助阳益精"], "indications": ["虚喘气促", "阳痿"], "usage": "煎服，3-6g", "contraindications": [], "category": "补虚药", "subcategory": "补阳药"},
    {"name": "紫河车", "pinyin": "Zi He Che", "latin_name": "Hominis Placenta", "nature": "温", "flavor": ["甘", "咸"], "meridian": ["肺经", "肝经", "肾经"], "effects": ["补肾益精", "益气养血"], "indications": ["虚劳羸瘦", "骨蒸盗汗", "阳痿"], "usage": "研末，1.5-3g", "contraindications": [], "category": "补虚药", "subcategory": "补阳药"},
    {"name": "锁阳", "pinyin": "Suo Yang", "latin_name": "Cynomorii Herba", "nature": "温", "flavor": ["甘"], "meridian": ["肝经", "肾经", "大肠经"], "effects": ["补肾助阳", "润肠通便"], "indications": ["阳痿遗精", "肠燥便秘"], "usage": "煎服，5-10g", "contraindications": [], "category": "补虚药", "subcategory": "补阳药"},
    {"name": "肉苁蓉", "pinyin": "Rou Cong Rong", "latin_name": "Cistanches Herba", "nature": "温", "flavor": ["甘", "咸"], "meridian": ["肾经", "大肠经"], "effects": ["补肾助阳", "润肠通便"], "indications": ["肾阳不足", "精血亏虚", "肠燥便秘"], "usage": "煎服，6-10g", "contraindications": [], "category": "补虚药", "subcategory": "补阳药"},
    
    # ====== 泻下药补充 ======
    {"name": "芒硝", "pinyin": "Mang Xiao", "latin_name": "Natrii Sulfas", "nature": "寒", "flavor": ["咸", "苦"], "meridian": ["胃经", "大肠经"], "effects": ["泻下通便", "润燥软坚", "清热消肿"], "indications": ["积滞便秘", "咽痛口疮"], "usage": "6-12g，冲服", "contraindications": ["孕妇禁用"], "category": "泻下药", "subcategory": "攻下药"},
    {"name": "甘遂", "pinyin": "Gan Sui", "latin_name": "Kansui Radix", "nature": "寒", "flavor": ["苦"], "meridian": ["肺经", "肾经", "大肠经"], "effects": ["泻水逐饮", "消肿散结"], "indications": ["水肿胀满", "胸腹积水"], "usage": "0.5-1g，入丸散", "contraindications": ["孕妇禁用"], "category": "泻下药", "subcategory": "峻下逐水药"},
    {"name": "京大戟", "pinyin": "Jing Da Ji", "latin_name": "Euphorbiae Pekinensis Radix", "nature": "寒", "flavor": ["苦"], "meridian": ["肺经", "肾经"], "effects": ["泻水逐饮", "消肿散结"], "indications": ["水肿胀满", "胸腹积水"], "usage": "1.5-3g，入丸散", "contraindications": ["孕妇禁用"], "category": "泻下药", "subcategory": "峻下逐水药"},
    {"name": "芫花", "pinyin": "Yuan Hua", "latin_name": "Genkwa Flos", "nature": "温", "flavor": ["辛", "苦"], "meridian": ["肺经", "肾经", "大肠经"], "effects": ["泻水逐饮", "祛痰止咳"], "indications": ["胸胁积水", "咳嗽痰喘"], "usage": "煎服，1.5-3g", "contraindications": ["孕妇禁用"], "category": "泻下药", "subcategory": "峻下逐水药"},
    {"name": "巴豆", "pinyin": "Ba Dou", "latin_name": "Crotonis Fructus", "nature": "热", "flavor": ["辛"], "meridian": ["胃经", "大肠经"], "effects": ["峻下冷积", "逐水消肿", "祛痰利咽"], "indications": ["寒积便秘", "腹水", "喉痹"], "usage": "0.1-0.3g，入丸散", "contraindications": ["孕妇禁用"], "category": "泻下药", "subcategory": "峻下逐水药"},
    {"name": "牵牛子", "pinyin": "Qian Niu Zi", "latin_name": "Pharbitidis Semen", "nature": "寒", "flavor": ["苦"], "meridian": ["肺经", "肾经", "大肠经"], "effects": ["泻下逐水", "去积杀虫"], "indications": ["水肿胀满", "虫积腹痛"], "usage": "煎服，3-6g", "contraindications": ["孕妇禁用"], "category": "泻下药", "subcategory": "峻下逐水药"},
    
    # ====== 利水渗湿药补充 ======
    {"name": "车前草", "pinyin": "Che Qian Cao", "latin_name": "Plantaginis Herba", "nature": "寒", "flavor": ["甘"], "meridian": ["肝经", "肾经", "肺经"], "effects": ["清热利尿", "祛痰凉血", "解毒"], "indications": ["热淋涩痛", "水肿", "暑湿泻痢"], "usage": "煎服，9-30g", "contraindications": [], "category": "利水渗湿药", "subcategory": "利尿通淋药"},
    {"name": "滑石", "pinyin": "Hua Shi", "latin_name": "Talcum", "nature": "寒", "flavor": ["甘", "淡"], "meridian": ["膀胱经", "肺经", "胃经"], "effects": ["利尿通淋", "清热解暑", "收湿敛疮"], "indications": ["热淋", "暑热烦渴", "湿疹"], "usage": "煎服，10-20g，包煎", "contraindications": [], "category": "利水渗湿药", "subcategory": "利尿通淋药"},
    {"name": "萆薢", "pinyin": "Bi Xie", "latin_name": "Dioscoreae Hypoglaucae Rhizoma", "nature": "平", "flavor": ["苦"], "meridian": ["肾经", "胃经"], "effects": ["利湿去浊", "祛风除痹"], "indications": ["膏淋", "白浊", "风湿痹痛"], "usage": "煎服，9-15g", "contraindications": [], "category": "利水渗湿药", "subcategory": "利尿通淋药"},
    {"name": "地肤子", "pinyin": "Di Fu Zi", "latin_name": "Kochiae Fructus", "nature": "寒", "flavor": ["辛", "苦"], "meridian": ["肾经", "膀胱经"], "effects": ["利尿通淋", "清热利湿", "止痒"], "indications": ["热淋涩痛", "湿疹瘙痒"], "usage": "煎服，9-15g", "contraindications": [], "category": "利水渗湿药", "subcategory": "利尿通淋药"},
    
    # ====== 理气药补充 ======
    {"name": "枳壳", "pinyin": "Zhi Ke", "latin_name": "Aurantii Fructus", "nature": "微寒", "flavor": ["苦", "辛", "酸"], "meridian": ["脾经", "胃经"], "effects": ["理气宽中", "行滞消胀"], "indications": ["胸胁气滞", "食积不化"], "usage": "煎服，3-9g", "contraindications": ["孕妇慎用"], "category": "理气药", "subcategory": ""},
    {"name": "香橼", "pinyin": "Xiang Yuan", "latin_name": "Citri Fructus", "nature": "温", "flavor": ["辛", "苦", "酸"], "meridian": ["肝经", "脾经", "肺经"], "effects": ["疏肝理气", "宽中化痰"], "indications": ["肝胃气滞", "痰多咳嗽"], "usage": "煎服，3-10g", "contraindications": [], "category": "理气药", "subcategory": ""},
    {"name": "大腹皮", "pinyin": "Da Fu Pi", "latin_name": "Arecae Pericarpium", "nature": "微温", "flavor": ["辛"], "meridian": ["脾经", "胃经", "大肠经", "小肠经"], "effects": ["行气宽中", "利水消肿"], "indications": ["脘腹胀满", "水肿"], "usage": "煎服，5-10g", "contraindications": [], "category": "理气药", "subcategory": ""},
    {"name": "柿蒂", "pinyin": "Shi Di", "latin_name": "Kaki Calyx", "nature": "平", "flavor": ["苦", "涩"], "meridian": ["胃经"], "effects": ["降气止呃"], "indications": ["呃逆"], "usage": "煎服，5-10g", "contraindications": [], "category": "理气药", "subcategory": ""},
    {"name": "梅花", "pinyin": "Mei Hua", "latin_name": "Mume Flos", "nature": "平", "flavor": ["微酸"], "meridian": ["肝经", "胃经", "肺经"], "effects": ["疏肝和中", "化痰散结"], "indications": ["肝胃气滞", "梅核气"], "usage": "煎服，3-6g", "contraindications": [], "category": "理气药", "subcategory": ""},
    
    # ====== 消食药补充 ======
    {"name": "莱菔子", "pinyin": "Lai Fu Zi", "latin_name": "Raphani Semen", "nature": "平", "flavor": ["辛", "甘"], "meridian": ["肺经", "脾经", "胃经"], "effects": ["消食除胀", "降气化痰"], "indications": ["食积气滞", "咳嗽痰多"], "usage": "煎服，5-12g", "contraindications": [], "category": "消食药", "subcategory": ""},
    {"name": "鸡矢藤", "pinyin": "Ji Shi Teng", "latin_name": "Paederiae Herba", "nature": "平", "flavor": ["甘", "苦"], "meridian": ["脾经", "胃经", "肝经", "肺经"], "effects": ["消食健胃", "化痰止咳", "清热解毒"], "indications": ["饮食积滞", "小儿疳积"], "usage": "煎服，15-30g", "contraindications": [], "category": "消食药", "subcategory": ""},
    
    # ====== 驱虫药 ======
    {"name": "使君子", "pinyin": "Shi Jun Zi", "latin_name": "Quisqualis Fructus", "nature": "温", "flavor": ["甘"], "meridian": ["脾经", "胃经"], "effects": ["杀虫消积"], "indications": ["蛔虫病", "小儿疳积"], "usage": "煎服，9-12g", "contraindications": [], "category": "驱虫药", "subcategory": ""},
    {"name": "苦楝皮", "pinyin": "Ku Lian Pi", "latin_name": "Meliae Cortex", "nature": "寒", "flavor": ["苦"], "meridian": ["肝经", "脾经", "胃经"], "effects": ["杀虫疗癣"], "indications": ["蛔虫病", "钩虫病", "疥癣"], "usage": "煎服，4.5-9g", "contraindications": ["孕妇慎用"], "category": "驱虫药", "subcategory": ""},
    {"name": "槟榔", "pinyin": "Bing Lang", "latin_name": "Arecae Semen", "nature": "温", "flavor": ["苦", "辛"], "meridian": ["胃经", "大肠经"], "effects": ["杀虫消积", "行气利水", "截疟"], "indications": ["绦虫病", "食积气滞", "水肿"], "usage": "煎服，3-10g", "contraindications": [], "category": "驱虫药", "subcategory": ""},
    {"name": "南瓜子", "pinyin": "Nan Gua Zi", "latin_name": "Cucurbitae Semen", "nature": "平", "flavor": ["甘"], "meridian": ["胃经", "大肠经"], "effects": ["杀虫"], "indications": ["绦虫病"], "usage": "研粉，60-120g", "contraindications": [], "category": "驱虫药", "subcategory": ""},
    {"name": "鹤草芽", "pinyin": "He Cao Ya", "latin_name": "Agrimoniae Gemma", "nature": "凉", "flavor": ["苦", "涩"], "meridian": ["肝经", "小肠经", "大肠经"], "effects": ["杀虫"], "indications": ["绦虫病"], "usage": "研粉，30-50g", "contraindications": [], "category": "驱虫药", "subcategory": ""},
    {"name": "雷丸", "pinyin": "Lei Wan", "latin_name": "Omphalia", "nature": "寒", "flavor": ["微苦"], "meridian": ["胃经", "大肠经"], "effects": ["杀虫消积"], "indications": ["绦虫病", "钩虫病", "蛔虫病"], "usage": "研粉，15-21g", "contraindications": [], "category": "驱虫药", "subcategory": ""},
    {"name": "鹤虱", "pinyin": "He Shi", "latin_name": "Carpesii Fructus", "nature": "平", "flavor": ["苦", "辛"], "meridian": ["脾经", "胃经"], "effects": ["杀虫消积"], "indications": ["蛔虫病", "蛲虫病"], "usage": "煎服，3-10g", "contraindications": [], "category": "驱虫药", "subcategory": ""},
    
    # ====== 涌吐药 ======
    {"name": "常山", "pinyin": "Chang Shan", "latin_name": "Dichroae Radix", "nature": "寒", "flavor": ["苦", "辛"], "meridian": ["肺经", "心经", "肝经"], "effects": ["涌吐痰饮", "截疟"], "indications": ["痰饮停积", "疟疾"], "usage": "煎服，4.5-9g", "contraindications": ["孕妇禁用"], "category": "涌吐药", "subcategory": ""},
    {"name": "瓜蒂", "pinyin": "Gua Di", "latin_name": "Pedixellu Melo", "nature": "寒", "flavor": ["苦"], "meridian": ["胃经"], "effects": ["涌吐痰食", "祛湿退黄"], "indications": ["痰涎壅盛", "宿食停滞"], "usage": "煎服，2.5-5g", "contraindications": ["孕妇禁用"], "category": "涌吐药", "subcategory": ""},
    {"name": "藜芦", "pinyin": "Li Lu", "latin_name": "Veratri Nigri Rhizoma", "nature": "寒", "flavor": ["辛", "苦"], "meridian": ["肺经", "胃经", "肝经"], "effects": ["涌吐风痰", "杀虫"], "indications": ["中风痰壅", "癫痫"], "usage": "0.3-0.9g，入丸散", "contraindications": ["孕妇禁用"], "category": "涌吐药", "subcategory": ""},
    
    # ====== 解毒杀虫燥湿止痒药 ======
    {"name": "雄黄", "pinyin": "Xiong Huang", "latin_name": "Realgar", "nature": "温", "flavor": ["辛"], "meridian": ["肝经", "大肠经"], "effects": ["解毒杀虫", "燥湿祛痰", "截疟"], "indications": ["痈肿疮毒", "虫蛇咬伤", "疟疾"], "usage": "0.05-0.1g，入丸散", "contraindications": ["孕妇禁用"], "category": "解毒杀虫燥湿止痒药", "subcategory": ""},
    {"name": "硫黄", "pinyin": "Liu Huang", "latin_name": "Sulfur", "nature": "温", "flavor": ["酸"], "meridian": ["肾经", "大肠经"], "effects": ["外用解毒杀虫", "内服补火助阳"], "indications": ["疥癣", "湿疹", "阳痿"], "usage": "内服1.5-3g", "contraindications": ["孕妇禁用"], "category": "解毒杀虫燥湿止痒药", "subcategory": ""},
    {"name": "白矾", "pinyin": "Bai Fan", "latin_name": "Alumen", "nature": "寒", "flavor": ["酸", "涩"], "meridian": ["肺经", "脾经", "肝经", "大肠经"], "effects": ["外用解毒杀虫", "内服止血止泻"], "indications": ["湿疹瘙痒", "久泻不止", "便血"], "usage": "内服0.6-1.5g", "contraindications": [], "category": "解毒杀虫燥湿止痒药", "subcategory": ""},
    {"name": "蛇床子", "pinyin": "She Chuang Zi", "latin_name": "Cnidii Fructus", "nature": "温", "flavor": ["辛", "苦"], "meridian": ["肾经"], "effects": ["燥湿杀虫", "祛风止痒", "温肾壮阳"], "indications": ["湿疹瘙痒", "阳痿宫冷"], "usage": "煎服，3-10g", "contraindications": [], "category": "解毒杀虫燥湿止痒药", "subcategory": ""},
    {"name": "蜂房", "pinyin": "Feng Fang", "latin_name": "Vespae Nidus", "nature": "平", "flavor": ["甘"], "meridian": ["胃经"], "effects": ["攻毒杀虫", "祛风止痛"], "indications": ["疮疡肿毒", "风湿痹痛"], "usage": "煎服，3-5g", "contraindications": [], "category": "解毒杀虫燥湿止痒药", "subcategory": ""},
    {"name": "土荆皮", "pinyin": "Tu Jing Pi", "latin_name": "Pseudolaricis Cortex", "nature": "温", "flavor": ["辛"], "meridian": ["肺经", "脾经"], "effects": ["杀虫止痒"], "indications": ["疥癣瘙痒"], "usage": "外用适量", "contraindications": [], "category": "解毒杀虫燥湿止痒药", "subcategory": ""},
    {"name": "大蒜", "pinyin": "Da Suan", "latin_name": "Allii Sativi Bulbus", "nature": "温", "flavor": ["辛"], "meridian": ["脾经", "胃经", "肺经"], "effects": ["解毒杀虫", "消肿止痢"], "indications": ["痈肿疮毒", "泄泻痢疾"], "usage": "煎服，9-15g", "contraindications": [], "category": "解毒杀虫燥湿止痒药", "subcategory": ""},
    
    # ====== 拔毒化腐生肌药 ======
    {"name": "升药", "pinyin": "Sheng Yao", "latin_name": "Hydrargyrum Oxydatum Crudum", "nature": "热", "flavor": ["辛"], "meridian": ["肺经", "脾经"], "effects": ["拔毒去腐"], "indications": ["痈疽溃后", "腐肉不脱"], "usage": "外用适量", "contraindications": ["孕妇禁用"], "category": "拔毒化腐生肌药", "subcategory": ""},
    {"name": "轻粉", "pinyin": "Qing Fen", "latin_name": "Calomelas", "nature": "寒", "flavor": ["辛"], "meridian": ["肝经", "肾经"], "effects": ["外用杀虫攻毒", "内服逐水通便"], "indications": ["疥癣", "疮疡", "水肿"], "usage": "内服0.1-0.2g", "contraindications": ["孕妇禁用"], "category": "拔毒化腐生肌药", "subcategory": ""},
    {"name": "砒石", "pinyin": "Pi Shi", "latin_name": "Arsenicum", "nature": "热", "flavor": ["辛"], "meridian": ["肺经", "肝经"], "effects": ["外用蚀疮去腐", "内服劫痰截疟"], "indications": ["瘰疬", "疟疾"], "usage": "内服0.002-0.004g", "contraindications": ["孕妇禁用"], "category": "拔毒化腐生肌药", "subcategory": ""},
    {"name": "硼砂", "pinyin": "Peng Sha", "latin_name": "Borax", "nature": "凉", "flavor": ["甘", "咸"], "meridian": ["肺经", "胃经"], "effects": ["外用清热解毒", "内服清肺化痰"], "indications": ["咽喉肿痛", "口舌生疮", "痰热咳嗽"], "usage": "内服1.5-3g", "contraindications": [], "category": "拔毒化腐生肌药", "subcategory": ""},
    {"name": "炉甘石", "pinyin": "Lu Gan Shi", "latin_name": "Calamina", "nature": "平", "flavor": ["甘"], "meridian": ["肝经", "脾经"], "effects": ["解毒明目退翳", "收湿止痒敛疮"], "indications": ["目赤肿痛", "湿疹瘙痒"], "usage": "外用适量", "contraindications": [], "category": "拔毒化腐生肌药", "subcategory": ""},
    
    # ====== 止血药补充 ======
    {"name": "苎麻根", "pinyin": "Zhu Ma Gen", "latin_name": "Boehmeriae Radix", "nature": "寒", "flavor": ["甘"], "meridian": ["心经", "肝经"], "effects": ["凉血止血", "安胎", "清热解毒"], "indications": ["血热出血", "胎动不安"], "usage": "煎服，10-30g", "contraindications": [], "category": "止血药", "subcategory": "凉血止血药"},
    {"name": "花蕊石", "pinyin": "Hua Rui Shi", "latin_name": "Ophicalcitum", "nature": "平", "flavor": ["酸", "涩"], "meridian": ["肝经"], "effects": ["化瘀止血"], "indications": ["出血证", "瘀滞疼痛"], "usage": "煎服，10-15g", "contraindications": [], "category": "止血药", "subcategory": "化瘀止血药"},
    {"name": "灶心土", "pinyin": "Zao Xin Tu", "latin_name": "Terra Flava Usta", "nature": "温", "flavor": ["辛"], "meridian": ["脾经", "胃经"], "effects": ["温中止血", "止呕止泻"], "indications": ["虚寒出血", "呕吐泄泻"], "usage": "煎服，15-30g", "contraindications": [], "category": "止血药", "subcategory": "温经止血药"},
    
    # ====== 活血化瘀药补充 ======
    {"name": "降香", "pinyin": "Jiang Xiang", "latin_name": "Dalbergiae Odoriferae Lignum", "nature": "温", "flavor": ["辛"], "meridian": ["肝经", "脾经"], "effects": ["化瘀止血", "理气止痛"], "indications": ["出血证", "瘀血痛证"], "usage": "煎服，3-6g", "contraindications": [], "category": "活血化瘀药", "subcategory": "活血止痛药"},
    {"name": "穿山甲", "pinyin": "Chuan Shan Jia", "latin_name": "Manitis Squama", "nature": "微寒", "flavor": ["咸"], "meridian": ["肝经", "胃经"], "effects": ["活血消癥", "通经下乳", "消肿排脓"], "indications": ["癥瘕", "乳汁不下"], "usage": "煎服，3-10g", "contraindications": ["孕妇慎用"], "category": "活血化瘀药", "subcategory": "破血消癥药"},
    
    # ====== 清热药补充 ======
    {"name": "白头翁", "pinyin": "Bai Tou Weng", "latin_name": "Pulsatillae Radix", "nature": "寒", "flavor": ["苦"], "meridian": ["胃经", "大肠经"], "effects": ["清热解毒", "凉血止痢"], "indications": ["热毒血痢", "疮痈"], "usage": "煎服，9-15g", "contraindications": [], "category": "清热药", "subcategory": "清热解毒药"},
    {"name": "白花蛇舌草", "pinyin": "Bai Hua She She Cao", "latin_name": "Hedyotidis Herba", "nature": "寒", "flavor": ["微苦", "甘"], "meridian": ["胃经", "大肠经", "小肠经"], "effects": ["清热解毒", "利湿通淋"], "indications": ["痈肿疮毒", "热淋"], "usage": "煎服，15-60g", "contraindications": [], "category": "清热药", "subcategory": "清热解毒药"},
    {"name": "水牛角", "pinyin": "Shui Niu Jiao", "latin_name": "Bubali Cornu", "nature": "寒", "flavor": ["苦"], "meridian": ["心经", "肝经"], "effects": ["清热凉血", "解毒定惊"], "indications": ["热入营血", "血热出血"], "usage": "煎服，15-30g", "contraindications": [], "category": "清热药", "subcategory": "清热凉血药"},
    
    # ====== 祛风湿药补充 ======
    {"name": "徐长卿", "pinyin": "Xu Zhang Qing", "latin_name": "Cynanchi Paniculati Radix", "nature": "温", "flavor": ["辛"], "meridian": ["肝经", "胃经"], "effects": ["祛风除湿", "止痛止痒"], "indications": ["风湿痹痛", "胃痛", "湿疹"], "usage": "煎服，3-12g", "contraindications": [], "category": "祛风湿药", "subcategory": "祛风湿散寒药"},
    {"name": "五加皮", "pinyin": "Wu Jia Pi", "latin_name": "Acanthopanacis Cortex", "nature": "温", "flavor": ["辛", "苦"], "meridian": ["肝经", "肾经"], "effects": ["祛风湿", "补肝肾", "强筋骨", "利水"], "indications": ["风湿痹痛", "腰膝酸软", "水肿"], "usage": "煎服，4.5-9g", "contraindications": [], "category": "祛风湿药", "subcategory": "祛风湿强筋骨药"},
    
    # ====== 解表药补充 ======
    {"name": "香薷", "pinyin": "Xiang Ru", "latin_name": "Moslae Herba", "nature": "微温", "flavor": ["辛"], "meridian": ["肺经", "胃经"], "effects": ["发汗解表", "化湿和中", "利水消肿"], "indications": ["暑湿感冒", "水肿"], "usage": "煎服，3-10g", "contraindications": [], "category": "解表药", "subcategory": "辛温解表药"},
    {"name": "木贼", "pinyin": "Mu Zei", "latin_name": "Equiseti Hiemalis Herba", "nature": "平", "flavor": ["甘", "苦"], "meridian": ["肺经", "肝经"], "effects": ["疏散风热", "明目退翳"], "indications": ["风热目赤", "翳障"], "usage": "煎服，3-10g", "contraindications": [], "category": "解表药", "subcategory": "辛凉解表药"},
    {"name": "羌活", "pinyin": "Qiang Huo", "latin_name": "Notopterygii Rhizoma et Radix", "nature": "温", "flavor": ["辛", "苦"], "meridian": ["膀胱经", "肾经"], "effects": ["解表散寒", "祛风除湿", "止痛"], "indications": ["风寒感冒", "风湿痹痛"], "usage": "煎服，3-10g", "contraindications": [], "category": "解表药", "subcategory": "辛温解表药"},
    {"name": "葱白", "pinyin": "Cong Bai", "latin_name": "Allii Fistulosi Bulbus", "nature": "温", "flavor": ["辛"], "meridian": ["肺经", "胃经"], "effects": ["发汗解表", "散寒通阳"], "indications": ["风寒感冒", "阴盛格阳"], "usage": "煎服，3-10g", "contraindications": [], "category": "解表药", "subcategory": "辛温解表药"},

    # ====== 清热药补充 ======
    {"name": "夏枯草", "pinyin": "Xia Ku Cao", "latin_name": "Prunellae Spica", "nature": "寒", "flavor": ["辛", "苦"], "meridian": ["肝经", "胆经"], "effects": ["清肝明目", "散结消肿"], "indications": ["目赤肿痛", "瘰疬瘿瘤"], "usage": "煎服，9-15g", "contraindications": [], "category": "清热药", "subcategory": "清热泻火药"},
    {"name": "决明子", "pinyin": "Jue Ming Zi", "latin_name": "Cassiae Semen", "nature": "微寒", "flavor": ["甘", "苦", "咸"], "meridian": ["肝经", "肾经", "大肠经"], "effects": ["清热明目", "润肠通便"], "indications": ["目赤涩痛", "头痛眩晕", "肠燥便秘"], "usage": "煎服，9-15g", "contraindications": [], "category": "清热药", "subcategory": "清热泻火药"},
    {"name": "芦根", "pinyin": "Lu Gen", "latin_name": "Phragmitis Rhizoma", "nature": "寒", "flavor": ["甘"], "meridian": ["肺经", "胃经"], "effects": ["清热生津", "除烦止呕", "利尿"], "indications": ["热病烦渴", "肺热咳嗽", "肺痈吐脓"], "usage": "煎服，15-30g", "contraindications": [], "category": "清热药", "subcategory": "清热泻火药"},
    {"name": "天花粉", "pinyin": "Tian Hua Fen", "latin_name": "Trichosanthis Radix", "nature": "微寒", "flavor": ["甘", "微苦"], "meridian": ["肺经", "胃经"], "effects": ["清热生津", "消肿排脓"], "indications": ["热病烦渴", "肺热燥咳", "疮疡肿毒"], "usage": "煎服，10-15g", "contraindications": ["孕妇慎用"], "category": "清热药", "subcategory": "清热泻火药"},
    {"name": "淡竹叶", "pinyin": "Dan Zhu Ye", "latin_name": "Lophatheri Herba", "nature": "寒", "flavor": ["甘", "淡"], "meridian": ["心经", "胃经", "小肠经"], "effects": ["清热泻火", "除烦利尿"], "indications": ["热病烦渴", "口舌生疮", "热淋"], "usage": "煎服，6-10g", "contraindications": [], "category": "清热药", "subcategory": "清热泻火药"},
    {"name": "鸭跖草", "pinyin": "Ya Zhi Cao", "latin_name": "Commelinae Herba", "nature": "寒", "flavor": ["甘", "淡"], "meridian": ["肺经", "胃经", "膀胱经"], "effects": ["清热泻火", "解毒利水"], "indications": ["风热感冒", "热淋涩痛", "痈肿疮毒"], "usage": "煎服，15-30g", "contraindications": [], "category": "清热药", "subcategory": "清热泻火药"},
    {"name": "寒水石", "pinyin": "Han Shui Shi", "latin_name": "Calcitum", "nature": "大寒", "flavor": ["辛", "咸"], "meridian": ["心经", "胃经", "肾经"], "effects": ["清热泻火", "利窍消肿"], "indications": ["热病烦渴", "丹毒烫伤"], "usage": "煎服，9-15g，先煎", "contraindications": [], "category": "清热药", "subcategory": "清热泻火药"},
    {"name": "竹叶", "pinyin": "Zhu Ye", "latin_name": "Phyllostachydis Folium", "nature": "寒", "flavor": ["甘", "淡"], "meridian": ["心经", "肺经", "胃经"], "effects": ["清热除烦", "生津利尿"], "indications": ["热病烦渴", "口疮尿赤"], "usage": "煎服，6-15g", "contraindications": [], "category": "清热药", "subcategory": "清热泻火药"},
    {"name": "密蒙花", "pinyin": "Mi Meng Hua", "latin_name": "Buddlejae Flos", "nature": "微寒", "flavor": ["甘"], "meridian": ["肝经"], "effects": ["清热养肝", "明目退翳"], "indications": ["目赤肿痛", "肝虚目暗"], "usage": "煎服，3-10g", "contraindications": [], "category": "清热药", "subcategory": "清热泻火药"},
    {"name": "谷精草", "pinyin": "Gu Jing Cao", "latin_name": "Eriocauli Flos", "nature": "平", "flavor": ["辛", "甘"], "meridian": ["肝经", "胃经"], "effects": ["疏散风热", "明目退翳"], "indications": ["风热目赤", "翳膜遮睛"], "usage": "煎服，5-10g", "contraindications": [], "category": "清热药", "subcategory": "清热泻火药"},
    {"name": "穿心莲", "pinyin": "Chuan Xin Lian", "latin_name": "Andrographitis Herba", "nature": "寒", "flavor": ["苦"], "meridian": ["心经", "肺经", "大肠经", "膀胱经"], "effects": ["清热解毒", "燥湿凉血"], "indications": ["风热感冒", "肺热咳嗽", "咽喉肿痛"], "usage": "煎服，6-9g", "contraindications": [], "category": "清热药", "subcategory": "清热解毒药"},
    {"name": "半边莲", "pinyin": "Ban Bian Lian", "latin_name": "Lobeliae Chinensis Herba", "nature": "寒", "flavor": ["甘", "淡"], "meridian": ["心经", "小肠经", "肺经"], "effects": ["清热解毒", "利水消肿"], "indications": ["痈肿疮毒", "蛇虫咬伤", "水肿"], "usage": "煎服，9-15g", "contraindications": [], "category": "清热药", "subcategory": "清热解毒药"},
    {"name": "山慈菇", "pinyin": "Shan Ci Gu", "latin_name": "Cremastrae Pseudobulbus", "nature": "凉", "flavor": ["甘", "微辛"], "meridian": ["肝经", "脾经"], "effects": ["清热解毒", "消痈散结"], "indications": ["痈肿疮毒", "瘰疬痰核"], "usage": "煎服，3-9g", "contraindications": [], "category": "清热药", "subcategory": "清热解毒药"},
    {"name": "漏芦", "pinyin": "Lou Lu", "latin_name": "Rhapontici Radix", "nature": "寒", "flavor": ["苦"], "meridian": ["胃经"], "effects": ["清热解毒", "消痈下乳", "舒筋通脉"], "indications": ["乳痈肿痛", "乳汁不通"], "usage": "煎服，5-9g", "contraindications": ["孕妇慎用"], "category": "清热药", "subcategory": "清热解毒药"},
    {"name": "白蔹", "pinyin": "Bai Lian", "latin_name": "Ampelopsis Radix", "nature": "微寒", "flavor": ["苦"], "meridian": ["心经", "胃经"], "effects": ["清热解毒", "消痈散结", "敛疮生肌"], "indications": ["痈肿疮毒", "水火烫伤"], "usage": "煎服，5-10g", "contraindications": [], "category": "清热药", "subcategory": "清热解毒药"},
    {"name": "绿豆", "pinyin": "Lv Dou", "latin_name": "Phaseoli Radiati Semen", "nature": "寒", "flavor": ["甘"], "meridian": ["心经", "胃经"], "effects": ["清热解毒", "消暑利水"], "indications": ["暑热烦渴", "疮毒痈肿", "食物中毒"], "usage": "煎服，15-30g", "contraindications": [], "category": "清热药", "subcategory": "清热解毒药"},
    {"name": "地锦草", "pinyin": "Di Jin Cao", "latin_name": "Euphorbiae Humifusae Herba", "nature": "平", "flavor": ["辛"], "meridian": ["肝经", "大肠经"], "effects": ["清热解毒", "凉血止血", "利湿退黄"], "indications": ["热毒泻痢", "便血崩漏", "湿热黄疸"], "usage": "煎服，9-15g", "contraindications": [], "category": "清热药", "subcategory": "清热解毒药"},
    {"name": "千里光", "pinyin": "Qian Li Guang", "latin_name": "Senecionis Scandentis Herba", "nature": "寒", "flavor": ["苦"], "meridian": ["肺经", "肝经"], "effects": ["清热解毒", "明目止痒"], "indications": ["目赤肿痛", "湿热泻痢", "湿疹"], "usage": "煎服，9-15g", "contraindications": [], "category": "清热药", "subcategory": "清热解毒药"},
    {"name": "白鲜皮", "pinyin": "Bai Xian Pi", "latin_name": "Dictamni Cortex", "nature": "寒", "flavor": ["苦"], "meridian": ["脾经", "胃经", "膀胱经"], "effects": ["清热燥湿", "祛风解毒"], "indications": ["湿热疮毒", "湿疹瘙痒", "黄疸"], "usage": "煎服，5-10g", "contraindications": [], "category": "清热药", "subcategory": "清热燥湿药"},

    # ====== 祛风湿药补充 ======
    {"name": "秦艽", "pinyin": "Qin Jiao", "latin_name": "Gentianae Macrophyllae Radix", "nature": "平", "flavor": ["辛", "苦"], "meridian": ["胃经", "肝经", "胆经"], "effects": ["祛风湿", "止痹痛", "退虚热", "清湿热"], "indications": ["风湿痹痛", "骨蒸潮热", "湿热黄疸"], "usage": "煎服，3-10g", "contraindications": [], "category": "祛风湿药", "subcategory": "祛风湿清热药"},
    {"name": "桑寄生", "pinyin": "Sang Ji Sheng", "latin_name": "Taxilli Herba", "nature": "平", "flavor": ["苦", "甘"], "meridian": ["肝经", "肾经"], "effects": ["祛风湿", "补肝肾", "强筋骨", "安胎"], "indications": ["风湿痹痛", "腰膝酸软", "胎动不安"], "usage": "煎服，9-15g", "contraindications": [], "category": "祛风湿药", "subcategory": "祛风湿强筋骨药"},
    {"name": "伸筋草", "pinyin": "Shen Jin Cao", "latin_name": "Lycopodii Herba", "nature": "温", "flavor": ["微苦", "辛"], "meridian": ["肝经"], "effects": ["祛风除湿", "舒筋活络"], "indications": ["风湿痹痛", "关节酸痛", "跌打损伤"], "usage": "煎服，9-15g", "contraindications": [], "category": "祛风湿药", "subcategory": "祛风湿散寒药"},
    {"name": "海风藤", "pinyin": "Hai Feng Teng", "latin_name": "Piperis Kadsurae Caulis", "nature": "微温", "flavor": ["辛", "苦"], "meridian": ["肝经"], "effects": ["祛风湿", "通经络", "止痹痛"], "indications": ["风湿痹痛", "关节不利"], "usage": "煎服，6-12g", "contraindications": [], "category": "祛风湿药", "subcategory": "祛风湿散寒药"},
    {"name": "路路通", "pinyin": "Lu Lu Tong", "latin_name": "Liquidambaris Fructus", "nature": "平", "flavor": ["苦"], "meridian": ["肝经", "肾经"], "effects": ["祛风通络", "利水消肿", "通经下乳"], "indications": ["风湿痹痛", "水肿", "乳汁不通"], "usage": "煎服，5-10g", "contraindications": [], "category": "祛风湿药", "subcategory": "祛风湿散寒药"},
    {"name": "丝瓜络", "pinyin": "Si Gua Luo", "latin_name": "Luffae Fructus Retinervus", "nature": "平", "flavor": ["甘"], "meridian": ["肺经", "胃经", "肝经"], "effects": ["祛风通络", "活血消肿"], "indications": ["风湿痹痛", "胸胁胀痛", "乳汁不通"], "usage": "煎服，5-12g", "contraindications": [], "category": "祛风湿药", "subcategory": "祛风湿清热药"},
    {"name": "老鹳草", "pinyin": "Lao Guan Cao", "latin_name": "Erodii seu Geranii Herba", "nature": "平", "flavor": ["辛", "苦"], "meridian": ["肝经", "肾经", "脾经"], "effects": ["祛风湿", "通经络", "止泻痢"], "indications": ["风湿痹痛", "泄泻痢疾"], "usage": "煎服，9-15g", "contraindications": [], "category": "祛风湿药", "subcategory": "祛风湿清热药"},
    {"name": "鹿衔草", "pinyin": "Lu Xian Cao", "latin_name": "Pyrolae Herba", "nature": "温", "flavor": ["甘", "苦"], "meridian": ["肝经", "肾经"], "effects": ["祛风湿", "强筋骨", "止血止咳"], "indications": ["风湿痹痛", "腰膝酸软", "咯血"], "usage": "煎服，9-15g", "contraindications": [], "category": "祛风湿药", "subcategory": "祛风湿强筋骨药"},

    # ====== 利水渗湿药补充 ======
    {"name": "猪苓", "pinyin": "Zhu Ling", "latin_name": "Polyporus", "nature": "平", "flavor": ["甘", "淡"], "meridian": ["肾经", "膀胱经"], "effects": ["利水渗湿"], "indications": ["小便不利", "水肿泄泻", "淋浊带下"], "usage": "煎服，6-12g", "contraindications": [], "category": "利水渗湿药", "subcategory": "利水消肿药"},
    {"name": "茵陈", "pinyin": "Yin Chen", "latin_name": "Artemisiae Scopariae Herba", "nature": "微寒", "flavor": ["苦", "辛"], "meridian": ["脾经", "胃经", "肝经", "胆经"], "effects": ["清热利湿", "利胆退黄"], "indications": ["黄疸", "湿温", "湿疹瘙痒"], "usage": "煎服，6-15g", "contraindications": [], "category": "利水渗湿药", "subcategory": "利湿退黄药"},
    {"name": "虎杖", "pinyin": "Hu Zhang", "latin_name": "Polygoni Cuspidati Rhizoma et Radix", "nature": "微寒", "flavor": ["微苦"], "meridian": ["肝经", "胆经", "肺经"], "effects": ["利湿退黄", "清热解毒", "散瘀止痛", "化痰止咳"], "indications": ["湿热黄疸", "淋浊带下", "烧烫伤"], "usage": "煎服，9-15g", "contraindications": ["孕妇慎用"], "category": "利水渗湿药", "subcategory": "利湿退黄药"},
    {"name": "玉米须", "pinyin": "Yu Mi Xu", "latin_name": "Maydis Stigma", "nature": "平", "flavor": ["甘"], "meridian": ["膀胱经", "肝经", "胆经"], "effects": ["利尿消肿", "利湿退黄"], "indications": ["水肿", "小便不利", "湿热黄疸"], "usage": "煎服，15-30g", "contraindications": [], "category": "利水渗湿药", "subcategory": "利水消肿药"},
    {"name": "垂盆草", "pinyin": "Chui Pen Cao", "latin_name": "Sedi Herba", "nature": "凉", "flavor": ["甘", "淡"], "meridian": ["肝经", "胆经", "小肠经"], "effects": ["利湿退黄", "清热解毒"], "indications": ["湿热黄疸", "痈肿疮毒", "蛇虫咬伤"], "usage": "煎服，15-30g", "contraindications": [], "category": "利水渗湿药", "subcategory": "利湿退黄药"},
    {"name": "海金沙", "pinyin": "Hai Jin Sha", "latin_name": "Lygodii Spora", "nature": "寒", "flavor": ["甘", "咸"], "meridian": ["膀胱经", "小肠经"], "effects": ["利尿通淋", "止痛"], "indications": ["热淋", "石淋", "血淋"], "usage": "煎服，6-15g，包煎", "contraindications": [], "category": "利水渗湿药", "subcategory": "利尿通淋药"},

    # ====== 温里药补充 ======
    {"name": "高良姜", "pinyin": "Gao Liang Jiang", "latin_name": "Alpiniae Officinarum Rhizoma", "nature": "热", "flavor": ["辛"], "meridian": ["脾经", "胃经"], "effects": ["温胃散寒", "消食止痛"], "indications": ["胃寒腹痛", "呕吐泄泻"], "usage": "煎服，3-6g", "contraindications": [], "category": "温里药", "subcategory": ""},
    {"name": "吴茱萸", "pinyin": "Wu Zhu Yu", "latin_name": "Evodiae Fructus", "nature": "热", "flavor": ["辛", "苦"], "meridian": ["肝经", "脾经", "胃经", "肾经"], "effects": ["散寒止痛", "降逆止呕", "助阳止泻"], "indications": ["厥阴头痛", "寒疝腹痛", "呕吐吞酸"], "usage": "煎服，1.5-4.5g", "contraindications": [], "category": "温里药", "subcategory": ""},
    {"name": "胡椒", "pinyin": "Hu Jiao", "latin_name": "Piperis Fructus", "nature": "热", "flavor": ["辛"], "meridian": ["胃经", "大肠经"], "effects": ["温中散寒", "下气消痰"], "indications": ["胃寒腹痛", "呕吐泄泻", "食欲不振"], "usage": "煎服，2-4g", "contraindications": [], "category": "温里药", "subcategory": ""},

    # ====== 理气药补充 ======
    {"name": "薤白", "pinyin": "Xie Bai", "latin_name": "Allii Macrostemonis Bulbus", "nature": "温", "flavor": ["辛", "苦"], "meridian": ["心经", "肺经", "胃经", "大肠经"], "effects": ["通阳散结", "行气导滞"], "indications": ["胸痹心痛", "脘腹痞满"], "usage": "煎服，5-10g", "contraindications": [], "category": "理气药", "subcategory": ""},
    {"name": "佛手", "pinyin": "Fo Shou", "latin_name": "Citri Sarcodactylis Fructus", "nature": "温", "flavor": ["辛", "苦", "酸"], "meridian": ["肝经", "脾经", "胃经", "肺经"], "effects": ["疏肝理气", "和胃止痛", "化痰"], "indications": ["肝胃气滞", "胸胁胀痛", "食欲不振"], "usage": "煎服，3-10g", "contraindications": [], "category": "理气药", "subcategory": ""},
    {"name": "玫瑰花", "pinyin": "Mei Gui Hua", "latin_name": "Rosae Rugosae Flos", "nature": "温", "flavor": ["甘", "微苦"], "meridian": ["肝经", "脾经"], "effects": ["行气解郁", "活血止痛"], "indications": ["肝胃气痛", "月经不调", "跌打损伤"], "usage": "煎服，3-6g", "contraindications": [], "category": "理气药", "subcategory": ""},
    {"name": "甘松", "pinyin": "Gan Song", "latin_name": "Nardostachyos Radix et Rhizoma", "nature": "温", "flavor": ["辛", "甘"], "meridian": ["脾经", "胃经"], "effects": ["理气止痛", "开郁醒脾"], "indications": ["脘腹胀痛", "食欲不振"], "usage": "煎服，3-6g", "contraindications": [], "category": "理气药", "subcategory": ""},
    {"name": "刀豆", "pinyin": "Dao Dou", "latin_name": "Canavaliae Semen", "nature": "温", "flavor": ["甘"], "meridian": ["胃经", "肾经"], "effects": ["降气止呃", "温肾助阳"], "indications": ["呃逆呕吐", "虚寒腰痛"], "usage": "煎服，6-9g", "contraindications": [], "category": "理气药", "subcategory": ""},

    # ====== 止血药补充 ======
    {"name": "藕节", "pinyin": "Ou Jie", "latin_name": "Nelumbinis Rhizomatis Nodus", "nature": "平", "flavor": ["甘", "涩"], "meridian": ["肝经", "肺经", "胃经"], "effects": ["收敛止血", "化瘀"], "indications": ["咯血", "衄血", "便血", "崩漏"], "usage": "煎服，9-15g", "contraindications": [], "category": "止血药", "subcategory": "收敛止血药"},
    {"name": "紫珠", "pinyin": "Zi Zhu", "latin_name": "Callicarpae Formosanae Folium", "nature": "凉", "flavor": ["苦", "涩"], "meridian": ["肝经", "肺经", "胃经"], "effects": ["凉血收敛止血", "清热解毒"], "indications": ["多种出血证", "痈肿疮毒"], "usage": "煎服，10-15g", "contraindications": [], "category": "止血药", "subcategory": "凉血止血药"},

    # ====== 活血化瘀药补充 ======
    {"name": "五灵脂", "pinyin": "Wu Ling Zhi", "latin_name": "Trogopterori Faeces", "nature": "温", "flavor": ["苦", "甘"], "meridian": ["肝经", "脾经"], "effects": ["活血止痛", "化瘀止血"], "indications": ["瘀血阻滞痛证", "出血证"], "usage": "煎服，3-10g，包煎", "contraindications": ["孕妇慎用"], "category": "活血化瘀药", "subcategory": "活血止痛药"},

    # ====== 化痰止咳平喘药补充 ======
    {"name": "白前", "pinyin": "Bai Qian", "latin_name": "Cynanchi Stauntonii Rhizoma et Radix", "nature": "微温", "flavor": ["辛", "苦"], "meridian": ["肺经"], "effects": ["降气化痰", "止咳"], "indications": ["咳嗽痰多", "气喘"], "usage": "煎服，3-10g", "contraindications": [], "category": "化痰止咳平喘药", "subcategory": "温化寒痰药"},
    {"name": "罗汉果", "pinyin": "Luo Han Guo", "latin_name": "Siraitiae Fructus", "nature": "凉", "flavor": ["甘"], "meridian": ["肺经", "大肠经"], "effects": ["清热润肺", "利咽开音", "润肠通便"], "indications": ["肺热燥咳", "咽痛失音", "肠燥便秘"], "usage": "煎服，9-15g", "contraindications": [], "category": "化痰止咳平喘药", "subcategory": "止咳平喘药"},
    {"name": "礞石", "pinyin": "Meng Shi", "latin_name": "Lapis Chloriti", "nature": "平", "flavor": ["甘", "咸"], "meridian": ["肺经", "肝经"], "effects": ["坠痰下气", "平肝镇惊"], "indications": ["顽痰胶结", "咳逆喘急", "惊痫癫狂"], "usage": "煎服，10-15g，布包先煎", "contraindications": [], "category": "化痰止咳平喘药", "subcategory": "清化热痰药"},

    # ====== 安神药补充 ======
    {"name": "琥珀", "pinyin": "Hu Po", "latin_name": "Succinum", "nature": "平", "flavor": ["甘"], "meridian": ["心经", "肝经", "膀胱经"], "effects": ["镇惊安神", "活血散瘀", "利尿通淋"], "indications": ["心悸失眠", "惊风癫痫", "血滞经闭"], "usage": "研末冲服，1.5-3g", "contraindications": [], "category": "安神药", "subcategory": "重镇安神药"},
    {"name": "远志", "pinyin": "Yuan Zhi", "latin_name": "Polygalae Radix", "nature": "温", "flavor": ["苦", "辛"], "meridian": ["心经", "肾经", "肺经"], "effects": ["安神益智", "交通心肾", "祛痰消肿"], "indications": ["心神不宁", "惊悸失眠", "健忘"], "usage": "煎服，3-10g", "contraindications": [], "category": "安神药", "subcategory": "养心安神药"},

    # ====== 平肝熄风药补充 ======
    {"name": "珍珠", "pinyin": "Zhen Zhu", "latin_name": "Margarita", "nature": "寒", "flavor": ["甘", "咸"], "meridian": ["心经", "肝经"], "effects": ["安神定惊", "明目消翳", "解毒生肌"], "indications": ["惊悸失眠", "目赤翳障", "疮疡不敛"], "usage": "研末，0.1-0.3g", "contraindications": [], "category": "平肝熄风药", "subcategory": ""},
    {"name": "牡蛎", "pinyin": "Mu Li", "latin_name": "Ostreae Concha", "nature": "微寒", "flavor": ["咸", "涩"], "meridian": ["肝经", "肾经"], "effects": ["平肝潜阳", "软坚散结", "收敛固涩"], "indications": ["眩晕耳鸣", "瘰疬瘿瘤", "自汗盗汗"], "usage": "煎服，9-30g，先煎", "contraindications": [], "category": "平肝熄风药", "subcategory": ""},
    {"name": "代赭石", "pinyin": "Dai Zhe Shi", "latin_name": "Haematitum", "nature": "寒", "flavor": ["苦"], "meridian": ["肝经", "心经"], "effects": ["平肝潜阳", "重镇降逆", "凉血止血"], "indications": ["眩晕耳鸣", "呕吐呃逆", "血热出血"], "usage": "煎服，9-30g，先煎", "contraindications": ["孕妇慎用"], "category": "平肝熄风药", "subcategory": ""},

    # ====== 开窍药补充 ======
    {"name": "石菖蒲", "pinyin": "Shi Chang Pu", "latin_name": "Acori Tatarinowii Rhizoma", "nature": "温", "flavor": ["辛", "苦"], "meridian": ["心经", "胃经"], "effects": ["开窍醒神", "化湿和胃", "宁神益智"], "indications": ["痰蒙清窍", "神昏癫痫", "健忘失眠"], "usage": "煎服，3-10g", "contraindications": [], "category": "开窍药", "subcategory": ""},
    {"name": "安息香", "pinyin": "An Xi Xiang", "latin_name": "Benzoinum", "nature": "平", "flavor": ["辛", "苦"], "meridian": ["心经", "脾经"], "effects": ["开窍醒神", "活血行气", "止痛"], "indications": ["闭证神昏", "心腹疼痛", "产后血晕"], "usage": "0.6-1.5g，入丸散", "contraindications": [], "category": "开窍药", "subcategory": ""},

    # ====== 补虚药补充 ======
    {"name": "大枣", "pinyin": "Da Zao", "latin_name": "Jujubae Fructus", "nature": "温", "flavor": ["甘"], "meridian": ["脾经", "胃经", "心经"], "effects": ["补中益气", "养血安神", "缓和药性"], "indications": ["脾虚食少", "血虚萎黄", "脏躁失眠"], "usage": "煎服，6-15g", "contraindications": [], "category": "补虚药", "subcategory": "补气药"},
    {"name": "刺五加", "pinyin": "Ci Wu Jia", "latin_name": "Acanthopanacis Senticosi Radix et Rhizoma", "nature": "温", "flavor": ["辛", "微苦"], "meridian": ["脾经", "肺经", "心经", "肾经"], "effects": ["益气健脾", "补肾安神"], "indications": ["脾肺气虚", "肾虚腰膝酸软", "失眠多梦"], "usage": "煎服，9-27g", "contraindications": [], "category": "补虚药", "subcategory": "补气药"},
    {"name": "红景天", "pinyin": "Hong Jing Tian", "latin_name": "Rhodiolae Crenulatae Radix et Rhizoma", "nature": "平", "flavor": ["甘", "苦"], "meridian": ["肺经", "心经"], "effects": ["益气活血", "通脉平喘"], "indications": ["气虚血瘀", "胸痹心痛", "中风偏瘫"], "usage": "煎服，3-6g", "contraindications": [], "category": "补虚药", "subcategory": "补气药"},
    {"name": "沙棘", "pinyin": "Sha Ji", "latin_name": "Hippophae Fructus", "nature": "温", "flavor": ["酸", "涩"], "meridian": ["脾经", "胃经", "肺经", "心经"], "effects": ["健脾消食", "止咳祛痰", "活血散瘀"], "indications": ["脾虚食少", "咳嗽痰多", "瘀血经闭"], "usage": "煎服，3-10g", "contraindications": [], "category": "补虚药", "subcategory": "补气药"},
    {"name": "桑椹", "pinyin": "Sang Shen", "latin_name": "Mori Fructus", "nature": "寒", "flavor": ["甘", "酸"], "meridian": ["肝经", "肾经"], "effects": ["滋阴补血", "生津润燥"], "indications": ["肝肾阴虚", "眩晕耳鸣", "须发早白", "肠燥便秘"], "usage": "煎服，9-15g", "contraindications": [], "category": "补虚药", "subcategory": "补血药"},
    {"name": "黑芝麻", "pinyin": "Hei Zhi Ma", "latin_name": "Sesami Semen Nigrum", "nature": "平", "flavor": ["甘"], "meridian": ["肝经", "肾经", "大肠经"], "effects": ["补肝肾", "益精血", "润肠燥"], "indications": ["精血亏虚", "须发早白", "肠燥便秘"], "usage": "煎服，9-15g", "contraindications": [], "category": "补虚药", "subcategory": "补血药"},
    {"name": "核桃仁", "pinyin": "He Tao Ren", "latin_name": "Juglandis Semen", "nature": "温", "flavor": ["甘"], "meridian": ["肾经", "肺经", "大肠经"], "effects": ["补肾温肺", "润肠通便"], "indications": ["肾阳虚衰", "虚寒喘咳", "肠燥便秘"], "usage": "煎服，6-9g", "contraindications": [], "category": "补虚药", "subcategory": "补阳药"},
    {"name": "仙茅", "pinyin": "Xian Mao", "latin_name": "Curculiginis Rhizoma", "nature": "热", "flavor": ["辛"], "meridian": ["肾经", "肝经", "脾经"], "effects": ["补肾壮阳", "强筋健骨", "祛寒除湿"], "indications": ["阳痿精寒", "腰膝冷痛", "风湿痹痛"], "usage": "煎服，3-10g", "contraindications": [], "category": "补虚药", "subcategory": "补阳药"},
    {"name": "韭菜子", "pinyin": "Jiu Cai Zi", "latin_name": "Allii Tuberosi Semen", "nature": "温", "flavor": ["辛", "甘"], "meridian": ["肝经", "肾经"], "effects": ["温补肝肾", "壮阳固精"], "indications": ["阳痿遗精", "腰膝酸软", "白带过多"], "usage": "煎服，3-9g", "contraindications": [], "category": "补虚药", "subcategory": "补阳药"},
    {"name": "胡芦巴", "pinyin": "Hu Lu Ba", "latin_name": "Trigonellae Semen", "nature": "温", "flavor": ["苦"], "meridian": ["肾经"], "effects": ["温肾助阳", "祛寒止痛"], "indications": ["阳痿滑精", "寒疝腹痛", "足膝冷痛"], "usage": "煎服，5-10g", "contraindications": [], "category": "补虚药", "subcategory": "补阳药"},
    {"name": "海马", "pinyin": "Hai Ma", "latin_name": "Hippocampus", "nature": "温", "flavor": ["甘", "咸"], "meridian": ["肝经", "肾经"], "effects": ["补肾壮阳", "活血散结", "消肿止痛"], "indications": ["阳痿遗精", "癥瘕积聚", "跌打损伤"], "usage": "研末，1-1.5g", "contraindications": ["孕妇禁用"], "category": "补虚药", "subcategory": "补阳药"},
    {"name": "楮实子", "pinyin": "Chu Shi Zi", "latin_name": "Broussonetiae Fructus", "nature": "寒", "flavor": ["甘"], "meridian": ["肝经", "肾经"], "effects": ["补肾清肝", "明目利尿"], "indications": ["腰膝酸软", "目昏耳鸣", "水肿"], "usage": "煎服，6-12g", "contraindications": [], "category": "补虚药", "subcategory": "补阴药"},

    # ====== 收涩药补充 ======
    {"name": "麻黄根", "pinyin": "Ma Huang Gen", "latin_name": "Ephedrae Radix et Rhizoma", "nature": "平", "flavor": ["甘", "涩"], "meridian": ["肺经"], "effects": ["固表止汗"], "indications": ["自汗盗汗"], "usage": "煎服，3-9g", "contraindications": [], "category": "收涩药", "subcategory": ""},
    {"name": "浮小麦", "pinyin": "Fu Xiao Mai", "latin_name": "Tritici Levis Fructus", "nature": "凉", "flavor": ["甘"], "meridian": ["心经"], "effects": ["固表止汗", "益气除热"], "indications": ["自汗盗汗", "骨蒸劳热"], "usage": "煎服，15-30g", "contraindications": [], "category": "收涩药", "subcategory": ""},
    {"name": "五倍子", "pinyin": "Wu Bei Zi", "latin_name": "Galla Chinensis", "nature": "寒", "flavor": ["酸", "涩"], "meridian": ["肺经", "肾经", "大肠经"], "effects": ["敛肺降火", "涩肠止泻", "固精止遗", "敛汗止血"], "indications": ["久咳痰多", "久泻久痢", "遗精盗汗"], "usage": "煎服，3-6g", "contraindications": [], "category": "收涩药", "subcategory": ""},
    {"name": "石榴皮", "pinyin": "Shi Liu Pi", "latin_name": "Granati Pericarpium", "nature": "温", "flavor": ["酸", "涩"], "meridian": ["大肠经"], "effects": ["涩肠止泻", "杀虫收敛"], "indications": ["久泻久痢", "便血脱肛", "虫积腹痛"], "usage": "煎服，3-10g", "contraindications": [], "category": "收涩药", "subcategory": ""},
    {"name": "禹余粮", "pinyin": "Yu Yu Liang", "latin_name": "Limonitum", "nature": "微寒", "flavor": ["甘", "涩"], "meridian": ["胃经", "大肠经"], "effects": ["涩肠止泻", "收敛止血", "止带"], "indications": ["久泻久痢", "崩漏带下"], "usage": "煎服，9-15g", "contraindications": [], "category": "收涩药", "subcategory": ""},
    {"name": "糯稻根", "pinyin": "Nuo Dao Gen", "latin_name": "Oryzae Glutinosae Radix", "nature": "平", "flavor": ["甘"], "meridian": ["肺经", "肾经"], "effects": ["固表止汗", "益胃生津"], "indications": ["自汗盗汗", "虚热不退"], "usage": "煎服，15-30g", "contraindications": [], "category": "收涩药", "subcategory": ""},

    # ====== 消食药补充 ======
    {"name": "阿魏", "pinyin": "A Wei", "latin_name": "Ferulae Resina", "nature": "温", "flavor": ["苦", "辛"], "meridian": ["肝经", "脾经", "胃经"], "effects": ["消食化积", "散瘀杀虫"], "indications": ["肉食积滞", "癥瘕痞块", "虫积腹痛"], "usage": "入丸散，1-1.5g", "contraindications": ["孕妇禁用"], "category": "消食药", "subcategory": ""},

    # ====== 泻下药补充 ======
    {"name": "郁李仁", "pinyin": "Yu Li Ren", "latin_name": "Pruni Semen", "nature": "平", "flavor": ["辛", "苦", "甘"], "meridian": ["脾经", "大肠经", "小肠经"], "effects": ["润肠通便", "利水消肿"], "indications": ["肠燥便秘", "水肿胀满"], "usage": "煎服，6-10g", "contraindications": ["孕妇慎用"], "category": "泻下药", "subcategory": "润下药"},

    # ====== 驱虫药补充 ======
    {"name": "榧子", "pinyin": "Fei Zi", "latin_name": "Torreyae Semen", "nature": "平", "flavor": ["甘"], "meridian": ["肺经", "胃经", "大肠经"], "effects": ["杀虫消积", "润肺止咳", "润肠通便"], "indications": ["多种肠道寄生虫", "肺燥咳嗽", "肠燥便秘"], "usage": "煎服，9-15g", "contraindications": [], "category": "驱虫药", "subcategory": ""},

    # ====== 解毒杀虫燥湿止痒药补充 ======
    {"name": "木槿皮", "pinyin": "Mu Jin Pi", "latin_name": "Hibisci Cortex", "nature": "微寒", "flavor": ["甘", "苦"], "meridian": ["大肠经", "小肠经"], "effects": ["清热利湿", "杀虫止痒"], "indications": ["疥癣瘙痒", "湿热泻痢"], "usage": "外用适量", "contraindications": [], "category": "解毒杀虫燥湿止痒药", "subcategory": ""},
    {"name": "樟脑", "pinyin": "Zhang Nao", "latin_name": "Camphora", "nature": "热", "flavor": ["辛"], "meridian": ["心经", "脾经"], "effects": ["除湿杀虫", "温散止痛", "开窍辟秽"], "indications": ["疥癣瘙痒", "跌打损伤", "神昏"], "usage": "外用适量", "contraindications": ["孕妇慎用"], "category": "解毒杀虫燥湿止痒药", "subcategory": ""},
    {"name": "大风子", "pinyin": "Da Feng Zi", "latin_name": "Hydnocarpi Semen", "nature": "热", "flavor": ["辛"], "meridian": ["肝经", "脾经", "肾经"], "effects": ["祛风燥湿", "攻毒杀虫"], "indications": ["麻风", "疥癣"], "usage": "外用适量", "contraindications": [], "category": "解毒杀虫燥湿止痒药", "subcategory": ""},
    {"name": "木鳖子", "pinyin": "Mu Bie Zi", "latin_name": "Momordicae Semen", "nature": "凉", "flavor": ["苦", "微甘"], "meridian": ["肝经", "脾经", "胃经"], "effects": ["攻毒疗疮", "消肿散结"], "indications": ["疮疡肿毒", "瘰疬"], "usage": "内服0.6-1.2g", "contraindications": ["孕妇慎用"], "category": "解毒杀虫燥湿止痒药", "subcategory": ""},

    # ====== 解表药补充2 ======
    {"name": "胡荽", "pinyin": "Hu Sui", "latin_name": "Coriandri Herba", "nature": "温", "flavor": ["辛"], "meridian": ["肺经", "胃经"], "effects": ["发表透疹", "开胃消食"], "indications": ["麻疹不透", "食欲不振"], "usage": "煎服，3-6g", "contraindications": [], "category": "解表药", "subcategory": "辛温解表药"},
    {"name": "柽柳", "pinyin": "Cheng Liu", "latin_name": "Tamaricis Cacumen", "nature": "平", "flavor": ["辛", "甘"], "meridian": ["肺经", "胃经", "心经"], "effects": ["发表透疹", "祛风除湿"], "indications": ["麻疹不透", "风湿痹痛"], "usage": "煎服，3-10g", "contraindications": [], "category": "解表药", "subcategory": "辛温解表药"},

    # ====== 清热药补充2 ======
    {"name": "四季青", "pinyin": "Si Ji Qing", "latin_name": "Ilicis Chinensis Folium", "nature": "寒", "flavor": ["苦", "涩"], "meridian": ["肺经", "心经"], "effects": ["清热解毒", "凉血敛疮"], "indications": ["烧烫伤", "疮疡", "外伤出血"], "usage": "煎服，15-30g", "contraindications": [], "category": "清热药", "subcategory": "清热解毒药"},
    {"name": "锦灯笼", "pinyin": "Jin Deng Long", "latin_name": "Physalis Calyx seu Fructus", "nature": "寒", "flavor": ["苦"], "meridian": ["肺经"], "effects": ["清热解毒", "利咽化痰", "利尿通淋"], "indications": ["咽喉肿痛", "肺热咳嗽", "热淋"], "usage": "煎服，5-9g", "contraindications": [], "category": "清热药", "subcategory": "清热解毒药"},
    {"name": "青果", "pinyin": "Qing Guo", "latin_name": "Canarii Fructus", "nature": "平", "flavor": ["甘", "酸"], "meridian": ["肺经", "胃经"], "effects": ["清热解毒", "利咽生津"], "indications": ["咽喉肿痛", "咳嗽", "烦渴"], "usage": "煎服，5-10g", "contraindications": [], "category": "清热药", "subcategory": "清热解毒药"},
    {"name": "木蝴蝶", "pinyin": "Mu Hu Die", "latin_name": "Oroxyli Semen", "nature": "凉", "flavor": ["苦", "甘"], "meridian": ["肺经", "肝经", "胃经"], "effects": ["清肺利咽", "疏肝和胃"], "indications": ["咽喉肿痛", "肺热咳嗽", "肝胃气痛"], "usage": "煎服，1.5-3g", "contraindications": [], "category": "清热药", "subcategory": "清热解毒药"},

    # ====== 祛风湿药补充2 ======
    {"name": "青风藤", "pinyin": "Qing Feng Teng", "latin_name": "Sinomenii Caulis", "nature": "平", "flavor": ["苦", "辛"], "meridian": ["肝经", "脾经"], "effects": ["祛风湿", "通经络", "利小便"], "indications": ["风湿痹痛", "关节肿痛", "水肿"], "usage": "煎服，6-12g", "contraindications": [], "category": "祛风湿药", "subcategory": "祛风湿清热药"},
    {"name": "穿山龙", "pinyin": "Chuan Shan Long", "latin_name": "Dioscoreae Nipponicae Rhizoma", "nature": "温", "flavor": ["甘", "苦"], "meridian": ["肝经", "肾经", "肺经"], "effects": ["祛风除湿", "活血通络", "化痰止咳"], "indications": ["风湿痹痛", "跌打损伤", "咳嗽气喘"], "usage": "煎服，9-15g", "contraindications": [], "category": "祛风湿药", "subcategory": "祛风湿散寒药"},

    # ====== 化湿药补充 ======
    {"name": "白豆蔻", "pinyin": "Bai Dou Kou", "latin_name": "Amomi Fructus Rotundus", "nature": "温", "flavor": ["辛"], "meridian": ["肺经", "脾经", "胃经"], "effects": ["化湿行气", "温中止呕", "开胃消食"], "indications": ["湿浊中阻", "脘腹胀满", "胃寒呕吐"], "usage": "煎服，3-6g，后下", "contraindications": [], "category": "化湿药", "subcategory": ""},

    # ====== 利水渗湿药补充2 ======
    {"name": "香加皮", "pinyin": "Xiang Jia Pi", "latin_name": "Periplocae Cortex", "nature": "温", "flavor": ["辛", "苦"], "meridian": ["肝经", "肾经", "心经"], "effects": ["利水消肿", "祛风湿", "强筋骨"], "indications": ["水肿", "小便不利", "风湿痹痛"], "usage": "煎服，3-6g", "contraindications": [], "category": "利水渗湿药", "subcategory": "利水消肿药"},
    {"name": "鸡骨草", "pinyin": "Ji Gu Cao", "latin_name": "Abri Herba", "nature": "凉", "flavor": ["甘", "微苦"], "meridian": ["肝经", "胃经"], "effects": ["利湿退黄", "清热解毒", "疏肝止痛"], "indications": ["湿热黄疸", "胁肋胀痛", "乳痈"], "usage": "煎服，15-30g", "contraindications": [], "category": "利水渗湿药", "subcategory": "利湿退黄药"},
    {"name": "枳椇子", "pinyin": "Zhi Ju Zi", "latin_name": "Hoveniae Semen", "nature": "平", "flavor": ["甘", "酸"], "meridian": ["胃经"], "effects": ["利水消肿", "解酒毒"], "indications": ["水肿", "醉酒"], "usage": "煎服，10-15g", "contraindications": [], "category": "利水渗湿药", "subcategory": "利水消肿药"},

    # ====== 活血化瘀药补充2 ======
    {"name": "夏天无", "pinyin": "Xia Tian Wu", "latin_name": "Corydalis Decumbentis Rhizoma", "nature": "温", "flavor": ["苦", "微辛"], "meridian": ["肝经"], "effects": ["活血通络", "行气止痛", "祛风除湿"], "indications": ["中风偏瘫", "跌打损伤", "风湿痹痛"], "usage": "煎服，6-12g", "contraindications": [], "category": "活血化瘀药", "subcategory": "活血止痛药"},

    # ====== 化痰止咳平喘药补充2 ======
    {"name": "金沸草", "pinyin": "Jin Fei Cao", "latin_name": "Inulae Herba", "nature": "温", "flavor": ["苦", "辛", "咸"], "meridian": ["肺经", "大肠经"], "effects": ["降气消痰", "行水"], "indications": ["咳嗽痰多", "胸膈痞满", "水肿"], "usage": "煎服，3-10g", "contraindications": [], "category": "化痰止咳平喘药", "subcategory": "温化寒痰药"},
    {"name": "满山红", "pinyin": "Man Shan Hong", "latin_name": "Rhododendri Daurici Folium", "nature": "寒", "flavor": ["辛", "苦"], "meridian": ["肺经"], "effects": ["止咳祛痰"], "indications": ["咳嗽痰多", "急慢性支气管炎"], "usage": "煎服，3-15g", "contraindications": [], "category": "化痰止咳平喘药", "subcategory": "止咳平喘药"},
    {"name": "矮地茶", "pinyin": "Ai Di Cha", "latin_name": "Ardisiae Japonicae Herba", "nature": "平", "flavor": ["辛", "微苦"], "meridian": ["肺经", "肝经"], "effects": ["化痰止咳", "清热利湿", "活血化瘀"], "indications": ["咳嗽痰多", "湿热黄疸", "跌打损伤"], "usage": "煎服，15-30g", "contraindications": [], "category": "化痰止咳平喘药", "subcategory": "止咳平喘药"},
    {"name": "洋金花", "pinyin": "Yang Jin Hua", "latin_name": "Daturae Flos", "nature": "温", "flavor": ["辛"], "meridian": ["肺经", "肝经"], "effects": ["平喘止咳", "解痉定痛"], "indications": ["哮喘咳嗽", "脘腹冷痛", "风湿痹痛"], "usage": "煎服，0.3-0.6g", "contraindications": ["孕妇禁用"], "category": "化痰止咳平喘药", "subcategory": "止咳平喘药"},

    # ====== 活血化瘀药补充3 ======
    {"name": "枫香脂", "pinyin": "Feng Xiang Zhi", "latin_name": "Liquidambaris Resina", "nature": "平", "flavor": ["辛", "微苦"], "meridian": ["肺经", "脾经"], "effects": ["活血止痛", "解毒生肌", "凉血"], "indications": ["跌打损伤", "痈疽肿痛", "吐血衄血"], "usage": "入丸散，1.5-3g", "contraindications": [], "category": "活血化瘀药", "subcategory": "活血止痛药"},

    # ====== 补虚药补充2 ======
    {"name": "绞股蓝", "pinyin": "Jiao Gu Lan", "latin_name": "Gynostemmatis Herba", "nature": "凉", "flavor": ["甘", "微苦"], "meridian": ["脾经", "肺经"], "effects": ["益气健脾", "化痰止咳", "清热解毒"], "indications": ["脾虚证", "肺虚咳嗽", "肿瘤辅助"], "usage": "煎服，10-20g", "contraindications": [], "category": "补虚药", "subcategory": "补气药"},
    {"name": "银耳", "pinyin": "Yin Er", "latin_name": "Tremellae Fructificatio", "nature": "平", "flavor": ["甘", "淡"], "meridian": ["肺经", "胃经", "肾经"], "effects": ["滋阴润肺", "养胃生津"], "indications": ["虚劳咳嗽", "痰中带血", "津少口渴"], "usage": "煎服，3-10g", "contraindications": [], "category": "补虚药", "subcategory": "补阴药"},
    {"name": "阳起石", "pinyin": "Yang Qi Shi", "latin_name": "Actinolitum", "nature": "温", "flavor": ["咸"], "meridian": ["肾经"], "effects": ["温肾壮阳"], "indications": ["阳痿不举", "宫冷不孕"], "usage": "煎服，3-6g", "contraindications": [], "category": "补虚药", "subcategory": "补阳药"},

    # ====== 收涩药补充2 ======
    {"name": "罂粟壳", "pinyin": "Ying Su Ke", "latin_name": "Papaveris Pericarpium", "nature": "平", "flavor": ["酸", "涩"], "meridian": ["肺经", "大肠经", "肾经"], "effects": ["敛肺涩肠", "止痛"], "indications": ["久咳不止", "久泻久痢", "心腹筋骨痛"], "usage": "煎服，3-6g", "contraindications": [], "category": "收涩药", "subcategory": ""},
    {"name": "刺猬皮", "pinyin": "Ci Wei Pi", "latin_name": "Erinacei Corium", "nature": "平", "flavor": ["苦"], "meridian": ["胃经", "大肠经", "肾经"], "effects": ["固精缩尿", "收敛止血", "化瘀止痛"], "indications": ["遗精遗尿", "便血痔血", "胃脘痛"], "usage": "煎服，3-10g", "contraindications": [], "category": "收涩药", "subcategory": ""},

    # ====== 拔毒化腐生肌药补充 ======
    {"name": "铅丹", "pinyin": "Qian Dan", "latin_name": "Plumbum Rubrum", "nature": "微寒", "flavor": ["辛", "咸"], "meridian": ["心经", "脾经", "肝经"], "effects": ["拔毒生肌", "杀虫止痒"], "indications": ["疮疡溃烂", "湿疮疥癣"], "usage": "外用适量", "contraindications": ["孕妇禁用"], "category": "拔毒化腐生肌药", "subcategory": ""},
    {"name": "密陀僧", "pinyin": "Mi Tuo Seng", "latin_name": "Lithargyrum", "nature": "平", "flavor": ["咸", "辛"], "meridian": ["肝经", "脾经"], "effects": ["拔毒生肌", "燥湿杀虫", "收敛止血"], "indications": ["疮疡久溃", "湿疮疥癣", "外伤出血"], "usage": "外用适量", "contraindications": [], "category": "拔毒化腐生肌药", "subcategory": ""},

    # ====== 解表药补充3 ======
    {"name": "西河柳", "pinyin": "Xi He Liu", "latin_name": "Tamaricis Cacumen", "nature": "平", "flavor": ["甘", "辛"], "meridian": ["肺经", "胃经", "心经"], "effects": ["发表透疹", "祛风除湿"], "indications": ["麻疹不透", "风湿痹痛"], "usage": "煎服，3-6g", "contraindications": [], "category": "解表药", "subcategory": "辛温解表药"},

    # ====== 清热药补充3 ======
    {"name": "委陵菜", "pinyin": "Wei Ling Cai", "latin_name": "Potentillae Chinensis Herba", "nature": "寒", "flavor": ["苦"], "meridian": ["肝经", "大肠经"], "effects": ["清热解毒", "凉血止痢"], "indications": ["热毒泻痢", "血热出血"], "usage": "煎服，9-15g", "contraindications": [], "category": "清热药", "subcategory": "清热解毒药"},
    {"name": "翻白草", "pinyin": "Fan Bai Cao", "latin_name": "Potentillae Discoloris Herba", "nature": "平", "flavor": ["甘", "微苦"], "meridian": ["肝经", "胃经", "大肠经"], "effects": ["清热解毒", "止血止痢"], "indications": ["湿热泻痢", "痈肿疮毒", "血热出血"], "usage": "煎服，9-15g", "contraindications": [], "category": "清热药", "subcategory": "清热解毒药"},
    {"name": "拳参", "pinyin": "Quan Shen", "latin_name": "Bistortae Rhizoma", "nature": "微寒", "flavor": ["苦", "涩"], "meridian": ["肺经", "肝经", "大肠经"], "effects": ["清热解毒", "消肿止血"], "indications": ["痈肿瘰疬", "热病惊痫", "血热出血"], "usage": "煎服，4.5-9g", "contraindications": [], "category": "清热药", "subcategory": "清热解毒药"},
    {"name": "苦地丁", "pinyin": "Ku Di Ding", "latin_name": "Corydalis Bungeanae Herba", "nature": "寒", "flavor": ["苦"], "meridian": ["心经", "肝经"], "effects": ["清热解毒", "散结消肿"], "indications": ["痈肿疮毒", "丹毒", "目赤肿痛"], "usage": "煎服，9-15g", "contraindications": [], "category": "清热药", "subcategory": "清热解毒药"},
    {"name": "杠板归", "pinyin": "Gang Ban Gui", "latin_name": "Polygoni Perfoliati Herba", "nature": "寒", "flavor": ["酸", "苦"], "meridian": ["肺经", "膀胱经"], "effects": ["清热解毒", "利水消肿", "止咳"], "indications": ["咽喉肿痛", "肺热咳嗽", "湿热泻痢"], "usage": "煎服，15-30g", "contraindications": [], "category": "清热药", "subcategory": "清热解毒药"},
    {"name": "木芙蓉叶", "pinyin": "Mu Fu Rong Ye", "latin_name": "Hibisci Mutabilis Folium", "nature": "凉", "flavor": ["微辛"], "meridian": ["肺经", "肝经"], "effects": ["凉血解毒", "消肿止痛"], "indications": ["痈肿疮毒", "丹毒", "烧烫伤"], "usage": "外用适量", "contraindications": [], "category": "清热药", "subcategory": "清热解毒药"},
    {"name": "蛇莓", "pinyin": "She Mei", "latin_name": "Duchesneae Indicae Herba", "nature": "寒", "flavor": ["甘", "苦"], "meridian": ["肺经", "肝经", "大肠经"], "effects": ["清热解毒", "散瘀消肿"], "indications": ["热毒痈肿", "咽喉肿痛", "毒蛇咬伤"], "usage": "煎服，9-15g", "contraindications": [], "category": "清热药", "subcategory": "清热解毒药"},
    {"name": "白毛夏枯草", "pinyin": "Bai Mao Xia Ku Cao", "latin_name": "Ajugae Herba", "nature": "寒", "flavor": ["苦", "甘"], "meridian": ["肺经"], "effects": ["清热解毒", "化痰止咳", "凉血止血"], "indications": ["咽喉肿痛", "肺热咳嗽", "肺痈"], "usage": "煎服，10-30g", "contraindications": [], "category": "清热药", "subcategory": "清热解毒药"},
    {"name": "一点红", "pinyin": "Yi Dian Hong", "latin_name": "Emiliae Herba", "nature": "凉", "flavor": ["苦"], "meridian": ["肺经", "大肠经"], "effects": ["清热解毒", "散瘀消肿"], "indications": ["咽喉肿痛", "痈肿疮毒", "湿热泻痢"], "usage": "煎服，9-15g", "contraindications": [], "category": "清热药", "subcategory": "清热解毒药"},
    {"name": "鬼针草", "pinyin": "Gui Zhen Cao", "latin_name": "Bidentis Bipinnatae Herba", "nature": "平", "flavor": ["苦"], "meridian": ["肝经", "肺经", "大肠经"], "effects": ["清热解毒", "散瘀消肿", "祛风除湿"], "indications": ["咽喉肿痛", "泄泻痢疾", "风湿痹痛"], "usage": "煎服，15-30g", "contraindications": [], "category": "清热药", "subcategory": "清热解毒药"},

    # ====== 化痰止咳平喘药补充3 ======
    {"name": "荜茇根", "pinyin": "Bi Ba Gen", "latin_name": "Piperis Longi Radix", "nature": "温", "flavor": ["辛"], "meridian": ["脾经", "胃经"], "effects": ["温中散寒", "下气消食"], "indications": ["胃寒腹痛", "食欲不振", "呕吐"], "usage": "煎服，3-6g", "contraindications": [], "category": "温里药", "subcategory": ""},
    {"name": "钟乳石", "pinyin": "Zhong Ru Shi", "latin_name": "Stalactitum", "nature": "温", "flavor": ["甘"], "meridian": ["肺经", "肾经", "胃经"], "effects": ["温肺助阳", "平喘制酸"], "indications": ["寒痰咳喘", "阳虚冷喘", "胃痛泛酸"], "usage": "煎服，9-15g", "contraindications": [], "category": "化痰止咳平喘药", "subcategory": "温化寒痰药"},
    {"name": "胆南星", "pinyin": "Dan Nan Xing", "latin_name": "Arisaema cum Bile", "nature": "凉", "flavor": ["苦", "微辛"], "meridian": ["肺经", "肝经", "脾经"], "effects": ["清热化痰", "息风定惊"], "indications": ["痰热咳嗽", "中风痰迷", "癫狂惊痫"], "usage": "煎服，3-6g", "contraindications": [], "category": "化痰止咳平喘药", "subcategory": "清热化痰药"},
    {"name": "岩白菜", "pinyin": "Yan Bai Cai", "latin_name": "Bergeniae Rhizoma", "nature": "平", "flavor": ["甘", "微涩"], "meridian": ["肺经", "肝经"], "effects": ["化痰止咳", "收敛止血"], "indications": ["咳嗽痰多", "咯血", "外伤出血"], "usage": "煎服，6-12g", "contraindications": [], "category": "化痰止咳平喘药", "subcategory": "止咳平喘药"},
    {"name": "华山参", "pinyin": "Hua Shan Shen", "latin_name": "Physochlainae Radix", "nature": "微温", "flavor": ["甘", "微苦"], "meridian": ["肺经"], "effects": ["补虚平喘", "温肺祛痰"], "indications": ["虚寒喘咳", "痰多"], "usage": "煎服，1-2g", "contraindications": [], "category": "化痰止咳平喘药", "subcategory": "止咳平喘药"},
    {"name": "杜鹃花叶", "pinyin": "Du Juan Hua Ye", "latin_name": "Rhododendri Simsii Folium", "nature": "平", "flavor": ["酸"], "meridian": ["肺经"], "effects": ["祛痰止咳", "清热解毒"], "indications": ["咳嗽痰多", "痈肿疮毒"], "usage": "煎服，3-10g", "contraindications": [], "category": "化痰止咳平喘药", "subcategory": "止咳平喘药"},

    # ====== 活血化瘀药补充3 ======
    {"name": "急性子", "pinyin": "Ji Xing Zi", "latin_name": "Impatientis Semen", "nature": "温", "flavor": ["微苦", "辛"], "meridian": ["肺经", "肝经"], "effects": ["破血软坚", "消积散结"], "indications": ["癥瘕痞块", "经闭", "噎膈"], "usage": "煎服，3-4.5g", "contraindications": ["孕妇慎用"], "category": "活血化瘀药", "subcategory": "破血消癥药"},
    {"name": "卷柏", "pinyin": "Juan Bai", "latin_name": "Selaginellae Herba", "nature": "平", "flavor": ["辛"], "meridian": ["肝经", "心经"], "effects": ["活血通经", "化瘀止血"], "indications": ["瘀血经闭", "癥瘕痞块", "跌打损伤"], "usage": "煎服，5-10g", "contraindications": ["孕妇慎用"], "category": "活血化瘀药", "subcategory": "活血调经药"},
    {"name": "北刘寄奴", "pinyin": "Bei Liu Ji Nu", "latin_name": "Siphonostegiae Herba", "nature": "凉", "flavor": ["苦"], "meridian": ["脾经", "胃经", "肝经", "胆经"], "effects": ["活血祛瘀", "清热利湿", "通络止痛"], "indications": ["血瘀经闭", "跌打损伤", "湿热黄疸"], "usage": "煎服，6-9g", "contraindications": [], "category": "活血化瘀药", "subcategory": "活血疗伤药"},

    # ====== 止血药补充3 ======
    {"name": "鸡冠花", "pinyin": "Ji Guan Hua", "latin_name": "Celosiae Cristatae Flos", "nature": "凉", "flavor": ["甘", "涩"], "meridian": ["肝经", "大肠经"], "effects": ["凉血止血", "收敛止带"], "indications": ["崩漏便血", "赤白带下"], "usage": "煎服，6-12g", "contraindications": [], "category": "止血药", "subcategory": "凉血止血药"},
    {"name": "断血流", "pinyin": "Duan Xue Liu", "latin_name": "Clinopodii Herba", "nature": "凉", "flavor": ["微苦", "辛"], "meridian": ["肝经"], "effects": ["收敛止血"], "indications": ["崩漏", "创伤出血"], "usage": "煎服，9-15g", "contraindications": [], "category": "止血药", "subcategory": "收敛止血药"},

    # ====== 祛风湿药补充3 ======
    {"name": "徐长卿根", "pinyin": "Xu Zhang Qing Gen", "latin_name": "Cynanchi Paniculati Radix et Rhizoma", "nature": "平", "flavor": ["辛"], "meridian": ["肝经", "胃经"], "effects": ["祛风除湿", "活血解毒"], "indications": ["风湿痹痛", "湿疹瘙痒", "毒蛇咬伤"], "usage": "煎服，6-12g", "contraindications": [], "category": "祛风湿药", "subcategory": "祛风湿散寒药"},
    {"name": "两面针", "pinyin": "Liang Mian Zhen", "latin_name": "Zanthoxyli Radix", "nature": "温", "flavor": ["辛", "苦"], "meridian": ["肝经", "胃经"], "effects": ["祛风通络", "行气止痛", "活血散瘀"], "indications": ["风湿痹痛", "牙痛", "跌打损伤"], "usage": "煎服，5-10g", "contraindications": [], "category": "祛风湿药", "subcategory": "祛风湿散寒药"},
    {"name": "闹羊花", "pinyin": "Nao Yang Hua", "latin_name": "Rhododendri Mollis Flos", "nature": "温", "flavor": ["辛"], "meridian": ["肝经"], "effects": ["祛风除湿", "散瘀定痛"], "indications": ["风湿痹痛", "跌打损伤"], "usage": "煎服，0.6-1.5g", "contraindications": ["孕妇禁用"], "category": "祛风湿药", "subcategory": "祛风湿散寒药"},

    # ====== 理气药补充2 ======
    {"name": "娑罗子", "pinyin": "Suo Luo Zi", "latin_name": "Aesculi Semen", "nature": "温", "flavor": ["甘"], "meridian": ["肝经", "胃经"], "effects": ["疏肝理气", "和胃止痛"], "indications": ["肝胃气滞", "胸胁胀痛", "经前腹痛"], "usage": "煎服，3-9g", "contraindications": [], "category": "理气药", "subcategory": ""},
    {"name": "天仙藤", "pinyin": "Tian Xian Teng", "latin_name": "Aristolochiae Herba", "nature": "温", "flavor": ["苦"], "meridian": ["肝经", "脾经"], "effects": ["行气活血", "祛风化湿"], "indications": ["心腹气痛", "疝气痛", "风湿痹痛"], "usage": "煎服，4.5-9g", "contraindications": [], "category": "理气药", "subcategory": ""},

    # ====== 驱虫药补充2 ======
    {"name": "芜荑", "pinyin": "Wu Yi", "latin_name": "Ulmi Macrocarpae Fructus Praeparatus", "nature": "温", "flavor": ["辛", "苦"], "meridian": ["脾经", "胃经"], "effects": ["杀虫消积"], "indications": ["虫积腹痛", "小儿疳积"], "usage": "煎服，3-10g", "contraindications": [], "category": "驱虫药", "subcategory": ""},

    # ====== 消食药补充2 ======
    {"name": "隔山消", "pinyin": "Ge Shan Xiao", "latin_name": "Cynanchi Wilfordii Radix", "nature": "平", "flavor": ["甘", "微苦"], "meridian": ["脾经", "胃经", "肝经"], "effects": ["消食健胃", "理气止痛", "催乳"], "indications": ["食积不化", "脘腹胀痛", "乳汁不下"], "usage": "煎服，9-15g", "contraindications": [], "category": "消食药", "subcategory": ""},

    # ====== 利水渗湿药补充3 ======
    {"name": "广金钱草", "pinyin": "Guang Jin Qian Cao", "latin_name": "Desmodii Styracifolii Herba", "nature": "凉", "flavor": ["甘", "淡"], "meridian": ["肝经", "肾经", "膀胱经"], "effects": ["利湿退黄", "利尿通淋"], "indications": ["湿热黄疸", "石淋", "热淋"], "usage": "煎服，15-30g", "contraindications": [], "category": "利水渗湿药", "subcategory": "利湿退黄药"},
    {"name": "连钱草", "pinyin": "Lian Qian Cao", "latin_name": "Glechomae Herba", "nature": "微寒", "flavor": ["辛", "微苦"], "meridian": ["肝经", "肾经", "膀胱经"], "effects": ["利湿通淋", "清热解毒", "散瘀消肿"], "indications": ["热淋", "石淋", "湿热黄疸"], "usage": "煎服，15-30g", "contraindications": [], "category": "利水渗湿药", "subcategory": "利尿通淋药"},
    {"name": "小通草", "pinyin": "Xiao Tong Cao", "latin_name": "Stachyuri seu Helwingiae Medulla", "nature": "寒", "flavor": ["甘", "淡"], "meridian": ["肺经", "胃经"], "effects": ["利尿通淋", "清热下乳"], "indications": ["热淋涩痛", "小便不利", "乳汁不下"], "usage": "煎服，3-6g", "contraindications": [], "category": "利水渗湿药", "subcategory": "利尿通淋药"},
    {"name": "溪黄草", "pinyin": "Xi Huang Cao", "latin_name": "Rabdosiae Serrae Herba", "nature": "寒", "flavor": ["苦"], "meridian": ["肝经", "胆经", "大肠经"], "effects": ["清热利湿", "凉血散瘀"], "indications": ["湿热黄疸", "湿热泻痢", "跌打损伤"], "usage": "煎服，15-30g", "contraindications": [], "category": "利水渗湿药", "subcategory": "利湿退黄药"},
    {"name": "冬葵子", "pinyin": "Dong Kui Zi", "latin_name": "Malvae Fructus", "nature": "寒", "flavor": ["甘", "淡"], "meridian": ["大肠经", "小肠经", "膀胱经"], "effects": ["利尿通淋", "下乳润肠"], "indications": ["淋证", "水肿", "乳汁不通", "便秘"], "usage": "煎服，3-9g", "contraindications": [], "category": "利水渗湿药", "subcategory": "利尿通淋药"},
    {"name": "地耳草", "pinyin": "Di Er Cao", "latin_name": "Hyperici Japonici Herba", "nature": "凉", "flavor": ["苦", "甘"], "meridian": ["肝经", "胆经"], "effects": ["利湿退黄", "清热解毒", "活血消肿"], "indications": ["湿热黄疸", "痈肿疮毒", "跌打损伤"], "usage": "煎服，15-30g", "contraindications": [], "category": "利水渗湿药", "subcategory": "利湿退黄药"},

    # ====== 补虚药补充3 ======
    {"name": "雪莲花", "pinyin": "Xue Lian Hua", "latin_name": "Saussureae Involucratae Herba", "nature": "温", "flavor": ["甘", "微苦"], "meridian": ["肝经", "肾经"], "effects": ["温肾壮阳", "祛风除湿", "调经止血"], "indications": ["阳痿", "腰膝酸软", "月经不调"], "usage": "煎服，3-6g", "contraindications": ["孕妇慎用"], "category": "补虚药", "subcategory": "补阳药"},
    {"name": "鹿茸草", "pinyin": "Lu Rong Cao", "latin_name": "Monochasmae Herba", "nature": "平", "flavor": ["苦", "涩"], "meridian": ["肺经", "肝经"], "effects": ["补肺益肾", "收敛止血"], "indications": ["虚劳咳嗽", "咯血", "创伤出血"], "usage": "煎服，9-15g", "contraindications": [], "category": "补虚药", "subcategory": "补阴药"},
    {"name": "手掌参", "pinyin": "Shou Zhang Shen", "latin_name": "Gymnadeniae Rhizoma", "nature": "平", "flavor": ["甘"], "meridian": ["肺经", "脾经", "胃经"], "effects": ["补益气血", "生津止渴"], "indications": ["体虚乏力", "肺虚咳喘", "消渴"], "usage": "煎服，3-10g", "contraindications": [], "category": "补虚药", "subcategory": "补气药"},
    {"name": "珠子参", "pinyin": "Zhu Zi Shen", "latin_name": "Panacis Majoris Rhizoma", "nature": "微寒", "flavor": ["苦", "甘"], "meridian": ["肝经", "肺经", "胃经"], "effects": ["补肺养阴", "祛瘀止痛", "止血"], "indications": ["肺虚咳嗽", "吐血衄血", "跌打损伤"], "usage": "煎服，3-9g", "contraindications": [], "category": "补虚药", "subcategory": "补阴药"},
    {"name": "竹节参", "pinyin": "Zhu Jie Shen", "latin_name": "Panacis Japonici Rhizoma", "nature": "温", "flavor": ["甘", "微苦"], "meridian": ["肺经", "脾经", "肝经"], "effects": ["滋补强壮", "散瘀止痛", "化痰止咳"], "indications": ["病后虚弱", "肺虚咳嗽", "跌打损伤"], "usage": "煎服，6-9g", "contraindications": [], "category": "补虚药", "subcategory": "补气药"},
    {"name": "鹿角胶", "pinyin": "Lu Jiao Jiao", "latin_name": "Cervi Cornus Colla", "nature": "温", "flavor": ["甘", "咸"], "meridian": ["肝经", "肾经"], "effects": ["温补肝肾", "益精养血"], "indications": ["虚劳羸瘦", "腰膝酸冷", "阳痿滑精"], "usage": "烊化兑服，3-6g", "contraindications": [], "category": "补虚药", "subcategory": "补阳药"},
    {"name": "紫河车粉", "pinyin": "Zi He Che Fen", "latin_name": "Hominis Placenta Pulvis", "nature": "平", "flavor": ["甘", "咸"], "meridian": ["肺经", "肝经", "肾经"], "effects": ["温肾补精", "益气养血"], "indications": ["虚劳羸瘦", "骨蒸盗汗", "咳喘"], "usage": "研末，1.5-3g", "contraindications": [], "category": "补虚药", "subcategory": "补阳药"},
    {"name": "明党参", "pinyin": "Ming Dang Shen", "latin_name": "Changii Radix", "nature": "微寒", "flavor": ["甘", "微苦"], "meridian": ["肺经", "脾经", "肝经"], "effects": ["润肺化痰", "养阴和胃", "平肝解毒"], "indications": ["肺热咳嗽", "胃阴不足", "眩晕"], "usage": "煎服，6-12g", "contraindications": [], "category": "补虚药", "subcategory": "补阴药"},
    {"name": "枸杞叶", "pinyin": "Gou Qi Ye", "latin_name": "Lycii Folium", "nature": "凉", "flavor": ["苦", "甘"], "meridian": ["肝经", "肾经"], "effects": ["补虚益精", "清热明目"], "indications": ["虚劳发热", "目赤肿痛", "消渴"], "usage": "煎服，6-12g", "contraindications": [], "category": "补虚药", "subcategory": "补阴药"},

    # ====== 收涩药补充3 ======
    {"name": "没食子", "pinyin": "Mo Shi Zi", "latin_name": "Galla Turcica", "nature": "温", "flavor": ["苦", "涩"], "meridian": ["肺经", "脾经", "肾经"], "effects": ["固气涩精", "敛肺止血"], "indications": ["久泻久痢", "遗精滑精", "咳嗽咯血"], "usage": "煎服，6-12g", "contraindications": [], "category": "收涩药", "subcategory": ""},
    {"name": "椿皮", "pinyin": "Chun Pi", "latin_name": "Ailanthi Cortex", "nature": "寒", "flavor": ["苦", "涩"], "meridian": ["大肠经", "胃经", "肝经"], "effects": ["清热燥湿", "涩肠止泻", "收敛止血"], "indications": ["湿热泻痢", "崩漏便血", "带下"], "usage": "煎服，6-9g", "contraindications": [], "category": "收涩药", "subcategory": ""},

    # ====== 安神药补充3 ======
    {"name": "紫石英", "pinyin": "Zi Shi Ying", "latin_name": "Fluoritum", "nature": "温", "flavor": ["甘"], "meridian": ["心经", "肝经"], "effects": ["镇心定惊", "温肺暖宫"], "indications": ["心悸易惊", "失眠多梦", "宫冷不孕"], "usage": "煎服，9-15g，打碎先煎", "contraindications": [], "category": "安神药", "subcategory": "重镇安神药"},

    # ====== 开窍药补充3 ======
    {"name": "樟木", "pinyin": "Zhang Mu", "latin_name": "Cinnamomi Camphorae Lignum", "nature": "温", "flavor": ["辛"], "meridian": ["心经", "脾经", "肝经"], "effects": ["祛风散寒", "温中理气", "活血通络"], "indications": ["风寒感冒", "胃寒腹痛", "风湿痹痛"], "usage": "煎服，9-15g", "contraindications": [], "category": "祛风湿药", "subcategory": "祛风湿散寒药"},

    # ====== 平肝熄风药补充3 ======
    {"name": "决明子炒", "pinyin": "Chao Jue Ming Zi", "latin_name": "Cassiae Semen Tostum", "nature": "微寒", "flavor": ["甘", "苦", "咸"], "meridian": ["肝经", "大肠经"], "effects": ["清热平肝", "润肠明目"], "indications": ["头痛眩晕", "目赤肿痛", "肠燥便秘"], "usage": "煎服，9-15g", "contraindications": [], "category": "平肝熄风药", "subcategory": ""},
    {"name": "天青地白", "pinyin": "Tian Qing Di Bai", "latin_name": "Gnaphalii Japonici Herba", "nature": "凉", "flavor": ["甘", "淡"], "meridian": ["肝经", "肺经"], "effects": ["平肝明目", "清热解毒"], "indications": ["目赤肿痛", "咽喉肿痛", "痈肿"], "usage": "煎服，15-30g", "contraindications": [], "category": "平肝熄风药", "subcategory": ""},

    # ====== 涌吐药补充2 ======
    {"name": "胆矾", "pinyin": "Dan Fan", "latin_name": "Chalcanthitum", "nature": "寒", "flavor": ["酸", "辛"], "meridian": ["肝经", "胆经"], "effects": ["涌吐痰涎", "解毒收湿", "蚀疮去腐"], "indications": ["风痰壅盛", "喉痹", "口疮"], "usage": "内服0.3-0.6g", "contraindications": [], "category": "涌吐药", "subcategory": ""},

    # ====== 解毒杀虫燥湿止痒药补充3 ======
    {"name": "皂矾", "pinyin": "Zao Fan", "latin_name": "Melanteritum", "nature": "凉", "flavor": ["酸", "涩"], "meridian": ["肝经", "脾经"], "effects": ["解毒燥湿", "杀虫补血"], "indications": ["疮毒疥癣", "黄肿虚肿"], "usage": "内服0.8-1.6g", "contraindications": [], "category": "解毒杀虫燥湿止痒药", "subcategory": ""},
    {"name": "蓖麻子", "pinyin": "Bi Ma Zi", "latin_name": "Ricini Semen", "nature": "平", "flavor": ["甘", "辛"], "meridian": ["大肠经", "肺经"], "effects": ["消肿拔毒", "泻下通滞"], "indications": ["痈疽肿毒", "瘰疬", "便秘"], "usage": "内服2-5g", "contraindications": ["孕妇禁用"], "category": "解毒杀虫燥湿止痒药", "subcategory": ""},

    # ====== 其他补充 ======
    {"name": "松花粉", "pinyin": "Song Hua Fen", "latin_name": "Pini Pollen", "nature": "温", "flavor": ["甘"], "meridian": ["肝经", "脾经"], "effects": ["收敛止血", "燥湿敛疮"], "indications": ["外伤出血", "湿疹", "黄水疮"], "usage": "外用适量", "contraindications": [], "category": "止血药", "subcategory": "收敛止血药"},
    {"name": "臭灵丹草", "pinyin": "Chou Ling Dan Cao", "latin_name": "Laggerae Herba", "nature": "寒", "flavor": ["辛", "苦"], "meridian": ["肺经"], "effects": ["清热解毒", "止咳祛痰"], "indications": ["风热感冒", "咽喉肿痛", "肺热咳嗽"], "usage": "煎服，9-15g", "contraindications": [], "category": "清热药", "subcategory": "清热解毒药"},
    {"name": "哈蟆油", "pinyin": "Ha Ma You", "latin_name": "Ranae Oviductus", "nature": "平", "flavor": ["甘", "咸"], "meridian": ["肺经", "肾经"], "effects": ["补肾益精", "养阴润肺"], "indications": ["病后体虚", "肺痨咳嗽", "盗汗"], "usage": "炖服，5-15g", "contraindications": [], "category": "补虚药", "subcategory": "补阴药"},
    {"name": "了哥王", "pinyin": "Liao Ge Wang", "latin_name": "Wikstroemiae Indicae Radix", "nature": "寒", "flavor": ["苦", "辛"], "meridian": ["肺经", "胃经"], "effects": ["清热解毒", "消肿散结", "止痛"], "indications": ["痈肿疮毒", "瘰疬", "风湿痹痛"], "usage": "煎服，6-9g", "contraindications": ["孕妇慎用"], "category": "清热药", "subcategory": "清热解毒药"},
    {"name": "铁包金", "pinyin": "Tie Bao Jin", "latin_name": "Berchemiae Lineatae Radix", "nature": "平", "flavor": ["苦", "微涩"], "meridian": ["肺经", "肝经"], "effects": ["化痰止咳", "散瘀止痛"], "indications": ["咳嗽痰多", "跌打损伤", "风湿骨痛"], "usage": "煎服，15-30g", "contraindications": [], "category": "化痰止咳平喘药", "subcategory": "止咳平喘药"},
    {"name": "三七花", "pinyin": "San Qi Hua", "latin_name": "Notoginseng Flos", "nature": "凉", "flavor": ["甘"], "meridian": ["肝经"], "effects": ["清热平肝", "降压安神"], "indications": ["头昏目眩", "高血压", "失眠"], "usage": "煎服，3-6g", "contraindications": [], "category": "平肝熄风药", "subcategory": ""},
    {"name": "野木瓜", "pinyin": "Ye Mu Gua", "latin_name": "Stauntoniae Caulis et Folium", "nature": "温", "flavor": ["微苦"], "meridian": ["肝经", "胃经"], "effects": ["祛风止痛", "舒筋活络"], "indications": ["风湿痹痛", "三叉神经痛", "坐骨神经痛"], "usage": "煎服，9-15g", "contraindications": [], "category": "祛风湿药", "subcategory": "祛风湿散寒药"},
    {"name": "叶下珠", "pinyin": "Ye Xia Zhu", "latin_name": "Phyllanthi Urinariae Herba", "nature": "凉", "flavor": ["甘", "苦"], "meridian": ["肝经", "脾经"], "effects": ["清热利湿", "解毒消疳", "平肝明目"], "indications": ["湿热黄疸", "泄泻痢疾", "目赤肿痛"], "usage": "煎服，15-30g", "contraindications": [], "category": "清热药", "subcategory": "清热解毒药"},
    {"name": "积雪草", "pinyin": "Ji Xue Cao", "latin_name": "Centellae Herba", "nature": "寒", "flavor": ["苦", "辛"], "meridian": ["肝经", "脾经", "肾经"], "effects": ["清热利湿", "解毒消肿"], "indications": ["湿热黄疸", "痈肿疮毒", "跌打损伤"], "usage": "煎服，15-30g", "contraindications": [], "category": "清热药", "subcategory": "清热解毒药"},
    {"name": "半枝莲", "pinyin": "Ban Zhi Lian", "latin_name": "Scutellariae Barbatae Herba", "nature": "寒", "flavor": ["辛", "苦"], "meridian": ["肺经", "肝经", "肾经"], "effects": ["清热解毒", "散瘀止血", "利水消肿"], "indications": ["痈肿疮毒", "咽喉肿痛", "毒蛇咬伤"], "usage": "煎服，15-30g", "contraindications": [], "category": "清热药", "subcategory": "清热解毒药"},
    {"name": "龙葵", "pinyin": "Long Kui", "latin_name": "Solani Nigri Herba", "nature": "寒", "flavor": ["苦", "微甘"], "meridian": ["肺经", "膀胱经"], "effects": ["清热解毒", "活血消肿", "利尿"], "indications": ["痈肿疮毒", "咽喉肿痛", "水肿"], "usage": "煎服，9-15g", "contraindications": [], "category": "清热药", "subcategory": "清热解毒药"},
    {"name": "豨莶草", "pinyin": "Xi Xian Cao", "latin_name": "Siegesbeckiae Herba", "nature": "寒", "flavor": ["辛", "苦"], "meridian": ["肝经", "肾经"], "effects": ["祛风湿", "利关节", "解毒"], "indications": ["风湿痹痛", "半身不遂", "疮疡"], "usage": "煎服，9-12g", "contraindications": [], "category": "祛风湿药", "subcategory": "祛风湿清热药"},

    # ====== 最终补充批次 ======
    {"name": "三白草", "pinyin": "San Bai Cao", "latin_name": "Saururi Herba", "nature": "寒", "flavor": ["甘", "辛"], "meridian": ["肺经", "膀胱经"], "effects": ["清热解毒", "利尿消肿"], "indications": ["小便不利", "淋沥涩痛", "水肿"], "usage": "煎服，15-30g", "contraindications": [], "category": "利水渗湿药", "subcategory": "利尿通淋药"},
    {"name": "鹿蹄草", "pinyin": "Lu Ti Cao", "latin_name": "Pyrolae Herba", "nature": "平", "flavor": ["甘", "苦"], "meridian": ["肝经", "肾经"], "effects": ["祛风湿", "强筋骨", "止血"], "indications": ["风湿痹痛", "腰膝无力", "月经过多"], "usage": "煎服，9-15g", "contraindications": [], "category": "祛风湿药", "subcategory": "祛风湿强筋骨药"},
    {"name": "凤尾草", "pinyin": "Feng Wei Cao", "latin_name": "Pteridis Multifidae Herba", "nature": "寒", "flavor": ["微苦"], "meridian": ["大肠经", "肝经", "心经"], "effects": ["清热利湿", "凉血止血", "解毒消肿"], "indications": ["湿热泻痢", "便血", "咽喉肿痛"], "usage": "煎服，9-15g", "contraindications": [], "category": "清热药", "subcategory": "清热解毒药"},
    {"name": "六月雪", "pinyin": "Liu Yue Xue", "latin_name": "Serissae Herba", "nature": "凉", "flavor": ["淡", "微辛"], "meridian": ["肝经", "脾经"], "effects": ["疏风解表", "清热利湿", "舒筋活络"], "indications": ["感冒", "湿热黄疸", "风湿痹痛"], "usage": "煎服，10-30g", "contraindications": [], "category": "解表药", "subcategory": "辛凉解表药"},
    {"name": "海藻石", "pinyin": "Hai Zao Shi", "latin_name": "Sargassum Lapideum", "nature": "寒", "flavor": ["咸"], "meridian": ["肝经", "胃经"], "effects": ["软坚散结", "消痰利水"], "indications": ["瘿瘤", "瘰疬", "痰饮"], "usage": "煎服，10-15g", "contraindications": [], "category": "化痰止咳平喘药", "subcategory": "消痰软坚药"},
    {"name": "牛大力", "pinyin": "Niu Da Li", "latin_name": "Millettiae Speciosae Radix", "nature": "平", "flavor": ["甘"], "meridian": ["肺经", "肾经"], "effects": ["补虚润肺", "强筋活络"], "indications": ["肺虚咳嗽", "腰肌劳损", "风湿痹痛"], "usage": "煎服，15-30g", "contraindications": [], "category": "补虚药", "subcategory": "补气药"},
    {"name": "五指毛桃", "pinyin": "Wu Zhi Mao Tao", "latin_name": "Fici Hirtae Radix", "nature": "平", "flavor": ["甘"], "meridian": ["脾经", "肺经", "肝经"], "effects": ["健脾补肺", "行气利湿", "舒筋活络"], "indications": ["脾虚浮肿", "食少无力", "风湿痹痛"], "usage": "煎服，15-30g", "contraindications": [], "category": "补虚药", "subcategory": "补气药"},
    {"name": "千斤拔", "pinyin": "Qian Jin Ba", "latin_name": "Flemingiae Radix", "nature": "平", "flavor": ["甘", "微涩"], "meridian": ["肝经", "肾经"], "effects": ["祛风除湿", "强筋健骨", "活血解毒"], "indications": ["风湿痹痛", "腰肌劳损", "跌打损伤"], "usage": "煎服，15-30g", "contraindications": [], "category": "祛风湿药", "subcategory": "祛风湿强筋骨药"},
    {"name": "黑老虎", "pinyin": "Hei Lao Hu", "latin_name": "Kadsurae Coccineae Radix", "nature": "温", "flavor": ["辛", "微苦"], "meridian": ["肝经", "胃经"], "effects": ["行气止痛", "活血散瘀"], "indications": ["胃痛", "痛经", "跌打损伤"], "usage": "煎服，9-15g", "contraindications": [], "category": "活血化瘀药", "subcategory": "活血止痛药"},
    {"name": "救必应", "pinyin": "Jiu Bi Ying", "latin_name": "Ilicis Rotundae Cortex", "nature": "寒", "flavor": ["苦"], "meridian": ["肺经", "胃经", "大肠经"], "effects": ["清热解毒", "利湿止痛"], "indications": ["感冒发热", "咽喉肿痛", "湿热泻痢"], "usage": "煎服，9-15g", "contraindications": [], "category": "清热药", "subcategory": "清热解毒药"},
    {"name": "布渣叶", "pinyin": "Bu Zha Ye", "latin_name": "Microctis Folium", "nature": "平", "flavor": ["酸"], "meridian": ["脾经", "胃经"], "effects": ["消食化滞", "清热利湿"], "indications": ["食积不化", "脘腹胀满", "湿热黄疸"], "usage": "煎服，15-30g", "contraindications": [], "category": "消食药", "subcategory": ""},
    {"name": "岗梅根", "pinyin": "Gang Mei Gen", "latin_name": "Ilicis Asprellae Radix", "nature": "凉", "flavor": ["苦", "甘"], "meridian": ["肺经", "胃经"], "effects": ["清热解毒", "生津止渴", "利咽"], "indications": ["感冒发热", "咽喉肿痛", "消渴"], "usage": "煎服，15-30g", "contraindications": [], "category": "清热药", "subcategory": "清热解毒药"},
    {"name": "火炭母", "pinyin": "Huo Tan Mu", "latin_name": "Polygoni Chinensis Herba", "nature": "凉", "flavor": ["微酸", "微涩"], "meridian": ["肝经", "脾经"], "effects": ["清热利湿", "凉血解毒", "明目退翳"], "indications": ["湿热泻痢", "目赤肿痛", "痈肿疮毒"], "usage": "煎服，9-15g", "contraindications": [], "category": "清热药", "subcategory": "清热解毒药"},
    {"name": "金荞麦茎", "pinyin": "Jin Qiao Mai Jing", "latin_name": "Fagopyri Dibotryis Herba", "nature": "凉", "flavor": ["微辛", "涩"], "meridian": ["肺经"], "effects": ["清热解毒", "化痰排脓"], "indications": ["肺痈", "咽喉肿痛", "痈肿疮毒"], "usage": "煎服，15-30g", "contraindications": [], "category": "清热药", "subcategory": "清热解毒药"},
    {"name": "荞麦花粉", "pinyin": "Qiao Mai Hua Fen", "latin_name": "Fagopyri Pollen", "nature": "平", "flavor": ["甘"], "meridian": ["脾经", "胃经"], "effects": ["健脾益气", "和胃消食"], "indications": ["脾胃虚弱", "食欲不振", "腹胀"], "usage": "冲服，5-10g", "contraindications": [], "category": "补虚药", "subcategory": "补气药"},
    {"name": "合萌", "pinyin": "He Meng", "latin_name": "Aeschynomenes Herba", "nature": "凉", "flavor": ["甘", "淡"], "meridian": ["肝经", "膀胱经"], "effects": ["利尿通淋", "清热解毒"], "indications": ["热淋", "水肿", "痈肿"], "usage": "煎服，15-30g", "contraindications": [], "category": "利水渗湿药", "subcategory": "利尿通淋药"},
    {"name": "鸡眼草", "pinyin": "Ji Yan Cao", "latin_name": "Kummerowiae Herba", "nature": "凉", "flavor": ["甘", "淡"], "meridian": ["肝经", "脾经"], "effects": ["清热解毒", "健脾利湿"], "indications": ["湿热黄疸", "泄泻", "痈肿疮毒"], "usage": "煎服，9-15g", "contraindications": [], "category": "清热药", "subcategory": "清热解毒药"},
    {"name": "田基黄", "pinyin": "Tian Ji Huang", "latin_name": "Hyperici Japonici Herba", "nature": "凉", "flavor": ["甘", "微苦"], "meridian": ["肝经", "肺经"], "effects": ["清热利湿", "解毒消肿", "散瘀止痛"], "indications": ["湿热黄疸", "痈肿疮毒", "跌打损伤"], "usage": "煎服，15-30g", "contraindications": [], "category": "清热药", "subcategory": "清热解毒药"},
    {"name": "紫草茸", "pinyin": "Zi Cao Rong", "latin_name": "Lacca", "nature": "平", "flavor": ["甘", "咸"], "meridian": ["肝经"], "effects": ["清热凉血", "解毒透疹"], "indications": ["麻疹不透", "疮疡湿疹"], "usage": "煎服，1.5-6g", "contraindications": [], "category": "清热药", "subcategory": "清热凉血药"},
    {"name": "穿破石", "pinyin": "Chuan Po Shi", "latin_name": "Cudraniae Radix", "nature": "凉", "flavor": ["微苦"], "meridian": ["肝经"], "effects": ["祛风通络", "清热除湿", "解毒消肿"], "indications": ["风湿痹痛", "湿热黄疸", "痈肿"], "usage": "煎服，9-30g", "contraindications": [], "category": "祛风湿药", "subcategory": "祛风湿清热药"},
    {"name": "大飞扬草", "pinyin": "Da Fei Yang Cao", "latin_name": "Euphorbiae Hirtae Herba", "nature": "凉", "flavor": ["微苦", "酸"], "meridian": ["肺经", "大肠经"], "effects": ["清热解毒", "利湿止痒", "通乳"], "indications": ["湿热泻痢", "湿疹瘙痒", "乳汁不通"], "usage": "煎服，15-30g", "contraindications": [], "category": "清热药", "subcategory": "清热解毒药"},
    {"name": "独一味", "pinyin": "Du Yi Wei", "latin_name": "Lamiophlomis Herba", "nature": "平", "flavor": ["甘", "苦"], "meridian": ["肝经"], "effects": ["活血止血", "祛风止痛"], "indications": ["跌打损伤", "外伤出血", "风湿痹痛"], "usage": "煎服，2-3g", "contraindications": [], "category": "活血化瘀药", "subcategory": "活血止痛药"},
    {"name": "沙枣", "pinyin": "Sha Zao", "latin_name": "Elaeagni Angustifoliae Fructus", "nature": "平", "flavor": ["酸", "微甘"], "meridian": ["脾经", "胃经", "肝经"], "effects": ["健脾止泻", "强筋健骨"], "indications": ["脾虚泄泻", "腰膝酸软", "消化不良"], "usage": "煎服，15-30g", "contraindications": [], "category": "收涩药", "subcategory": ""},
    {"name": "苦豆子", "pinyin": "Ku Dou Zi", "latin_name": "Sophorae Alopecuroidis Semen", "nature": "寒", "flavor": ["苦"], "meridian": ["胃经", "大肠经"], "effects": ["清热燥湿", "止痛杀虫"], "indications": ["湿热泻痢", "湿疹", "牙痛"], "usage": "煎服，1.5-3g", "contraindications": [], "category": "清热药", "subcategory": "清热燥湿药"},
    {"name": "黑芝麻叶", "pinyin": "Hei Zhi Ma Ye", "latin_name": "Sesami Folium", "nature": "凉", "flavor": ["甘"], "meridian": ["肝经", "肾经"], "effects": ["滋补肝肾", "润肠通便"], "indications": ["肝肾亏虚", "须发早白", "便秘"], "usage": "煎服，9-15g", "contraindications": [], "category": "补虚药", "subcategory": "补阴药"},
    {"name": "玉米花粉", "pinyin": "Yu Mi Hua Fen", "latin_name": "Maydis Pollen", "nature": "平", "flavor": ["甘"], "meridian": ["脾经", "胃经", "肝经"], "effects": ["健脾利湿", "清热利胆"], "indications": ["脾胃虚弱", "湿热黄疸", "水肿"], "usage": "冲服，5-10g", "contraindications": [], "category": "利水渗湿药", "subcategory": "利水消肿药"},
    {"name": "黄藤", "pinyin": "Huang Teng", "latin_name": "Fibraureae Caulis", "nature": "寒", "flavor": ["苦"], "meridian": ["心经", "肝经"], "effects": ["清热解毒", "泻火通便"], "indications": ["热毒疮疡", "目赤肿痛", "便秘"], "usage": "煎服，6-9g", "contraindications": [], "category": "清热药", "subcategory": "清热解毒药"},
    {"name": "蛇蜕", "pinyin": "She Tui", "latin_name": "Serpentis Periostracum", "nature": "平", "flavor": ["咸", "甘"], "meridian": ["肝经"], "effects": ["祛风定惊", "解毒退翳", "消肿杀虫"], "indications": ["惊风癫痫", "目翳", "痈肿疮毒"], "usage": "煎服，2-3g", "contraindications": [], "category": "平肝熄风药", "subcategory": ""},
    {"name": "蝉花", "pinyin": "Chan Hua", "latin_name": "Cordyceps Cicadae", "nature": "寒", "flavor": ["甘"], "meridian": ["肺经", "肝经"], "effects": ["疏风散热", "明目退翳", "定惊"], "indications": ["风热目赤", "翳膜遮睛", "惊痫抽搐"], "usage": "煎服，3-6g", "contraindications": [], "category": "解表药", "subcategory": "辛凉解表药"},
    {"name": "人中白", "pinyin": "Ren Zhong Bai", "latin_name": "Urinae Sedimentum Calcinatum", "nature": "寒", "flavor": ["咸"], "meridian": ["肺经", "肝经", "膀胱经"], "effects": ["清热降火", "消瘀止血"], "indications": ["咽喉肿痛", "牙疳", "衄血"], "usage": "研末，3-6g", "contraindications": [], "category": "清热药", "subcategory": "清热解毒药"},
]

def main():
    input_path = 'assets/data/medicines.json'
    with open(input_path, 'r', encoding='utf-8') as f:
        medicines = json.load(f)
    
    existing_names = {m['name'] for m in medicines}
    
    # Find filler entries to replace
    filler_indices = [i for i, m in enumerate(medicines) if m['name'].startswith('中药')]
    
    added = 0
    skipped = 0
    fi = 0
    
    for herb in missing_herbs:
        if herb['name'] in existing_names:
            skipped += 1
            continue
        if fi < len(filler_indices):
            idx = filler_indices[fi]
            herb['id'] = f"medicine_{idx+1:03d}"
            medicines[idx] = herb
            existing_names.add(herb['name'])
            fi += 1
            added += 1
    
    # Count remaining filler
    remaining = sum(1 for m in medicines if m['name'].startswith('中药'))
    
    with open(input_path, 'w', encoding='utf-8') as f:
        json.dump(medicines, f, ensure_ascii=False, indent=2)
    
    real = sum(1 for m in medicines if not m['name'].startswith('中药'))
    print(f"Total: {len(medicines)}, Real: {real}, Filler: {remaining}")
    print(f"Added: {added}, Skipped: {skipped}")

if __name__ == '__main__':
    main()
