from app.enums import Priority

SUMMARIZE_PROMPT = """\
Summarize the following text.
Style: {style}
Maximum Length: {max_length} characters.
Text: {text}
Summary:\
"""

EXTRACT_PROMPT = """\
Extract the following information from the text.

Text: {text}
Customer:
Company:
Issue in max 10 words:
Priority: only in [low,medium,high,critical]
Output Format should be in json:
{{"customer": "<customer name>", "company": "<company name>", "issue": "<issue description>", "priority": "<priority level>"}}
"""

CLASSIFY_PROMPT = """\
    Classify the issue category(billing,technical,security,account,feature_request,other) with confidence by analyzing the examples below.

    Example 1:
    Text: I was charged twice for my subscription.
    Answer: {{category: billing, confidence: 0.97}}

    Example 2:
    Text: I am stuck on page and the loader is keeps loading after payment
    Answer: {{category: technical, confidence: 0.90}}

    Example 3:
    Text: I am not able to login since morning
    Answer: {{category: account, confidence: 0.87}}

    Example 4:
    Text: My password reset link is not working
    Answer: {{category: security, confidence: 0.87}}

    Example 5:
    Text: I am not able to add my credit card in the payment section the card type isn't available in the list 
    Answer: {{category: feature_request, confidence: 0.75}}

    Text: {text}
    Answer: {{"category": "<category>", "confidence": <confidence>}}
"""


GENERATE_PROMPT = """\
    You are a {role} writer specialized in {domain} domain
    Explain the user about {topic}
    The content should be understandable to {audience} 
    tone should be {tone}
    Length: {length}

    Output Format: {{ "content": "<content>" }}
    """

COMPANY_POLICY_PROMPT = """
    Context: {context}
    Question: {question}
    Answer:
"""

SYSTEM_PROMPT = """
     You are a company policy assistant. Answer the question based on the context provided.
    If the answer cannot be found in the context, say: "I don't have enough information to answer that."
    """
