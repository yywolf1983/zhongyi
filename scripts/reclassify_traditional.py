#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将三大模块的标注按中医传统体系重新归类（仅改标注，不改条目本身）：

1) 辨证(syndromes)
   - category(大类) = 辨证纲领：八纲辨证 / 脏腑辨证 / 六经辨证 /
     卫气营血辨证 / 三焦辨证 / 气血津液辨证 / 病因辨证(六淫) / 经络辨证
     （合并 六淫辨证→病因辨证、病机辨证→气血津液辨证）
   - classification(子类) = 具体证型：从证型名/病因/病机文本中，按所属纲领
     派生传统细分（脏腑：心肝肾…；六经：太阳/阳明…；卫气营血：卫分/血分…；
     三焦：上/中/下焦；气血津液：气虚/血瘀/痰/湿…；六淫：风/寒/暑/湿/燥/火/食/虫…；
     经络：督脉/任脉/各经…），并保留原有八纲标签（表/里/寒/热/虚/实…）。

2) 方剂(formulas)
   - 规范化大类别名：外科剂→痈疡剂、杂疗剂→其他（其余保持 22 大类传统体系）。

3) 针方(needle_prescriptions)
   - 规范化功效(治法)别名：补阴/补阳/补血→补益；回阳→温里；疏肝→理气；
     清心→清热；急症→开窍。（病证科目内科/妇科…维持原样，由前端按功效维度筛选）

