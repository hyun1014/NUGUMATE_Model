import json
import sys
import numpy as np
from konlpy.tag import Okt
from keras.models import load_model

parser = Okt()
target_model = "NLP_model/" + sys.argv[1] + ".h5"

# Load selected_word
with open("NLP_model/selected_word.json", "r") as sf:
    selected_word = json.load(sf)
# Load model
model = load_model(target_model)


def tokenize(sentence):
    return [t[0] for t in parser.pos(sentence, norm=True, stem=True)]


# selected_word 안에 있는 word들이 각각 얼마나 나왔나
def term_frequency(doc):
    return [doc.count(word) for word in selected_word]


def predict_pos(sent):
    tokens = tokenize(sent)
    tf = term_frequency(tokens)
    data = np.expand_dims(np.asarray(tf).astype("float32"), axis=0)
    score = float(model.predict(data))
    print("\n\nTarget sentence: " + sent)
    if score > 0.5:
        print("긍정일 확률 {:.2f}%".format(score * 100))
    else:
        print("부정일 확률 {:.2f}%".format((1 - score) * 100))


test_case = input("Input a sentence.\n")
predict_pos(test_case)