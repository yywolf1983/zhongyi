#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""中医知识库数据质量检查脚本（准确性 / 完整性 / 可靠性）。

覆盖：
  - 完整性：核心字段空值统计
  - 准确性：枚举列取值分布（category/subcategory 等是否落在已知字典内）
  - 可靠性：重复记录、孤儿引用（外键指向不存在的主键）、跨表一致性
结果打印到 stdout，供人工复核。
"""
import sqlite3
import os

DB = os.path.join(os.path.dirname(__file__), "..", "db", "zhongyi.db")
DB = os.path.abspath(DB)


def q(cur, sql, args=()):
    cur.execute(sql, args)
    return cur.fetchall()


def report(title):
    print("\n" + "=" * 64)
    print(title)
    print("=" * 64)


def main():
    con = sqlite3.connect(DB)
    cur = con.cursor()

    # ---------- 统计各表行数 ----------
    report("一、各表规模")
    tables = [r[0] for r in q(cur, "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
    for t in tables:
        n = q(cur, f"SELECT COUNT(*) FROM {t}")[0][0]
        print(f"  {t:40s} {n:>6}")

    # ---------- 二、完整性：核心字段空值 ----------
    report("二、完整性 · 核心字段空值率")
    core_fields = {
        "medicines": ["name", "pinyin", "category", "flavor", "nature", "meridian", "indications", "functions", "dosage", "usage", "contraindications", "classic"],
        "formulas": ["name", "pinyin", "category", "source", "ingredients", "usage", "modern_applications", "note"],
        "syndromes": ["name", "pinyin", "pathogenesis", "etiology"],
        "needle_prescriptions": ["name", "pinyin", "category", "syndrome", "method", "acupoints", "source"],
        "acupoints": ["name", "pinyin", "meridian", "location", "method"],
        "meridians": ["name", "pinyin", "category", "yin_yang", "element", "path", "subcategory"],
        "treatments": ["name", "category", "principle", "modern_explanation"],
        "effects": ["name", "description", "auto_desc"],
        "modern_mapping": ["chinese_term", "modern_term", "category"],
    }
    for t, fields in core_fields.items():
        print(f"\n  [{t}]")
        n = q(cur, f"SELECT COUNT(*) FROM {t}")[0][0]
        for f in fields:
            # 注意：needle_prescriptions 没有 acupoints 列，acupoints 来自子表
            if f == "acupoints":
                cnt = q(cur, f"SELECT COUNT(*) FROM {t}_acupoints WHERE parent_id IN (SELECT id FROM {t})")[0][0]
                empty = (n - q(cur, f"SELECT COUNT(DISTINCT parent_id) FROM {t}_acupoints")[0][0])
                print(f"    acupoints(子表关联)   缺失 {empty}/{n}")
                continue
            try:
                empty = q(cur, f"SELECT COUNT(*) FROM {t} WHERE {f} IS NULL OR TRIM({f})=''")[0][0]
            except sqlite3.OperationalError:
                continue
            flag = "  <-- 注意" if (empty > 0 and f not in ("functions", "modern_applications", "note", "contraindications", "classic", "dosage", "usage")) else ""
            print(f"    {f:22s} 空 {empty:>5}/{n}{flag}")

    # ---------- 三、准确性：枚举分布 ----------
    report("三、准确性 · 关键枚举列分布")
    enum_cols = {
        "medicines": ["category", "subcategory", "nature"],
        "formulas": ["category", "subcategory"],
        "needle_prescriptions": ["category", "subcategory"],
        "meridians": ["category", "yin_yang", "element"],
        "treatments": ["category"],
        "modern_mapping": ["category"],
    }
    for t, cols in enum_cols.items():
        for c in cols:
            rows = q(cur, f"SELECT {c}, COUNT(*) FROM {t} GROUP BY {c} ORDER BY 2 DESC")
            print(f"\n  {t}.{c}:")
            for val, cnt in rows:
                print(f"    {str(val):28s} {cnt}")

    # ---------- 四、可靠性：重复记录 ----------
    report("四、可靠性 · 重复名称记录")
    name_tables = {
        "medicines": "name", "formulas": "name", "syndromes": "name",
        "needle_prescriptions": "name", "acupoints": "name", "meridians": "name",
        "treatments": "name", "effects": "name", "modern_mapping": "chinese_term",
    }
    for t, col in name_tables.items():
        dups = q(cur, f"SELECT {col}, COUNT(*) c FROM {t} GROUP BY {col} HAVING c>1")
        if dups:
            print(f"\n  [{t}] 重复:")
            for name, c in dups:
                print(f"    {name}  x{c}")

    # ---------- 五、可靠性：孤儿引用（外键完整性） ----------
    report("五、可靠性 · 孤儿引用检查")
    # 1) formulas_ingredients.medicine_id 应存在于 medicines.id
    orphans = q(cur, "SELECT COUNT(*) FROM formulas_ingredients fi LEFT JOIN medicines m ON fi.medicine_id=m.id WHERE m.id IS NULL")[0][0]
    print(f"  formulas_ingredients.medicine_id 孤儿: {orphans}")
    # 2) needle_prescriptions_acupoints.acupoint_id 应存在于 acupoints.id
    orphans = q(cur, "SELECT COUNT(*) FROM needle_prescriptions_acupoints npa LEFT JOIN acupoints a ON npa.acupoint_id=a.id WHERE a.id IS NULL")[0][0]
    print(f"  needle_prescriptions_acupoints.acupoint_id 孤儿: {orphans}")
    # 3) acupoints.meridian_id 应存在于 meridians.id
    orphans = q(cur, "SELECT COUNT(*) FROM acupoints a LEFT JOIN meridians m ON a.meridian_id=m.id WHERE a.meridian_id IS NOT NULL AND m.id IS NULL")[0][0]
    print(f"  acupoints.meridian_id 孤儿: {orphans}")
    # 4) syndromes_category/syndromes_classification 的 parent_id 应存在于 syndromes.id
    for child in ["syndromes_category", "syndromes_classification", "syndromes_comparison", "syndromes_diagnosis_points", "syndromes_modern_medicine", "syndromes_related_effects", "syndromes_related_formulas", "syndromes_related_needle", "syndromes_related_treatments", "syndromes_classic_excerpts"]:
        orphans = q(cur, f"SELECT COUNT(*) FROM {child} c LEFT JOIN syndromes s ON c.parent_id=s.id WHERE s.id IS NULL")[0][0]
        print(f"  {child}.parent_id 孤儿: {orphans}")
    # 5) medicines 子表 parent 孤儿
    for child in ["medicines_classic_excerpts", "medicines_contraindications", "medicines_effect_ids", "medicines_effects", "medicines_flavor", "medicines_indications", "medicines_meridian", "medicines_meridian_ids", "medicines_usage"]:
        orphans = q(cur, f"SELECT COUNT(*) FROM {child} c LEFT JOIN medicines m ON c.parent_id=m.id WHERE m.id IS NULL")[0][0]
        print(f"  {child}.parent_id 孤儿: {orphans}")

    # ---------- 六、可靠性：引用一致性 / 子表关联缺失 ----------
    report("六、可靠性 · 主表缺少必要子表关联")
    # 方剂是否都有组成
    no_ing = q(cur, "SELECT COUNT(*) FROM formulas f WHERE f.id NOT IN (SELECT parent_id FROM formulas_ingredients)")[0][0]
    print(f"  formulas 无组成(ingredients): {no_ing}")
    # 方剂是否都有功效
    no_eff = q(cur, "SELECT COUNT(*) FROM formulas f WHERE f.id NOT IN (SELECT parent_id FROM formulas_effects)")[0][0]
    print(f"  formulas 无功效(effects): {no_eff}")
    # 方剂是否都有主治
    no_ind = q(cur, "SELECT COUNT(*) FROM formulas f WHERE f.id NOT IN (SELECT parent_id FROM formulas_indications)")[0][0]
    print(f"  formulas 无主治(indications): {no_ind}")
    # 中药是否都有功效
    no_eff = q(cur, "SELECT COUNT(*) FROM medicines m WHERE m.id NOT IN (SELECT parent_id FROM medicines_effects)")[0][0]
    print(f"  medicines 无功效(effects): {no_eff}")
    # 中药是否都有归经
    no_mer = q(cur, "SELECT COUNT(*) FROM medicines m WHERE m.id NOT IN (SELECT parent_id FROM medicines_meridian)")[0][0]
    print(f"  medicines 无归经(meridian): {no_mer}")
    # 针方是否都有穴位
    no_acu = q(cur, "SELECT COUNT(*) FROM needle_prescriptions n WHERE n.id NOT IN (SELECT parent_id FROM needle_prescriptions_acupoints)")[0][0]
    print(f"  needle_prescriptions 无穴位(acupoints): {no_acu}")
    # 穴位是否都有定位
    no_loc = q(cur, "SELECT COUNT(*) FROM acupoints WHERE location IS NULL OR TRIM(location)=''")[0][0]
    print(f"  acupoints 无定位(location): {no_loc}")

    # ---------- 七、可靠性：medicine.category 是否在分类字典内 ----------
    report("七、准确性 · medicines.category 与已知分类字典对比")
    known = {"补虚药","解表药","清热药","泻下药","祛风湿药","化湿药","利水渗湿药","温里药","理气药","消食药","驱虫药","止血药","活血化瘀药","化痰止咳平喘药","安神药","平肝息风药","开窍药","补益药","收涩药","涌吐药","攻毒杀虫止痒药","拔毒化腐生肌药"}
    rows = q(cur, "SELECT DISTINCT category FROM medicines")
    for (cat,) in rows:
        mark = "" if cat in known else "  <-- 不在字典内"
        print(f"    {cat}{mark}")

    # ---------- 八、配方 ingredients 的 name 与 quantity 完整性 ----------
    report("八、完整性 · formulas_ingredients 明细")
    bad = q(cur, "SELECT COUNT(*) FROM formulas_ingredients WHERE name IS NULL OR TRIM(name)='' OR quantity IS NULL OR TRIM(quantity)=''")[0][0]
    print(f"  ingredients 缺药名或用量: {bad}")
    orphan_med = q(cur, "SELECT fi.parent_id, fi.name FROM formulas_ingredients fi LEFT JOIN medicines m ON fi.medicine_id=m.id WHERE m.id IS NULL AND fi.name NOT IN (SELECT name FROM medicines)")
    # 找出 medicine_id 为空但 name 也查不到中药的
    really_orphan = q(cur, "SELECT COUNT(*) FROM formulas_ingredients fi WHERE (fi.medicine_id IS NULL OR fi.medicine_id='') AND fi.name NOT IN (SELECT name FROM medicines)")[0][0]
    print(f"  ingredients 关联不到中药(既无 id 也 name 不在 medicines): {really_orphan}")

    con.close()
    print("\n检查完成。")


if __name__ == "__main__":
    main()
