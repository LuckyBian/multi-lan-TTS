# 打开并读取文件
with open('/home/weizhenbian/vits_all/filelists/train.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 存储没有文字的行的索引
no_text_lines = []

# 遍历每一行，检查格式
for index, line in enumerate(lines):
    parts = line.strip().split('|')
    # 检查是否存在两部分，且第二部分（文字）是否为空
    if len(parts) != 2 or not parts[1]:
        no_text_lines.append(index + 1)  # 将行号添加到列表中，行号从1开始

# 打印结果
if no_text_lines:
    print("以下行没有文字:")
    for line_number in no_text_lines:
        print(f"第 {line_number} 行")
else:
    print("所有行都有文字。")
