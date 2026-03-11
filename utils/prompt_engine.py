def generate_prompt(order):

    content_type = order["content_type"]

    structure = ""

    if content_type == "Blog Article":
        structure = """
• Title
• Introduction
• H2 Sections
• H3 Subsections
• Bullet Points
• Examples
• FAQ
• Conclusion
"""

    elif content_type == "SEO Landing Page":
        structure = """
• Headline
• Value Proposition
• Product/Service Explanation
• Benefits
• Features
• Social Proof
• Call To Action
"""

    elif content_type == "Comparison Page":
        structure = """
• Introduction
• Comparison Table
• Feature Analysis
• Pros and Cons
• Best Use Cases
• Final Recommendation
"""

    elif content_type == "Tool Page":
        structure = """
• Tool Overview
• Features
• Use Cases
• Benefits
• Step-by-Step Usage
"""

    elif content_type == "Directory Page":
        structure = """
• Category Introduction
• List of Resources
• Short Descriptions
• Use Case Suggestions
"""

    elif content_type == "Essay":
        structure = """
• Title
• Introduction with Thesis
• Argument Sections
• Supporting Evidence
• Conclusion
"""

    elif content_type == "Speech":
        structure = """
• Opening Hook
• Main Message
• Supporting Points
• Storytelling Elements
• Closing Statement
"""

    elif content_type == "Debate Script":
        structure = """
• Opening Statement
• Main Arguments
• Counterarguments
• Rebuttal
• Closing Statement
"""

    elif content_type == "Official Letter":
        structure = """
• Sender
• Recipient
• Greeting
• Body Message
• Closing
"""

    elif content_type == "FAQ Page":
        structure = """
• Introduction
• List of Questions
• Clear Answers
• Additional Tips
"""

    elif content_type == "Educational Guide":
        structure = """
• Topic Overview
• Step-by-Step Sections
• Examples
• Best Practices
• Key Takeaways
"""

    prompt = f"""
You are a professional editorial production team.

CONTENT REQUEST

Content Type: {order['content_type']}
Topic: {order['topic']}
Audience: {order['audience']}
Purpose: {order['purpose']}
Tone: {order['tone']}
Length: {order['length']}
Keywords: {order['keywords']}
Tier: {order['tier']}

CONTENT STRUCTURE

{structure}

CONTENT TIER INSTRUCTIONS

Tier 1:
Basic article only.

Tier 2:
Article + SEO metadata + FAQ.

Tier 3:
Article + SEO + Visual suggestions + Repurposing content.

OUTPUT FORMAT

ARTICLE CONTENT

[Write the full content]

SEO GUIDE

Meta Title
Meta Description
URL Slug
Keyword Suggestions

VISUAL CONTENT IDEAS

Image Ideas
Chart Suggestions
Diagram Suggestions

CONTENT REPURPOSING

LinkedIn Post
Twitter Thread
Newsletter Summary
"""

    return prompt
