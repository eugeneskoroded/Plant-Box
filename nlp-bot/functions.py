from googletrans import Translator

    
class Translating:
    def __init__(self):
        self.translator = Translator(service_urls=['translate.googleapis.com'])
        
    def to_english(self, text):
        return self.translator.translate(text,
                                         src='ru',
                                         dest='en').text
    def to_russian(self, text):
        return self.translator.translate(text,
                                         src='en',
                                         dest='ru').text
    
tr = Translating()


def get_category_info(plant, category):
    try:
        with open(f"texts/{plant}/{category}.txt", 'r', encoding="utf-8") as f:
            text = f.read()
            return tr.to_english(category).title() + ":\n" + tr.to_english(text) + "\n"
    except:
        return ""

    
def create_plants_information(plants, categories):
    prompt = ""
    for plant in plants:
        plant_eng = tr.to_english(plant)

        if categories:
            for category in categories:
                info = get_category_info(plant, category)

                if info:
                    prompt += info + "\n"

        else:
            info = get_category_info(plant, "Описание")

            if info:
                prompt += info + "\n"

        prompt = plant_eng.upper() + ":\n" + prompt
    
    return prompt