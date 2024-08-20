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



## Pre-processing

1. After ASR, different tags are added to different languages. [Cantonese text], {English text}, (Chinese text).
```
python addlabel.py
```

2. Merge and slice the audio into 10s segments by [this](https://github.com/LuckyBian/GPTSOVITS2)


3. Resample the audio to a sampling rate of 22050.

```
python resam.py
```

4. Change the audio to mono.

```
python channel.py
```

5. Denosing

Use the noise reduction method [here](https://github.com/LuckyBian/GPTSOVITS2) to reduce the noise of the audio

6. Organize file paths and text and split into training and validation sets.

```
python getdata.py
python split.py
```

7. Change the data file path in the config file.


## Training Exmaple
```
python train.py -c path/to/json/file -m path/to/model
```

## Inference

```
python infer.py
```

