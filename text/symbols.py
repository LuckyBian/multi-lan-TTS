import sys
sys.path.append('/home/weizhenbian/vits_all')

# 填充符号和粤语拼音的声母、韵母
from text import cmudicts
_pad = "_"

punctuation = ['.', '!', '?',',','~','$','，','。','？','！','：','-',' ','\'',';','；','(',')','@']  # 标点符号列表

pu_symbols = punctuation + ["SP", "SP2", "SP3", "UNK"]

c = ['b', 'p', 'm', 'f', 'd', 't', 'n', 'l', 'g', 'k', 'ng', 'h', 'gw', 'kw', 'w', 'z', 'c', 's', 'j']

v = ['aa', 'aai', 'aau', 'aam', 'aan', 'aang', 'aap', 'aat', 'aak', 'ai', 'au', 'am', 'an', 'ang',
     'ap', 'at', 'ak', 'e', 'ei', 'eng', 'ek', 'oe', 'oeng', 'oek', 'eoi', 'eon', 'eot', 'o', 'oi',
     'ou', 'on', 'ong', 'ot', 'ok', 'i', 'iu', 'im', 'in', 'ing', 'ip', 'it', 'ik', 'yu', 'yun', 'yut',
     'u', 'ui', 'un', 'ung', 'ut', 'uk', 'm', 'ng']
tones = ['1', '2', '3', '4', '5', '6']


c2 = [
    "AA",
    "EE",
    "OO",
    "b",
    "c",
    "ch",
    "d",
    "f",
    "g",
    "h",
    "j",
    "k",
    "l",
    "m",
    "n",
    "p",
    "q",
    "r",
    "s",
    "sh",
    "t",
    "w",
    "x",
    "y",
    "z",
    "zh",
]
v2 = [
    "E1",
    "En1",
    "a1",
    "ai1",
    "an1",
    "ang1",
    "ao1",
    "e1",
    "ei1",
    "en1",
    "eng1",
    "er1",
    "i1",
    "i01",
    "ia1",
    "ian1",
    "iang1",
    "iao1",
    "ie1",
    "in1",
    "ing1",
    "iong1",
    "ir1",
    "iu1",
    "o1",
    "ong1",
    "ou1",
    "u1",
    "ua1",
    "uai1",
    "uan1",
    "uang1",
    "ui1",
    "un1",
    "uo1",
    "v1",
    "van1",
    "ve1",
    "vn1",
    "E2",
    "En2",
    "a2",
    "ai2",
    "an2",
    "ang2",
    "ao2",
    "e2",
    "ei2",
    "en2",
    "eng2",
    "er2",
    "i2",
    "i02",
    "ia2",
    "ian2",
    "iang2",
    "iao2",
    "ie2",
    "in2",
    "ing2",
    "iong2",
    "ir2",
    "iu2",
    "o2",
    "ong2",
    "ou2",
    "u2",
    "ua2",
    "uai2",
    "uan2",
    "uang2",
    "ui2",
    "un2",
    "uo2",
    "v2",
    "van2",
    "ve2",
    "vn2",
    "E3",
    "En3",
    "a3",
    "ai3",
    "an3",
    "ang3",
    "ao3",
    "e3",
    "ei3",
    "en3",
    "eng3",
    "er3",
    "i3",
    "i03",
    "ia3",
    "ian3",
    "iang3",
    "iao3",
    "ie3",
    "in3",
    "ing3",
    "iong3",
    "ir3",
    "iu3",
    "o3",
    "ong3",
    "ou3",
    "u3",
    "ua3",
    "uai3",
    "uan3",
    "uang3",
    "ui3",
    "un3",
    "uo3",
    "v3",
    "van3",
    "ve3",
    "vn3",
    "E4",
    "En4",
    "a4",
    "ai4",
    "an4",
    "ang4",
    "ao4",
    "e4",
    "ei4",
    "en4",
    "eng4",
    "er4",
    "i4",
    "i04",
    "ia4",
    "ian4",
    "iang4",
    "iao4",
    "ie4",
    "in4",
    "ing4",
    "iong4",
    "ir4",
    "iu4",
    "o4",
    "ong4",
    "ou4",
    "u4",
    "ua4",
    "uai4",
    "uan4",
    "uang4",
    "ui4",
    "un4",
    "uo4",
    "v4",
    "van4",
    "ve4",
    "vn4",
    "E5",
    "En5",
    "a5",
    "ai5",
    "an5",
    "ang5",
    "ao5",
    "e5",
    "ei5",
    "en5",
    "eng5",
    "er5",
    "i5",
    "i05",
    "ia5",
    "ian5",
    "iang5",
    "iao5",
    "ie5",
    "in5",
    "ing5",
    "iong5",
    "ir5",
    "iu5",
    "o5",
    "ong5",
    "ou5",
    "u5",
    "ua5",
    "uai5",
    "uan5",
    "uang5",
    "ui5",
    "un5",
    "uo5",
    "v5",
    "van5",
    "ve5",
    "vn5",
]

_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

# Prepend "@" to ARPAbet symbols to ensure uniqueness:
_arpabet = ['@' + s for s in cmudicts.valid_symbols]


def find_duplicates(input_list):
    seen = set()
    duplicates = set()
    
    for item in input_list:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
    
    return duplicates


# 声母、韵母和韵母加声调的组合
symbolsyue = [_pad] + pu_symbols + c + v + [vowel + tone for vowel in v for tone in tones]
symbolszh = [_pad] + pu_symbols + c2 + v2
symbolsen = [_pad] + pu_symbols + list(_letters) + list(_arpabet)


symbols = [_pad] + pu_symbols + c + v + [vowel + tone for vowel in v for tone in tones] + c2 + v2 + list(_letters) + list(_arpabet)


#print(len([_pad] + pu_symbols))
#print(len(c + v + [vowel + tone for vowel in v for tone in tones]))
#print(len(c2 + v2))
#print(len(list(_letters) + list(_arpabet)))
#duplicates = find_duplicates(symbols)

#print("重复的字符串有:", duplicates)