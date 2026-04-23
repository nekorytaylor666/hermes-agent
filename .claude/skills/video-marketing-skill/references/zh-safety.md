# Seedance 2.0 — ZH Safety Vocabulary

Chinese prompt safety rules for passing platform content filters. Critical for any ZH generation.

## Hard Blocks — These Words Cause Rejection

These character sequences must NOT appear in ZH output:

| ID | Blocked | Replacement | Notes |
|----|---------|-------------|-------|
| H1 | 血 / 流血 | Remove entirely | No substitution (红色液体 also fails). Exception: 血红色 as color adjective is safe |
| H2 | 杀 / 击毙 | 倒下 / 瘫倒 / 失去行动力 | Exception: 杀青 (film "wrap") is safe |
| H3 | 自杀 / 自残 | Remove entirely | Reframe as visual state description |
| H4 | 毒品 / 吸毒 | Remove entirely | |
| H5 | 非法 / 违法 | Remove | Describe spaces through architecture, not legality |
| H6 | 裸露 | 外露 or structural description | Even 裸露管道 (exposed pipes) triggers NSFW. Write 管道沿天花板延伸 instead |
| H7 | 骚乱 / 骚动 | 出现动静 / 气氛变化 | Politically sensitive |

## Context Poisoning — Safe Words That Cluster Dangerously

These words are each safe alone, but **3+ appearing together** signals "underground fight ring" or "illegal gathering":

**Danger set:** 地下, 围, 圈, 圆形, 拳, 击打, 密集人群, 大叫, 打击, 混乱, 搏击, 赌

| ID | Pattern | Replacement |
|----|---------|-------------|
| C1 | 地下 + crowd words | Remove 地下. Use 低矮空间 / 低层空间. Describe through architecture (低矮混凝土空间) |
| C2 | 围成圈/围成圆形/围成一圈/人群围 | **ALWAYS replace.** Use 四周人影密布 / 模糊观众层层叠叠 / 周围站满了人 |
| C3 | 拳 / 拳头 / 握拳 in tense crowd | Replace. 握拳 → 手指紧握 / 紧握的拳. 拳头击打 → 手指稳步挥出 |
| C4 | 大叫 / 高呼 / 打击 in tense crowd | 大声说出 / 同时发出声 / 声音响起 |
| C5 | 沮丧/悲丧 + 大叫/叫 | Separate them. Face only: 面部表情夹杂复杂情. No vocal outburst + negative emotion combo |

## Post-Gen Triggers (Strict/Rewrite modes)

| ID | Pattern | Replacement |
|----|---------|-------------|
| P1 | 反抗 | Remove entirely |
| P2 | 瞪目凝视 | 注视 / 凝视 / 目光平视 |
| P3 | English weapon nouns in ZH text | Translate AND genericize: 远程装置 / 射击装置 / 发射装置 |
| P4 | 侮辱 / 辱骂 | 言辞尖锐 / 语言施压 |
| P5 | 怪物 (as person-label) | Remove. (怪物 as literal creature is safe) |
| P6 | 人 + 加速 + impact surface | Remove 加速 → 向下移动 |
| P7 | 猛烈 + person-on-person | 剧烈 / 大幅度. (猛烈 for vehicles/environment is safe) |
| P8 | 尖叫 / 嘶吼 | 大幅张嘴 / 高强度发声 |
| P9 | 杀/死 in description | 走着瞧吧 or 别逼我. **NEVER use:** 这不会到此为止 / 你不会有好结果 / 你会后悔的 — all blocked |
| P10 | Negation with trigger (没有血 / 没有暴力) | Remove entire negation phrase |
| P11 | No cinematic framing | Add camera/lens/lighting anchor at start |

## Confirmed Safe Terms — Never Replace

- 血红色 (blood-red as color)
- 杀青 (film wrap)
- 怪物 as literal creature
- 环绕 alone (without 反抗)
- 对抗 in sports context
- Vehicle verbs: 追逐 / 飘逸 / 碰撞 / 漂移 / 摩擦
- Environment: 爆炸 / 坍塌 / 死亡 / 打击 / 腐蚀 / 毁灭
- Emotion: 愤怒 / 嫉妒 / 愤怒 / 悲伤
- Combat verbs (SOFT mode): 击打 / 缠绕 / 踢 / 砍 / 劈

## Safe Dialogue Alternatives

Only two confirmed-safe threat alternatives:
- ✅ 走着瞧吧 (wait and see)
- ✅ 别逼我 (don't push me)

All others tested are blocked or unstable. Do not invent new alternatives.

## Micro-Expressions — Physics Not Emotion

| Don't Write | Write Instead |
|-------------|--------------|
| looks angry | jaw clenched, nostrils flared, rapid breathing |
| crying | moisture on cheeks, uneven breathing |
| screaming | mouth wide open, tendons visible in neck |
| terrified | eyes widened, body pulled back, shallow breathing |
| disgusted | leans back quickly with widened eyes |
| threatening | leans forward, jaw tight, eyes narrowed |
