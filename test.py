import json
import time

packs = {
    "Spanish IV":{
        "cotidiano":"everyday"
    },
    "English":{
        "foreshadowing":"an indication of future plot events",
        "irony":"something that is not as it seems"
    },
    "History":{
        "Batle of Bull Run":"showed people that the war would not be a quick easy war"
    },
    "Math":{
        "Integral":"the area under a curve"
    },
    "Art":{
        "art":"cool stuff"
    },
    "Coding":{
        "code":"cool techy stuff"
    },
    "Christianity and Social Justice":{
        "privilege":"an unearned advantage"
    }
}

with open("vocabulary.json", "w") as file:
    
    json.dump(packs, file)