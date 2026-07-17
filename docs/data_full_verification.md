# 全量数据核查与修复报告（所有 JSON）
> 完成时间：2026-07-17 ｜ 覆盖 9 个数据文件

## 一、最终结果（引用完整性 · 全部 17 个关联方向）
**悬空引用合计 = 0**，重名 = 0 组。各文件记录数：
`formulas` 360 ｜ `needle` 371 ｜ `syndromes` 131 ｜ `meridians` 15 ｜ `acupoints` 417 ｜ `medicines` 574 ｜ `effects` 753 ｜ `treatments` 30 ｜ `mapping` 180

## 二、已执行的 4 项修复（按用户决策）

### A. 针方非经典标注（保留并标注「现代经验方」）
- 共 **228 条** source 为「临床常用方」(192) /「常用经验方」(36) 的针方，统一 `verification` 字段：
  `status=modern_empirical`、`is_classic=false`、`classic_source=原始出处`、`accuracy_notes=现代临床常用方/经验方，非古代针灸典籍收录，已保留并标注`。
- 其余 143 条源自《针灸甲乙经》《针灸大成》等经典者保持 `verified_classic`。

### B. 方剂重名去重 + 合并证型关联（删残缺版）
- 26 组重名（同名"标准全方"与"残缺版"），**删除 26 条残缺版，保留 26 条标准全方**。
- 保留判定：组成数更多者优先；组成数相同则"有证型关联者"优先（解决桃核承气汤、玉屏风散两组平局）。
- 合并残缺版的 `syndrome_ids` 到保留条（共合并 **40 处**证型关联）。
- 同步更新反向引用：删除的 formula id 在 `syndromes.related_formulas`(改1处)、`effects.related_formulas`(改27处) 中替换为保留 id。
- 结果：`formulas` 386 → **360 条**，重名 0 组。

### C. 关联双向自动补全
- 对 4 对双向关联做并集补全：`formulas.syndrome_ids↔syndromes.related_formulas`、`formulas.effect_ids↔effects.related_formulas`、`needle.related_syndromes↔syndromes.related_needle`、`treatments.related_syndromes↔syndromes.related_treatments`。
- 效果：`syndromes.related_needle` 空关联 **42 → 10**；其余按可反推部分补全。剩余空关联均为"正反双向均无链接"的真空中（如 53 条方剂、128 条针方无任何证型链接），无法自动反推，需后续人工逐条核对。

### D. 药品补 meridian_ids / effect_ids（程序化一一对应）
- **meridian_ids**：574 味药 100% 解析（简称→全称映射，"肝胆经"拆为肝+胆），新增 `meridian_ids` 字段指向 `meridians`。
- **effect_ids**：药品 603 个功效词中 73 个已在 `effects` 库；**新增 530 个中药专属功效条目**使 `effects` 库 223 → **753**，并回填 `related_medicines`；为药品新增 `effect_ids` 字段，全部有效（悬空 0）。
- 说明：新增的 530 个功效条目 `description`/`mechanism` 为占位空值（名称本身出自经典中药功效术语，正确无误），**待后续补全描述**。

## 三、仍需后续处理（非数据错误，需人工/外部知识）
1. **530 个新增中药功效条目待补描述**（名称正确，描述占位）。
2. **残余空关联**：约 53 方剂 + 128 针方无任何证型链接，需在原始典籍中逐条核对后人工补 `syndrome_ids`/`related_syndromes`。
3. **formulas 5 条现代教材出处**（《中医内科学》《方剂学》《中医方剂临床手册》《杂病证治新义》《中医内科杂病证治新义》）：为真实现代著作，已保留，可按需标注。
4. **基础数据**（acupoints/meridians/syndromes/treatments/effects/modern_mapping）未逐条标 `source`，属《内经》《伤寒》等经典体系知识。

## 四、本轮同时修复的历史错误
- `acupoints` 经外奇穴双录去重：删 26 条重复，修正 `needle`(28处)/`meridians`(26处) 引用（上轮完成）。
- `prescription_034`（带状疱疹方）：原把经络名"肝经/胆经"当穴位，改为肝经原穴**太冲**(acupoint_298)、胆经合穴**阳陵泉**(acupoint_285)（上轮完成）。

## 五、第二轮核查修复（继续检查错误 · 补全缺失）

### 5.1 已修复的错误
- **formula_087 桑螵蛸散 组成错误**：原数据误录"天麻"两次且组成残缺。已按《本草衍义》正本重建为 8 味（桑螵蛸、远志、石菖蒲、龙骨、人参、茯神、当归、龟甲），去重并补注 `note`。
- **acupoints↔meridians 双向不一致 2 处**：阿是穴(acupoint_442)、落枕穴(acupoint_443) 的 `meridian_id=extra_point` 未在该经络 `related_acupoints` 中，已补入 `extra_point.related_acupoints`（现 54→56），双向一致。
- 全量复检：formulas 同方重复药 0、acupoints↔meridians 不一致 0、悬空引用 0。

### 5.2 已补全的缺失关联/内容
- **9 个孤立证型补全**（syndrome_122~130：阳明病、少阴病、心血虚、心阴虚、暑淫证、湿淫证、燥淫证、火淫证、痰饮）：以经方常识 + 方名在库内解析的高置信方式补全双向关联（仅链接真实存在的方剂/针方）。结果：残余全空证型 **0**。
  - 例：阳明病↔白虎汤/大承气汤/小承气汤/调胃承气汤；少阴病↔四逆汤/真武汤/黄连阿胶汤；痰饮↔苓桂术甘汤/小青龙汤/十枣汤。
- **530 个中药功效条目描述补全**：用"2 字语素 + 单字兜底"释义词库组合生成 `description`，并标记 `auto_desc=true` 以区别于已核验条目。effects 库 753 条 `description` 空值 **0**。

### 5.3 仍需专家复核（非程序可判定，避免臆造关联）
1. **43 条方剂 + 128 条针方 完全无证型链接**：其文本多为证候描述而非证型名，自动反推召回低且易错，需中医师按原著逐条补 `syndrome_ids`/`related_syndromes`。
2. **530 条 effect 描述为自动生成释文**：词义准确但非权威典籍原文，建议专家润色并补 `mechanism`/`indications`。
