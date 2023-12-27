#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import os
from hazm import Normalizer
import pandas as pd
import re
import hazm
from txt_processing import *
import numpy as np

all_symbols_in_message = []
all_message_by_ambiguous = []
indices_data = pd.read_excel("I:\\master_matus\\payan_name1\\2_implement1\\New_folder\\symbol.xlsx")
symbol_list_deterministic = indices_data[indices_data['label'] == 0].reset_index()
symbol_list_ambiguous = indices_data[indices_data['label'] == 1].reset_index()
print(symbol_list_deterministic.to_numpy())
print(symbol_list_ambiguous.to_numpy())

def recognize_symbols(text):
    pos_key_words = "رنج منفی|رنج مثبت|صف فروش|صف خرید"
    hard_symbol = ["ما", "بورس", "فرابورس" ,'پرداخت' , 'همراه','آینده','امید','ملت']
    flag = False
    flag_FN = False
    text_symbol = []
    text_sentence = hazm.sent_tokenize(text)
    text_words = hazm.word_tokenize(text)
    for i in range(len(symbol_list_deterministic)):
        symbol = symbol_list_deterministic.iloc[i, :]
        if (text.find(" " + symbol[2] + " ") != -1) or (text.find("#" + symbol[2] + " ") != -1):
            if symbol[2] not in text_symbol:
                text_symbol.append(symbol[2])
            all_symbols_in_message.append(symbol[2])

    for i in range(len(symbol_list_ambiguous)):

        symbol = symbol_list_ambiguous.iloc[i, :]
        if symbol[2] in hard_symbol:
            continue
        s = None
        if "#" + symbol[2] + " " in text_words:
            s = symbol[2]
        elif "نماد " + symbol[2] in text_words:
            s = symbol[2]
        elif text.find(" " + symbol[2] + " ") != -1:
            s = symbol[2]
        elif "«" + symbol[2].strip() + "»" in text:
            s = symbol[2]
        elif '"' + symbol[2].strip() + '"' in text:
            s = symbol[2]
        elif text.find("“" + symbol[2].strip() + "”") != -1:
            s = symbol[2]
        elif symbol[2] in text_words and symbol[2] not in hard_symbol:
            for sen in text_sentence:
                if sen.find(" " + symbol[2] + " ") != -1:
                    sen_words = hazm.word_tokenize(sen)
                    if len(set(symbol_list_deterministic.iloc[:, 1]) & set(sen_words)) > 0:
                        s = symbol[2]
                    elif re.search(pos_key_words, sen):
                        s = symbol[2]
                    else:
                        s = symbol[2]
        if s:
          all_symbols_in_message.append(s)
          if s not in text_symbol:
              text_symbol.append(s)

    return text_symbol


def normalize_company_name(text):
    return Normalizer().normalize(text.replace("\u200c", " "))


def get_symbols(text):
      text = text.replace("|", " ").replace("\n", " ").replace("،", " ")
      text_symbol = []
      hard_symbol = ["ما", "بورس", "فرابورس", 'پرداخت', 'همراه', 'آینده','ملت','امید']
      for i in range(len(symbol_list_ambiguous)):

            symbol = symbol_list_ambiguous.loc[i, "symbol"]
            if symbol in hard_symbol:
                continue
            company_list = symbol_list_ambiguous.loc[i, "symbol"]
            if symbol not in text_symbol:
                if ("«" + symbol.strip() + "»") in text:
                        text_symbol.append(symbol)
                elif "“" + symbol.strip() + "”" in text:
                    text_symbol.append(symbol)
                elif '" ' + symbol.strip() + ' "' in text:
                    text_symbol.append(symbol)
                elif (len(symbol_list_ambiguous.loc[i, "company"]) > 5 and
                    (" "+ symbol_list_ambiguous.loc[i, "company"] + " " in text
                     or normalize_company_name(symbol_list_ambiguous.loc[i, "company"]) in text )):
                        text_symbol.append(symbol)
                else :
                    search = re.findall(r'نماد[^.]+( )'+ symbol, text)
                    count_find = len(search)
                    for cmpny in company_list:
                        if count_find > 0:
                               count_find -= len(re.findall(r''+cmpny, text))
                        else:
                            break
                    if count_find > 0:
                        text_symbol.append(symbol)

      return text_symbol


def load_data(path):
    file_reader = pd.ExcelFile(path)
    all_daily_data = {}
    for per_day in file_reader.sheet_names:
        all_daily_data[per_day] = pd.read_excel(file_reader, sheet_name=per_day)
    return all_daily_data


def process_messages(messages_list, t_preprocess):
    process_data,symbol_data , symbols_list = [], [], []

    for messages in messages_list:
        try:
            txt = t_preprocess.cleaning(t_preprocess.find_urls(messages.replace("#", " #")))
            symbols = list(np.unique(np.array(get_symbols(txt) + recognize_symbols(txt))))
        except AttributeError:
            txt = messages
            symbols = []

        if len(symbols)>0:
            for s in symbols:
                txt = txt.replace(s, " نمادبورسی ")
        try:
            txt = txt.replace("#", " ")
        except AttributeError:
           pass
        symbol_data.append(txt)
        symbols_list.append(symbols)
        process_data.append(txt)
        # print(new_txt.replace("#", " "),"???????????")
        # print("**********************************************")


    return symbols_list,process_data, symbol_data


def main(data_directory, data_directory_des):
    t_process = Preprocess()
    data_files_name = os.listdir(data_directory)
    print(data_files_name)
    all_message = 0
    for file_path in data_files_name:
      print(file_path)
      try:
        all_daily_data = load_data(os.path.join(data_directory, file_path))
        file_writers = pd.ExcelWriter(os.path.join(data_directory_des, file_path))
        itr = 0
        for day in all_daily_data.keys():
            all_message += len(all_daily_data[day]["text"].values)
            all_daily_data[day]["symbols"], all_daily_data[day]["processed text"], all_daily_data[day]["processed text Symbol"] = process_messages(all_daily_data[day]["text"].values, t_process)
            all_daily_data[day].to_excel(file_writers, sheet_name=day)
        file_writers.close()
      except ValueError:
          continue

    print(data_directory, all_message)


if __name__ == '__main__':
    directory_path = "I:\\master_matus\\payan_name1\\2_implement1\\data".strip()
    try:
        os.makedirs("I:\\master_matus\\payan_name1\\2_implement1\\New_folder\\dataset\\dataset\\dataset_languagemoldel\\processed_data")
    except OSError:
        pass
    print(os.listdir(directory_path))
    for folders in os.listdir(directory_path):
        # try:
        #     os.makedirs(os.path.join(directory_path, folders, directory_path+"_processed_data"))
        # except OSError:
        #     pass

        if  os.path.isdir(os.path.join(directory_path, folders)):
             print(folders)
             main(os.path.join(directory_path, folders),
             "I:\master_matus\payan_name1\\2_implement1\\New_folder\\dataset\\dataset\\dataset_languagemoldel\\processed_data"
             )


