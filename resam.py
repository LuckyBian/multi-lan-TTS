import os
import glob
from pydub import AudioSegment

def resample_wav_files(input_folder, target_sr=22050):
    # 获取文件夹中的所有wav文件
    wav_files = glob.glob(os.path.join(input_folder, '*.wav'))
    
    # 遍历每一个wav文件
    for wav_file in wav_files:
        try:
            # 加载音频文件
            audio = AudioSegment.from_wav(wav_file)
            
            # 打印音频文件的基本信息
            print(f'Processing file: {wav_file}')
            print(f'Original sample rate: {audio.frame_rate}')
            print(f'Duration: {len(audio) / 1000} seconds')
            
            # 进行重采样
            audio_resampled = audio.set_frame_rate(target_sr)
            
            # 获取文件名和扩展名
            base_name = os.path.basename(wav_file)
            name, ext = os.path.splitext(base_name)
            
            # 构造新的文件路径
            new_file_path = os.path.join(input_folder, f'{name}{ext}')
            
            # 保存重采样后的音频文件，格式为s16
            audio_resampled.export(new_file_path, format="wav", codec="pcm_s16le")
            
            print(f'File {wav_file} resampled and saved as {new_file_path}')
        except Exception as e:
            print(f'Error processing file {wav_file}: {e}')

# 使用示例
input_folder = '/aifs4su/data/weizhen/data/emo/wavs'  # 替换为你的文件夹路径
resample_wav_files(input_folder)
