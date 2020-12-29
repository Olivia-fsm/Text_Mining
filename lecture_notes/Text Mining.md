# Text Mining

---

## Module 1: Handling Text in Python

### Part1: Word(string) comparison functions

- Checking Functions

  ```python
  s.startswith('t')  #Warning: 单复数！
  s.endswith('t')
  t in s
  s.isupper() s.islower() s.istitle()
  s.isalpha() s.isdigit() s.isalnum()
  ```

- String Operation: string would be **changed!**

  ```python
  # Case Modifications
  s.lower()	
  s.upper()
  s.titlecase()
  
  # Split&join
  s.split(t) #-->split by character `t` 
  s.splitlines() #-->split by the newline character `\n`, 分行
  s.join(t) #-->
  
  # Cleaning operations
  s.strip() #-->strip from front of each word
  s.rstrip() #-->strip from end of each word
  
  s.find(substr) #-->find from front
  s.rfind(substr) #-->find from end
  
  s.replace(u, v) #replace all u in s with v
  ```

- Handling larger texts–>Files

  ```python
  # Reading files line by line
  f = open('UNDHR.txt', 'r')
  f.readline()
  
  # Read the full file
  f.seek(0)
  text12 = f.read() #-->text12.splitlines() != f.readlines (readlines 最后会保留\n!)-->用rstrip()可以去除
  
  f.read(n) #-->从第n位开始读
  
  # write
  f.write(message)
  
  # close
  f.close()
  f.closed #-->check if closed
  ```

  ### Part2: Regular Expressions

  - Example 1: Parsing the callout regular expression

    `@[A-Za-z0-9]+` 

    	- Starts with `@`
    	- Followed by any alphabet(upper or lower case), digit, or underscore
    	- that pattern repeats for at least once, but any number of times

    

  - Meta-characters: **Character Matches!**

    - `.`  — wildcard, matches any single character
    - `^`  — start of a string
    - `$`  — end of a string (often \n)
    - `[ ]`  — matches one of the set of characters within  `[ ]`
    - `[a-z]`  — matches one of lowercase alphabets
    - `[^abc]`  — matches a characters that is not a, b or c
    - `a|b`  — matches either a or b, where a and b are strings
    - `( )`  — Scoping for operators
    - `\`  — Escape character for special characters (`\t, \n, \b`)
      - `\b`: word boundary
      - `\d`: Any digit == `[0-9]`
      - `\D` : Any non-digit == `[^0-9]`
      - `\s`: Any whitespace, equivalent to `[ \t\n\r\f\v]`
      - `\S`: Any NON-whitespace, equivalent to `[^ \t\n\r\f\v]`
      - `\w`: Alphanumeric character, equivalent to `[a-zA-Z0-9_]`
      - `\W`: NON-Alphanumeric character, equivalent to `[^a-zA-Z0-9_]`
    - Meta-characters: **Repetitions**
      - `*`  — matches **zero or more** occurrences
      - `+` — matches **one or more** occurrences
      - `?` — matches **zero or one** occurrences
      - `{n}` — exactly $$n$$ repetitions
      - `{,n}` — at most $$n$$ repetitions
      - `{n,}` — at least $$n$$ repetitions
      - `{m,n}` — $$[m,n]$$ repetitions

#### – Coding Example

```python
text = '"Ethics are built right into the ideals and objectives of the United Nations" #UNSG @ NY Society for Ethical Culture bit.ly/2guVelr @UN @UN_Women'

# Find all @addresses (must be something after @)
text1 = [w for w in text if re.search('@[0-9A-Za-z_]+', w)]
text1 = [w for w in text if re.search('@\w+', w)]
   # --> Both with the same output: ['@UN', '@UN_Women']

# Find specific characters
text='ouagadougou'

