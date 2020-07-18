from .vocabulary import indexesFromSentence, normalizeString
import torch

from gtts import gTTS 
from IPython.display import Audio  


MAX_LENGTH = 10  # Maximum sentence length
device = torch.device("cpu")

def evaluate(searcher, voc, sentence, max_length=MAX_LENGTH):
    try:
        indexes_batch = [indexesFromSentence(voc, sentence)]
        lengths = torch.tensor([len(indexes) for indexes in indexes_batch])
        input_batch = torch.LongTensor(indexes_batch).transpose(0, 1)
        input_batch = input_batch.to(device)
        lengths = lengths.to(device)
        tokens, scores = searcher(input_batch, lengths, max_length)
        decoded_words = [voc.index2word[token.item()] for token in tokens]
        return decoded_words
    except KeyError:
        print("Error: Encountered unknown word.")
        erreur = random.choice(["Sorry, i did not understand you ,Please change the way you say it",
                          "please be a little simple in your discussion i m not a human",
                          "Sorry, get in mind  that you are talking only with a computer "])
        return erreur.split()

# Evaluate inputs from user input (stdin)
def evaluateInput(searcher, voc,input_sentence):
    #input_sentence = ''
    while(1):
        try:

            input_sentence = normalizeString(input_sentence)
            output_words = evaluate(searcher, voc, input_sentence)
            output_words[:] = [x for x in output_words if not (x == 'EOS' or x == 'PAD')]
            engine = gTTS(''.join(output_words))  
            engine.save('a1.wav') 
            Audio('a1.wav', autoplay=True)  
            print('Bot:', ' '.join(output_words))
        except KeyError:
            print("Error: Encountered unknown word.")
            erreur = random.choice(["Sorry, i did not understand you ,Please change the way you say it",
                          "please be a little simple in your discussion i m not a human",
                          "Sorry, get in mind  that you are talking only with a computer "])
            return erreur.split()


