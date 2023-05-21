from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd
import re

NAMES = pd.read_csv("features.csv")["Название"].values

def strip_symbols(text):
    # Regular expression pattern to match symbols
    pattern = r'[^\w\s]'

    # Use re.sub() to replace symbols with an empty string
    stripped_text = re.sub(pattern, '', text)
    return stripped_text

def create_bigrams(text):
    words = strip_symbols(text).split()
    bigrams = [" ".join([words[i], words[i+1]]) for i in range(len(words) - 1)]
    return bigrams


def find_nearest(found_names, ratios, n=1):
    zipped_list = list(zip(found_names, ratios))
    sorted_list = sorted(zipped_list, key=lambda x: x[1], reverse=True)
    return [item[0] for item in sorted_list[:n]]


def get_plants(text):
    found_names, ratios = [], []
    for pairs in create_bigrams(text):
        for name in NAMES:
            ratio = fuzz.token_sort_ratio(pairs, name)
            
            if ratio > 80:
                ratios.append(ratio)
                found_names.append(name)
                
    #Ограничение на максимум два цветка для анализа
    return find_nearest(found_names, ratios)