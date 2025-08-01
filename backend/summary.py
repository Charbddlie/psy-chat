import os
import json
import csv

header = [
    "ID",
    "性别(男=0,女=1)",
    "年龄",
    "专业",
    "年级",
    "对AI的态度",
    "知识前测_1",
    "知识前测_2",
    "知识前测_3",
    "知识前测_4",
    "知识前测_5",
    "知识前测_6",
    "知识前测_7",
    "知识前测_8",
    "根据知识前测是否纳入(是/否）",
    "ai经验_1",
    "ai经验_2",
    "ai经验_3",
    "ai经验_4",
    "ai经验_average",
    "前测情绪状态_1",
    "前测情绪状态_2",
    "前测情绪状态_3",
    "前测情绪状态_4",
    "前测情绪状态_5",
    "前测情绪状态_6",
    "前测情绪状态_7",
    "前测情绪状态_8",
    "前测正性情绪_average",
    "前测负性情绪_average",
    "总交互时长",
    "后测情绪状态_1",
    "后测情绪状态_2",
    "后测情绪状态_3",
    "后测情绪状态_4",
    "后测情绪状态_5",
    "后测情绪状态_6",
    "后测情绪状态_7",
    "后测情绪状态_8",
    "后测正性情绪_average",
    "后测负性情绪_average",
    "拟人化感知_1",
    "拟人化感知_2",
    "拟人化感知_3",
    "拟人化感知_4",
    "拟人化感知_5",
    "拟人化感知_6",
    "拟人化感知_7",
    "拟人化感知_8",
    "拟人化感知_9",
    "拟人化感知_10",
    "拟人化感知_11",
    "拟人化感知_12",
    "拟人化感知_13",
    "拟人化感知_14",
    "拟人化感知_15",
    "拟人化感知_16",
    "拟人化感知_17",
    "拟人化感知_18",
    "社交性_average(拟人化感知_1+2+3+4)",
    "生命性_average(拟人化感知_5+6+7+8)",
    "能动性_average(拟人化感知_9+10+11)",
    "教学支持_average(拟人化感知_12+13+14)",
    "干扰性_average(拟人化感知_15+16+17+18)",
    "Godspeed_1",
    "Godspeed_2",
    "Godspeed_3",
    "Godspeed_4",
    "Godspeed_5",
    "Godspeed_6",
    "拟人化 = (Godspeed_1+ Godspeed_1) / 2",
    "生命性 = (Godspeed_3+ Godspeed_4) / 2",
    "喜爱度 = (Godspeed_5+ Godspeed_6) / 2",
    "知识后测_1",
    "知识后测_2",
    "知识后测_3",
    "知识后测_4",
    "知识后测_5",
    "知识后测_6",
    "知识后测_7",
    "知识后测_8",
    "知识后测_9",
    "知识后测_10",
    "知识后测_11",
    "知识后测_12",
    "total score",
    "NASA_1",
    "NASA_2",
    "NASA_3",
    "NASA_average",
    "使用意愿_1",
    "使用意愿_2",
    "使用意愿_3",
    "使用意愿_average",
    "学习满意度_4",
    "学习满意度_5",
    "学习满意度_6",
    "学习满意度_average",
    "社会临场感_1",
    "社会临场感_2",
    "社会临场感_3",
    "社会临场感_4",
    "社会临场感_5",
    "社会临场感_6",
    "社会临场感_average",
    "技术信任_1",
    "技术信任_2",
    "技术信任_3",
    "技术信任_4",
    "技术信任_5",
    # "技术信任_6",
    # "技术信任_7",
    "技术信任_average",
]

def get_gender_code(gender):
    if gender == "男":
        return 0
    elif gender == "女":
        return 1
    else:
        return ""

def safe_list(l, n):
    # 保证长度为n，不足补空
    if l is None:
        l = []
    return [(str(x) if x is not None else "") for x in l] + [""] * (n - len(l))

def avg(lst):
    vals = [x for x in lst if isinstance(x, (int, float))]
    if not vals:
        return ""
    return round(sum(vals) / len(vals), 2)

def avg_by_index(lst, idxs):
    vals = []
    for i in idxs:
        if i < len(lst) and lst[i] is not None:
            vals.append(lst[i])
    if not vals:
        return ""
    return round(sum(vals) / len(vals), 2)

def sum_chat_time(chat_path):
    # 计算总交互时长(秒）
    import datetime
    times = []
    with open(chat_path, encoding="utf-8") as f:
        lines = f.readlines()
    for line in lines[1:]:
        parts = line.strip().split('\t')
        if len(parts) >= 3:
            times.append(parts[2])
    if len(times) < 2:
        return ""
    try:
        t0 = datetime.datetime.strptime(times[0], "%Y-%m-%d %H:%M:%S.%f")
        t1 = datetime.datetime.strptime(times[-1], "%Y-%m-%d %H:%M:%S.%f")
        return int((t1 - t0).total_seconds())
    except Exception:
        return ""

