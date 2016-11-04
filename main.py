# Consize - Automatic Text Summarization & Storage
# Made by John Carveth, (c) November, 2016
import os,sys
import re
from nltk.tokenize import sent_tokenize
import datetime

current_version = 1.1
os.chdir("data")

# Keep all blacklisted words in a text file for easy access/updating
try:
    blacklist_file = open("blacklist.txt", "r+")
    with open("content.txt", "r+") as content_file:
        content = content_file.read()
except IOError:
    print('Error opening file.')

blacklist = []
for line in blacklist_file.readlines():
    blacklist.append(line.strip('\n'))

# Split the content string into a list, then remove all blacklisted words.
def scrub_n_split(text):
    '''
    String -> List[#of words in str]

    Converts a string to a list, making each word its own element and removing
    useless characters I don't need.
    '''
    content_list = re.sub('[()\/!@#$%^&*|{}!><.,\n]',' ', text)
    content_list = content_list.split(' ')
    content_list = [x.lower() for x in content_list]
    content_list = [x for x in content_list if x not in blacklist]
    return content_list


def split_to_sentence(content):
    '''
    List of Str -> List of Str
    '''
    sentences = sent_tokenize(content)
    return sentences

def frequency(l):
    '''
    List of Strings -> List[Str, int]
    
    Takes a scrubbed list of words and counts the frequency of each word in
    the list. Returns a nested list with the word and an integer representing
    how frequent the word is in the text.
    '''
    frequency = []
    for i in range(0,len(l)):
        if(l[i] not in frequency):
            occur = l.count(l[i])
            frequency.append([occur, l[i]])
        else:
            pass
    f_set = set(tuple(x) for x in frequency)
    frequency = [list(x) for x in f_set]
    frequency.sort(reverse=True)
    return frequency

def rank_sentences(s, f):
    '''
    (List of Str, List of [int, Str]) -> List of [int, Str]

    Takes as input the following:
        1. s = List of sentences extracted from text
        2. f = Nested list of words in the text and their occurence
    Returns a nested list with sentences and their 'points' based on how many
    popular key words they contain. 
    '''
    ranked_s = []
    
    for x in range(len(s)):
        score = 0
        for y in range(len(f)):
            if f[y][1] in s[x]:
                score += f[y][0]
        ranked_s.append([score, s[x]])
        
    return ranked_s

def sentence_trim(sr, s, constrict=70):
    '''
    ([int, List of str], List of Str, int=.5) -> [int, List of str]

    Takes as input nested list with [int (repr. sentence points/rank)
    and a List of sentences], and a List of sentences, and returns a nested list
    with sentences in their original order, and superflous sentences dropped.

    Consize optional argument with a default of 50% controls how many sentences
    to include in the final list.
    '''
    x = len(sr)
    y = x - (x * (constrict/100))
    sr_sorted = sr[:]
    sr_sorted.sort(reverse=True)
    
    for i in range(int(x-y)):
        try:
            sr_sorted.pop()
        except IndexError:
            pass
    result = [x for x in sr if x in sr_sorted]
    return(result)

def write_log(org_wordc, fin_wordc):
    '''
    (int, int) -> None

    Logs actions to a text file.
    '''
    current_time = datetime.datetime.now()
    with open('log.txt', 'a') as log_file:
        log_file.write("#"*40+'\n')
        log_file.write('Action: Summarize\n')
        log_file.write('Time: '+str(current_time) + '\n')
        log_file.write('Words in Original:'+ str(org_wordc) + '\n')
        log_file.write('Words in Consized: '+ str(fin_wordc) + '\n')

def main():
    words = scrub_n_split(content)
    sentences = split_to_sentence(content)

    word_frequency = frequency(words)
    sentence_frequency = rank_sentences(sentences, word_frequency)

    final = sentence_trim(sentence_frequency, sentences)
    final_words = 0
    for x in range(len(final)):
        print(final[x][1], end=" ")
        final_words += len(final[x][1].split(' '))
    write_log(len(words), final_words)

blacklist_file.close()
