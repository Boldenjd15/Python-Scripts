# ###################################################################################################################
# Text Mining Chatbot Project
# Dylan Bolden, Joe Gardner, Beth Vasquez, Liliana Castillo
# Due Date: 11/7/20

# This chatbot is using Trump Text data collected from several sources to provide Trump-Like responses.
# ####################################################################################################################
# Start by pulling in all possible libraries to be called for filtering text data and generating the chatbot.
# You will need to install pandas, sklearn and nltk packages if you haven't already.
# import nltk, nltk.download() <- we used all packages to download but will take ~ 300mb of storage

import pandas
import io
import random
import string
import warnings
import numpy as np
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

warnings.filterwarnings('ignore')

# pull stemming words from nltk to help filter the text data
from nltk.stem import WordNetLemmatizer
nltk.download('popular', quiet=True)
nltk.download('punkt')
nltk.download('wordnet')

# You will need to change the file path to wherever you saved the text data file.
with open(r'C:/Users/bolde/Desktop/!School_Work_Fall_2020/Text_Mining/Trumptextfiles/TrumpOnlyResponsesFinal.csv',
          'r',
          encoding='utf8',
          errors='ignore') as fin:
    raw = fin.read().lower()

sent_tokens = nltk.sent_tokenize(raw)

word_tokens = nltk.word_tokenize(raw)
lemmer = WordNetLemmatizer()


def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]


remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)


def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

# let's create a generic user input and pre-programmed response
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

def response(user_response):
    trump_response = ''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if (req_tfidf == 0):
        robo_response = trump_response + "I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = trump_response + sent_tokens[idx]
        return robo_response


flag = True
print("Trump: This is your President, Donald J. Trump. Ask me anything, I will be able to answer all your questions... because I know all! "
      "If you want to exit, type Bye!")
while (flag == True):
    user_response = input()
    user_response = user_response.lower()
    if (user_response != 'bye'):
        if (user_response == 'thanks' or user_response == 'thank you'):
            flag = False
            print("Trump: You are welcome..")
        else:
            if (greeting(user_response) != None):
                print("Trump: " + greeting(user_response))
            else:
                print("Trump: ", end="")
                print(response(user_response))
                sent_tokens.remove(user_response)
    else:
        flag = False
        print("Trump: Bye! Make America Great Again!")


#Example Questions:
# Hola
# What will you do about Mexico?
# What do you like about me?
# What do you think about Hillary?
# What do you think about the trade deficit?
# What will NATO do in the fight against terrorism?
