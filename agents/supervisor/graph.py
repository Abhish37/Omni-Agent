from typing import Literal
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from agents.state import MultiAgentState
from agents.sql_agent.agent import SQLQueryAgent
from agents.rag_agent.agent import RAGPolicyAgent

class RouterOutput(BaseModel):
    next_agent: Literal["SQLAgent", "RAGAgent", "FINISH"] = Field(
        description="The agent to route the task to. 'SQLAgent' for quantitative data/DB queries. 'RAGAgent' for policy/SOP questions."
    )

class SupervisorGraph:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)
        self.router = self.llm.with_structured_output(RouterOutput)
        
        self.sql_agent = SQLQueryAgent()
        self.rag_agent = RAGPolicyAgent()
        
        self.graph = self._build_graph()

    def supervisor_node(self, state: MultiAgentState) -> dict:
        """
        Evaluates user intent and routes to the correct subagent.
        """
        last_message = state["messages"][-1].content
        
        prompt = f"Determine the appropriate agent to handle this request: '{last_message}'"
        routing_decision = self.router.invoke(prompt)
        
        return {"next_agent": routing_decision.next_agent}

    def _build_graph(self):
        workflow = StateGraph(MultiAgentState)
        
        workflow.add_node("Supervisor", self.supervisor_node)
        workflow.add_node("SQLAgent", self.sql_agent.invoke)
        workflow.add_node("RAGAgent", self.rag_agent.invoke)
        
        workflow.set_entry_point("Supervisor")
        
        # Conditional edges based on Supervisor's 'next_agent' output
        workflow.add_conditional_edges(
            "Supervisor",
            lambda x: x["next_agent"],
            {
                "SQLAgent": "SQLAgent",
                "RAGAgent": "RAGAgent",
                "FINISH": END
            }
        )
        
        # After subagents finish, they set next_agent to FINISH (or back to Supervisor if multi-step)
        workflow.add_edge("SQLAgent", END)
        workflow.add_edge("RAGAgent", END)
        
        return workflow.compile()