text2 = re.findall(r'[aeiou]', text)
text3 = re.findall(r'[^aeiou]', text)
```

#### – Case Study: Regular expression for Dates Variants

```python
re.find(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', text) # Case1: 23-10-2002   # Case2: 23/10/(20)02
re.findall(r'\d{2} (Jan|Feb|Mar|...|Dec) \d{4}', text) #--> would only output 'OCT'! 
re.findall(r'\d{2} (?:Jan|Feb|Mar|...|Dec) \d{4}', text) #--> would output '23 Oct 2002' (full string)
re.findall(r'\d{2} (?:Jan|Feb|Mar|...|Dec)[a-z]* \d{4}', text) #--> 'October' instead of Oct
# ():小括号means Scoping！ 用到()的话就只会extract小括号内的内容。 
# (?:) 表示非限制组，match到()内的内容，但是返回一整段text

re.findall(r'(?:\d{2})? (?:Jan|Feb|Mar|...|Dec)[a-z]* (?:\d{2},? )?\d{4}', text)
```

#### – Demonstration: Regex with Pandas and Named Groups

```python
import pandas as pd
time_sentences = ["Monday: The doctor's appointment is at 2:45pm.", 
                  "Tuesday: The dentist's appointment is at 11:30 am.",
                  "Wednesday: At 7:00pm, there is a basketball game!",
                  "Thursday: Be back home by 11:15 pm at the latest.",
                  "Friday: Take the train at 08:10 am, arrive at 09:00am."]

df = pd.DataFrame(time_sentences, columns=['text'])
df


# .str.property   .str.method()  : help with the text operations in Pandas DataFrame
df['text'].str.len() #-->return the total number of char in each blocks
df['text'].str.split().str.len() #-->return the total number of words in each blocks
df['text'].str.count(r'\d') #-->find the frequency a digit(can be replaced) occurs in each blocks
df['text'].str.contains('appointment') #-->findout whether each blocks contains the substring
df['text'].str.findall(r'\d') #-->find all the occurances of the digits(can be replaced). Return all the digits as a list!
df['text'].str.findall(r'(\d?\d):(\d\d)') #-->group and find the tuple (hours:minutes). Return as a list of tuples
df['text'].str.findall(r'(?:\d{1,2}):\d{2}') #-->这其实是re packge的用法...Return as a list of "08:10" strings
df['text'].str.replace(r'\w+day\b', '???') #-->??? instead of workday!!
df['text'].str.replace(r'\w+day\b', lambda x:x.groups()[0][:3]) #--> Replace each workday with its 3-char abbreviation


df['text'].str.extract(r'(\d?\d):(\d\d)') 
df['text'].str.extractall(r'((\d?\d):(\d\d) ?([ap]m))')
#-->.str.extract() : create new columns using extracted groups
#-->.str.extractall() : create new columns using extracted groups, and the whole pattern string(whole pattern always in col0)

#NAME GROUP
df['text'].str.extractall(r'((?P<time>\d?\d):(?P<minute>\d\d) ?(?P<period>[ap]m))')
#--> (?P<myName>\d{2}) : name the pattern group \d{2} as myName
```

### Part3. Internationalization and Issues with Non-ASCII Characters

- ASCII:

  ![image-20201217104153562](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201217104153562.png)

![image-20201217104322430](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201217104322430.png)

- Unicode:

![](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201217104547789.png)

![image-20201217104642220](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201217104642220.png)

![image-20201217104746351](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201217104746351.png)



## Module2. Basic Natural Language Processing

### Part1. Basic NLP tasks with NLTK

#### Download Built-in Dataset

```python
import nltk
nltk.download() # --> 选择Downloader时填  d all
from nltk.book import *

text7 # built-in text books
sent7 # built-in sentences book
```

![image-20201217235841197](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201217235841197.png)



#### Words Frequency

```python
dist = FreqDist(text7) # return a dict of words-frequency in text7
len(dist)

vocabList = dist.keys()
vocabList['something'] # Return the frequency of word 'something'
# In python2: each word would be displayed as u'something', indicating the unicode format. In python3 NO.

freqwords = [w for w in vocabList if len(w)>5 and dist[w]>100]
```



#### Normalization and Stemming

```python
inputList = "List listed lists listing listings"
wordsList = inputList.lower.split(' ') # Preprocessing(naive..) of original text


# Stemming: Find the Root Word!
porter = nltk.PorterStemmer()
[porter.stem(t) for t in wordsList]

# Lemmatization: (词形还原)
# Stemming, but resulting stems are all valid words
udhr = nltk.corpus.udhr.words('English-Latin1')

```

#### Tokenization

```python
# Previous method
text11.split(' ')

#nltk method
nltk.word_tokenize(text11)
```



### Part2. Advanced NLP tasks with NLTK

#### Part-of-speech(POS) Tagging

![image-20201223212642305](C:\Users\Olivia\AppData\Roaming\Typora\typora-user-images\image-20201223212642305.png)

```python
# help with explanation of each tags
>>> nltk.help.upenn_tagset('MD')
MD: modal auxiliary
    can cannot could couldn't dare may might must need ought shall should shouldn't will would

### --> How to do POS Tagging with NLTK
# 1. Recall splitting a sentence into words/tokens
text11 = "Children shouldn't drink a sugary drink before bed."
text12 = nltk.word_tokenize(text11)

# 2. NLTK's Tokenizer
>>>nltk.pos_tag(text12)
[('Children', 'NNP'), ('should', 'MD'), ("n't", 'RB'), ('drink', 'VB'), ('a', 'DT'), ('sugary', 'JJ'), ('drink', 'NN'), ('before', 'IN'), ('bed', 'NN'), ('.', '.')] # NNP: Prural Noun
```

#### Ambiguity in POS Tagging: e.g. -ing words can be NN or JJ

#### Parsing Sentence Structure

![image-20201223223501656](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201223223501656.png)

![image-20201223224243998](C:\Users\Olivia\AppData\Roaming\Typora\typora-user-images\image-20201223224243998.png)

![image-20201223224534175](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201223224534175.png)

![image-20201223224743050](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201223224743050.png)

![image-20201223224908397](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201223224908397.png)

## Module3. Text Classification

![image-20201225122230158](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201225122230158.png)

### Qeustion1: Feature Identification in Supervise Learning Classification

---

##### 1. Words:

- Handling commonly-occurring words: **Stop words** (a,an,the…)
- Normalization: Make lower case **V.S.** leave as-is
- Stemming/Lemmatization

##### 2. Characteristics of words: 

- **Characteristics of words**
  -  e.g.: U.S. ; White House / white house
- **Parts-of-speech of words in a sentence**
- **Grammatical structure, sentence parsing**
- **Grouping words of similar meaning, semantics**
  - {buy, purchase}
  - {Mr. , Ms. , Dr. , Prof.}
  - Numbers / Digits; 
  - Dates…

##### 3. Features may come from inside words and word-sequences

- bigrams, trigrams, …, n-grams: “White House”
- character sub-sequences in words: “ing”, “ion” …

### Naïve Bayes Classifiers

---

#### Case Study: Classifying text search queries

![image-20201225181215376](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201225181215376.png)



##### Probabilistic Model

- Update the likelihood of the class given new information

- Prior Probability:

  - Pr(y=Entertainment), Pr(y=CS), Pr(y=Zoology)

- Posterior Probability: (conditional probability) 

  - Pr(y=Entertainment|x=“Python”)

- Bayes’s Rule

  ![image-20201225181641000](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201225181641000.png)

![image-20201225182035819](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201225182035819.png)

![image-20201225182137165](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201225182137165.png)

![image-20201225182738175](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201225182738175.png)

![image-20201225183105013](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201225183105013.png)

![image-20201227103611052](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201227103611052.png)

![image-20201227103702854](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201227103702854.png)

![image-20201227103723675](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201227103723675.png)

- Smoothing

![image-20201227104615720](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201227104615720.png)

![image-20201227104204533](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201227104204533.png)

### SVM

![image-20201227114427836](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201227114427836.png)

![image-20201227114758544](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201227114758544.png)

![image-20201227115101344](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201227115101344.png)

![image-20201227115239772](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201227115239772.png)

![image-20201227115411447](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201227115411447.png)

#### Learning Text Classifier in Python

- Toolkit: Sklearn, nltk, weka

- Using Naive-Bayes Classifier in sklearn

  ![image-20201227120620326](C:\Users\Olivia\AppData\Roaming\Typora\typora-user-images\image-20201227120620326.png)

![image-20201227121102794](C:\Users\Olivia\AppData\Roaming\Typora\typora-user-images\image-20201227121102794.png)

![image-20201227121231550](C:\Users\Olivia\AppData\Roaming\Typora\typora-user-images\image-20201227121231550.png)

![image-20201227121326213](C:\Users\Olivia\AppData\Roaming\Typora\typora-user-images\image-20201227121326213.png)

![image-20201227121434777](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201227121434777.png)

- NLTK Naive-Bayes Classifier

![image-20201227121637786](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201227121637786.png)

![image-20201227121837437](C:\Users\Olivia\AppData\Roaming\Typora\typora-user-images\image-20201227121837437.png)

![image-20201227122022909](C:\Users\Olivia\AppData\Roaming\Typora\typora-user-images\image-20201227122022909.png)

![image-20201227122055348](C:\Users\Olivia\AppData\Roaming\Typora\typora-user-images\image-20201227122055348.png)

## Module 4. Semantic Similarity

### WordNet

---

- LCS Similarity

![image-20201229153704744](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201229153704744.png)

- Path Similarity

$$=\frac{1}{Num(path)+1}$$

![image-20201229153420573](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201229153420573.png)

- Lin Similarity

![image-20201229153558618](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201229153558618.png)

### Accomplishment in Python

---

- NLTK Toolkit

```python
import nltk
from nltk.corpus import wordnet as wn 
# wordnet 是nltk里的一个词库

# Find appropriate sense of the words
deer = wn.synset('deer.n.01')
elk = wn.synset('elk.n.01')

```

![image-20201229153830237](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201229153830237.png)

![image-20201229155210773](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201229155210773.png)

- Distributional Similarity (Context related!)

![image-20201229155324848](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201229155324848.png)

![image-20201229155441531](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201229155441531.png)

![image-20201229155543376](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201229155543376.png)

![image-20201229155650180](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201229155650180.png)

![image-20201229155712578](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201229155712578.png)

### Topic Modelling

---

![image-20201229164203153](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201229164203153.png)

### Generative Models and LDA

---

![image-20201229174719744](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201229174719744.png)

![image-20201229175059063](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201229175059063.png)

![image-20201229175458312](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201229175458312.png)

#### LDA

![image-20201229175351463](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201229175351463.png)

![image-20201229175653728](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201229175653728.png)

![image-20201229175810848](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201229175810848.png)

```python
import gensim
from gensim import corpora, models
# REQUIRES: doc_set: preprocessed text document
dictionary = corpora.Dictionary(doc_set)
corpus = [dictionary.doc2bow(doc) for doc in doc_set]
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=4, id2word=dictionary, passes=50)
print(ldamodel.print_topics(num_topics=4, num_words=5))
```

![image-20201229180357013](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201229180357013.png)

### Information Extraction

---

![image-20201229180928382](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201229180928382.png)

![image-20201229181049536](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201229181049536.png)

![image-20201229181331290](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201229181331290.png)

![image-20201229181437983](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201229181437983.png)

![image-20201229181710100](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201229181710100.png)

---

### Tools for Name Entity Recognition

![image-20201229182416086](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201229182416086.png)

![image-20201229182447914](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201229182447914.png)

![image-20201229182635200](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201229182635200.png)

![image-20201229182750146](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201229182750146.png)

![image-20201229182824651](C:\Users\Olivia\Desktop\TODO_LIST\Text_Mining_coursera\lecture_notes\image-20201229182824651.png)