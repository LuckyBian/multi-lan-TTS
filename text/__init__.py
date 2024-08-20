import sys
sys.path.append('/home/weizhenbian/vits_all')
import re
from text.symbols import symbols
from text import english
from text import chinese
from text.chinese import g2pzh
from text.english import g2pen
from text.cantonese import cantonese_to_ipa
from text.symbols import symbolsyue
from text.symbols import symbolszh
from text.symbols import symbolsen
from text import cmudicts

from text import cleaners
_curly_re = re.compile(r'(.*?)\{(.+?)\}(.*)')

_symbol_to_id = {s: i for i, s in enumerate(symbolsen)}
_id_to_symbol = {i: s for i, s in enumerate(symbolsen)}

cmudict = cmudicts.CMUDict('/home/weizhenbian/vits_all/text/cmu_dictionary')

def _clean_text(text, cleaner_names):
    for name in cleaner_names:
        cleaner = getattr(cleaners, name)
        if not cleaner:
            raise Exception('Unknown cleaner: %s' % name)
        text = cleaner(text)
    return text

def text_to_sequence_en(text, cleaner_names=["english_cleaners"], dictionary=None):
    sequence = []
    space = _symbols_to_sequence(' ')
    # Check for curly braces and treat their contents as ARPAbet:
    while len(text):
        m = _curly_re.match(text)
        if not m:
            clean_text = _clean_text(text, cleaner_names)
            if dictionary is not None:
                clean_text = [get_arpabet(w, dictionary) for w in clean_text.split(" ")]
                for i in range(len(clean_text)):
                    t = clean_text[i]
                    if t.startswith("{"):
                        sequence += _arpabet_to_sequence(t[1:-1])
                    else:
                        # Ensure each symbol is a number, if not, skip adding to sequence
                        temp_sequence = _symbols_to_sequence(t)
                        sequence += [item for item in temp_sequence if isinstance(item, int)]
                    sequence += space
            else:
                temp_sequence = _symbols_to_sequence(clean_text)
                sequence += [item for item in temp_sequence if isinstance(item, int)]
            break
        sequence += _symbols_to_sequence(_clean_text(m.group(1), cleaner_names))
        sequence += _arpabet_to_sequence(m.group(2))
        text = m.group(3)
  
    # remove trailing space
    if dictionary is not None and sequence:
        sequence = sequence[:-1] if sequence[-1] == space[0] else sequence
    return sequence




def add_dollar_signs_to_list(input_list):
    # 初始化结果列表，并在开头添加$
    result = ['$','$']
    
    # 遍历输入列表
    for item in input_list:
        # 如果item不是标点符号，添加item和$
        if not re.match(r'[^\w\s]', item):  # 使用正则表达式检查item是否为标点符号
            result.append(item)
            result.append('$')
            result.append('$')
        else:
            # 如果是标点符号，仅添加item
            result.append(item)
    
    # 检查最后一个元素是否为$，如果不是则添加（处理末尾标点符号的情况）
    if result[-1] != '$':
        result.append('$')
        result.append('$')
    
    return result


def add_dollar_signs_to_list2(input_list):
    # 初始化结果列表，并在开头添加$
    result = ['~','~']
    
    # 遍历输入列表
    for item in input_list:
        # 如果item不是标点符号，添加item和$
        if not re.match(r'[^\w\s]', item):  # 使用正则表达式检查item是否为标点符号
            result.append(item)
            result.append('~')
            result.append('~')
        else:
            # 如果是标点符号，仅添加item
            result.append(item)
    
    # 检查最后一个元素是否为$，如果不是则添加（处理末尾标点符号的情况）
    if result[-1] != '~':
        result.append('~')
        result.append('~')
    
    return result


def get_arpabet(word, dictionary):
    word_arpabet = dictionary.lookup(word)
    if word_arpabet is not None:
        return "{" + word_arpabet[0] + "}"
    else:
        return word

def add_fives(lst):
    # 创建一个新的空列表用来存储结果
    result = []
    # 遍历原始列表中的每个元素
    for number in lst:
        # 在每个元素前后添加数字5
        result.extend([5, number, 5])

    result = [5] + result + [5]
    return result

def text_to_sequence(text):
    sequence = []
    # 处理中文
    if text[0] == '(' and text[-1] == ')':
        text = text[1:-1]
        clean_text = chinese.text_normalize(text)
        text = chinese.g2pzh(clean_text)
        # ['w', 'o3', 'j', 'in1', 't', 'ian1', 'h', 'en3', 'g', 'ao1', 'x', 'ing4', ',', 'AA', 'a5', 'AA', 'a5', 'AA', 'a5']
        text = add_dollar_signs_to_list(text)
        sequence = [symbolszh.index(symbol) for symbol in text if symbol in symbolszh]

        for index,s in enumerate(sequence):
            if int(s) > 23:
                sequence[index] = int(s) + 390

    # 处理英语
    elif text[0] == '{' and text[-1] == '}':
        t = text[1:-1]
        #clean_text = _clean_text(text)
        #print(clean_text)
        #text = english.g2pen(clean_text)
        # ['AY1', 'AE1', 'M', 'V', 'EH1', 'R', 'IY0', 'HH', 'AE1', 'P', 'IY0', 'T', 'AH0', 'D', 'EY1']
        #text = add_dollar_signs_to_list(text)
        #sequence = [symbolsen.index(symbol) for symbol in text if symbol in symbolsen]
        sequence = text_to_sequence_en(text=t,dictionary=cmudict)
        sequence = add_fives(sequence)

        for index,s in enumerate(sequence):
            if int(s) > 23:
                sequence[index] = int(s) + 611

    # 处理粤语
    elif text[0] == '[' and text[-1] == ']':
        text = text[1:-1]
        clean_text = chinese.text_normalize(text)
        text = cantonese_to_ipa(clean_text)
        # ['ng', 'o5', 'g', 'am1', 't', 'in1', 'h', 'an2', 'g', 'ou1', 'h', 'ing1', ',', 'aa', 'aa2', 'aa', 'aa2', 'aa', 'aa2']
        text = add_dollar_signs_to_list(text)
        sequence = [symbolsyue.index(symbol) for symbol in text if symbol in symbolsyue]

    #clean_text = add_dollar_signs(clean_text)
    #sequence = cantonese_to_ipa(clean_text)

    #print(text)
    return sequence

def sequence_to_text(sequence):
    '''Converts a sequence of IDs back to a string'''
    result = []
    for symbol_id in sequence:
        if symbol_id in _id_to_symbol:
            s = _id_to_symbol[symbol_id]
            result.append(s)
    return result


def _clean_text(text, cleaner_names):
    for name in cleaner_names:
        cleaner = getattr(cleaners, name)
        if not cleaner:
            raise Exception('Unknown cleaner: %s' % name)
        text = cleaner(text)
    return text


def _symbols_to_sequence(symbolsen):
    return [_symbol_to_id[s] for s in symbolsen if _should_keep_symbol(s)]


def _arpabet_to_sequence(text):
    return _symbols_to_sequence(['@' + s for s in text.split()])


def _should_keep_symbol(s):
    return s in _symbol_to_id and s != '_' and s != '~'


#t = '{This is english}'
#t1 = '[这是一句粤语]'
#t2 = '(这是一句普通话)'
#print(text_to_sequence(t))