# 2. 遍历所有样本文件夹
rows = []
for d in os.listdir("log"):
    if not os.path.isdir(d) or d.startswith("."):
        continue
    info_path = os.path.join(d, "info.json")
    pre_path = os.path.join(d, "pre.json")
    chat_path = os.path.join(d, "chat.tsv")
    post_path = os.path.join(d, "post.json")
    # if not (os.path.exists(info_path) and os.path.exists(pre_path) and os.path.exists(chat_path) and os.path.exists(post_path)):
    #     continue

    # 读取info.json
    with open(info_path, encoding="utf-8") as f:
        info = json.load(f)
    # 读取pre.json
    with open(pre_path, encoding="utf-8") as f:
        pre = json.load(f)
    # 读取post.json
    with open(post_path, encoding="utf-8") as f:
        post = json.load(f)

    # 1. 基本信息
    row = []
    row.append(info.get("userId", ""))
    row.append(info.get("gender", ""))
    row.append(info.get("age", ""))
    row.append(info.get("major", ""))
    row.append(info.get("grade", ""))
    row.append(info.get("aiAttitude", ""))

    # 2. 知识前测
    pre_knowledge = pre.get("knowledgePayload", {}).get("answers", [])
    row += safe_list(pre_knowledge, 8)

    # 3. 根据知识前测是否纳入
    excluded = pre.get("excluded", False)
    row.append("否" if not excluded else "是")

    # 4. ai经验
    ai_exp = pre.get("aiScalePayload", {}).get("answers", [])
    row += safe_list(ai_exp, 4)
    ai_exp_avg = avg([x for x in ai_exp if isinstance(x, (int, float))])
    row.append(ai_exp_avg)

    # 5. 前测情绪
    pre_affect = pre.get("affectPayload", {}).get("answers", [])
    row += safe_list(pre_affect, 8)
    pre_pos = pre.get("affectPayload", {}).get("positive", "")
    pre_neg = pre.get("affectPayload", {}).get("negative", "")
    row.append(pre_pos)
    row.append(pre_neg)

    # 6. 总交互时长
    row.append(sum_chat_time(chat_path))

    # 7. 后测情绪
    post_affect = post.get("affect", {}).get("answers", [])
    row += safe_list(post_affect, 8)
    post_pos = post.get("affect", {}).get("positive", "")
    post_neg = post.get("affect", {}).get("negative", "")
    row.append(post_pos)
    row.append(post_neg)

    # 8. 拟人化感知(主观感受 subjective）
    subj = post.get("subjective", {}).get("answers", [])
    row += safe_list(subj, 18)
    # 9. 各类主观感受平均分
    # 社交性: 1-4, 生命性: 5-8, 能动性: 9-11, 教学支持: 12-14, 干扰性: 15-18
    subj_num = [x if isinstance(x, (int, float)) else None for x in subj]
    row.append(avg_by_index(subj_num, [0,1,2,3]))
    row.append(avg_by_index(subj_num, [4,5,6,7]))
    row.append(avg_by_index(subj_num, [8,9,10]))
    row.append(avg_by_index(subj_num, [11,12,13]))
    row.append(avg_by_index(subj_num, [14,15,16,17]))

    # 10. Godspeed量表
    godspeed = post.get("godSpeed", {}).get("answers", [])
    row += safe_list(godspeed, 6)
    # 11. Godspeed三类平均
    godspeed1 = godspeed[0] if len(godspeed) > 0 and godspeed[0] is not None else ""
    godspeed2 = godspeed[1] if len(godspeed) > 1 and godspeed[1] is not None else ""
    godspeed3 = godspeed[2] if len(godspeed) > 2 and godspeed[2] is not None else ""
    godspeed4 = godspeed[3] if len(godspeed) > 3 and godspeed[3] is not None else ""
    godspeed5 = godspeed[4] if len(godspeed) > 4 and godspeed[4] is not None else ""
    godspeed6 = godspeed[5] if len(godspeed) > 5 and godspeed[5] is not None else ""
    row.append(avg_by_index(godspeed, [0,1]))  # Godspeed_1+Godspeed_1/2
    row.append(avg_by_index(godspeed, [2,3]))  # Godspeed_3+Godspeed_4/2
    row.append(avg_by_index(godspeed, [4,5]))  # Godspeed_5+Godspeed_6/2

    # 12. 知识后测
    post_knowledge = post.get("knowledge", {}).get("answers", [])
    row += safe_list(post_knowledge, 12)
    row.append(post.get("knowledge", {}).get("knowledgeScore", ""))

    # 13. NASA
    cognitive = post.get("cognitive", {}).get("answers", [])
    row += safe_list(cognitive, 3)
    row.append(post.get("cognitive", {}).get("cogLoad", ""))

    # 14. 使用意愿
    system = post.get("system", {}).get("answers", [])
    row += safe_list(system[:3], 3)
    row.append(post.get("system", {}).get("willingness", ""))

    # 学习满意度
    row += safe_list(system[3:6] if len(system) >= 6 else [], 3)
    row.append(post.get("system", {}).get("satisfaction", ""))

    # 15. 社会临场感
    social = post.get("social", {}).get("answers", [])
    row += safe_list(social, 6)
    row.append(post.get("social", {}).get("socialPresence", ""))

    # 16. 技术信任
    technical = post.get("technical", {}).get("answers", [])
    row += safe_list(technical, 5)
    row.append(post.get("technical", {}).get("techTrust", ""))

    rows.append(row)

# 3. 写入TSV
with open("log/summary_utf8.tsv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow(header)
    for row in rows:
        writer.writerow(row)

# 3. 写入TSV
with open("log/summary_gbk.tsv", "w", encoding="gbk", newline="") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow(header)
    for row in rows:
        writer.writerow(row)

