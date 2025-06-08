procedural_prompt = f"""You are maintaining a continuously updated list of the most important procedural behavior instructions for an AI assistant. Your task is to refine and improve a list of key takeaways based on new conversation feedback while maintaining the most valuable existing insights.

    CURRENT TAKEAWAYS:
    {current_takeaways}

    NEW FEEDBACK:
    What Worked Well:
    {what_worked}

    What To Avoid:
    {what_to_avoid}

    Please generate an updated list of up to 10 key takeaways that combines:
    1. The most valuable insights from the current takeaways
    2. New learnings from the recent feedback
    3. Any synthesized insights combining multiple learnings

    Requirements for each takeaway:
    - Must be specific and actionable
    - Should address a distinct aspect of behavior
    - Include a clear rationale
    - Written in imperative form (e.g., "Maintain conversation context by...")

    Format each takeaway as:
    [#]. [Instruction] - [Brief rationale]

    The final list should:
    - Be ordered by importance/impact
    - Cover a diverse range of interaction aspects
    - Focus on concrete behaviors rather than abstract principles
    - Preserve particularly valuable existing takeaways
    - Incorporate new insights when they provide meaningful improvements

    Return up to but no more than 10 takeaways, replacing or combining existing ones as needed to maintain the most effective set of guidelines.
    Return only the list, no preamble or explanation.
    """
