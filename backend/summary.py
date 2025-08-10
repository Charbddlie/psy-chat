import os
import json
import csv

header = [
    "ID",
    "昵称",
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
    "根据知识前测是否纳入(是/否)",
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
    "总交互时长(秒)",
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
    "知识后测_score",
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
    "延迟测试_1",
    "延迟测试_2",
    "延迟测试_3",
    "延迟测试_4",
    "延迟测试_5",
    "延迟测试_score",
    "保持率",
]

def get_gender_code(gender):
    if gender == "男":
        return 0
    elif gender == "女":
        return 1
    else:
        return "null"

def safe_list(l, n):
    # 保证长度为n，不足补空
    if l is None:
        l = []
    return [(str(x) if x is not None else "null") for x in l] + ["null"] * (n - len(l))

def avg(lst):
    vals = [x for x in lst if isinstance(x, (int, float))]
    if not vals:
        return "null"
    return round(sum(vals) / len(vals), 2)

def avg_by_index(lst, idxs):
    vals = []
    for i in idxs:
        if i < len(lst) and lst[i] is not None:
            vals.append(lst[i])
    if not vals:
        return "null"
    return round(sum(vals) / len(vals), 2)

def sum_chat_time(chat_path):
    # 计算总交互时长(秒)
    import datetime
    times = []
    if not os.path.exists(chat_path): return "null"
    with open(chat_path, encoding="utf-8") as f:
        lines = f.readlines()
    for line in lines[1:]:
        parts = line.strip().split('\t')
        if len(parts) >= 3:
            times.append(parts[2])
    if len(times) < 2:
        return "null"
    try:
        t0 = datetime.datetime.strptime(times[0], "%Y-%m-%dT%H:%M:%S.%f")
        t1 = datetime.datetime.strptime(times[-1], "%Y-%m-%dT%H:%M:%S.%f")
        return int((t1 - t0).total_seconds())
    except Exception:
        return "null"

# 2. 遍历所有样本文件夹
rows = []
for d in os.listdir("./log"):
    dir_name = d
    d = os.path.join("./log", d)
    if not os.path.isdir(d) or '_' not in d:
        continue
    info_path = os.path.join(d, "info.json")
    pre_path = os.path.join(d, "pre.json")
    chat_path = os.path.join(d, "chat.tsv")
    post_path = os.path.join(d, "post.json")
    final_path = os.path.join(d, "final.json")

    # 读取info.json
    if not os.path.exists(info_path):
        info = {}
    else:
        with open(info_path, encoding="utf-8") as f:
            info = json.load(f)
    # 读取pre.json
    if not os.path.exists(pre_path):
        pre = {}
    else:
        with open(pre_path, encoding="utf-8") as f:
            pre = json.load(f)
    # 读取post.json
    if not os.path.exists(post_path):
        post = {}
    else:
        with open(post_path, encoding="utf-8") as f:
            post = json.load(f)
    # 读取final.json
    if not os.path.exists(final_path):
        final = {}
    else:
        with open(final_path, encoding="utf-8") as f:
            final = json.load(f)
    if not (info or pre or post or final): continue

    # 1. 基本信息
    row = []
    row.append(dir_name.split('_')[-1])
    row.append('_'.join(dir_name.split('_')[:-1]))
    # row.append(info.get("user_name", "null"))
    # row.append(info.get("user_id", "null"))
    row.append(info.get("gender", "null"))
    row.append(info.get("age", "null"))
    row.append(info.get("major", "null"))
    row.append(info.get("grade", "null"))
    row.append(info.get("aiAttitude", "null"))

    # 2. 知识前测
    pre_knowledge = pre.get("knowledgePayload", {}).get("answers", [])
    row += safe_list(pre_knowledge, 8)

    # 3. 根据知识前测是否纳入
    excluded = pre.get("excluded", True)
    if excluded:
        row.append("否")
    else:
        row.append("是")
    # if excluded:
    #     row.append("否")
    #     rows.append(row)
    #     continue
    # else:
    #     row.append("是")
    
    # 4. ai经验
    ai_exp = pre.get("aiScalePayload", {}).get("answers", [])
    row += safe_list(ai_exp, 4)
    ai_exp_avg = avg([x for x in ai_exp if isinstance(x, (int, float))])
    row.append(ai_exp_avg)

    # 5. 前测情绪
    pre_affect = pre.get("affectPayload", {}).get("answers", [])
    row += safe_list(pre_affect, 8)
    pre_pos = pre.get("affectPayload", {}).get("positive", "null")
    pre_neg = pre.get("affectPayload", {}).get("negative", "null")
    row.append(pre_pos)
    row.append(pre_neg)

    # 6. 总交互时长
    row.append(sum_chat_time(chat_path))

    # 7. 后测情绪
    post_affect = post.get("affect", {}).get("answers", [])
    row += safe_list(post_affect, 8)
    post_pos = post.get("affect", {}).get("positive", "null")
    post_neg = post.get("affect", {}).get("negative", "null")
    row.append(post_pos)
    row.append(post_neg)

    # 8. 拟人化感知(主观感受 subjective)
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
    godspeed1 = godspeed[0] if len(godspeed) > 0 and godspeed[0] is not None else "null"
    godspeed2 = godspeed[1] if len(godspeed) > 1 and godspeed[1] is not None else "null"
    godspeed3 = godspeed[2] if len(godspeed) > 2 and godspeed[2] is not None else "null"
    godspeed4 = godspeed[3] if len(godspeed) > 3 and godspeed[3] is not None else "null"
    godspeed5 = godspeed[4] if len(godspeed) > 4 and godspeed[4] is not None else "null"
    godspeed6 = godspeed[5] if len(godspeed) > 5 and godspeed[5] is not None else "null"
    row.append(avg_by_index(godspeed, [0,1]))  # Godspeed_1+Godspeed_1/2
    row.append(avg_by_index(godspeed, [2,3]))  # Godspeed_3+Godspeed_4/2
    row.append(avg_by_index(godspeed, [4,5]))  # Godspeed_5+Godspeed_6/2

    # 12. 知识后测
    post_knowledge = post.get("knowledge", {}).get("answers", [])
    row += safe_list(post_knowledge, 12)
    post_score = post.get("knowledge", {}).get("knowledgeScore", "null")
    row.append(post_score)

    # 13. NASA
    cognitive = post.get("cognitive", {}).get("answers", [])
    row += safe_list(cognitive, 3)
    row.append(post.get("cognitive", {}).get("cogLoad", "null"))

    # 14. 使用意愿
    system = post.get("system", {}).get("answers", [])
    row += safe_list(system[:3], 3)
    row.append(post.get("system", {}).get("willingness", "null"))

    # 学习满意度
    row += safe_list(system[3:6] if len(system) >= 6 else [], 3)
    row.append(post.get("system", {}).get("satisfaction", "null"))

    # 15. 社会临场感
    social = post.get("social", {}).get("answers", [])
    row += safe_list(social, 6)
    row.append(post.get("social", {}).get("socialPresence", "null"))

    # 16. 技术信任
    technical = post.get("technical", {}).get("answers", [])
    row += safe_list(technical, 5)
    row.append(post.get("technical", {}).get("techTrust", "null"))

    # 17. 延迟测试
    final_knowledge = final.get("knowledgePayload", {}).get("answers", [])
    row += safe_list(final_knowledge, 5)
    final_score = final.get("knowledgePayload", {}).get("score", "null")
    row.append(final_score)
    try:
        row.append(f"{round((float(final_score)/float(post_score))*100, 2)}%")
    except:
        row.append("null")

    rows.append(row)

