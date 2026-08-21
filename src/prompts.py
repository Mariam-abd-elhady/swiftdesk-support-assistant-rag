def get_prompt_instruction(prompt_style):

    if prompt_style == "few_shot":
        return """
Use the retrieved examples as guidance.
Follow their helpful style, but do not copy
irrelevant information.
"""

    if prompt_style == "reasoned":
        return """
Analyze the customer's issue internally.
Identify the main problem and the safest
appropriate support response.
Do not reveal your internal reasoning.
Only provide the final reply.
"""

    return """
Write a concise and professional support reply.
"""