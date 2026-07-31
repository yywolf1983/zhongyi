#!/usr/bin/env python3
"""为 24 首缺 beginner_note 的方剂生成【方解】(通俗讲解)，完全复用现有组成(role)+主治(source)，不杜撰。
dry-run 预览；--apply 写入。"""
import sqlite3, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(ROOT, "db", "zhongyi.db")
con = sqlite3.connect(DB); con.row_factory = sqlite3.Row; cur = con.cursor()
APPLY = "--apply" in sys.argv

rows = cur.execute("SELECT id,name,source FROM formulas WHERE beginner_note IS NULL OR TRIM(beginner_note)=''").fetchall()
for f in rows:
    fid = f["id"]
    ings = cur.execute("SELECT name,quantity,role FROM formulas_ingredients WHERE parent_id=? ORDER BY rowid", (fid,)).fetchall()
    inds = cur.execute("SELECT value FROM formulas_indications WHERE parent_id=?", (fid,)).fetchall()
    # 按 role 分组
    groups = {}
    for i in ings:
        groups.setdefault(i["role"] or "未标", []).append(i["name"])
    parts = []
    for role in ["君","臣","佐","使","未标"]:
        if role in groups:
            parts.append(f"{role}：{'、'.join(groups[role])}")
    comp = "；".join(parts) if parts else "、".join(i["name"] for i in ings)
    ind = "；".join(v["value"] for v in inds) if inds else ""
    src = f["source"] or "佚名"
    src_disp = src if (src.startswith("《") and src.endswith("》")) else f"《{src}》"
    note = f"【方解】本方出自{src_disp}。由{comp}组成。"
    if ind:
        note += f"主治{ind}。"
    note += "诸药配伍，共奏其效。"
    print(f"\n=== {f['name']} (id={fid}) ===")
    print(note)
    if APPLY:
        cur.execute("UPDATE formulas SET beginner_note=? WHERE id=?", (note, fid))
if APPLY:
    con.commit(); print("\n已写入。")
else:
    print(f"\n(dry-run) 共 {len(rows)} 条；加 --apply 写入。")
con.close()
