import os

def add_parentheses_to_files(folder_path):
    # 获取文件夹中所有txt文件的文件名
    file_names = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    
    for file_name in file_names:
        file_path = os.path.join(folder_path, file_name)
        
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 在内容前后加上括号
        new_content = '{'+ content + '}'
        
        # 将新的内容写回文件
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)

# 指定txt文件所在的文件夹路径
folder_path = '/aifs4su/data/weizhen/data/zh-en-yue/en/en-text'

# 调用函数处理文件夹中的所有txt文件
add_parentheses_to_files(folder_path)
