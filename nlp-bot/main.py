from functions import Translating, get_category_info, create_plants_information
from flask import Flask, request, jsonify
from model import GPT
from name_detector import get_plants

app = Flask(__name__)
print(1)
gptj = GPT("ggml-gpt4all-j-v1.3-groovy")
print(1)
tr = Translating()
print(1)


PROMPT = """### Instruction:
You are helpful chatbot.
Based on this text answer questions:
 _PLANTSINFO_

### Prompt: 
 _QUESTION_
"""
print(1)
INVALID_RESPONSE = """Недостаточно информации, повторите запрос (возможно растение отсутствует в базе)"""
print(1)

@app.route('/get_answer', methods=['POST'])
def process_text():
    question  = request.form.get('text')
    
    
    #question = "Расскажи про ареал и сырье аира обыкновенного?"
    
    plants = get_plants(question)
    
    if not plants:
        return jsonify({'response': INVALID_RESPONSE})
    
    #plants = ['аир обыкновенный']
    
    categories= ['Ареал', 'Сырьё', 'Экология', 'Ресурсы',
                 'Применение в медицине', 'Химический состав',
                 'Фармакологические свойства']
    
    plants_info_en = create_plants_information(plants, categories)
    question_en = tr.to_english(question)
    
    instruction = PROMPT.replace("_PLANTSINFO_", plants_info_en).replace("_QUESTION_", question_en)
    
    response = tr.to_russian(gptj.get_response(instruction))

    return jsonify({'response': response})
    
    
if __name__ == '__main__':
    print(2)
    app.run("0.0.0.0", port=3333)