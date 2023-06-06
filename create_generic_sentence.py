import spacy

def generate_generic_sentence(input_text):
    nlp = spacy.load("en_core_web_sm")
    
    # Process the input text
    doc = nlp(input_text)
    
    # Extract the main noun phrases
    noun_phrases = [chunk.text for chunk in doc.noun_chunks]
    
    # Select the first noun phrase as the generic sentence
    if noun_phrases:
        generic_sentence = noun_phrases[0]
    else:
        generic_sentence = ""
    print(generic_sentence)
    return generic_sentence
# Output: "Ukraine war"