# 对rows中的所有数字，如果小数位数大于2，都保留两位小数
for i, row in enumerate(rows):
    new_row = []
    for val in row:
        # 检查是否为float或可以转为float且不是None
        if isinstance(val, float):
            # 只对有小数点的float保留两位
            new_row.append(round(val, 2))
        elif isinstance(val, int):
            new_row.append(val)
        else:
            # 尝试转为float再判断
            try:
                fval = float(val)
                # 如果原始字符串是数字且有小数点
                if '.' in str(val):
                    # 保留两位小数
                    fval_2 = round(fval, 2)
                    # 保持字符串类型与原类型一致
                    if isinstance(val, str):
                        # 去除多余的.0
                        if fval_2 == int(fval_2):
                            new_row.append(str(int(fval_2)))
                        else:
                            new_row.append(f"{fval_2:.2f}")
                    else:
                        new_row.append(fval_2)
                else:
                    new_row.append(val)
            except Exception:
                new_row.append(val)
    rows[i] = new_row

# 找到“根据知识前测是否纳入(是/否)”在header中的idx
include_idx = None
for i, h in enumerate(header):
    if "根据知识前测是否纳入" in h:
        include_idx = i
        break

if include_idx is not None:
    # 写入仅纳入（是）的样本的TSV (UTF-8)
    skip_count_include_utf8 = 0
    with open("log/summary_include_utf8.tsv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(header)
        for row in rows:
            if len(row) > include_idx and row[include_idx] == "是":
                try:
                    writer.writerow(row)
                except Exception as e:
                    print(f"[INCLUDE-UTF8] 跳过行: {row}，错误: {e}")
                    skip_count_include_utf8 += 1
    print(f"[INCLUDE-UTF8] 共跳过 {skip_count_include_utf8} 行")

    # 写入仅纳入（是）的样本的TSV (GBK)
    skip_count_include_gbk = 0
    with open("log/summary_include_gbk.tsv", "w", encoding="gbk", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(header)
        for row in rows:
            if len(row) > include_idx and row[include_idx] == "是":
                try:
                    writer.writerow(row)
                except Exception as e:
                    print(f"[INCLUDE-GBK] 跳过行: {row}，错误: {e}")
                    skip_count_include_gbk += 1
    print(f"[INCLUDE-GBK] 共跳过 {skip_count_include_gbk} 行")

# 3. 写入TSV (UTF-8)
skip_count_utf8 = 0
with open("log/summary_utf8.tsv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow(header)
    for row in rows:
        try:
            writer.writerow(row)
        except Exception as e:
            print(f"[UTF-8] 跳过行: {row}，错误: {e}")
            skip_count_utf8 += 1
print(f"[UTF-8] 共跳过 {skip_count_utf8} 行")

# 3. 写入TSV (GBK)
skip_count_gbk = 0
with open("log/summary_gbk.tsv", "w", encoding="gbk", newline="") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow(header)
    for row in rows:
        try:
            writer.writerow(row)
        except Exception as e:
            print(f"[GBK] 跳过行: {row}，错误: {e}")
            skip_count_gbk += 1
print(f"[GBK] 共跳过 {skip_count_gbk} 行")

