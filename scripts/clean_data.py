#!/usr/bin/env python3
"""对 zhongyi.db 做安全的数据清洗/增补（只做可派生、不编造内容的改动）：
1) 删除现代映射完全重复记录（mapping_172 == mapping_051）
2) 回填针方 syndrome 标量字段（由 related_syndromes 派生证型名）
3) 对所有双向关系做对称闭包增补（反向链接补全）
用法: python3 scripts/clean_data.py <db路径>   (默认 db/zhongyi.db)
"""
import sqlite3, os, sys

DEFAULT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "db", "zhongyi.db")
DB = sys.argv[1] if len(sys.argv) > 1 else DEFAULT


def main():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    added = 0
    removed = 0

    # ---- 1. 删除完全重复的现代映射 ----
    dup = cur.execute(
        "SELECT id FROM modern_mapping WHERE chinese_term='慢性肾炎' "
        "AND modern_term='慢性肾小球肾炎 (Chronic Glomerulonephritis)' AND related_syndrome='syndrome_074'"
    ).fetchall()
    if len(dup) > 1:
        for d in dup[1:]:
            cur.execute("DELETE FROM modern_mapping WHERE id=?", (d["id"],))
            cur.execute("DELETE FROM modern_mapping_comparison WHERE parent_id=?", (d["id"],))
            removed += 1
            print(f"  删除重复 modern_mapping: {d['id']}")

    # ---- 2. 回填针方 syndrome 标量（派生自 related_syndromes） ----
    sy_name = {r["id"]: r["name"] for r in cur.execute("SELECT id, name FROM syndromes")}
    rows = cur.execute(
        "SELECT id FROM needle_prescriptions WHERE TRIM(syndrome)='' OR syndrome IS NULL"
    ).fetchall()
    filled = 0
    for r in rows:
        rel = cur.execute(
            "SELECT value FROM needle_prescriptions_related_syndromes WHERE parent_id=?",
            (r["id"],),
        ).fetchall()
        if rel:
            names = [sy_name.get(x["value"], "") for x in rel if sy_name.get(x["value"])]
            if names:
                cur.execute(
                    "UPDATE needle_prescriptions SET syndrome=? WHERE id=?",
                    ("、".join(names), r["id"]),
                )
                filled += 1
    print(f"  针方 syndrome 标量回填: {filled} 条")

    # ---- 3. 双向关系对称闭包 ----
    def edges(tbl, fld, vcol):
        d = {}
        for r in cur.execute(f"SELECT parent_id, {vcol} FROM {tbl}_{fld}"):
            if r[vcol]:
                d.setdefault(r["parent_id"], set()).add(r[vcol])
        return d

    def add_edge(tbl, fld, vcol, pid, val):
        nonlocal added
        ex = cur.execute(
            f"SELECT 1 FROM {tbl}_{fld} WHERE parent_id=? AND {vcol}=?", (pid, val)
        ).fetchone()
        if not ex:
            cur.execute(f"INSERT INTO {tbl}_{fld}(parent_id,{vcol}) VALUES(?,?)", (pid, val))
            added += 1

    # (A表, A字段, B表, B字段) 均为 value-list 子表
    PAIRS = [
        ("formulas", "syndrome_ids", "syndromes", "related_formulas"),
        ("formulas", "related_syndromes", "syndromes", "related_formulas"),
        ("formulas", "effect_ids", "effects", "related_formulas"),
        ("medicines", "effect_ids", "effects", "related_medicines"),
        ("effects", "related_medicines", "medicines", "effect_ids"),
        ("effects", "related_formulas", "formulas", "effect_ids"),
        ("effects", "related_syndromes", "syndromes", "related_effects"),
        ("syndromes", "related_effects", "effects", "related_syndromes"),
        ("syndromes", "related_needle", "needle_prescriptions", "related_syndromes"),
        ("syndromes", "related_treatments", "treatments", "related_syndromes"),
        ("needle_prescriptions", "related_syndromes", "syndromes", "related_needle"),
        ("treatments", "related_syndromes", "syndromes", "related_treatments"),
    ]
    for A, af, B, bf in PAIRS:
        a = edges(A, af, "value")
        b = edges(B, bf, "value")
        for aid, bvals in a.items():
            for bv in bvals:
                if aid not in b.get(bv, set()):
                    add_edge(B, bf, "value", bv, aid)
                    b.setdefault(bv, set()).add(aid)
        for bid, avals in b.items():
            for av in avals:
                if bid not in a.get(av, set()):
                    add_edge(A, af, "value", av, bid)
                    a.setdefault(av, set()).add(bid)
    print(f"  双向链接增补(INSERT): {added} 条")

    # 穴位 meridian_id(标量) <-> meridians_related_acupoints(列表)
    acu_mer = {r["id"]: r["meridian_id"] for r in cur.execute("SELECT id, meridian_id FROM acupoints")}
    m_ra = edges("meridians", "related_acupoints", "value")  # meridian -> set(acupoint)
    for mid, acus in m_ra.items():
        for aid in acus:
            if acu_mer.get(aid) != mid:
                cur.execute("UPDATE acupoints SET meridian_id=? WHERE id=?", (mid, aid))
                acu_mer[aid] = mid
    for aid, mid in acu_mer.items():
        if mid and aid not in m_ra.get(mid, set()):
            add_edge("meridians", "related_acupoints", "value", mid, aid)
            m_ra.setdefault(mid, set()).add(aid)
    print(f"  穴位-经络链接修正/增补完成")

    con.commit()
    con.close()
    print(f"\n完成。db={DB}  删除重复 {removed}, 新增链接 {added}, 针方回填 {filled}")


if __name__ == "__main__":
    main()
