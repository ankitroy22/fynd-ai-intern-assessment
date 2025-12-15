USER_RESPONSE_PROMPT = """
You are a professional customer support assistant.

Write a short, natural response to the customer review below.

STRICT RULES:
- Do NOT ask the customer any questions
- Do NOT request additional information or contact
- Do NOT use sales or marketing language
- Keep the response to 1–2 sentences
- Match the tone to the star rating

Tone guidelines:
- 1–2 stars: Apologetic and empathetic
- 3 stars: Neutral and appreciative
- 4–5 stars: Warm and appreciative

Rating: {rating}
Review: {review}

Write only the response message.
"""



SUMMARY_PROMPT = """
Summarize the following customer review in 1–2 concise sentences.

Review:
{review}
"""

ACTIONS_PROMPT = """
You are a business analyst.

Based on the customer review below, suggest 2–4 clear actions
the business should take to address the feedback.

Review:
{review}

Return the actions as bullet points.
"""
