from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI
from agents.state import MultiAgentState
from backend.core.config import settings

class SQLQueryAgent:
    def __init__(self):
        # Establish a read-only database connection
        # (Assuming the main URI works, ideally use a specific read-only user/URI)
        self.db = SQLDatabase.from_uri(settings.SQLALCHEMY_DATABASE_URI)
        
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)
        
        self.agent = create_sql_agent(
            llm=self.llm,
            toolkit=None,  # We would inject SQLDatabaseToolkit here
            db=self.db,
            agent_type="openai-tools",  # Works with Gemini tool calling too
            verbose=True,
            handle_parsing_errors=True
        )

    def invoke(self, state: MultiAgentState) -> dict:
        """
        Takes the state, queries the database, and returns updated state messages.
        """
        # We only pass the latest user query to prevent token bloat
        last_message = state["messages"][-1].content
        
        # Self-correction is inherently handled by LangChain's SQL agent handle_parsing_errors
        response = self.agent.invoke({"input": last_message})
        
        # Update the state with the SQL agent's findings
        return {
            "final_response": response["output"],
            "next_agent": "FINISH"  # Route back to supervisor or end
        }
