### Programming
### Take Home Exam 1

import ast
import os

## Q3

dictionary = {}
working_dict = dictionary.copy()


def entry():
    temp = input("word_in_1st_language,word_in_2nd_language").split(sep=",")
    if type(temp) is not str:
        raise Exception("invalid input")
    if temp[0] in working_dict.keys():
        raise Exception("value already exist")
    working_dict.update({temp[0]: temp[1]})
    return "entry added to dictionary"


def query():
    temp = input("searched_word")
    if working_dict.get(temp) is None:
        try:
            a = (list(working_dict.keys())[list(working_dict.values()).index(temp)])
        except:
            raise Exception("value is not in the dictionary")
    else:
        a = working_dict.get(temp)
    return a


def save():
    save = open("mydictionary.txt", "w+")
    save.write(str(working_dict))
    save.close()
    return "dictionary saved on text file"


def load():
    text = open("mydictionary.txt", "r")
    loaded = text.read()
    global dictionary
    dictionary = ast.literal_eval(loaded)
    text.close()
    return dictionary


def all():
    print(dictionary)

def exit():
    os.system('cls')
    os.system("TASKKILL /F /IM HT1_Q3.py")


def help():
    print("""
  to enter a new value in the dictionary type:
  entry(), then word_in_1st_language,word_in_2nd_language
    
  ===
  to query a word's translation in either language: 
  type query(), then enter the desired word
    
  ===
  to see the full dictionary, enter "all()"
    
  ===
  to save the entries, enter command "save()"
  ===
  to leave the app, simply type "exit()"
    
  """)

