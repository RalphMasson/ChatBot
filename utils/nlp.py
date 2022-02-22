import spacy
import numpy as np
from spacy.matcher import Matcher


nlp = spacy.load("fr_core_news_sm")
about_interest_text = ('Montre moi des images de Emmanuel Macron')
about_interest_doc = nlp(about_interest_text)

for tokens in about_interest_doc:
    print(tokens.text,tokens.pos_)
for ent in about_interest_doc.ents:
    print(ent.text, ent.label_)


matcher = Matcher(nlp.vocab)
pattern = [[{"TEXT": "de"}, {"POS": "PROPN"}],[{"TEXT": "de"}, {"POS": "NOUN"}],[{"TEXT": "de"}, {"POS": "NOUN"},{"POS":"ADP"},{"POS":"NOUN"}],[{"TEXT": "de"}, {"POS": "NOUN"},{"POS":"ADJ"}],[{"TEXT": "de"}, {"POS": "PROPN"},{"POS":"ADJ"}],[{"TEXT": "de"}, {"POS": "NOUN"},{"POS":"NOUN"}],[{"TEXT": "de"}, {"POS": "NOUN"},{"POS":"ADJ"}],[{"TEXT": "de"}, {"POS": "PROPN"},{"POS":"PROPN"}]]
matcher.add("montre", pattern)
matches = matcher(about_interest_doc)
matches = [about_interest_doc[start+1:end].text for match_id, start, end in matches]

print(matches)
matches = matches[np.argmax(matches)]

print(matches)



from meteofrance_api import MeteoFranceClient
client = MeteoFranceClient()
list_places = client.search_places("Le Havre")[0]
my_place_weather_forecast = client.get_forecast_for_place(list_places)
meteo = my_place_weather_forecast.current_forecast.get('weather')['desc']
temp = my_place_weather_forecast.current_forecast.get('T')['value']

