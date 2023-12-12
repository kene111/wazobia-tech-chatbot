import os
from dotenv import load_dotenv
load_dotenv()

class WZBConfig:
    """
    Wazobia configuration class.
    """
    stage = os.getenv('STAGE')
   
    model = None
    embedding_model = None
    vector_store = None
    vector_store_path = "wzb_logic/vector_db/wzb_faiss_index"
    
    bot  =  None
    
    if stage == "DEV":        
        mongodb_path = "mongodb://127.0.0.1:27017"
    elif stage == "PROD":
        mongodb_path = os.getenv('DATABASE_URL')
        

    
    
    





