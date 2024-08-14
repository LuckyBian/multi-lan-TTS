import matplotlib.pyplot as plt
import IPython.display as ipd
import re
import os
import json
import math
import torch
from torch import nn
from torch.nn import functional as F
from torch.utils.data import DataLoader

import commons
import utils
from data_utils import TextAudioLoader, TextAudioCollate, TextAudioSpeakerLoader, TextAudioSpeakerCollate
from models import SynthesizerTrn
from text.symbols import symbols
from text import text_to_sequence

from scipy.io.wavfile import write

def get_text(text, hps):

    # 定义正则表达式匹配括号及其内容
    pattern = r'\(.*?\)|\[.*?\]|\{.*?\}'
    matches = re.findall(pattern, text)
    
    sequence = []

    # 打印所有匹配的括号及其内容
    for i, match in enumerate(matches):
        print(match)
        sequence = sequence + text_to_sequence(match)

    #text_norm = text_to_sequence(text)
    text_norm = sequence
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = torch.LongTensor(text_norm)
    return text_norm

hps = utils.get_hparams_from_file("/home/weizhenbian/vits_two/configs/cantonese_base.json")
net_g = SynthesizerTrn(
    len(symbols),
    hps.data.filter_length // 2 + 1,
    hps.train.segment_size // hps.data.hop_length,
    **hps.model).cuda()
_ = net_g.eval()

_ = utils.load_checkpoint("/home/weizhenbian/vits_all/model/G_271000.pth", net_g, None)

stn_tst = get_text("(这是一句普通话或者广东话)[这是一句普通话或者广东话]", hps)

with torch.no_grad():
    x_tst = stn_tst.cuda().unsqueeze(0)
    x_tst_lengths = torch.LongTensor([stn_tst.size(0)]).cuda()
    audio = net_g.infer(x_tst, x_tst_lengths, noise_scale=.667, noise_scale_w=0.8, length_scale=1)[0][0,0].data.cpu().float().numpy()

# Save audio to file instead of playing it in IPython
audio_path = "/home/weizhenbian/vits_two/output/out.wav"
write(audio_path, hps.data.sampling_rate, audio)
print(f"Audio saved to {audio_path}")
