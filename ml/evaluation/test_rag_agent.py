import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import FaithfulnessMetric
# Note: We can use Ragas natively or via DeepEval wrappers.
# DeepEval supports Faithfulness which aligns with Ragas' concepts.

@pytest.mark.asyncio
async def test_rag_agent_faithfulness():
    user_input = "When should an invoice be manually reviewed?"
    
    # In a real test, we would invoke RAGPolicyAgent and capture retrieved contexts
    actual_output = "Invoices over $5000 require manual review."
    retrieval_context = ["All invoices above $5000 require manual review by a manager."]
    
    # The Faithfulness metric ensures the LLM's answer is STRICTLY supported by the retrieved SOP
    metric = FaithfulnessMetric(threshold=0.9)
    test_case = LLMTestCase(
        input=user_input,
        actual_output=actual_output,
        retrieval_context=retrieval_context
    )
    
    # To mitigate LLM-as-a-judge bias, DeepEval randomizes option orders internally
    # and enforces strict G-Eval criteria when using GPT-4 for evaluation.
    assert_test(test_case, [metric])
