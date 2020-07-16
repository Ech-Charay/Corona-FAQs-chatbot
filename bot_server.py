import os
import numpy as np
import pandas as pd
import speech_recognition as spechrec 
from gtts import gTTS #Import Google Text to Speech

import librosa
from datetime import datetime
import random 

import wave #zdtha
import contextlib #zdtha
import subprocess #zdtha

from cosine_similarity_based_retrieval_chatbot import Processing
from generative_smart_chatbot import GreedySearchDecoder, normalizeString, evaluate, buildModels

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity

from flask import jsonify, request
from werkzeug.utils import secure_filename


class BotServer:
    def __init__(self, file_path):
        """
        Initialize corpus, bag-of-words, and TFIDF from CSV file at argument
        file_path.
        """
        processing = Processing()
        # Read in FAQ data
        self.faq = pd.read_csv(file_path, keep_default_na=False)
        self.corpus = self.faq.question + ' ' + self.faq.answer

        # Create BOW tranformer based on faq.question + faq.answer
        self.bow_transformer = CountVectorizer(analyzer=processing.text_process).fit(self.faq.question)
        # Tranform faq.question itself into BOW
        self.corpus_bow = self.bow_transformer.transform(self.faq.question)

        # Create TFIDF transformer based on faq.question's BOW
        self.tfidf_transformer = TfidfTransformer().fit(self.corpus_bow)
        # Transform faq.question's BOW into TFIDF
        self.corpus_tfidf = self.tfidf_transformer.transform(self.corpus_bow)

        # Initialize search module
        encoder, decoder, decoder_n_layers, self.voc = buildModels()
        self.searcher = GreedySearchDecoder(encoder, decoder,decoder_n_layers)

        # Set upload folder and output records folder
        self.UPLOAD_FOLDER = '/app/records/in'
        self.REC_RES_FOLDER = '/app/records/out'

        # Set allowed extensions
        self.ALLOWED_EXTENSIONS = {'wav'}

    def tfidf_similarity(self, query):
        """
        Returns (index, similarity value) of string argument query's most similar
        match in FAQ, determined by cosine similarity.
        """
        # Transform test question into BOW using BOW transformer
        query_bow = self.bow_transformer.transform([query])
        # Transform test question's BOW into TFIDF
        query_tfidf = self.tfidf_transformer.transform(query_bow)

        # Calculate cosine similarity and return maximum value with accompanying index
        similarities = np.transpose(cosine_similarity(query_tfidf, self.corpus_tfidf))
        max_similarity = similarities.max()
        max_index = np.argmax(similarities)

        return max_index, max_similarity

    def match_query(self, query):
        """
        Prints most similar match in FAQ to user query.
        """
        index, similarity = self.tfidf_similarity(query)

        if similarity > 0.5 :
          response = self.faq.answer.iloc[index]
          print(similarity)
        else :
          query = normalizeString(query)
          output_words = evaluate(self.searcher, self.voc, query)
          output_words[:] = [x for x in output_words if not (x == 'EOS' or x == 'PAD')]
          response = ' '.join(output_words)
       
        return response

    def allowed_file(self, filename):
      return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    def get_duration(self, audio_name_only):
        os.rename(r''+os.path.join(self.REC_RES_FOLDER, audio_name_only + ".wav"),r''+os.path.join(self.REC_RES_FOLDER, audio_name_only+".mp3"))
        subprocess.call(['ffmpeg', '-i', os.path.join(self.REC_RES_FOLDER, audio_name_only+".mp3"), os.path.join(self.REC_RES_FOLDER, audio_name_only + ".wav")])
        fname = os.path.join(self.REC_RES_FOLDER, audio_name_only + ".wav")
        with contextlib.closing(wave.open(fname,'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
        return duration

    def bot_dialog(self, request):
        """
        Given the argument POST request, parse it according to json or form data,
        and return a json response or html template based on sklearn matching
        within the FAQ.
        """
        
        # Handle webhook request
        #.get_json(force=True)
        duration=1
        req = request.form
        msg_type = req.get('type')
        if msg_type == "Text":
          message = req.get('message')
          response_text = self.match_query(message)
          # Return json file as webhook response 
          messages = [
                      {
                          "type": "Text",
                          "message": msg,
                          "fromBot": True
                      }
                      for msg in response_text.split("\n\n")
                      ]
        elif msg_type == "Audio":
          respfilename=''
          record = request.files['record']
          if record and self.allowed_file(record.filename):
            filename = secure_filename(record.filename)
            record.save(os.path.join(self.UPLOAD_FOLDER, filename))
          list_records = []
          durations = []
          try:
            r = spechrec.Recognizer()
            with spechrec.AudioFile(os.path.join(self.UPLOAD_FOLDER, filename)) as source:
              # listen for the data (load audio to memory)
              audio_data = r.record(source)
              # recognize (convert from speech to text)
              input_sentence = r.recognize_google(audio_data)
            #searcher = GreedySearchDecoder(encoder, decoder,decoder_n_layers)
            response_text = self.match_query(input_sentence)
            for msg in response_text.split("\n\n"):
              now = datetime.now()
              respfilename = now.strftime("%d-%m-%Y-%H:%M:%S")
              engine = gTTS('' + response_text)
              engine.save(os.path.join(self.REC_RES_FOLDER, respfilename + ".wav"))
              list_records.append(respfilename + ".wav")
              durations.append(self.get_duration(respfilename))
 
              #durations.append(librosa.get_duration(filename= self.REC_RES_FOLDER + '/' + respfilename))
          except AssertionError as error:
            print(error) 
            erreur = random.choice(["Sorry, i did not understand you ,Please change the way you say it",
                          "please be a little simple in your discussion i m not a human",
                          "Sorry, get in mind  that you are talking only with a computer "])
            print(""+erreur)
            now = datetime.now()
            respfilename = now.strftime("%d-%m-%Y-%H:%M:%S")
            #audio_name_only=now.strftime("%d-%m-%Y-%H:%M:%S")
            #respfilename = audio_name_only + ".wav" 
            engine = gTTS(''+erreur)
            engine.save(os.path.join(self.REC_RES_FOLDER, respfilename + ".wav"))
            list_records.append(respfilename + ".wav")
            durations.append(self.get_duration(respfilename))
            

            #durations.append(librosa.get_duration(filename= self.REC_RES_FOLDER + '/' + respfilename))
            
            #while os.path.isfile(self.REC_RES_FOLDER +'/'+ respfilename) == False:
            #print("file isn't created yet")
            #duration = round(librosa.get_duration(filename= self.REC_RES_FOLDER + '/' + respfilename))

                

            
          #Return json file as webhook response 
          messages = [
                      {
                          "type": "Audio",
                          "path": "https://coronafaqsbot.herokuapp.com/records/"+list_records[i],
                          "isLocal": False,
                          "duration": durations[i],
                          "fromBot": True
                      }
                      for i in range(len(list_records))
                      ]
        return jsonify({"messages": messages})
