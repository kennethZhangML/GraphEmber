import spacy
import nltk
import torch

from transformers import BertTokenizer, BertForTokenClassification
nltk.download("averaged_perceptron_tagger")

def BERT_template(text):
    tokenizer = BertTokenizer.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")
    model = BertForTokenClassification.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")

    inputs = tokenizer(text, return_tensors = "pt")
    outputs = model(**inputs)

    predicted_labels = torch.argmax(outputs.logits, dim=2)
    entity_spans = predicted_labels[0].tolist()

    entities = []
    current_entity = ""
    for i, label_id in enumerate(entity_spans):
        token = tokenizer.convert_ids_to_tokens(label_id)
        if token.startswith("B-"):
            if current_entity:
                entities.append(current_entity.strip())
            current_entity = token[2:]
        elif token.startswith("I-"):
            if current_entity:
                current_entity += " " + text.split()[i]
            else:
                current_entity = text.split()[i]

    if current_entity:
        entities.append(current_entity.strip())

    print("Entities:", entities)

def spacy_template(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    entities = [doc.text for ent in doc.ents]
    relationships = [(ent.root.head.text, ent.text) for ent
    in doc.ents if ent.root.head.text != ent.text]

    print("Entities: ", entities)
    print("Relationships: ", relationships)

def nltk_template(text):
    sentences = nltk.sent_tokenize(text)
    words = [nltk.word_tokenize(sent) for sent in sentences]
    tagged_words = [nltk.pos_tag(word) for word in words]

    entities = []
    relationships = []

    for tagged_sentence in tagged_words:
        for i in range(len(tagged_sentence) - 1):
            word1, tag1 = tagged_sentence[i]
            word2, tag2 = tagged_sentence[i + 1]

            if tag1.startswith('NNP') and tag2.startswith('NNP'):
                entities.append(word1)
                entities.append(word2)
                relationships.append((word1, word2))

    print("Entities: ", entities)
    print("Relationships: ", relationships)

if __name__ == "__main__":
    text = "John works at CompanyXYZ. CompanyXYZ is located in New York City."

    nltk_template(text)
    spacy_template(text)
    BERT_template(text)
