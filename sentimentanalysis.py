from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer 
from textblob import TextBlob
from flask import Flask, render_template,request,jsonify,make_response

app=Flask(__name__)
app.debug = True
def preprocessdata(sentence):
    #normalizing capital to small 
    sentence = sentence.lower()

    #Tokenization
    word_tokens = word_tokenize(sentence)

    #stopwords removal
    stop_words = set(stopwords.words('english')) 
    filtered_sentence = [w for w in word_tokens if not w in stop_words] 


    #stemming
    ps = PorterStemmer()
    stemmed_lst=[]
    for word in filtered_sentence:
        stemmed_token = ps.stem(word)
        stemmed_lst.append(stemmed_token)
    

    #lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmatizeded_lst=[]
    for word in filtered_sentence:
        lemmatizeded_token = lemmatizer.lemmatize(word)
        lemmatizeded_lst.append(lemmatizeded_token)
        

    final = ' '.join(lemmatizeded_lst)
    #print(final)
    return final

#print(sentence)




def classify_sentence(analysis_polarity,analysis_subjectivity):
    if analysis_polarity > 0:
        type_sen = "positive"
    elif analysis_polarity < 0:
        type_sen = "negative"
    else:
        type_sen = "neutral"

    if analysis_subjectivity < 0.5:
        sub = "objective sentence"
    else:
        sub = "subjective sentence"
    return type_sen,sub

@app.route('/',methods=['POST'])
def sentiment_analysis():
    sentence=request.form['sentence']
    #sentence = "She is a kind staff.Her lectures are really intresting and very usefull. She treats all the students equally"
    preprocesseddata = preprocessdata(sentence)
    analysis_polarity = TextBlob(preprocesseddata).sentiment.polarity
    analysis_subjectivity = TextBlob(preprocesseddata).sentiment.subjectivity
    type_sen,sub = classify_sentence(analysis_polarity,analysis_subjectivity)
    print(TextBlob(preprocesseddata).sentiment)
    print("The sentence is "+type_sen+" and a "+sub)
    result1 = TextBlob(preprocesseddata).sentiment
    result2 = "The sentence is "+type_sen+" and a "+sub
    response = make_response(
                jsonify(
                    {"result": {"polarity":result1[0],"subjectivity":result1[1]}, "interpretation": result2}
                ))
    return response


if __name__ =='__main__':
   
    app.run()