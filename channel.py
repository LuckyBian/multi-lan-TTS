from pydub import AudioSegment
import os

# 设置你要检查的文件夹路径
folder_path = '/aifs4su/data/weizhen/data/hua/cut'

# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    if filename.endswith('.wav'):  # 检查文件扩展名
        file_path = os.path.join(folder_path, filename)
        audio = AudioSegment.from_wav(file_path)

        # 检查音频是否是单声道
        if audio.channels > 1:
            print(f"Converting {filename} to mono.")
            mono_audio = audio.set_channels(1)
            mono_audio.export(file_path, format='wav')  # 覆盖原文件
        else:
            print(f"{filename} is already mono.")
