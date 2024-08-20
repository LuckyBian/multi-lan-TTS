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

## Pre-requisites


## Training Exmaple
```
python train.py -c path/to/json/file -m model
```

## Inference

```
python infer.py
```

