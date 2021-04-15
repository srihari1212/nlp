from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer 
from textblob import TextBlob
from flask import Flask, render_template,request,jsonify,make_response
import logging
import logging.config
import re

app=Flask(__name__)
app.debug = True

logging.config.fileConfig(fname='log.conf', disable_existing_loggers=False)
logger = logging.getLogger('nlpLogger')

def preprocessdata(sentence):
    logger.info('Entered preprocessdata function')
    #She is a kind staff.Her lectures are really intresting and very usefull. She treats all the students equally
    #print(type(sentence))
    sentence = re.sub('[^a-zA-Z]', ' ', sentence)
    try:
        logger.info("normalizing")
        #normalizing capital to small 
        sentence = sentence.lower()
    except:
        logger.error("Error in normalizing",exc_info=True)
        return make_response(jsonify(
                    {
                        'status' : 'fail',
                        'desc':'Error in normalizing',
                        'result' : {}
                    }
                ), 400)
    #print(sentence)
    #she is a kind staff her lectures are really intresting and very usefull  she treats all the students equally
    try:
        logger.info("tokenizing")
        #Tokenization
        word_tokens = word_tokenize(sentence)
    except:
        logger.error("Error in Tokenization",exc_info=True)
        return make_response(jsonify(
                    {
                        'status' : 'fail',
                        'desc':'Error in Tokenization',
                        'result' : {}
                    }
                ), 400)
    #print(word_tokens)
    #['she', 'is', 'a', 'kind', 'staff', 'her', 'lectures', 'are', 'really', 'intresting', 'and', 'very', 'usefull', 'she', 'treats', 'all', 'the', 'students', 'equally']
    try:
        #stopwords removal
        logger.info("removing stopwords")
        stop_words = set(stopwords.words('english')) 
        filtered_sentence = [w for w in word_tokens if not w in stop_words] 
    except:
        logger.error("Error in stopwords removal",exc_info=True)
        return make_response(jsonify(
                    {
                        'status' : 'fail',
                        'desc':'Error in stopwords removal',
                        'result' : {}
                    }
                ), 400)
    #print(filtered_sentence)
    #['kind', 'staff', 'lectures', 'really', 'intresting', 'usefull', 'treats', 'students', 'equally']
    try:
        logger.info('stemming')
        #stemming
        ps = PorterStemmer()
        stemmed_lst=[]
        for word in filtered_sentence:
            stemmed_token = ps.stem(word)
            stemmed_lst.append(stemmed_token)
    except:
        logger.error("Error in stemming",exc_info=True)
        return make_response(jsonify(
                    {
                        'status' : 'fail',
                        'desc':'Error in stemming',
                        'result' : {}
                    }
                ), 400)
    #print(stemmed_lst)
    #['kind', 'staff', 'lectur', 'realli', 'intrest', 'useful', 'treat', 'student', 'equal']


    #print(filtered_sentence)
    #['kind', 'staff', 'lectures', 'really', 'intresting', 'usefull', 'treats', 'students', 'equally']
    try:
        logger.info('lemmatization')
        #lemmatization
        lemmatizer = WordNetLemmatizer()
        lemmatizeded_lst=[]
        for word in filtered_sentence:
            lemmatizeded_token = lemmatizer.lemmatize(word)
            lemmatizeded_lst.append(lemmatizeded_token)
    except:
        logger.error("Error in lemmatization",exc_info=True)
        return make_response(jsonify(
                    {
                        'status' : 'fail',
                        'desc':'Error in lemmatization',
                        'result' : {}
                    }
                ), 400)
    #print(lemmatizeded_lst)
    #['kind', 'staff', 'lecture', 'really', 'intresting', 'usefull', 'treat', 'student', 'equally']
    final = ' '.join(lemmatizeded_lst)
    #print(final)
    #kind staff lecture really intresting usefull treat student equally
    return final

#print(sentence)




def classify_sentence(analysis_polarity,analysis_subjectivity):
    logger.info("entered classify_sentence")
    try:
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
    except:
        logger.error("Error in classify_sentence",exc_info=True)
        return make_response(jsonify(
                    {
                        'status' : 'fail',
                        'desc':'Error in classify_sentence',
                        'result' : {}
                    }
                ), 400)

@app.route('/',methods=['POST'])
def sentiment_analysis():
    logger.info("Entered sentiment analysis API")
    sentence=request.form['sentence']
    if len(sentence.split()) >= 1:
        pass
    else:
        logger.error("The sentence must contain atleat one word in it")
        return make_response(jsonify(
            {
                'status' : 'fail',
                'desc':'The sentence must contain atleat one word in it',
                'result' : {}
            }
        ), 207)

    if sentence.isdigit():
        logger.error("The sentence contain only numeric values.")
        return make_responce(jsonify(
            {
                'status' : 'fail',
                'desc' : 'The sentence contain only numeric values',
                'result' : {}
            }
        ))
    else:
        pass

    #sentence = "She is a kind staff.Her lectures are really intresting and very usefull. She treats all the students equally"
    preprocesseddata = preprocessdata(sentence)
    try:
        analysis_polarity = TextBlob(preprocesseddata).sentiment.polarity
        analysis_subjectivity = TextBlob(preprocesseddata).sentiment.subjectivity
    except:
        logger.error("Error in calculating polarity and subjectivity",exc_info=True)
        return make_response(jsonify(
                    {
                        'status' : 'fail',
                        'desc':'Error in calculating polarity and subjectivity',
                        'result' : {}
                    }
                ), 400)
    
    type_sen,sub = classify_sentence(analysis_polarity,analysis_subjectivity)

    result1 = TextBlob(preprocesseddata).sentiment
    result2 = "The sentence is "+type_sen+" and a "+sub
    response = make_response(
                jsonify(
                    {"result": {"polarity":result1[0],"subjectivity":result1[1]}, "interpretation": result2}
                ))
    return response


if __name__ =='__main__':
   
    app.run()