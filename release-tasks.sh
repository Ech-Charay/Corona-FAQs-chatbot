wget "https://download.pytorch.org/models/tutorials/4000_checkpoint.tar"
python -m spacy download en_core_web_sm
python ./cosine_similarity_based_retrieval_chatbot/construct_csv_files
python ./generative_smart_chatbot/buillding_models
mkdir -p records/in records/out
