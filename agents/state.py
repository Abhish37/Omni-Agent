from typing import TypedDict, Annotated, Sequence, Optional
from langchain_core.messages import BaseMessage
import operator

class MultiAgentState(TypedDict):
    """
    Rigid shared state schema that flows through the LangGraph nodes.
    Ensures multi-turn memory without token bloat.
    """
    # The entire conversation history
    messages: Annotated[Sequence[BaseMessage], operator.add]
    
    # The subagent assigned by the supervisor
    next_agent: Optional[str]
    
    # Optional metadata extracted during routing
    extracted_entities: Optional[dict]
    
    # The final output generated for the user
    final_response: Optional[str]
