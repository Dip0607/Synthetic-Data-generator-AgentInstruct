import openai

openai.api_type = "azure"
openai.api_base = "https://<your-endpoint>.openai.azure.com/"
openai.api_version = "2024-03-01-preview"
openai.api_key = "<your-key>"
openai.azure_endpoint = ""

class BaseAgent:
    def __init__(self, name, system_prompt, user_prompt_template):
        self.name = name
        self.system_prompt = system_prompt
        self.user_prompt_template = user_prompt_template

    def process(self, text):
        # Format the user prompt with the provided text
        user_prompt = self.user_prompt_template.format(text=text)
        
        # Use OpenAI API to process the text
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        

        content  = response.choices[0].message.content

        transformed_contents = [{
            'type': self.name.lower().replace(' ', '_'),
            'content': content
        }]
        return transformed_contents