from utils.text_extraction import parse_instruction_answer_pairs
import openai

openai.api_type = "azure"
openai.api_base = ""
openai.api_version = "2024-03-01-preview"
openai.api_key = ""
openai.azure_endpoint = ""


def generate_instructions(transformed_contents):
    instruction_answer_pairs = []
    for item in transformed_contents:
        
        system_prompt = """As an AI expert, generate high-quality question-answer pairs based on provided content, ensuring:
        1.Full support from given information
        2.Critical thinking and deep understanding
        3.Medium to advanced difficulty levels
        4.Specific, targeted questions avoiding broad inquiries

        Guidelines:
        -No external knowledge or assumptions beyond provided content
        -Direct derivation from and relevance to provided text
        -Varied cognitive processes (recall, analysis, evaluation)
        -Nuanced questions testing comprehension within provided context.
        -Generate questions and answers that are uniquely relevant to company/organization, avoiding generic responses applicable to all companies."""
        
        instruction_taxonomy = """
        1. Abstractive: Reasoning and inference
        2. Aggregative: Summarization, grouping, or quantitative analysis.
        3. Numeric
        """
        
        user_prompt = f"""
        Generate diverse question-answer pairs based solely on the provided content, adhering to guidelines and {instruction_taxonomy}.

        Content: {item['content']}

        Instructions:
            -Vary complexity levels and cognitive processes
            -Limit questions and answers to explicit or directly implied content
            -Craft concise, comprehensive answers
            -Specify question type from taxonomy
            -Provide crisp, concise answers
            -Categories each Questions and answer pairs in category of -Financial Health Analyzer, Investment Viability Evaluator, Creditworthiness Assessor, Retail Investor Guide, Departmental Performance Analyzer, Regulatory Compliance Checker
            -Generate questions and answers that are uniquely relevant to company/organization, avoiding generic responses applicable to all companies.
            
            
        output Format:
            Category: [Specify category]
            Question: [Generated question]
            Answer: [Answer based on content]
        """


        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                #{"role": "assistant" ,"content": sample_interactions},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.24
        )

        generated_pairs = response.choices[0].message.content
        print(generated_pairs)
        pairs = parse_instruction_answer_pairs(generated_pairs)
        instruction_answer_pairs.extend(pairs)
    
    return instruction_answer_pairs
