# Multi-Lan TTS
This is a TTS based on VITS, which can support Chinese, English and Cantonese. It can achieve mixed output of Chinese, English and Cantonese.

## Create Env

```
conda create -n mulan-tts python=3.8
conda activate mulan-tts
```

## Install packages

```
pip install -r requirements.txt
python env.py
```

## Dataset

Find the Chinese, English and Cantonese corpora of the same speaker and convert the speech into text (using asr in [this](https://github.com/LuckyBian/GPTSOVITS2)). Finally, put the speech and text into two folders. The name of the speech and the corresponding text must be the same.

If you can't find the same person speaking multiple languages, you can use [this](https://github.com/Grace9994/CoMoSVC) to convert voices.



## Pre-requisites


## Training Exmaple
```
python train.py -c path/to/json/file -m model
```

## Inference

```
python infer.py
```

