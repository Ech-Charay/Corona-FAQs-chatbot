mkdir -p records/in records/out models
python -m wget -o "/app/models/4000_checkpoint.tar" "https://download.pytorch.org/models/tutorials/4000_checkpoint.tar"
heroku ps:copy /app/models/4000_checkpoint.tar --app=coronafaqsbot --output=/app/models/4000_checkpoint.tar
