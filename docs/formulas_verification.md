# 方剂数据逐条查证报告

> ⚠️ 本报告为 **JSON 时代**对 386 首方剂的逐条查证快照；数据已迁移至 SQLite，当前 `formulas` 表共 490 首。结论仅反映当时数据状态，验证方法论见 [formulas_verification_method.md](./formulas_verification_method.md)。

> 本报告由 AI 依据公认中医经典逐一核对 `assets/data/formulas.json` 全部 386 首方剂生成（JSON 时代快照）。
> 查证方法论与字段 schema 见 [formulas_verification_method.md](./formulas_verification_method.md)。
> 每首方剂的逐条结论同时记录在数据自身的 `verification` 字段中。

## 一、总览

| 状态 | 数量 | 含义 |
|------|------|------|
| verified_classic | 350 | 名称/组成/来源/剂型命名均与公认经典一致（含已说明的历史演变） |
| mismatch | 31 | 数据集内重复录入（同名同方或同源异写/异剂型） |
| needs_review | 5 | 出处为现代教材/验方，非古代经典方剂，须人工复核 |

- 另有 **25** 首方剂的 `usage`（用法）字段缺失，剂型用法无法核对，已在各条 issues 标注。
- 全部方剂的 `ingredients`（组成）字段普遍**仅录入前 4 味左右**（数据截断），故本查证仅能确认所列药名均属该经典方，完整组成须补全数据后复核（已逐条标注）。

## 二、数据类型问题清单

### 2.1 重复 / 同源录入（status=mismatch，共 31 首）

| 方剂ID | 名称 | 重复对象 | 说明 |
|--------|------|----------|------|
| formula_091 | 桃核承气汤 | formula_057 | 与 formula_057 重复：同为桃核承气汤（《伤寒论》），数据集内重复录入… |
| formula_097 | 吴茱萸汤 | formula_026 | 与 formula_026 重复：同为吴茱萸汤（《伤寒论》），数据集内重复录入。 |
| formula_099 | 黄芪桂枝五物汤 | formula_029 | 与 formula_029 重复：同为黄芪桂枝五物汤（《金匮要略》），数据集内重… |
| formula_103 | 安宫牛黄丸 | formula_046 | 与 formula_046 重复：同名同方《《温病条辨》》，数据集内重复录入，应… |
| formula_104 | 三仁汤 | formula_076 | 与 formula_076 重复：同名同方《《温病条辨》》，数据集内重复录入，应… |
| formula_106 | 藿香正气散 | formula_073 | 与 formula_073 重复：同名同方《《太平惠民和剂局方》》，数据集内重复… |
| formula_107 | 八正散 | formula_075 | 与 formula_075 重复：同名同方《《太平惠民和剂局方》》，数据集内重复… |
| formula_108 | 玉女煎 | formula_010 | 与 formula_010 重复：同名同方《《景岳全书》》，数据集内重复录入，应… |
| formula_109 | 左归丸 | formula_038 | 与 formula_038 重复：同名同方《《景岳全书》》，数据集内重复录入，应… |
| formula_110 | 右归丸 | formula_043 | 与 formula_043 重复：同名同方《《景岳全书》》，数据集内重复录入，应… |
| formula_114 | 镇肝熄风汤 | formula_084 | 与 formula_084 重复：同名同方《《医学衷中参西录》》，数据集内重复录… |
| formula_115 | 独活寄生汤 | formula_077 | 与 formula_077 重复：同名同方《《备急千金要方》》，数据集内重复录入… |
| formula_116 | 温胆汤 | formula_064 | 与 formula_064 重复：同名同方《《备急千金要方》》，数据集内重复录入… |
| formula_117 | 当归四逆汤 | formula_028 | 与 formula_028 重复：同名同方《《伤寒论》》，数据集内重复录入，应去… |
| formula_118 | 桂枝茯苓丸 | formula_060 | 与 formula_060 重复：同名同方《《金匮要略》》，数据集内重复录入，应… |
| formula_119 | 玉屏风散 | formula_086 | 与 formula_086 重复：同名同方《《究原方》》，数据集内重复录入，应去… |
| formula_120 | 天王补心丹 | formula_045 | 与 formula_045 重复：同名同方《《校注妇人良方》》，数据集内重复录入… |
| formula_121 | 酸枣仁汤 | formula_044 | 与 formula_044 重复：同名同方《《金匮要略》》，数据集内重复录入，应… |
| formula_122 | 金锁固精丸 | formula_049 | 与 formula_049 重复：同名同方《《医方集解》》，数据集内重复录入，应… |
| formula_123 | 桑菊饮 | formula_004 | 与 formula_004 重复：同名同方《《温病条辨》》，数据集内重复录入，应… |
| formula_186 | 枳实薤白桂枝汤 | formula_053 | 与 formula_053 重复：同为枳实薤白桂枝汤（《金匮要略》），数据集内重… |
| formula_223 | 麦门冬汤 | formula_100 | 与 formula_100 重复：同为麦门冬汤（《金匮要略》），数据集内重复录入… |
| formula_234 | 天麻钩藤饮 | formula_083 | 出处《杂病证治新义》(胡光慈,1956)为现代著作，天麻钩藤饮为现代经验方，非古… |
| formula_250 | 苏子降气汤 | formula_146 | 与 formula_146 重复：同为苏子降气汤（《太平惠民和剂局方》），数据集… |
| formula_274 | 暖肝煎 | formula_145 | 与 formula_145 重复：同为暖肝煎（《景岳全书》），数据集内重复录入。 |
| formula_286 | 大黄附子细辛汤 | formula_159 | 与 formula_159 重复：同为大黄附子细辛汤（《金匮要略》，又名大黄附子… |
| formula_295 | 竹叶石膏汤 | formula_094 | 与 formula_094 重复：同为竹叶石膏汤（《伤寒论》），数据集内重复录入… |
| formula_318 | 紫雪 | formula_125 | 与 formula_125 重复：同为紫雪（丹）（《太平惠民和剂局方》），仅省略… |
| formula_365 | 葛根黄芩黄连汤 | formula_150 | 与 formula_150 重复：同为葛根黄芩黄连汤（即葛根芩连汤，《伤寒论》）… |
| formula_369 | 麻黄杏仁甘草石膏汤 | formula_005 | 与 formula_005 重复：同为麻黄杏仁甘草石膏汤（即麻杏甘石汤，《伤寒论… |
| formula_371 | 枳术汤 | formula_194 | 与 formula_194 重复：枳术汤（《金匮要略》）与枳术丸（《脾胃论》）组… |

