# ReverseRecommendation
### Big Data Analytics Final Project - Team 25 - ReverseRecommendation
------
####remember to run the following command before development:
pip install -t lib -r requirements.txt

####If you want to try this program, you can go to this website:
http://reverse-recommendation.appspot.com/

####Here is our project video introduction:
[![Reverse Recommendation Screenshot](http://i.imgur.com/XXUK7ZD.png)](https://www.youtube.com/watch?v=9JE_l1XQtKw "Reverse Recommendation Screenshot")

General Purpose
------
*  Find out the insight of customer's negative reviews.
*  Provide the recommendations from the negative reviews.

Introduction
------
This project focused on recommending restaurants for Yelp users based on their review article. A naïve approach to build a recommendation system could just be based on user queries and star ratings. However, personal interests and preferences are difficult to identify and sometimes not even aware by consumers themselves. In this project, we build our recommendation model based on low-rating reviews. The major challenge is to identify preferences of consumers, and map it to features of products.
A crucial component in this project is to recognize the relations between information hidden in negative reviews and user preferences. In the final stage, our system generates searchable words and phrases into Yelp search API to fetch recommendation results. This step mimics human actions when our mind translates preferences into searchable keywords.

How To Use Our Service?
------
   1.   Post your negative review at the location our website indicates:
   ![Imgur](http://i.imgur.com/OxwyVvS.png)

   2.   Click "Recommend for me!":
   ![Imgur](http://i.imgur.com/yxeVb6n.png?1)

   3.   Now, you can get the recommendations from our service:
   ![Imgur](http://i.imgur.com/StPYBAM.png)

   4.   As you can see, there are reversed keywords our service extracts from your review:
   ![Imgur](http://i.imgur.com/uhLwnaw.png)

   5.   Also, you can read the reviews from our servie to understand why we recommend it for you:
   ![Imgur](http://i.imgur.com/keahIHW.png)

   6.   Evenmore, you can click on the picture or the name, we will redirect you to the yelp website:
   ![Imgur](http://i.imgur.com/VHvqPhw.png)
        Here is the original Yelp Website:
   ![Imgur](http://i.imgur.com/2iNhjI8.png)

System Work Flow
------
   1.   Generate the reversed keywords from the negative review
   2.   Put the reversed keywords to the Yelp API to query the result
   3.   Google App Engine get the Yelp API response
   4.   Render the recommendations & keywords to our frontend.

Web app
------
There are three main parts for our web app:
- **Google App Engine**
- **Yelp API**
- **Key Word Search**

We will go through these three parts in the following sections. 

- Google App Engine
------
![GAE](https://deciphertools.com/blog/img/google-app-engine-logo.jpg)

For our backend, we use Google App Engine with Python SDK to build the platform.
Google App Engine for Python is based on WebApp2. It provides the framework for user to build the website.
So basically, this website contains one main routes - MainPage, which will handle two http request,
one is get and other one is post. Get action just handles rendering the main page, and post action handles the clicking recommendation button and rendering the recommendation results.

- Yelp API
------
![YelpAPI](https://appdevelopermagazine.com/images/news_images%5Cyelp-api-updates_eb2hb3el.jpg)


Since we request the yelp result through yelp API, so we create one function to handle all of the yelp results. You can see the detail in the YelpAPI folder. With the 3 generated keywords, we feed it in to the Yelp API along with other searching criteria that we care about according to the scenario of the application. For example, we can combine the location of the user can recommend the user of the restaurants that are near by him or only recommend. 

- Key Word Search
------
The keyword we extracted so far can be interpreted as the concept that the user mentions most and cares about most. Also it may include some negative words. So when we want to recommend new restaurant to this user, we have to map these keywords into some positive
search term so that the recommended restaurants may have some characteristic that can satisfy the user most. We to this procedure manually, for example, for the negative word “dirty”, we map it into “clean”. For the neutral terms like “service”, we simply map it into “good service”. These mapped searching keywords are the keys of another hash map. When certain word gets mapped to, we increment its count by 1. In the end we select 3 searching keywords with largest count.

#### Hope you enjoy our project!
![BOOM](http://www.yelpblog.com/.a/6a00d83452b44469e201b7c786b047970b-pi)
