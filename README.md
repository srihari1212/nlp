# nlp API
============


Created By
----------
Sri hari K V
https://bit.ly/34R7lrj


Description
-----------
This is a API that gets a review as a input then preprocess that review using nltk and 
classifies it as positive or negative or neutral review with polarity and subjectivity score 


requirements.txt File Included
------------------------------
set your working directory in terminal and install required packages for this API using
pip install -r requirements.txt


Logging is included
-------------------
This API is completely logged in nlp.txt file


Sample input
------------
She is a kind staff.Her lectures are really intresting and very usefull. She treats all the students equally


Sample output
-------------
{
    "interpretation": "The sentence is positive and a objective sentence",
    "result": {
        "polarity": 0.26666666666666666,
        "subjectivity": 0.45
    }
}

Method
-----
post


data-type
---------
form-data


parameter
---------
sentence
