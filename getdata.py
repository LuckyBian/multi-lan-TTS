import os

def pair_files_and_save(audio_folder, text_folder, output_path):
    # 确保输出文件夹存在
    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))
        
    # 打开输出文件
    with open(output_path, 'w', encoding='utf-8') as output_file:
        # 遍历音频文件夹中的所有文件
        for audio_file in os.listdir(audio_folder):
            if audio_file.endswith('.wav'):
                # 构造文本文件的文件名
                text_file = audio_file[:-4] + '.txt'
                # 检查对应的文本文件是否存在
                if text_file in os.listdir(text_folder):
                    # 构造完整路径
                    audio_path = os.path.join(audio_folder, audio_file)
                    text_path = os.path.join(text_folder, text_file)
                    # 读取文本内容
                    with open(text_path, 'r', encoding='utf-8') as file:
                        text_content = file.read().strip()  # 去除可能的首尾空白字符
                    # 写入到输出文件，音频路径和文本内容
                    output_file.write(f'{audio_path}|{text_content}\n')

# 使用示例
audio_folder_path = '/aifs4su/data/weizhen/data/zh-en-yue/all/wavs'  # 音频文件夹路径
text_folder_path = '/aifs4su/data/weizhen/data/zh-en-yue/all/text'    # 文本文件夹路径
output_file_path = '/home/weizhenbian/vits_all/filelists/all.txt' # 输出文件路径

pair_files_and_save(audio_folder_path, text_folder_path, output_file_path)
