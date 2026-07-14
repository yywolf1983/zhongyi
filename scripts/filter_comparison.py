#!/usr/bin/env python3
"""
过滤中西医对照数据：
只保留「症状」和「病因/病机」相关的对比维度
删除治疗、药理、分类、体征等非目标维度
"""

import json
import os

data_dir = os.path.join(os.path.dirname(__file__), '..', 'assets', 'data')

# 保留的 aspect 关键词 — 只要 症状 + 病因/病机
KEEP_ASPECTS = {'症状', '核心症状', '病因', '病理', '病理机制', '病理意义', '机制', '病机'}


def filter_comparison(comparison_list):
    """过滤 comparison 数组，只保留 症状 和 病因/病机 维度"""
    if not comparison_list:
        return []
    return [c for c in comparison_list if c.get('aspect', '') in KEEP_ASPECTS]


# ---- modern_mapping.json ----
with open(os.path.join(data_dir, 'modern_mapping.json'), 'r', encoding='utf-8') as f:
    mappings = json.load(f)

for m in mappings:
    m['comparison'] = filter_comparison(m.get('comparison', []))

# 删除完全没有 comparison 的条目
mappings = [m for m in mappings if m.get('comparison') and len(m['comparison']) > 0]

with open(os.path.join(data_dir, 'modern_mapping.json'), 'w', encoding='utf-8') as f:
    json.dump(mappings, f, ensure_ascii=False, indent=2)

print(f'modern_mapping.json: {len(mappings)} 条（只含症状/病因病机对照）')


# ---- syndromes.json ----
with open(os.path.join(data_dir, 'syndromes.json'), 'r', encoding='utf-8') as f:
    syndromes = json.load(f)

kept_count = 0
for s in syndromes:
    orig = s.get('comparison', [])
    s['comparison'] = filter_comparison(orig)
    if s['comparison']:
        kept_count += 1

with open(os.path.join(data_dir, 'syndromes.json'), 'w', encoding='utf-8') as f:
    json.dump(syndromes, f, ensure_ascii=False, indent=2)

print(f'syndromes.json: {len(syndromes)} 条，{kept_count} 条有症状/病因病机对照')

# 统计
all_aspects = set()
for m in mappings:
    for c in m.get('comparison', []):
        all_aspects.add(c['aspect'])
for s in syndromes:
    for c in s.get('comparison', []):
        all_aspects.add(c['aspect'])

print(f'保留的对比维度: {sorted(all_aspects)}')
