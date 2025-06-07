customer_support_reflection_prompt = """
You are analyzing a customer support conversation to create a memory that improves future support interactions. Your job is to extract the most helpful insights and strategies that will guide similar future conversations.

Follow these rules:

1. Use "N/A" if the information is unavailable or irrelevant
2. Be concise—each field should be one clear, actionable sentence
3. Focus only on patterns that can improve future support outcomes
4. Use specific but reusable context tags (e.g., "refund_request", "billing_issue", "login_problem")

Output valid JSON in this format:
{
    "context_tags": [
        string
    ],
    "conversation_summary": string,
    "what_worked": string,
    "what_to_avoid": string
}

Examples:
- Good context_tags: ["subscription_cancelation", "account_verification"]
- Bad context_tags: ["support_chat", "customer_question"]

- Good conversation_summary: "Resolved subscription cancelation by guiding user to self-service portal"
- Bad conversation_summary: "Talked about canceling account"

- Good what_worked: "Empathizing with frustration and clearly outlining next steps"
- Bad what_worked: "Gave clear answers"

- Good what_to_avoid: "Asking for account info before confirming user identity"
- Bad what_to_avoid: "Delayed the response"

Do not include any text outside the JSON object in your response.

Here is the prior conversation:

{conversation}
"""

code_assistant_reflection_prompt = """
You are analyzing a technical coding conversation to create a memory reflection that improves future developer support. Extract insights that will help handle similar programming discussions more effectively.

Follow these rules:

1. Use "N/A" for any missing or irrelevant info
2. Each sentence must be concise, clear, and actionable
3. Use specific tags (e.g., "python_typing", "react_hooks", "bugfixing")

Return only this JSON format:
{
    "context_tags": [
        string
    ],
    "conversation_summary": string,
    "what_worked": string,
    "what_to_avoid": string
}

Examples:
- Good context_tags: ["python_asyncio", "error_traceback", "state_management"]
- Bad context_tags: ["coding", "debugging"]

- Good conversation_summary: "Fixed async await bug in Python by wrapping coroutine in asyncio.run"
- Bad conversation_summary: "Helped fix Python bug"

- Good what_worked: "Walking through traceback line by line with user"
- Bad what_worked: "Explained error"

- Good what_to_avoid: "Suggesting advanced syntax before confirming basic familiarity"
- Bad what_to_avoid: "Confused the user"

Do not include any text outside the JSON object in your response.

Here is the prior conversation:

{conversation}
"""

ecommerce_support_reflection_prompt = """
You are analyzing a customer support conversation in an e-commerce setting to create a memory reflection that enhances future support interactions. Extract insights that will help handle similar customer queries more effectively.

Follow these rules:

1. Use "N/A" for any missing or irrelevant info
2. Each sentence must be concise, clear, and actionable
3. Use specific tags (e.g., "order_tracking", "payment_issue", "return_policy")

Return only this JSON format:
{
    "context_tags": [
        string
    ],
    "conversation_summary": string,
    "what_worked": string,
    "what_to_avoid": string
}

Examples:
- Good context_tags: ["order_tracking", "refund_process", "shipping_delay"]
- Bad context_tags: ["customer_support", "complaint"]

- Good conversation_summary: "Guided customer through refund process for delayed shipment"
- Bad conversation_summary: "Helped customer with order"

- Good what_worked: "Providing clear step-by-step instructions on tracking order status"
- Bad what_worked: "Explained the refund"

- Good what_to_avoid: "Using jargon like 'RMA' without explanation"
- Bad what_to_avoid: "Customer was upset"

Do not include any text outside the JSON object in your response.

Here is the prior conversation:

{conversation}
"""

energy_mgmt_support_reflection_prompt = """
You are analyzing a customer support conversation related to energy management systems to create a memory reflection that improves future technical support. Extract key insights to better handle similar technical or billing inquiries.

Follow these rules:

1. Use "N/A" for any missing or irrelevant info
2. Each sentence must be concise, clear, and actionable
3. Use specific tags (e.g., "meter_reading", "billing_dispute", "energy_consumption")

Return only this JSON format:
{
    "context_tags": [
        string
    ],
    "conversation_summary": string,
    "what_worked": string,
    "what_to_avoid": string
}

Examples:
- Good context_tags: ["smart_meter", "energy_consumption", "billing_error"]
- Bad context_tags: ["customer_support", "energy"]

- Good conversation_summary: "Resolved billing dispute by explaining meter reading process"
- Bad conversation_summary: "Helped customer with bill"

- Good what_worked: "Using visual aids to explain consumption patterns"
- Bad what_worked: "Provided good support"

- Good what_to_avoid: "Assuming technical knowledge without verification"
- Bad what_to_avoid: "Customer was confused"

Do not include any text outside the JSON object in your response.

Here is the prior conversation:

{conversation}
"""
academic_research_reflection_prompt = """
You are analyzing conversations about research papers to create memories that will help guide future interactions. Your task is to extract key elements that would be most helpful when encountering similar academic discussions in the future.

Review the conversation and create a memory reflection following these rules:

1. For any field where you don't have enough information or the field isn't relevant, use "N/A"
2. Be extremely concise - each string should be one clear, actionable sentence
3. Focus only on information that would be useful for handling similar future conversations
4. Context_tags should be specific enough to match similar situations but general enough to be reusable

Output valid JSON in exactly this format:
{{
    "context_tags": [              // 2-4 keywords that would help identify similar future conversations
        string,                    // Use field-specific terms like "deep_learning", "methodology_question", "results_interpretation"
        ...
    ],
    "conversation_summary": string, // One sentence describing what the conversation accomplished
    "what_worked": string,         // Most effective approach or strategy used in this conversation
    "what_to_avoid": string        // Most important pitfall or ineffective approach to avoid
}}

Examples:
- Good context_tags: ["transformer_architecture", "attention_mechanism", "methodology_comparison"]
- Bad context_tags: ["machine_learning", "paper_discussion", "questions"]

- Good conversation_summary: "Explained how the attention mechanism in the BERT paper differs from traditional transformer architectures"
- Bad conversation_summary: "Discussed a machine learning paper"

- Good what_worked: "Using analogies from matrix multiplication to explain attention score calculations"
- Bad what_worked: "Explained the technical concepts well"

- Good what_to_avoid: "Diving into mathematical formulas before establishing user's familiarity with linear algebra fundamentals"
- Bad what_to_avoid: "Used complicated language"
Additional examples for different research scenarios:

Context tags examples:
- ["experimental_design", "control_groups", "methodology_critique"]
- ["statistical_significance", "p_value_interpretation", "sample_size"]
- ["research_limitations", "future_work", "methodology_gaps"]

Conversation summary examples:
- "Clarified why the paper's cross-validation approach was more robust than traditional hold-out methods"
- "Helped identify potential confounding variables in the study's experimental design"

What worked examples:
- "Breaking down complex statistical concepts using visual analogies and real-world examples"
- "Connecting the paper's methodology to similar approaches in related seminal papers"

What to avoid examples:
- "Assuming familiarity with domain-specific jargon without first checking understanding"
- "Over-focusing on mathematical proofs when the user needed intuitive understanding"

Do not include any text outside the JSON object in your response.

Here is the prior conversation:

{conversation}
"""
