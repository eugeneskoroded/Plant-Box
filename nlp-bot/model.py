from gpt4all import GPT4All


class GPT:
    def __init__(self, name):
        self.gpt = GPT4All(name)
        
    def get_response(self, text):
        messages = [{"role": "user", "content": text}]
        response =self.gpt.chat_completion(messages, default_prompt_header=False)
        return response['choices'][0]['message']['content'].strip()