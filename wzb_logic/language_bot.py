import os
from .config.wzb_config import WZBConfig
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.memory import MongoDBChatMessageHistory
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT

class WazobiaBot:
    """Answers users questions regarding wazobia tech.
        
    Attributes
    ----------      
    model : object
       Model Class object.

    prompt_template: str
        Base prompt template for conversations.

    chat_template: str
        Conversation structure template.

    chat_prompt_template: str
        Full Model prompt.


    user_request_info : dict
       User request information.

    qst_chain : object
        LangChain LLMChain Object
      
    user_session_identifier : str
       Unique identifier for a conversation between user and llm.

   
    wazobia_db_name : str
        wazobia DB name.

    vector_store: object
        Faiss class object.

    Methods
    -------
    set_user_request_info
        Sets the user resquests to the class user_request_info attribute.
        
    construct_user_session_identifier
        Creates the identifier tag used in creating a session and storing conversation on the chat db.

    create_message_history_memory_db
        Sets the message history for the user and llm.

    _setup_model_question_chain
        Setup the model language chain for question answering.

    answer_question
        Runs the process of answering a users question.
    """

    def __init__(self):
        self.model = WZBConfig.model
        self.user_request_info = None
        self.vector_store = WZBConfig.vector_store
        self.qst_chain = None
        self.user_session_identifier = None
        self.prompt_template = """
                                You are the first line of customer service at wazobia tech, you are a very warm, kind, and understanding customer service attendant.
                                Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.  
                                Answer the question to the best of your own knowledge about wazobia tech."
                               """
        self.chat_template = """
                            Chat History:
                            {chat_history}
                            Follow Up Input: {question}
                            Standalone question:
                            """
        self.chat_prompt_template = self.prompt_template + "\n" + self.chat_template
        self.wazobia_db_name = "user_sessions"

    def set_user_request_info(self, user_request_info):
        """Sets the user resquests to the class user_request_info attribute.
        
        Parameters
        ----------
        
        Returns
        -------
        """
        self.user_request_info = user_request_info

    def construct_user_session_identifier(self):
        """Creates the identifier tag used in creating a session and storing conversation on the chat db.
        
        Parameters
        ----------
        
        Returns
        -------
        """

        if self.user_request_info == None:
           return None
        else:

            # Extract user Information
            user_id  = self.user_request_info["unique_id"]
            # construct user session identifier for each lecture
            self.user_session_identifier = f"usr_{user_id}_session"
            return 

    def create_message_history_memory_db(self):
        """Sets the message history for the user and llm.
        
        Parameters
        ----------
        
        Returns
        -------
        """
        message_history = MongoDBChatMessageHistory(
            connection_string = WZBConfig.mongodb_path, 
            session_id = f"{self.user_session_identifier}", 
            database_name = self.wazobia_db_name 
        )

        memory = ConversationBufferMemory(
            memory_key="chat_history", chat_memory=message_history, return_messages=True
        )

        return memory
        
    def _setup_model_question_chain(self):
        """Setup the model language chain for question answering.

        Parameters
        ----------
        Returns
        -------
        """    
        memory = self.create_message_history_memory_db()
        INTERACTIONS_PROMPT = PromptTemplate.from_template(self.chat_prompt_template)
        self.qst_chain = ConversationalRetrievalChain.from_llm(
                self.model,
                self.vector_store.as_retriever(),
                condense_question_prompt=INTERACTIONS_PROMPT,
                memory=memory,
                get_chat_history=lambda h : h[:20]
            )
        return 


    
    def answer_question(self):
        """Runs the process of answering a users question.
        
        Parameters
        ----------
        
        Returns
        -------
        result: str
            models response
        """

        self.construct_user_session_identifier()
        self._setup_model_question_chain()
        
        query = self.user_request_info["query"]
        result = self.qst_chain({"question": query})
        result = result['answer']
        return result
            