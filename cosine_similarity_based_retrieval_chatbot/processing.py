import string
from sklearn.feature_extraction import stop_words
from nltk.stem import WordNetLemmatizer
import nltk

class Processing:
  def __init__(self):
    print("init processing")
    nltk.download('wordnet')

  def lem(self, words):
      """Returns list of lemmas from argument list of words."""
      wordnet_lemmatizer = WordNetLemmatizer()
      lem_sentence = []
      for word in words:
          lem_sentence.append(wordnet_lemmatizer.lemmatize(word))
      return lem_sentence


  def text_process(self, mess, lemmas=True):
      """
      Returns list of tokenized lemmas in argument string mess, with stopwords,
      punctuation removed.
      """
      clean = [char if char not in string.punctuation else ' ' for char in mess]
      clean = ''.join(clean)
      clean = [word.lower() for word in clean.split() if word.lower()
              not in stop_words.ENGLISH_STOP_WORDS]
      
      if lemmas:
          clean = self.lem(clean)
          
      return clean