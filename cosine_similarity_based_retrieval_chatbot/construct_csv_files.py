#!/usr/bin/env python3
# Preprocess raw text Excel file into CSV using spaCy to tokenize sentences

import pandas as pd
import unicodedata
import spacy


def preprocess(entry):
    '''
    Normalize string argument entry, remove new line characters,
    add space after '?' chars, and return entry with trailing space.
    '''
    entry = entry.replace('\n', ' ')
    entry = unicodedata.normalize("NFKD", entry)
    entry = entry.replace('?', '? ')
    return entry + ' '


def sentence_tokenize(entry):
    '''
    Tokenize string argument entry into sentences using spaCy,
    then join sentences with double new lines and return as string.
    '''
    doc = nlp(entry)
    sentences = list(doc.sents)
    sentences = '\n\n'.join([(s.text) for s in sentences])
    return sentences

    
def paragraph_tokenize(entry):
    '''
    Tokenize string argument entry into paragraphs,
    then join sentences with double new lines and return as string.
    '''

    bloc = []
    paragraphs = []
    for s in entry.split('\n'):
      if len(s) == 0:
        continue
      elif (s[0] == '-' or s[0] == '*' or s[0] == '+' or (s[0] >= '0' and s[0] <= '9')) :
        bloc.append(s)
      elif len(bloc) != 0:
        paragraphs.append('\n'.join(bloc))
        paragraphs.append(s)
        bloc = []
      else :
        paragraphs.append(s)
    if len(bloc) != 0:
      paragraphs.append('\n'.join(bloc))
    return '\n\n'.join(paragraphs)

if __name__ == '__main__':
    spacy_model = 'en_core_web_sm'
    print('Loading spaCy model', spacy_model, '...')
    nlp = spacy.load(spacy_model)
    print('-Done.')
    faq = pd.read_excel("/app/data/Q&A_COVID-19.xlsx")
    #faq = raw.drop(labels=('Active'), axis=1).dropna()
    #faq.question = faq.question.apply(preprocess)
    #faq.question = faq.question.apply(sentence_tokenize)
    #faq.answer = faq.answer.apply(preprocess)
    #faq.answer = faq.answer.apply(sentence_tokenize)
    faq.answer = faq.answer.apply(paragraph_tokenize)
    faq.to_csv('/app/data/faq-text-preprocessed.csv', index=False)
