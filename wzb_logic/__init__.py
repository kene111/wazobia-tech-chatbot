import os
from flask import Flask
from flask_cors import CORS
from langchain.llms import Cohere
from .language_bot import WazobiaBot
from langchain.vectorstores import FAISS
from .config.deploy_config import config
from .config.wzb_config import WZBConfig
from langchain.embeddings import HuggingFaceEmbeddings

os.environ["COHERE_API_KEY"] = os.getenv('COHERE_API_KEY')


def create_app(env_config=None):
    # instantiate the app
    app = Flask(__name__)
    cors = CORS(app)

    ###### ENVIROMENT VARIABLE CONFIGURATION #######################
    if env_config is None:
        env_config = os.getenv("PROD_APP_SETTINGS", "development")
    app.config.from_object(config[env_config])

    ###### MODEL INITIALIZATION #####################################
    WZBConfig.model = Cohere()
    model_id = 'sentence-transformers/all-MiniLM-L12-v2'#'sentence-transformers/all-MiniLM-L6-v2'
    model_kwargs = {'device': 'cpu'}
    WZBConfig.embedding_model = HuggingFaceEmbeddings(
            model_name=model_id,
            model_kwargs=model_kwargs
        )
    ###### VECTOR STORE INITIALIZATION ##############################
    WZBConfig.vector_store = FAISS.load_local(WZBConfig.vector_store_path, WZBConfig.embedding_model)

    ##### REGISTER REFLECTLY_LLM BLUEPRINT ENDPOINTS ################
    from .wzb_connect import wzb_endpoints
    app.register_blueprint(wzb_endpoints)

    ########################### WZB CUSTOMER SERVICE BOT ##########################
    WZBConfig.bot  = WazobiaBot()

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app}
    return app
