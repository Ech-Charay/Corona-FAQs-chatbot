mkdir -p records/in records/out models
python -m wget -o "/app/models/4000_checkpoint.tar" "https://download.pytorch.org/models/tutorials/4000_checkpoint.tar"
python -m spacy download en_core_web_sm
python /app/cosine_similarity_based_retrieval_chatbot/construct_csv_files.py
