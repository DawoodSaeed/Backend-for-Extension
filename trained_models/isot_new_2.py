# imports
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import joblib
import sys

# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('omw-1.4')
# stopwords array
stop_words = stopwords.words("english")

# cleaning data for tf-idf
# 1. remove punctutaion using re
# 2. tokenize the words
# 3. remove stopwords
# 4. lemmatize the words

lemmatizer = WordNetLemmatizer()

# pre-processing
def preprocessing(sentence):
  # to store cleaned data
  filtered_sentence = ""
  # change to lowercase first
  sentence = sentence.lower()
  # 1. using re to remove punctuation
  sentence = re.sub("<[^>]*>", "", str(sentence))
  sentence = re.sub(r"[^\w\s]", "", str(sentence))
  # 2. tokenize
  words = nltk.word_tokenize(sentence)
  # 3. stopwords
  words = [w for w in words if not w in stop_words]
  # 4. lemmatizing
  for word in words:
      filtered_sentence = filtered_sentence + " " + str(lemmatizer.lemmatize(word))
  # return the processed data
  return filtered_sentence

# tf-idf vectorizer to transform the data
tfidf = joblib.load('./python/machine_learning_models/fake_news/tfidf.pkl') 

# loading the model
loaded_model = joblib.load("./python/machine_learning_models/fake_news/ISOT_new1.pkl")

arg = sys.argv[1:]

text = ""
for word in arg:
  text = text + " " + word
# print(text)

text = tfidf.transform([text])

# print(text)

print(loaded_model.predict_proba(text))

# sys.stdout.flush()

# text2 = "Canada to boost defence, cyber security in Indo-Pacific policy OTTAWA: Canada launched its long-awaited Indo-Pacific strategy on Sunday, outlining C$2.3 billion ($1.7 billion) in spending to boost military and cyber security in the region and vowed to deal with a “disruptive” China while working with it on climate change and trade issues.The plan detailed in a 26-page document said Canada will tighten foreign investment rules to protect intellectual property and prevent Chinese state-owned enterprises from snapping up critical mineral supplies.Canada is seeking to deepen ties with a fast-growing Indo-Pacific region of 40 countries accounting for almost C$50 trillion in economic activity. But the focus is on China, which is mentioned more than 50 times, at a moment when bilateral ties are frosty. Four cabinet ministers at a news conference in Vancouver took turns detailing the new plan, saying the strategy was crucial for Canada’s national security and climate as well as its economic goals. “We will engage in diplomacy because we think diplomacy is a strength, at the same time we’ll be firm and that’s why we have now a very transparent plan to engage with China,” Foreign Minister Melanie Joly said. Prime Minister Justin Trudeau’s Liberal government wants to diversify trade and economic ties that are overwhelmingly reliant on the United States. Official data for September show bilateral trade with China accounted for under 7% of the total, compared to 68% for the United States. Canada’s outreach to Asian allies also comes as Washington has shown signs of becoming increasingly leery of free trade in recent years. The document underscored Canada’s dilemma in forging ties with China, which offers significant opportunities for Canadian exporters, even as Beijing looks to shape the international order into a more “permissive environment for interests and values that increasingly depart from ours,” it added. Yet, the document said cooperation with the world’s second-biggest economy was necessary to address some of the “world’s existential pressures,” including climate change, global health and nuclear proliferation. “China is an increasingly disruptive global power,” said the strategy. “Our approach ... is shaped by a realistic and clear-eyed assessment of today’s China. In areas of profound disagreement, we will challenge China.” Tensions with China soared in late 2018 after Canadian police detained a Huawei Technologies executive and Beijing subsequently arrested two Canadians on spying charges. All three were released last year, but relations remain sour. Canada earlier this month ordered three Chinese companies to divest their investments in Canadian critical minerals, citing national security. The document, in a section mentioning China, said Ottawa would review and update legislation enabling it to act “decisively when investments from state-owned enterprises and other foreign entities threaten our national security, including our critical minerals supply chains.” “Because the region is both large and diverse, one size definitely does not fit all,” Canadian Chamber of Commerce President Perrin Beatty said in a statement, adding that Canada’s priorities will need to be very nuanced both between and within countries. The document said Canada would boost its naval presence in the region and “increase our military engagement and intelligence capacity as a means of mitigating coercive behavior and threats to regional security.” Canada belongs to the Group of Seven major industrialised nations, which wants significant measures in response to North Korean missile launches. The document said Ottawa was engaging in the region with partners such as the United States and the European Union. Canada needed to keep talking to nations it had fundamental disagreements with, it said, but did not name them."
# text2 = tfidf.transform([text2])

# print(loaded_model.predict_proba(text2))

# text3 = "The co-chair of Trump s voter fraud commission, set up to prove that Hillary Clinton didn t win the popular vote because of the  millions  of illegal votes he says were cast for his opponent, just inserted both feet in his mouth, grew a new foot, then shoved that one in the other available orifice on Wednesday when he admitted that Trump may not be our legitimate president. You know, we may never know the answer to that,  Kansas Secretary of State Kris Kobach told MSNBC s Katy Tur when asked whether he thought Clinton won the popular vote by 3 to 5 million votes. We will probably never know the answer to that question,  he said. In reality, Clinton only won by 2.87 million votes   but Kobach is a moron. How do you say we may never know the answer to that question?  Tur asked. Then things got really stupid: What I m saying is, let s suppose that the commission determined that there were a certain number of votes cast by ineligible voters. You still won t know whether those people who were ineligible voted for Trump or for Clinton or for somebody else.And so, it s impossible to ever know exactly, if you took out all the ineligible votes, what the final tally would be in that election. You can obviously, based on the data, you can make some very educated guesses. So are the votes for Donald Trump that led him to win the election in doubt as well?  Tur pressed. Absolutely,  replied Kobach.Voter fraud   especially in-person   is extremely rare, though a couple of Trump supporters have been caught illegally voting multiple times after he told them people would illegally vote for Hillary Clinton.In other words, the system works and people who try to vote illegally do get caught. The integrity of the voting systems themselves, however, could be questioned as Russian agents provably hacked our electoral system in 39 states.Is Donald Trump the legitimate President? The answer is that  he s an idiot  until we know the full extent of Russian attacks on our election.Watch the interview below:"
# text3 = tfidf.transform([text3])

# print(loaded_model.predict_proba(text3))
