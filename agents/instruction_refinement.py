import openai
from utils.text_extraction import parse_refined_instruction_answer

openai.api_type = "azure"
openai.api_base = ""
openai.api_version = "2024-03-01-preview"
openai.api_key = ""
openai.azure_endpoint = ""


def refine_instructions(instruction_answer_pairs, persona, max_rounds=1):
    refined_pairs = instruction_answer_pairs.copy()
    print(refined_pairs)
    for round_number in range(max_rounds):
        print(f"Refinement Round {round_number + 1}")
        new_refined_pairs = []
        for pair in refined_pairs:
            question = pair['Question']
            answer = pair['Answer']
            category= pair['Category']
            
            system_prompt = f"""Refine Q&A pairs to align with relevant personas' expertise and focus areas, ensuring:
                        1. Persona alignment: Match complexity to personas' expertise
                        2. Relevant analysis: Provide insights relevant to personas' focus areas
                        3. Core relevance: Adhere strictly to original content
                        4. Nuanced insights: Offer detailed, insightful analysis
                        """

            user_prompt = f"""Analyze and refine the following question and answer pair, enhancing its quality, complexity, and challenge level while aligning with the specified persona.

        Personas: {persona}
        Category: {category}

        Persona-Based Refinement Guidelines:
            - Role of Personas: Personas will guide the complexity, technical language, and analytical depth used in the refinement. 
            - No Persona Content: Do not introduce persona-specific details or topics into the questions or answers. Personas only influence style and difficulty, not content.
            - Provide analysis relevant to each persona's focus (e.g., Quantitative Analysis for Financial Analysts).

        Here are the Questions and answer that you need to refine:
            Original Question: {question}
            Original Answer: {answer}
            
        Refinement Instructions:
            1. Persona Alignment: Tailor the complexity, technical language, and analytical depth to match the persona's expertise in {category}.
            2. Content Focus: Refine based on the original content without introducing new topics or persona-specific details.
            3. Analytical Depth: Provide nuanced insights and detailed analysis relevant to the persona's interests and concerns.
            4. Clarity and Precision: Ensure refinements are clear, concise, and precise while maintaining depth.
            5. Company Specificity: Generate questions and answers uniquely relevant to the company/organization, avoiding generic responses.
            6. Original Content Adherence: Base all refinements strictly on the given question and answer.

        Output Format:

        Provide your response in plain text, without any special formatting, JSON, or code blocks. Use the following structure:

        Refined Question: [Your refined question]
        Refined Answer: [Your refined answer]
        Persona : [Include the complete details of the single persona used for refinement]

        Strict Rules:
            1. Use only one persona for refinement,matching their expertise to the given category..
            2. Do not introduce external information or concepts not present in the original content.
            3. Maintain the core information while enhancing complexity and analytical depth.
            4. Prioritize clarity and precision in refinements.
            5. Avoid generic questions and answers applicable to all companies.
            6. Do not use any special formatting, JSON, or code blocks in the output.
            7. Ensure that the Persona section in the output contains the exact persona details provided in the input, not the category or any placeholder."""

            sample_interactions="""
            {
            "Refined Question": "How has JPMorgan Chase's dividend payout ratio changed over the past three years, and is it in line with industry standards?"
            "Refined Answer": "JPMorgan Chase's dividend payout ratio has fluctuated over the past three years, with a high of 33% in 2022 and lows of 25% in 2021 and 2023. This indicates a relatively stable dividend policy, with some year-over-year variation. The payout ratio is within a reasonable range, suggesting the firm is balancing dividend payments with reinvesting earnings for growth. Compared to industry standards, the payout ratio is relatively conservative, implying JPMorgan Chase prioritizes retaining capital for strategic initiatives and maintaining a strong capital position."
            "Persona":"Padma is a Financial Analyst who specializes in analyzing SEC reports to support investment decisions and corporate financial planning. She focuses on key sections like the Income Statement, Balance Sheet, Cash Flow Statement, MD&A, and Risk Factors to extract insights on profitability, solvency, liquidity, cash flow, management commentary, and risks. By conducting ratio and trend analysis, comparing historical data and industry benchmarks, and preparing detailed reports, Padma provides insights into a company's financial health, key profitability drivers, revenue and expense trends, and strategic initiatives."
            }"""


            response = openai.chat.completions.create(
                model="gpt-4o",
                temperature=0.20,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                    {"role": "assistant" ,"content": sample_interactions}
                ]
            )

            refined_output = response.choices[0].message.content
            print(f"Refined Output:\n{refined_output}\n")

            # Parse the refined question and answer
            refined_pair = parse_refined_instruction_answer(refined_output)
            if refined_pair:
                new_refined_pairs.append(refined_pair)
            else:
                # If parsing fails, keep the original pair
                new_refined_pairs.append(pair)
        
        # Update the refined pairs for the next round
        refined_pairs = new_refined_pairs
    
    return refined_pairs