穴位(acupoints) 已按十四经 + 特定穴(井荥输原经合郄络会) 分类，保持不动。
"""
import sqlite3
import sys

DB_PATHS = [
    'db/zhongyi.db',
    'public/zhongyi.db',
    'android/app/src/main/assets/public/zhongyi.db',
]

# ---------- 辨证纲领规范 ----------
CAT_MAP = {
    '六淫辨证': '病因辨证',
    '病机辨证': '气血津液辨证',
}
PRINCIPLES_ORDER = [
    '八纲辨证', '脏腑辨证', '六经辨证', '卫气营血辨证', '三焦辨证',
    '气血津液辨证', '病因辨证', '经络辨证',
]
BA_GANG = {'表证', '里证', '寒证', '热证', '虚证', '实证', '阴证', '阳证',
           '半表半里证', '寒热错杂', '虚实夹杂'}

# 脏腑（按长度降序，避免「心」误命中「心包」等）
ZANGFU = [('心包', '心包'), ('三焦', '三焦'), ('小肠', '小肠'), ('大肠', '大肠'),
          ('膀胱', '膀胱'), ('胃', '胃'), ('胆', '胆'), ('心', '心'), ('肝', '肝'),
          ('脾', '脾'), ('肺', '肺'), ('肾', '肾'), ('胞宫', '胞宫')]
LIUJING = ['太阳', '阳明', '少阳', '太阴', '少阴', '厥阴']
WEI = ['卫分', '气分', '营分', '血分']
SANJIAO = ['上焦', '中焦', '下焦']
QIXUE = [('气虚', '气虚'), ('气滞', '气滞'), ('气逆', '气逆'), ('气陷', '气陷'),
         ('血虚', '血虚'), ('血瘀', '血瘀'), ('血热', '血热'), ('血寒', '血寒'),
         ('阴虚', '阴虚'), ('阳虚', '阳虚'), ('阴阳两虚', '阴阳两虚'),
         ('津亏', '津亏'), ('痰', '痰浊'), ('饮', '水饮'), ('水停', '水停'),
         ('水肿', '水停'), ('湿', '湿邪'), ('燥', '燥邪'), ('瘀', '血瘀')]
LIUYIN = [('风寒', '风邪'), ('风热', '风邪'), ('风湿', '风邪'), ('风', '风邪'),
          ('寒', '寒邪'), ('暑', '暑邪'), ('湿', '湿邪'), ('燥', '燥邪'),
          ('火', '火热'), ('热', '火热'), ('毒', '毒邪'), ('食积', '食滞'),
          ('食', '食滞'), ('虫', '虫积'), ('郁', '气郁'), ('怒', '气郁'),
          ('劳', '劳倦')]
JINGLUO = ['督脉', '任脉', '冲脉', '带脉', '阴维脉', '阳维脉', '阴跷脉', '阳跷脉',
           '肺经', '心经', '心包经', '小肠经', '大肠经', '三焦经', '胃经',
           '脾经', '肝经', '胆经', '肾经', '膀胱经']


def extract(text, terms):
    """terms: list of (keyword, label)；返回命中的 label 列表（保序去重）"""
    out = []
    seen = set()
    for kw, label in terms:
        if kw in text and label not in seen:
            out.append(label)
            seen.add(label)
    return out


def derive_classification(old_cat, old_class, name, etiology, pathogenesis):
    text = ' '.join([name or '', etiology or '', pathogenesis or ''])
    new = []
    seen = set()
    # 保留原有八纲标签
    for c in old_class:
        if c in BA_GANG and c not in seen:
            new.append(c)
            seen.add(c)
    for raw in old_cat:
        principle = CAT_MAP.get(raw, raw)
        if principle == '脏腑辨证':
            for kw, label in ZANGFU:
                if kw in text and label not in seen:
                    new.append(label); seen.add(label)
        elif principle == '六经辨证':
            for kw in LIUJING:
                if kw in text and kw not in seen:
                    new.append(kw); seen.add(kw)
        elif principle == '卫气营血辨证':
            for kw in WEI:
                if kw in text and kw not in seen:
                    new.append(kw); seen.add(kw)
        elif principle == '三焦辨证':
            for kw in SANJIAO:
                if kw in text and kw not in seen:
                    new.append(kw); seen.add(kw)
        elif principle == '气血津液辨证':
            for kw, label in QIXUE:
                if kw in text and label not in seen:
                    new.append(label); seen.add(label)
        elif principle == '病因辨证':
            for kw, label in LIUYIN:
                if kw in text and label not in seen:
                    new.append(label); seen.add(label)
        elif principle == '经络辨证':
            for kw in JINGLUO:
                if kw in text and kw not in seen:
                    new.append(kw); seen.add(kw)
    return new


def reclassify_syndromes(con):
    cur = con.cursor()
    cur.execute('SELECT id, name, etiology, pathogenesis FROM syndromes')
    rows = cur.fetchall()
    cur.execute('SELECT parent_id, value FROM syndromes_category')
    old_cat = {}
    for pid, v in cur.fetchall():
        old_cat.setdefault(pid, []).append(v)
    cur.execute('SELECT parent_id, value FROM syndromes_classification')
    old_class = {}
    for pid, v in cur.fetchall():
        old_class.setdefault(pid, []).append(v)

    for sid, name, eti, path in rows:
        raw_cat = old_cat.get(sid, [])
        raw_class = old_class.get(sid, [])
        # 规范纲领
        new_cat = []
        seen = set()
        for r in raw_cat:
            p = CAT_MAP.get(r, r)
            if p not in seen:
                new_cat.append(p); seen.add(p)
        new_class = derive_classification(raw_cat, raw_class, name, eti, path)
        # 写回
        cur.execute('DELETE FROM syndromes_category WHERE parent_id=?', (sid,))
        cur.execute('DELETE FROM syndromes_classification WHERE parent_id=?', (sid,))
        for v in new_cat:
            cur.execute('INSERT INTO syndromes_category (parent_id, value) VALUES (?,?)', (sid, v))
        for v in new_class:
            cur.execute('INSERT INTO syndromes_classification (parent_id, value) VALUES (?,?)', (sid, v))
    con.commit()
    return len(rows)


def normalize_formulas(con):
    cur = con.cursor()
    MAP = {'外科剂': '痈疡剂', '杂疗剂': '其他'}
    cur.execute('SELECT id, category FROM formulas')
    changed = 0
    for fid, cat in cur.fetchall():
        if cat in MAP:
            cur.execute('UPDATE formulas SET category=? WHERE id=?', (MAP[cat], fid))
            changed += 1
    con.commit()
    return changed


def normalize_needle(con):
    cur = con.cursor()
    MAP = {'补阴': '补益', '补阳': '补益', '补血': '补益', '回阳': '温里',
           '疏肝': '理气', '清心': '清热', '急症': '开窍'}
    cur.execute('SELECT id, category FROM needle_prescriptions')
    changed = 0
    for nid, cat in cur.fetchall():
        if cat in MAP:
            cur.execute('UPDATE needle_prescriptions SET category=? WHERE id=?', (MAP[cat], nid))
            changed += 1
    con.commit()
    return changed


def main():
    for path in DB_PATHS:
        try:
            con = sqlite3.connect(path)
        except sqlite3.Error as e:
            print(f'[跳过] 无法打开 {path}: {e}')
            continue
        n_syn = reclassify_syndromes(con)
        n_f = normalize_formulas(con)
        n_n = normalize_needle(con)
        con.close()
        print(f'[完成] {path}  辨证:{n_syn}  方剂规范化:{n_f}  针方规范化:{n_n}')


if __name__ == '__main__':
    main()
