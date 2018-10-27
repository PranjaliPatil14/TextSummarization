import string
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords, words
from collections import defaultdict
from string import punctuation
from heapq import nlargest
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.probability import  FreqDist
import itertools
from nltk.stem import PorterStemmer, WordNetLemmatizer
import collections, re
from nltk.corpus import CategorizedPlaintextCorpusReader
import matplotlib.pyplot as plt

tagged_words=["hospital","facility","cost","hospitality","treatment","service","doctor","staff","patient","administration","admin","water",
"management","room","nurses","care","checkup","charge","test","appointment","report","money","experience","response","diagnosis","surgery",
"budget","nature","medical","pharmacy","multispeciality","overall","health","cleanness","cleanliness","treat","technology","quality","qualification","help",
"interaction","support","bill","behaviour","emergency","ambulance","availability","admit","punctuality","location","transport","trust"]


file_name='input.txt'
f=open(file_name)
text=f.readlines()
read_string=str(text)
sent_tokens=sent_tokenize(read_string)
word_tokens=word_tokenize(read_string)

stop_words=set(stopwords.words('english'))
filtered_sentence=[]
for w in word_tokens:
    if (w.lower() not in stop_words and w.lower() not in string.punctuation):
        filtered_sentence.append(w.lower())
#print(word_tokens)
#print(filtered_sentence)

ps=PorterStemmer()
stem=[]
for w in filtered_sentence:
    stem.append(w)
word=nltk.pos_tag(stem)
#sentence=nltk.pos_tag(sent_tokens)
print(word)
NN_list=[]
for i in word:
        if(i[1]=="NN"or i[1]=="NNS" ):
                NN_list.append(i[0])
#print("NN printing")
#print(NN_list)
dup_items = set()
uniq_items = []
for x in NN_list:
    if x not in dup_items:
        uniq_items.append(x)
        dup_items.add(x)
#print("Printing unique")
#print(uniq_items)

summary=[]
summary2=[]
#Printing 8 pattern
no=len(word)
print("-----------------------witth NN----------------------------")
i=0
while i<no-1:
        w_tuple=word[i]
        next_w_tuple=word[i+1]
        if((w_tuple[1]=="JJ" or w_tuple[1]=="JJR" or w_tuple[1]=="JJS")  and (next_w_tuple[1]=="NN" or next_w_tuple[1]=="NNS")):
                s=" "
                if(next_w_tuple[0] in tagged_words):
                        print(w_tuple[0]," ",next_w_tuple[0])
                        summary2.append(w_tuple[0])
                        summary2.append(next_w_tuple[0])
                        s=(w_tuple[0],next_w_tuple[0])
                        summary.append(s)
        i+=1

print("-------------------------------witth NNS-----------------------------")
no=len(word)
i=0
while i<no-2:
        w_tuple=word[i]
        next_w_tuple=word[i+1]
        next_next=word[i+2]
        if((w_tuple[1]=="JJ" or w_tuple[1]=="JJR" or w_tuple[1]=="JJS") and (next_w_tuple[1]=="NN" or next_w_tuple[1]=="NNS") and (next_next[1]=="NN"  or next_next[1]=="NNS")):
                   if((next_w_tuple[0] in tagged_words )or (next_next[0] in tagged_words)):
                           print(w_tuple[0]," ",next_w_tuple[0]," ",next_next[0])
                           summary2.append(w_tuple[0])
                           summary2.append(next_w_tuple[0])
                           summary2.append(next_next[0])
                           s=(w_tuple[0],next_w_tuple[0],next_next[0])
                           summary.append(s)
        i+= 1
        
print("--------------------------------witth verb----------------------------------------")
no=len(word)
i=0
while i<no-1:
        w_tuple=word[i]
        next_w_tuple=word[i+1] 
        if((w_tuple[1]=="VB"or w_tuple[1]=="VBN"or w_tuple[1]=="VBD"or w_tuple[1]=="VBZ"or w_tuple[1]=="VBP" )  and (next_w_tuple[1]=="RB" or next_w_tuple[1]=="RBR"or next_w_tuple[1]=="RBS" )):
                if(w_tuple[0] in tagged_words):
                        print(w_tuple[0]," ",next_w_tuple[0])
                        summary2.append(w_tuple[o])
                        summary2.append(next_w_tuple[0])
                        s=(w_tuple[0],next_w_tuple[0])
                        summary.append(s)
        i+=1
print("summary printing")
print(summary)

'''for word in summary:
        print(word)
        bagofwords=[collections.Counter(re.findall(r'\w+',i) )for i in summary2]
        sumbags1=sum(bagofwords,collections.Counter())
print("----------------------bag of words ------------------")
print(sumbags1)
'''
#print("----------sentiments ----------")
sid=SentimentIntensityAnalyzer()
sp=[]
comp=[]
for sen in summary:
    s=sen[0]+" "+sen[1]
    print(s)
    ss=sid.polarity_scores(s)
    for k in sorted(ss):
        if((ss["compound"]!=0) and (s not in sp)):
            sp.append(s)
            comp.append(ss[k])
            #print('{0}:{1},'.format(k,ss[k]),end='')
            #print("\n")
print("****************** ANALYSED REVIEWS*******************************")            
print("***************************",file_name.split(".")[0],"****************************")

print(sp)
#print(comp)
i=0
final_words=[]
while(i<len(sp)):
    final_words.append(sp[i].split()[1])
    i+=1
#print( i[1] for i in sp[0])
#print(final_words)
p1=plt.figure(file_name.split(".")[0]+"Bar")
plt.bar(final_words,comp,width=0.8,color=['blue','grey'])
plt.xlabel("Features")
plt.title("Reviews")
p1.show()
p2=plt.figure(file_name.split(".")[0])
p=sid.polarity_scores(read_string)
total_analysis=[]
print("***********************TOTAL ANALYSIS *****************************")
for k in sorted(p):
    print('{0}:{1},'.format(k,p[k],end='' ))
    total_analysis.append(p[k])
i=1
totalt=[]
while i<4:
    totalt.append(total_analysis[i])
    i=i+1
print(totalt)
activities=['neg','neu','pos']
colors = ['red','blue','green']
plt.pie(totalt, labels = activities, colors=colors, 
        startangle=90, shadow = True, 
        radius = 1.2, autopct = '%1.1f%%')
plt.legend()
p2.show()

