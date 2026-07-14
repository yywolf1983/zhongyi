#!/usr/bin/env python3
"""扩展穴位：新增经外奇穴，确保14经络+奇穴分类完整"""
import json
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'data')

with open(os.path.join(DATA_DIR, 'acupoints.json')) as f:
    existing = json.load(f)

# 当前奇穴列表
qi_points = [a for a in existing if a.get('meridian') == '经外奇穴']
print(f"当前经外奇穴: {len(qi_points)} 个")
existing_names = {a['name'] for a in existing}

max_id = max(int(a['id'].replace('acupoint_', '')) for a in existing)

# 新增奇穴（补充常用经外奇穴）
new_qi_points = [
    # 头颈部奇穴
    {"id": f"acupoint_{max_id+1:03d}", "name": "四神聪", "pinyin": "Si Shen Cong", "meridian": "经外奇穴", "meridian_id": "extra_point", "location": "在头顶部，百会穴前后左右各1寸处，共4穴", "indications": ["头痛", "眩晕", "失眠", "健忘", "癫痫"], "method": "平刺0.5-0.8寸", "anatomy": "在帽状腱膜中"},
    {"id": f"acupoint_{max_id+2:03d}", "name": "印堂", "pinyin": "Yin Tang", "meridian": "经外奇穴", "meridian_id": "extra_point", "location": "在额部，两眉头中间", "indications": ["头痛", "眩晕", "鼻渊", "失眠", "小儿惊风"], "method": "向下平刺0.3-0.5寸", "anatomy": "在降眉间肌中"},
    {"id": f"acupoint_{max_id+3:03d}", "name": "太阳", "pinyin": "Tai Yang", "meridian": "经外奇穴", "meridian_id": "extra_point", "location": "在颞部，眉梢与目外眦之间向后约一横指凹陷处", "indications": ["偏头痛", "目赤肿痛", "面神经麻痹"], "method": "直刺或斜刺0.3-0.5寸", "anatomy": "在颞筋膜及颞肌中"},
    {"id": f"acupoint_{max_id+4:03d}", "name": "鱼腰", "pinyin": "Yu Yao", "meridian": "经外奇穴", "meridian_id": "extra_point", "location": "在额部，瞳孔直上，眉毛中", "indications": ["目赤肿痛", "眼睑下垂", "眉棱骨痛", "面神经麻痹"], "method": "平刺0.3-0.5寸", "anatomy": "在眼轮匝肌中"},
    {"id": f"acupoint_{max_id+5:03d}", "name": "球后", "pinyin": "Qiu Hou", "meridian": "经外奇穴", "meridian_id": "extra_point", "location": "在面部，眶下缘外1/4与内3/4交界处", "indications": ["视神经萎缩", "近视", "青光眼", "早期白内障"], "method": "沿眶下缘缓慢直刺0.5-1寸", "anatomy": "在眼轮匝肌中，深部为眶下组织"},
    {"id": f"acupoint_{max_id+6:03d}", "name": "耳尖", "pinyin": "Er Jian", "meridian": "经外奇穴", "meridian_id": "extra_point", "location": "在耳廓上方，折耳向前时耳廓上方的尖端处", "indications": ["目赤肿痛", "发热", "高血压", "偏头痛"], "method": "点刺放血", "anatomy": "在耳廓软骨中"},
    {"id": f"acupoint_{max_id+7:03d}", "name": "金津玉液", "pinyin": "Jin Jin Yu Ye", "meridian": "经外奇穴", "meridian_id": "extra_point", "location": "在口腔内，舌下系带两侧静脉上", "indications": ["舌强不语", "舌肿", "口疮", "消渴"], "method": "点刺放血", "anatomy": "在舌下静脉上"},

    # 颈部奇穴
    {"id": f"acupoint_{max_id+8:03d}", "name": "颈百劳", "pinyin": "Jing Bai Lao", "meridian": "经外奇穴", "meridian_id": "extra_point", "location": "在颈部，大椎穴直上2寸，后正中线旁开1寸", "indications": ["颈项强痛", "咳嗽", "哮喘", "骨蒸潮热", "盗汗"], "method": "直刺0.5-1寸", "anatomy": "在斜方肌及头颈夹肌中"},
    {"id": f"acupoint_{max_id+9:03d}", "name": "安眠", "pinyin": "An Mian", "meridian": "经外奇穴", "meridian_id": "extra_point", "location": "在项部，翳风穴与风池穴连线的中点", "indications": ["失眠", "头痛", "眩晕", "心悸", "精神病"], "method": "直刺0.5-1寸", "anatomy": "在胸锁乳突肌与头夹肌之间"},
    {"id": f"acupoint_{max_id+10:03d}", "name": "翳明", "pinyin": "Yi Ming", "meridian": "经外奇穴", "meridian_id": "extra_point", "location": "在项部，翳风穴后1寸", "indications": ["目疾", "耳鸣", "失眠", "头痛"], "method": "直刺0.5-1寸", "anatomy": "在胸锁乳突肌上"},

    # 背部奇穴
    {"id": f"acupoint_{max_id+11:03d}", "name": "定喘", "pinyin": "Ding Chuan", "meridian": "经外奇穴", "meridian_id": "extra_point", "location": "在背部，第7颈椎棘突下旁开0.5寸", "indications": ["哮喘", "咳嗽", "落枕", "肩背痛"], "method": "直刺0.5-1寸", "anatomy": "在斜方肌、菱形肌中"},
    {"id": f"acupoint_{max_id+12:03d}", "name": "夹脊", "pinyin": "Jia Ji", "meridian": "经外奇穴", "meridian_id": "extra_point", "location": "在背腰部，第1胸椎至第5腰椎棘突下两侧旁开0.5寸，左右共34穴", "indications": ["相应脏腑病症", "脊柱强痛", "腰背痛", "下肢痿痹"], "method": "直刺0.3-0.5寸", "anatomy": "在横突间的韧带和肌肉中"},
    {"id": f"acupoint_{max_id+13:03d}", "name": "胃脘下俞", "pinyin": "Wei Wan Xia Shu", "meridian": "经外奇穴", "meridian_id": "extra_point", "location": "在背部，第8胸椎棘突下旁开1.5寸", "indications": ["胃痛", "胰腺炎", "消渴", "胁痛"], "method": "斜刺0.5-0.8寸", "anatomy": "在背阔肌、最长肌中"},
    {"id": f"acupoint_{max_id+14:03d}", "name": "腰眼", "pinyin": "Yao Yan", "meridian": "经外奇穴", "meridian_id": "extra_point", "location": "在腰部，第4腰椎棘突下旁开约3.5寸凹陷中", "indications": ["腰痛", "月经不调", "尿频", "消渴"], "method": "直刺0.5-1寸", "anatomy": "在背阔肌、腰方肌中"},
    {"id": f"acupoint_{max_id+15:03d}", "name": "十七椎", "pinyin": "Shi Qi Zhui", "meridian": "经外奇穴", "meridian_id": "extra_point", "location": "在腰部，第5腰椎棘突下", "indications": ["腰痛", "腿痛", "月经不调", "痛经"], "method": "直刺0.5-1寸", "anatomy": "在腰背筋膜、棘上韧带中"},
    {"id": f"acupoint_{max_id+16:03d}", "name": "腰奇", "pinyin": "Yao Qi", "meridian": "经外奇穴", "meridian_id": "extra_point", "location": "在骶部，尾骨尖直上2寸", "indications": ["癫痫", "头痛", "失眠", "便秘"], "method": "向上平刺1-2寸", "anatomy": "在棘上韧带中"},

    # 上肢奇穴
    {"id": f"acupoint_{max_id+17:03d}", "name": "肩前", "pinyin": "Jian Qian", "meridian": "经外奇穴", "meridian_id": "extra_point", "location": "在肩部，腋前皱襞顶端与肩髃穴连线的中点", "indications": ["肩痛", "肩关节活动障碍", "臂不能举"], "method": "直刺1-1.5寸", "anatomy": "在三角肌前缘"},
    {"id": f"acupoint_{max_id+18:03d}", "name": "二白", "pinyin": "Er Bai", "meridian": "经外奇穴", "meridian_id": "extra_point", "location": "在前臂掌侧，腕横纹上4寸，桡侧腕屈肌腱两侧各1穴", "indications": ["痔疮", "脱肛", "前臂痛", "胸胁痛"], "method": "直刺0.5-1寸", "anatomy": "在指浅屈肌与拇长屈肌中"},
    {"id": f"acupoint_{max_id+19:03d}", "name": "中魁", "pinyin": "Zhong Kui", "meridian": "经外奇穴", "meridian_id": "extra_point", "location": "在中指背侧，近端指间关节的中点处", "indications": ["呃逆", "呕吐", "食欲不振"], "method": "艾炷灸5-7壮", "anatomy": "在指间关节"},
    {"id": f"acupoint_{max_id+20:03d}", "name": "四缝", "pinyin": "Si Feng", "meridian": "经外奇穴", "meridian_id": "extra_point", "location": "在手掌侧，第2-5指近端指间关节中央，左右共8穴", "indications": ["小儿疳积", "百日咳", "食欲不振", "蛔虫病"], "method": "点刺挤出黄白色透明液", "anatomy": "在指间关节囊"},
    {"id": f"acupoint_{max_id+21:03d}", "name": "十宣", "pinyin": "Shi Xuan", "meridian": "经外奇穴", "meridian_id": "extra_point", "location": "在手十指尖端，距指甲游离缘0.1寸，左右共10穴", "indications": ["昏迷", "高热", "癫痫", "咽喉肿痛"], "method": "点刺放血", "anatomy": "在指端神经末梢丰富处"},
    {"id": f"acupoint_{max_id+22:03d}", "name": "八邪", "pinyin": "Ba Xie", "meridian": "经外奇穴", "meridian_id": "extra_point", "location": "在手背侧，第1-5指间指蹼缘后方赤白肉际处，左右共8穴", "indications": ["手背肿痛", "手指麻木", "烦热", "手关节痛"], "method": "斜刺0.5-0.8寸", "anatomy": "在骨间背侧肌中"},

    # 下肢奇穴
    {"id": f"acupoint_{max_id+23:03d}", "name": "鹤顶", "pinyin": "He Ding", "meridian": "经外奇穴", "meridian_id": "extra_point", "location": "在膝上部，髌底中点上方凹陷处", "indications": ["膝关节痛", "鹤膝风", "下肢痿痹"], "method": "直刺0.5-0.8寸", "anatomy": "在股四头肌腱中"},
    {"id": f"acupoint_{max_id+24:03d}", "name": "膝眼", "pinyin": "Xi Yan", "meridian": "经外奇穴", "meridian_id": "extra_point", "location": "在膝关节部，髌韧带两侧凹陷中，内膝眼和外膝眼", "indications": ["膝关节痛", "下肢痿痹", "鹤膝风"], "method": "向膝中斜刺0.5-1寸", "anatomy": "在髌韧带两侧"},
    {"id": f"acupoint_{max_id+25:03d}", "name": "胆囊穴", "pinyin": "Dan Nang Xue", "meridian": "经外奇穴", "meridian_id": "extra_point", "location": "在小腿外侧，阳陵泉穴直下2寸处", "indications": ["胆囊炎", "胆石症", "胆道蛔虫症", "胁痛"], "method": "直刺1-1.5寸", "anatomy": "在腓骨长肌与趾长伸肌中"},
    {"id": f"acupoint_{max_id+26:03d}", "name": "阑尾穴", "pinyin": "Lan Wei Xue", "meridian": "经外奇穴", "meridian_id": "extra_point", "location": "在小腿前外侧，足三里穴直下2寸处", "indications": ["阑尾炎", "足痿痹", "胃痛"], "method": "直刺1-1.5寸", "anatomy": "在胫骨前肌中"},
    {"id": f"acupoint_{max_id+27:03d}", "name": "八风", "pinyin": "Ba Feng", "meridian": "经外奇穴", "meridian_id": "extra_point", "location": "在足背侧，第1-5趾间趾蹼缘后方赤白肉际处，左右共8穴", "indications": ["趾痛", "足跗肿痛", "毒蛇咬伤", "头痛"], "method": "斜刺0.5-0.8寸", "anatomy": "在骨间背侧肌中"},
    {"id": f"acupoint_{max_id+28:03d}", "name": "气端", "pinyin": "Qi Duan", "meridian": "经外奇穴", "meridian_id": "extra_point", "location": "在足十趾尖端，距趾甲游离缘0.1寸", "indications": ["中风急救", "足趾麻木", "脚气", "下肢疼痛"], "method": "点刺放血", "anatomy": "在趾端神经末梢丰富处"},

    # 腹部奇穴
    {"id": f"acupoint_{max_id+29:03d}", "name": "子宫穴", "pinyin": "Zi Gong Xue", "meridian": "经外奇穴", "meridian_id": "extra_point", "location": "在下腹部，脐中下4寸，前正中线旁开3寸", "indications": ["月经不调", "痛经", "不孕", "子宫脱垂"], "method": "直刺0.5-1寸", "anatomy": "在腹直肌中"},
    {"id": f"acupoint_{max_id+30:03d}", "name": "三角灸", "pinyin": "San Jiao Jiu", "meridian": "经外奇穴", "meridian_id": "extra_point", "location": "以患者两口角的长度为一边，作一等边三角形，顶点置脐心，底边呈水平线，两底角处是穴", "indications": ["疝气", "腹痛", "不孕"], "method": "艾炷灸5-7壮", "anatomy": "在腹直肌中"},
]

# 累加ID
current_max = max_id
for p in new_qi_points:
    current_max += 1
    p['id'] = f"acupoint_{current_max:03d}"

all_points = existing + new_qi_points

# 重新编号确保连续
for i, p in enumerate(all_points, 1):
    p['id'] = f"acupoint_{i:03d}"

with open(os.path.join(DATA_DIR, 'acupoints.json'), 'w', encoding='utf-8') as f:
    json.dump(all_points, f, ensure_ascii=False, indent=2)

# 统计分类
from collections import Counter
ms = Counter(p.get('meridian','未知') for p in all_points)
print(f"穴位总数：{len(all_points)}（新增 {len(new_qi_points)} 个奇穴）")
print("\n经络分类分布：")
for m, c in ms.most_common():
    print(f"  {m}: {c}个")
print(f"\n其中十四正经: {sum(c for m,c in ms.items() if m != '经外奇穴')}个")
print(f"经外奇穴: {ms.get('经外奇穴', 0)}个")
