# wazobia-tech-chatbot

## Introduction & Aim:
The Wazobia tech chatbot is a simple first responder automated chat service that answers basic to mid level questions regarding wazobia tech.

## Development Process:
1.  Information curation.
2.  RAG - based Information retrival development.
3.  Software development and deployment.

### Information curation:
This process entailed gathering information a web user would be interested in regarding wazobia tech. The content of the data was collected from the companys [web](https://wazobia.tech/) page. Link to curated [data](https://docs.google.com/document/d/1HkT6knWZ0iBJz_eZp8dHf4sTrX0fYld8-NQ4RpdeH4k/edit?usp=sharing).

### RAG - based Information retrival development:
Large Language models are deep learning algorithms based on the transformer architecture trained on an extremely large corpus of properly pre-processed real word data curated within a specified time frame. Although
the advantages of these models are endless, there are two draw backs; the first being that these models are too generalised they don't do so well on questions demanding specific knowledge. The other being that since
the curated data is within a time frame, information requring knowledge outside the timeframe would be give incorrect responses.

RAG which stands for Retrieval Augmented Generation, is one of the methods that is used to solve the issues explained above. This process accesses specific information stored in a location (ideally a vector database), and then uses the power of the 
language model to generate the adequate response to the question or query asked. For this project  ```FAISS``` was used as the vector database, and huggingface ```sentence-transformers/all-MiniLM-L6-v2``` embedding model.

### Software development and deployment:
The chatbot application is served as an api endpoint using flask as the web framework.

## Repository Breakdown:
1. ```wzb_logic/config```: This folder contains both system and deployment configurations.
2. ```wzb_logic/vector_db```: This folder contains the serialized vector database.
3. ```wzb_logic/language_bot.py```: This script contains bot logic.
4. ```wzb_logic/wzb_connect.py```: This script contains the flask blueprint endpoints.
5. ```wzb_logic/__init__.py```: Flask application factory configuration.
6. ```app.py```: Runs the flask application.
7. ```requirements.txt```: Requirement file.
