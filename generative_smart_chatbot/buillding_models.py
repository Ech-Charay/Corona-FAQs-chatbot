import os
import torch
import torch.nn as nn

from vocabulary import Voc
from encoder_rnn import EncoderRNN
from attention_decoder import LuongAttnDecoderRNN

def buildModels():
  save_dir = os.path.join("data", "save")
  corpus_name = "cornell movie-dialogs corpus"

  # Configure models
  model_name = 'cb_model'
  attn_model = 'dot'
  #attn_model = 'general'
  #attn_model = 'concat'
  hidden_size = 500
  encoder_n_layers = 2
  decoder_n_layers = 2
  dropout = 0.1
  batch_size = 64

  # If you're loading your own model
  # Set checkpoint to load from
  checkpoint_iter = 4000
  # loadFilename = os.path.join(save_dir, model_name, corpus_name,
  #                             '{}-{}_{}'.format(encoder_n_layers, decoder_n_layers, hidden_size),
  #                             '{}_checkpoint.tar'.format(checkpoint_iter))

  # If you're loading the hosted model
  loadFilename = '../models/4000_checkpoint.tar'

  # Load model
  # Force CPU device options (to match tensors in this tutorial)
  device = torch.device('cpu')
  checkpoint = torch.load(loadFilename, map_location=device)
  encoder_sd = checkpoint['en']
  decoder_sd = checkpoint['de']
  encoder_optimizer_sd = checkpoint['en_opt']
  decoder_optimizer_sd = checkpoint['de_opt']
  embedding_sd = checkpoint['embedding']
  voc = Voc(corpus_name)
  voc.__dict__ = checkpoint['voc_dict']


  print('Building encoder and decoder ...')
  # Initialize word embeddings
  embedding = nn.Embedding(voc.num_words, hidden_size)
  embedding.load_state_dict(embedding_sd)
  # Initialize encoder & decoder models
  encoder = EncoderRNN(hidden_size, embedding, encoder_n_layers, dropout)
  decoder = LuongAttnDecoderRNN(attn_model, embedding, hidden_size, voc.num_words, decoder_n_layers, dropout)
  # Load trained model params
  encoder.load_state_dict(encoder_sd)
  decoder.load_state_dict(decoder_sd)
  # Use appropriate device
  encoder = encoder.to(device)
  decoder = decoder.to(device)
  # Set dropout layers to eval mode
  encoder.eval()
  decoder.eval()
  print('Models built and ready to go!')
  return encoder, decoder
