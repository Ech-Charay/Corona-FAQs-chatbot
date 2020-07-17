from .vocabulary import indexesFromSentence, normalizeString
import torch

from gtts import gTTS #Import Google Text to Speech
from IPython.display import Audio  


MAX_LENGTH = 10  # Maximum sentence length
device = torch.device("cpu")

def evaluate(searcher, voc, sentence, max_length=MAX_LENGTH):
    try:
        ### Format input sentence as a batch
        # words -> indexes
        indexes_batch = [indexesFromSentence(voc, sentence)]
        # Create lengths tensor
        lengths = torch.tensor([len(indexes) for indexes in indexes_batch])
        # Transpose dimensions of batch to match models' expectations
        input_batch = torch.LongTensor(indexes_batch).transpose(0, 1)
        # Use appropriate device
        input_batch = input_batch.to(device)
        lengths = lengths.to(device)
        # Decode sentence with searcher
        tokens, scores = searcher(input_batch, lengths, max_length)
        # indexes -> words
        decoded_words = [voc.index2word[token.item()] for token in tokens]
        return decoded_words
    except KeyError:
        print("Error: Encountered unknown word.")
        return "I didn't understand you correctly, you may have written a word wrong. Please correct your language!"

# Evaluate inputs from user input (stdin)
def evaluateInput(searcher, voc,input_sentence):
    #input_sentence = ''
    while(1):
        try:
            # Get input sentence
            #input_sentence = input('> ')
            # Check if it is quit case
            #if input_sentence == 'q' or input_sentence == 'quit': break
            # Normalize sentence
            input_sentence = normalizeString(input_sentence)
            # Evaluate sentence
            output_words = evaluate(searcher, voc, input_sentence)
            # Format and print response sentence
            output_words[:] = [x for x in output_words if not (x == 'EOS' or x == 'PAD')]
            engine = gTTS(''.join(output_words))  
            engine.save('a1.wav') 
            Audio('a1.wav', autoplay=True)  
            print('Bot:', ' '.join(output_words))
        except KeyError:
            print("Error: Encountered unknown word.")
            return "I didn't understand you correctly, you may have written a word wrong. Please correct your language!"



# Evaluate inputs from user input (stdin)
def evaluateInput2(searcher, voc):
  input_sentence = ''
  try:
    # Get input sentence
    input_sentence = input('> ')
    # Check if it is quit case
    # Normalize sentence
    input_sentence = normalizeString(input_sentence)
    # Evaluate sentence
    output_words = evaluate(searcher, voc, input_sentence)
    # Format and print response sentence
    output_words[:] = [x for x in output_words if not (x == 'EOS' or x == 'PAD')]
    print('Bot:', ' '.join(output_words))
    bot_answer=' '.join(output_words)
    engine = gTTS(''+bot_answer)  
    engine.save('a1.wav') 
  except KeyError:
    print("Error: Encountered unknown word.")
    return "I didn't understand you correctly, you may have written a word wrong. Please correct your language!"






# Normalize input sentence and call evaluate()
def evaluateExample(sentence, searcher, voc):
    try:
        print("> " + sentence)
        # Normalize sentence
        input_sentence = normalizeString(sentence)
        # Evaluate sentence
        output_words = evaluate(searcher, voc, input_sentence)
        output_words[:] = [x for x in output_words if not (x == 'EOS' or x == 'PAD')]
        print('Bot:', ' '.join(output_words))
    except KeyError:
        print("Error: Encountered unknown word.")
        return "I didn't understand you correctly, you may have written a word wrong. Please correct your language!"