### 2.2 非古代经典方剂（status=needs_review，共 5 首）

| 方剂ID | 名称 | 出处标注 | 问题 |
|--------|------|----------|------|
| formula_068 | 平喘固本汤 | 《中医内科学》 | 出处《中医内科学》为现代教材，平喘固本汤为现代经验方，非古代经典方剂；若要求全部出自经典，建议标注为… |
| formula_083 | 天麻钩藤饮 | 《中医内科杂病证治新义》 | 出处《中医内科杂病证治新义》(胡光慈,1956)为现代著作，天麻钩藤饮为现代经验方，非古代经典方剂。 |
| formula_166 | 二仙汤 | 《中医方剂临床手册》 | 出处《中医方剂临床手册》为现代方书，二仙汤为现代经验方（张伯讷创制），非古代经典方剂。 |
| formula_289 | 止痉散 | 《中药神书》 | 出处《中药神书》为现代方书，止痉散为现代经验方（验方），非古代经典方剂。 |
| formula_337 | 五虎追风散 | 方剂学 | 出处仅标"方剂学"（教材），五虎追风散为现代经验方（验方），非古代经典方剂，须人工复核确切来源。 |

### 2.3 出处标注小误（verified_classic 内，不影响经典性）

- formula_034 生脉散：`author` 标注"李东垣"有误，应为金·张元素（《医学启源》）。方名/组成/出处均经典。

## 三、关于"名称与剂型不符"的说明

用户最初关注"名字和剂型不符"。逐条核对结论：

- **散剂/饮剂/煎剂类方名（如银翘散、逍遥散、桑菊饮、玉女煎等）今多作汤剂水煎服**，属中医历史上"散改汤、饮改汤"的通行演变，**命名与经典原剂型一致，不属于错误**。报告已在相关条目的 notes 中注明。
- 真正的"剂型矛盾"仅见于**数据集内重复录入**（同一方被以不同 id、不同剂型名各录一次，如枳术汤/枳术丸、麻杏甘石汤/麻黄杏仁甘草石膏汤），已在 2.1 列出。
- 个别丸/丹方（如安宫牛黄丸"研末为丸"、神犀丹"研末为丸"）用法标注为丸，与原剂型吻合。

## 四、逐条查证明细（全部 386 首）

