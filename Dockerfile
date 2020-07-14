# Use an official Python runtime as a parent image
FROM python:3.7.2-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt
RUN pip install python-dotenv
RUN python -m nltk.downloader wordnet
RUN python -m wget -o "/app/models/4000_checkpoint.tar" "https://download.pytorch.org/models/tutorials/4000_checkpoint.tar"

# Set environmental variables
ENV FLASK_APP=main.py
ENV FLASK_ENV=development

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run main.py when the container launches
CMD ["python", "main.py"]