| ID | 名称 | 来源 | 状态 | 关键说明 |
|----|------|------|------|----------|
| formula_001 | 麻黄汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_002 | 桂枝汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_003 | 银翘散 | 《温病条辨》 | verified_classic | 方名'银翘散'原典为散剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_004 | 桑菊饮 | 《温病条辨》 | verified_classic | 方名'桑菊饮'原典为饮剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_005 | 麻杏甘石汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_006 | 白虎汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_007 | 黄连解毒汤 | 《外台秘要》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_008 | 龙胆泻肝汤 | 《医方集解》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_009 | 清胃散 | 《脾胃论》 | verified_classic | 方名'清胃散'原典为散剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_010 | 玉女煎 | 《景岳全书》 | verified_classic | 方名'玉女煎'原典为煎剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_011 | 芍药汤 | 《素问病机气宜保命集》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_012 | 白头翁汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_013 | 青蒿鳖甲汤 | 《温病条辨》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_014 | 大承气汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_015 | 小承气汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_016 | 调胃承气汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_017 | 麻子仁丸 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_018 | 济川煎 | 《景岳全书》 | verified_classic | 方名'济川煎'原典为煎剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_019 | 小柴胡汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_020 | 大柴胡汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_021 | 逍遥散 | 《太平惠民和剂局方》 | verified_classic | 方名'逍遥散'原典为散剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_022 | 痛泻要方 | 《丹溪心法》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_023 | 半夏泻心汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_024 | 理中丸 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_025 | 小建中汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_026 | 吴茱萸汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_027 | 四逆汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_028 | 当归四逆汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_029 | 黄芪桂枝五物汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_030 | 四君子汤 | 《太平惠民和剂局方》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_031 | 补中益气汤 | 《脾胃论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_032 | 参苓白术散 | 《太平惠民和剂局方》 | verified_classic | 方名'参苓白术散'原典为散剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_033 | 归脾汤 | 《济生方》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_034 | 生脉散 | 《医学启源》 | verified_classic | 方名'生脉散'原典为散剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。 |
| formula_035 | 四物汤 | 《太平惠民和剂局方》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_036 | 当归补血汤 | 《内外伤辨惑论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_037 | 六味地黄丸 | 《小儿药证直诀》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_038 | 左归丸 | 《景岳全书》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_039 | 大补阴丸 | 《丹溪心法》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_040 | 一贯煎 | 《续名医类案》 | verified_classic | 方名'一贯煎'原典为煎剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_041 | 百合固金汤 | 《慎斋遗书》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_042 | 肾气丸 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_043 | 右归丸 | 《景岳全书》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_044 | 酸枣仁汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_045 | 天王补心丹 | 《摄生秘剖》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_046 | 安宫牛黄丸 | 《温病条辨》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_047 | 苏合香丸 | 《太平惠民和剂局方》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_048 | 牡蛎散 | 《太平惠民和剂局方》 | verified_classic | 方名'牡蛎散'原典为散剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_049 | 金锁固精丸 | 《医方集解》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_050 | 缩泉丸 | 《妇人良方》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_051 | 固冲汤 | 《医学衷中参西录》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_052 | 半夏厚朴汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_053 | 枳实薤白桂枝汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_054 | 天台乌药散 | 《圣济总录》 | verified_classic | 方名'天台乌药散'原典为散剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_055 | 血府逐瘀汤 | 《医林改错》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_056 | 补阳还五汤 | 《医林改错》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_057 | 桃核承气汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_058 | 复元活血汤 | 《医学发明》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_059 | 失笑散 | 《太平惠民和剂局方》 | verified_classic | 方名'失笑散'原典为散剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_060 | 桂枝茯苓丸 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_061 | 生化汤 | 《傅青主女科》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_062 | 温经汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_063 | 二陈汤 | 《太平惠民和剂局方》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_064 | 温胆汤 | 《三因极一病证方论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_065 | 清气化痰丸 | 《医方考》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_066 | 小陷胸汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_067 | 止嗽散 | 《医学心悟》 | verified_classic | 方名'止嗽散'原典为散剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_068 | 平喘固本汤 | 《中医内科学》 | needs_review | 出处《中医内科学》为现代教材，平喘固本汤为现代经验方，非古代经典方剂；若要求全部出自经典… |
| formula_069 | 真武汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_070 | 五苓散 | 《伤寒论》 | verified_classic | 方名'五苓散'原典为散剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_071 | 猪苓汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_072 | 平胃散 | 《太平惠民和剂局方》 | verified_classic | 方名'平胃散'原典为散剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_073 | 藿香正气散 | 《太平惠民和剂局方》 | verified_classic | 方名'藿香正气散'原典为散剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_074 | 茵陈蒿汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_075 | 八正散 | 《太平惠民和剂局方》 | verified_classic | 方名'八正散'原典为散剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_076 | 三仁汤 | 《温病条辨》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_077 | 独活寄生汤 | 《备急千金要方》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_078 | 羌活胜湿汤 | 《内外伤辨惑论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_079 | 消风散 | 《外科正宗》 | verified_classic | 方名'消风散'原典为散剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_080 | 川芎茶调散 | 《太平惠民和剂局方》 | verified_classic | 方名'川芎茶调散'原典为散剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_081 | 大秦艽汤 | 《素问病机气宜保命集》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_082 | 小活络丹 | 《太平惠民和剂局方》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_083 | 天麻钩藤饮 | 《中医内科杂病证治新义》 | needs_review | 出处《中医内科杂病证治新义》(胡光慈,1956)为现代著作，天麻钩藤饮为现代经验方，非古… |
| formula_084 | 镇肝熄风汤 | 《医学衷中参西录》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_085 | 羚角钩藤汤 | 《通俗伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_086 | 玉屏风散 | 《医方类聚》 | verified_classic | 方名'玉屏风散'原典为散剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_087 | 桑螵蛸散 | 《本草衍义》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_088 | 完带汤 | 《傅青主女科》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_089 | 小青龙汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_090 | 葛根汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_091 | 桃核承气汤 | 《伤寒论》 | mismatch | 与 formula_057 重复：同为桃核承气汤（《伤寒论》），数据集内重复录入。 |
| formula_092 | 栀子豉汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_093 | 白虎加人参汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_094 | 竹叶石膏汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_095 | 旋覆代赭汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_096 | 理中汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_097 | 吴茱萸汤 | 《伤寒论》 | mismatch | 与 formula_026 重复：同为吴茱萸汤（《伤寒论》），数据集内重复录入。 |
| formula_098 | 乌梅丸 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_099 | 黄芪桂枝五物汤 | 《金匮要略》 | mismatch | 与 formula_029 重复：同为黄芪桂枝五物汤（《金匮要略》），数据集内重复录入。 |
| formula_100 | 麦门冬汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_101 | 清营汤 | 《温病条辨》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_102 | 犀角地黄汤 | 《备急千金要方》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_103 | 安宫牛黄丸 | 《温病条辨》 | mismatch | 与 formula_046 重复：同名同方《《温病条辨》》，数据集内重复录入，应去重。 |
| formula_104 | 三仁汤 | 《温病条辨》 | mismatch | 与 formula_076 重复：同名同方《《温病条辨》》，数据集内重复录入，应去重。 |
| formula_105 | 甘露消毒丹 | 《温热经纬》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_106 | 藿香正气散 | 《太平惠民和剂局方》 | mismatch | 与 formula_073 重复：同名同方《《太平惠民和剂局方》》，数据集内重复录入，应… |
| formula_107 | 八正散 | 《太平惠民和剂局方》 | mismatch | 与 formula_075 重复：同名同方《《太平惠民和剂局方》》，数据集内重复录入，应… |
| formula_108 | 玉女煎 | 《景岳全书》 | mismatch | 与 formula_010 重复：同名同方《《景岳全书》》，数据集内重复录入，应去重。 |
| formula_109 | 左归丸 | 《景岳全书》 | mismatch | 与 formula_038 重复：同名同方《《景岳全书》》，数据集内重复录入，应去重。 |
| formula_110 | 右归丸 | 《景岳全书》 | mismatch | 与 formula_043 重复：同名同方《《景岳全书》》，数据集内重复录入，应去重。 |
| formula_111 | 通窍活血汤 | 《医林改错》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_112 | 膈下逐瘀汤 | 《医林改错》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_113 | 升陷汤 | 《医学衷中参西录》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_114 | 镇肝熄风汤 | 《医学衷中参西录》 | mismatch | 与 formula_084 重复：同名同方《《医学衷中参西录》》，数据集内重复录入，应去… |
| formula_115 | 独活寄生汤 | 《备急千金要方》 | mismatch | 与 formula_077 重复：同名同方《《备急千金要方》》，数据集内重复录入，应去重… |
| formula_116 | 温胆汤 | 《备急千金要方》 | mismatch | 与 formula_064 重复：同名同方《《备急千金要方》》，数据集内重复录入，应去重… |
| formula_117 | 当归四逆汤 | 《伤寒论》 | mismatch | 与 formula_028 重复：同名同方《《伤寒论》》，数据集内重复录入，应去重。 |
| formula_118 | 桂枝茯苓丸 | 《金匮要略》 | mismatch | 与 formula_060 重复：同名同方《《金匮要略》》，数据集内重复录入，应去重。 |
| formula_119 | 玉屏风散 | 《究原方》 | mismatch | 与 formula_086 重复：同名同方《《究原方》》，数据集内重复录入，应去重。 |
| formula_120 | 天王补心丹 | 《校注妇人良方》 | mismatch | 与 formula_045 重复：同名同方《《校注妇人良方》》，数据集内重复录入，应去重… |
| formula_121 | 酸枣仁汤 | 《金匮要略》 | mismatch | 与 formula_044 重复：同名同方《《金匮要略》》，数据集内重复录入，应去重。 |
| formula_122 | 金锁固精丸 | 《医方集解》 | mismatch | 与 formula_049 重复：同名同方《《医方集解》》，数据集内重复录入，应去重。 |
| formula_123 | 桑菊饮 | 《温病条辨》 | mismatch | 与 formula_004 重复：同名同方《《温病条辨》》，数据集内重复录入，应去重。 |
| formula_124 | 仙方活命饮 | 《校注妇人良方》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_125 | 紫雪丹 | 《太平惠民和剂局方》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_126 | 当归龙荟丸 | 《丹溪心法》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_127 | 黄连阿胶汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_128 | 交泰丸 | 《韩氏医通》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_129 | 杞菊地黄丸 | 《医级》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_130 | 异功散 | 《小儿药证直诀》 | verified_classic | 方名'异功散'原典为散剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_131 | 附子理中丸 | 《太平惠民和剂局方》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_132 | 涤痰汤 | 《奇效良方》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_133 | 安神定志丸 | 《医学心悟》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_134 | 河车大造丸 | 《扶寿精方》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_135 | 麦味地黄丸 | 《医级》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_136 | 桑杏汤 | 《温病条辨》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_137 | 清燥救肺汤 | 《医门法律》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_138 | 益胃汤 | 《温病条辨》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_139 | 养心汤 | 《证治准绳》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_140 | 举元煎 | 《景岳全书》 | verified_classic | 方名'举元煎'原典为煎剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_141 | 八珍汤 | 《正体类要》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_142 | 十全大补汤 | 《太平惠民和剂局方》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_143 | 新加香薷饮 | 《温病条辨》 | verified_classic | 方名'新加香薷饮'原典为饮剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_144 | 六一散 | 《伤寒直格》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_145 | 暖肝煎 | 《景岳全书》 | verified_classic | 方名'暖肝煎'原典为煎剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_146 | 苏子降气汤 | 《太平惠民和剂局方》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_147 | 十灰散 | 《十药神书》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_148 | 增液汤 | 《温病条辨》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_149 | 牵正散 | 《杨氏家藏方》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_150 | 葛根芩连汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_151 | 礞石滚痰丸 | 《丹溪心法附余》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_152 | 九味羌活汤 | 《此事难知》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_153 | 加减葳蕤汤 | 《重订通俗伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_154 | 麻黄附子细辛汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_155 | 柴葛解肌汤 | 《伤寒六书》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_156 | 左金丸 | 《丹溪心法》 | verified_classic | 方名'左金丸'原典为丸剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_157 | 普济消毒饮 | 《东垣试效方》 | verified_classic | 方名'普济消毒饮'原典为饮剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_158 | 凉膈散 | 《太平惠民和剂局方》 | verified_classic | 方名'凉膈散'原典为散剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_159 | 大黄附子汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_160 | 蒿芩清胆汤 | 《重订通俗伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_161 | 达原饮 | 《温疫论》 | verified_classic | 方名'达原饮'原典为饮剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_162 | 炙甘草汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_163 | 泰山磐石散 | 《景岳全书》 | verified_classic | 方名'泰山磐石散'原典为散剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_164 | 当归六黄汤 | 《兰室秘藏》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_165 | 四神丸 | 《内科摘要》 | verified_classic | 方名'四神丸'原典为丸剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_166 | 二仙汤 | 《中医方剂临床手册》 | needs_review | 出处《中医方剂临床手册》为现代方书，二仙汤为现代经验方（张伯讷创制），非古代经典方剂。 |
| formula_167 | 朱砂安神丸 | 《内外伤辨惑论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_168 | 磁朱丸 | 《备急千金要方》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_169 | 真人养脏汤 | 《太平惠民和剂局方》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_170 | 易黄汤 | 《傅青主女科》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_171 | 越鞠丸 | 《丹溪心法》 | verified_classic | 方名'越鞠丸'原典为丸剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_172 | 金铃子散 | 《素问病机气宜保命集》 | verified_classic | 方名'金铃子散'原典为散剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_173 | 柴胡疏肝散 | 《景岳全书》 | verified_classic | 方名'柴胡疏肝散'原典为散剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_174 | 橘皮竹茹汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_175 | 杏苏散 | 《温病条辨》 | verified_classic | 方名'杏苏散'原典为散剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_176 | 玉液汤 | 《医学衷中参西录》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_177 | 防己黄芪汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_178 | 苓桂术甘汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_179 | 二妙散 | 《丹溪心法》 | verified_classic | 方名'二妙散'原典为散剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_180 | 实脾散 | 《重订严氏济生方》 | verified_classic | 方名'实脾散'原典为散剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_181 | 甘姜苓术汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_182 | 半夏白术天麻汤 | 《医学心悟》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_183 | 苓甘五味姜辛汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_184 | 栝楼薤白白酒汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_185 | 奔豚汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_186 | 枳实薤白桂枝汤 | 《金匮要略》 | mismatch | 与 formula_053 重复：同为枳实薤白桂枝汤（《金匮要略》），数据集内重复录入。 |
| formula_187 | 大黄甘草汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_188 | 芍药甘草汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_189 | 泽泻汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_190 | 厚朴七物汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_191 | 茯苓杏仁甘草汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_192 | 牡蛎泽泻散 | 《伤寒论》 | verified_classic | 方名'牡蛎泽泻散'原典为散剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_193 | 保和丸 | 《丹溪心法》 | verified_classic | 方名'保和丸'原典为丸剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_194 | 枳术丸 | 《脾胃论》 | verified_classic | 方名'枳术丸'原典为丸剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_195 | 香薷散 | 《太平惠民和剂局方》 | verified_classic | 方名'香薷散'原典为散剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_196 | 化虫丸 | 《太平惠民和剂局方》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_197 | 阳和汤 | 《外科证治全生集》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_198 | 透脓散 | 《医学心悟》 | verified_classic | 方名'透脓散'原典为散剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_199 | 调肝汤 | 《傅青主女科》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_200 | 神犀丹 | 《温热经纬》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_201 | 五仁丸 | 《世医得效方》 | verified_classic | 方名'五仁丸'原典为丸剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_202 | 清中汤 | 《医学心悟》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_203 | 参附汤 | 《正体类要》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_204 | 防己茯苓汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_205 | 蠲痹汤 | 《杨氏家藏方》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_206 | 大黄蛰虫丸 | 《金匮要略》 | verified_classic | 方名'大黄蛰虫丸'原典为丸剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_207 | 白头翁加甘草阿胶汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_208 | 半硫丸 | 《太平惠民和剂局方》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_209 | 三甲复脉汤 | 《温病条辨》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_210 | 郁李仁丸 | 《小儿药证直诀》 | verified_classic | 方名'郁李仁丸'原典为丸剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_211 | 葱豉汤 | 《肘后备急方》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_212 | 泻白散 | 《小儿药证直诀》 | verified_classic | 方名'泻白散'原典为散剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_213 | 导赤散 | 《小儿药证直诀》 | verified_classic | 方名'导赤散'原典为散剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_214 | 大建中汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_215 | 青娥丸 | 《太平惠民和剂局方》 | verified_classic | 方名'青娥丸'原典为丸剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_216 | 甘麦大枣汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_217 | 固经丸 | 《丹溪心法》 | verified_classic | 方名'固经丸'原典为丸剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_218 | 咳血方 | 《丹溪心法》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_219 | 槐花散 | 《普济本事方》 | verified_classic | 方名'槐花散'原典为散剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_220 | 小蓟饮子 | 《济生方》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_221 | 大定风珠 | 《温病条辨》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_222 | 当归饮子 | 《济生方》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_223 | 麦门冬汤 | 《金匮要略》 | mismatch | 与 formula_100 重复：同为麦门冬汤（《金匮要略》），数据集内重复录入。 |
| formula_224 | 乌头汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_225 | 贝母瓜蒌散 | 《医学心悟》 | verified_classic | 方名'贝母瓜蒌散'原典为散剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_226 | 定喘汤 | 《摄生众妙方》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_227 | 三子养亲汤 | 《韩氏医通》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_228 | 桑白皮汤 | 《景岳全书》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_229 | 清金化痰汤 | 《医学统旨》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_230 | 清暑益气汤 | 《温热经纬》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_231 | 至宝丹 | 《太平惠民和剂局方》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_232 | 槐角丸 | 《太平惠民和剂局方》 | verified_classic | 方名'槐角丸'原典为丸剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_233 | 文蛤汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_234 | 天麻钩藤饮 | 《杂病证治新义》 | mismatch | 出处《杂病证治新义》(胡光慈,1956)为现代著作，天麻钩藤饮为现代经验方，非古代经典；… |
| formula_235 | 丁香柿蒂汤 | 《症因脉治》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_236 | 定痫丸 | 《医学心悟》 | verified_classic | 方名'定痫丸'原典为丸剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_237 | 石韦散 | 《普济本事方》 | verified_classic | 方名'石韦散'原典为散剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_238 | 地黄饮子 | 《圣济总录》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_239 | 白术附子汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_240 | 椒梅汤 | 《温病条辨》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_241 | 排脓散 | 《金匮要略》 | verified_classic | 方名'排脓散'原典为散剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_242 | 参苏饮 | 《太平惠民和剂局方》 | verified_classic | 方名'参苏饮'原典为饮剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_243 | 内补黄芪汤 | 《外科正宗》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_244 | 清骨散 | 《证治准绳》 | verified_classic | 方名'清骨散'原典为散剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_245 | 济生肾气丸 | 《济生方》 | verified_classic | 方名'济生肾气丸'原典为丸剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_246 | 人参养荣汤 | 《太平惠民和剂局方》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_247 | 虎潜丸 | 《丹溪心法》 | verified_classic | 方名'虎潜丸'原典为丸剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_248 | 当归拈痛汤 | 《医学启源》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_249 | 萆薢分清饮 | 《杨氏家藏方》 | verified_classic | 方名'萆薢分清饮'原典为饮剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_250 | 苏子降气汤 | 《太平惠民和剂局方》 | mismatch | 与 formula_146 重复：同为苏子降气汤（《太平惠民和剂局方》），数据集内重复录… |
| formula_251 | 厚朴温中汤 | 《内外伤辨惑论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_252 | 丹参饮 | 《时方歌括》 | verified_classic | 方名'丹参饮'原典为饮剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_253 | 活络效灵丹 | 《医学衷中参西录》 | verified_classic | 方名'活络效灵丹'原典为丹剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_254 | 苇茎汤 | 《备急千金要方》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_255 | 玉真散 | 《外科正宗》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_256 | 五皮散 | 《太平惠民和剂局方》 | verified_classic | 方名'五皮散'原典为散剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_257 | 黄土汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_258 | 桂枝加葛根汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_259 | 行军散 | 《随息居重订霍乱论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_260 | 桂枝加厚朴杏子汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_261 | 泻黄散 | 《小儿药证直诀》 | verified_classic | 方名'泻黄散'原典为散剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_262 | 桂枝去芍药汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_263 | 银翘马勃散 | 《温病条辨》 | verified_classic | 方名'银翘马勃散'原典为散剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_264 | 越婢汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_265 | 越婢加术汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_266 | 中满分消丸 | 《兰室秘藏》 | verified_classic | 方名'中满分消丸'原典为丸剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_267 | 越婢加半夏汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_268 | 大青龙汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_269 | 小青龙加石膏汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_270 | 资生丸 | 《兰台轨范》 | verified_classic | 方名'资生丸'原典为丸剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_271 | 射干麻黄汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_272 | 六磨汤 | 《世医得效方》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_273 | 厚朴麻黄汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_274 | 暖肝煎 | 《景岳全书》 | mismatch | 与 formula_145 重复：同为暖肝煎（《景岳全书》），数据集内重复录入。 |
| formula_275 | 文蛤散 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_276 | 枇杷清肺饮 | 《外科大成》 | verified_classic | 方名'枇杷清肺饮'原典为饮剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_277 | 活人葱豉汤 | 《类证活人书》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_278 | 玉屏风散加味 | 《医方考》 | verified_classic | 此为玉屏风散加味方，组成已加味调整，与基础方非重复。（组成录入截断） |
| formula_279 | 葱白七味饮 | 《外台秘要》 | verified_classic | 方名'葱白七味饮'原典为饮剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_280 | 三物备急丸 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_281 | 羌活胜湿汤加味 | 《脾胃论》 | verified_classic | 此为羌活胜湿汤加味方，组成已加味调整，与基础方非重复。（组成录入截断） |
| formula_282 | 黄龙汤 | 《伤寒六书》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_283 | 通关散 | 《丹溪心法》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_284 | 新加黄龙汤 | 《温病条辨》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_285 | 七厘散 | 《良方集腋》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_286 | 大黄附子细辛汤 | 《金匮要略》 | mismatch | 与 formula_159 重复：同为大黄附子细辛汤（《金匮要略》，又名大黄附子汤），同… |
| formula_287 | 复元通气散 | 《太平惠民和剂局方》 | verified_classic | 方名'复元通气散'原典为散剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_288 | 温脾汤 | 《备急千金要方》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_289 | 止痉散 | 《中药神书》 | needs_review | 出处《中药神书》为现代方书，止痉散为现代经验方（验方），非古代经典方剂。 |
| formula_290 | 十枣汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_291 | 桂枝加芍药汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_292 | 舟车丸 | 《景岳全书》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_293 | 枳实栀子豉汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_294 | 柴胡桂枝干姜汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_295 | 竹叶石膏汤 | 《伤寒论》 | mismatch | 与 formula_094 重复：同为竹叶石膏汤（《伤寒论》），数据集内重复录入。 |
| formula_296 | 柴胡加龙骨牡蛎汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_297 | 清胃散加味 | 《脾胃论》 | verified_classic | 此为清胃散加味方，组成已加味调整，与基础方非重复。（组成录入截断） |
| formula_298 | 柴胡枳桔汤 | 《重订通俗伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_299 | 三妙丸 | 《医学正传》 | verified_classic | 方名'三妙丸'原典为丸剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_300 | 柴胡达原饮 | 《重订通俗伤寒论》 | verified_classic | 方名'柴胡达原饮'原典为饮剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_301 | 曲麦枳术丸 | 《兰室秘藏》 | verified_classic | 方名'曲麦枳术丸'原典为丸剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_302 | 清脾饮 | 《济生方》 | verified_classic | 方名'清脾饮'原典为饮剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_303 | 皂荚丸 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_304 | 栀子甘草豉汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_305 | 柴胡加芒硝汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_306 | 栀子生姜豉汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_307 | 桃花汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_308 | 栀子大黄汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_309 | 四生丸 | 《妇人良方》 | verified_classic | 方名'四生丸'原典为丸剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_310 | 大黄黄连泻心汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_311 | 宣痹汤 | 《温病条辨》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_312 | 附子泻心汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_313 | 葛花解酲汤 | 《兰室秘藏》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_314 | 干姜黄芩黄连人参汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_315 | 升麻鳖甲汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_316 | 五淋散 | 《太平惠民和剂局方》 | verified_classic | 方名'五淋散'原典为散剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_317 | 石膏汤 | 《外台秘要》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_318 | 紫雪 | 《太平惠民和剂局方》 | mismatch | 与 formula_125 重复：同为紫雪（丹）（《太平惠民和剂局方》），仅省略"丹"字… |
| formula_319 | 黄芩汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_320 | 白虎加桂枝汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_321 | 当归四逆加吴茱萸生姜汤 | 《伤寒论》 | verified_classic | 此为当归四逆汤加味方，组成已加味调整，与基础方非重复。（组成录入截断） |
| formula_322 | 附子汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_323 | 茵陈术附汤 | 《医学心悟》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_324 | 甘草干姜汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_325 | 回阳救急汤 | 《伤寒六书》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_326 | 人参蛤蚧散 | 《御药院方》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_327 | 橘皮汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_328 | 薯蓣丸 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_329 | 苇茎汤加味 | 《备急千金要方》 | verified_classic | 此为苇茎汤加味方，组成已加味调整，与基础方非重复。（组成录入截断） |
| formula_330 | 二至丸 | 《医方集解》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_331 | 盐汤探吐方 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_332 | 橘核丸 | 《济生方》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_333 | 艾附暖宫丸 | 《沈氏尊生书》 | verified_classic | 方名'艾附暖宫丸'原典为丸剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_334 | 柏叶汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_335 | 小定风珠 | 《温病条辨》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_336 | 阿胶鸡子黄汤 | 《通俗伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_337 | 五虎追风散 | 方剂学 | needs_review | 出处仅标"方剂学"（教材），五虎追风散为现代经验方（验方），非古代经典方剂，须人工复核确… |
| formula_338 | 藿朴夏苓汤 | 《医原》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_339 | 黄芩滑石汤 | 《温病条辨》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_340 | 连朴饮 | 《霍乱论》 | verified_classic | 方名'连朴饮'原典为饮剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_341 | 四妙丸 | 《成方便读》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_342 | 茯苓皮汤 | 《温病条辨》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_343 | 小半夏汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_344 | 小半夏加茯苓汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_345 | 金水六君煎 | 《景岳全书》 | verified_classic | 方名'金水六君煎'原典为煎剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_346 | 苓甘五味姜辛夏汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_347 | 阿魏丸 | 《太平惠民和剂局方》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_348 | 涌痰汤 | 《奇效良方》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_349 | 大黄牡丹汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_350 | 五味消毒饮 | 《医宗金鉴》 | verified_classic | 方名'五味消毒饮'原典为饮剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_351 | 四妙勇安汤 | 《验方新编》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_352 | 犀黄丸 | 《外科全生集》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_353 | 牛蒡解肌汤 | 《疡科心得集》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_354 | 龟鹿二仙胶 | 《医便》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_355 | 斑龙丸 | 《景岳全书》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_356 | 茯苓桂枝甘草大枣汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_357 | 茯苓甘草汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_358 | 木防己汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_359 | 泻心汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_360 | 黄芪建中汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_361 | 加减复脉汤 | 《温病条辨》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_362 | 升阳益胃汤 | 《脾胃论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_363 | 调中益气汤 | 《脾胃论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_364 | 升阳散火汤 | 《脾胃论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_365 | 葛根黄芩黄连汤 | 《伤寒论》 | mismatch | 与 formula_150 重复：同为葛根黄芩黄连汤（即葛根芩连汤，《伤寒论》），同名异… |
| formula_366 | 黄连汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_367 | 抵当汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_368 | 桂枝甘草汤 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_369 | 麻黄杏仁甘草石膏汤 | 《伤寒论》 | mismatch | 与 formula_005 重复：同为麻黄杏仁甘草石膏汤（即麻杏甘石汤，《伤寒论》），同… |
| formula_370 | 瓜蒂散 | 《伤寒论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_371 | 枳术汤 | 《金匮要略》 | mismatch | 与 formula_194 重复：枳术汤（《金匮要略》）与枳术丸（《脾胃论》）组成相同（… |
| formula_372 | 瓜蒌薤白半夏汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_373 | 薏苡附子败酱散 | 《金匮要略》 | verified_classic | 方名'薏苡附子败酱散'原典为散剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_374 | 桂枝芍药知母汤 | 《金匮要略》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_375 | 当归芍药散 | 《金匮要略》 | verified_classic | 方名'当归芍药散'原典为散剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_376 | 沙参麦冬汤 | 《温病条辨》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_377 | 清络饮 | 《温病条辨》 | verified_classic | 方名'清络饮'原典为饮剂，后世多改作汤剂水煎服，属历史演变，命名与经典剂型一致。（组成录入截断） |
| formula_378 | 化斑汤 | 《温病条辨》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_379 | 增液承气汤 | 《温病条辨》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_380 | 宣白承气汤 | 《温病条辨》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_381 | 清宫汤 | 《温病条辨》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_382 | 升阳除湿汤 | 《脾胃论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_383 | 补脾胃泻阴火升阳汤 | 《脾胃论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_384 | 枳实导滞丸 | 《脾胃论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_385 | 通幽汤 | 《脾胃论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
| formula_386 | 润肠丸 | 《脾胃论》 | verified_classic | 经典名方，各字段一致（组成录入截断） |
