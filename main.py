from flask import Flask, request, jsonify, render_template,flash,redirect,session,url_for
import twitter
import tweepy
from numpy  import array
from tweepy import OAuthHandler
from textblob import TextBlob
from urllib.parse import unquote
from datetime import datetime
import os
import io
from google.cloud import vision
from google.cloud import storage
from google.cloud.vision import types
import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt
import tempfile
from six.moves.urllib.request import urlopen
from six import BytesIO
import numpy as np
from werkzeug.utils import secure_filename
from langdetect import detect
import re
from google.cloud import language_v1
from google.cloud.language_v1 import enums
from firebase_admin import credentials, firestore, initialize_app
from monkeylearn import MonkeyLearn
from operator import itemgetter 
from uclassify import uclassify
from google.cloud import firestore
import time

global i


current_milli_time = lambda: int(round(time.time() * 1000))

ml = MonkeyLearn("d3380df585fa254763c9590ce7ece2e076423720")
model_id="cl_o46qggZq"
i=0
tf.compat.v1.enable_eager_execution()
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

allt=[]
fff=[]
res = []
tts=[]
fin=[]
urls=[]
app = Flask(__name__)

#put your twitter keys
consumer_key=""
consumer_secret=""
access_token=""
access_token_secret=""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


#download the key from gclod and save it as key.json in the current directory
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=r"key.json"

#download the key from firebase firestaore and save them as key2.json
cred = credentials.Certificate('key2.json')
default_app = initialize_app(cred)

#relplace collection name where you want to sore the result with your collection name
hashes = firestore.Client().collection([your collection])

#replce collection with your users collection
ussssse = firestore.Client().collection([yours users collection])
mydata = hashes.document()

app.secret_key = "secret key"

gt="submit"


client = vision.ImageAnnotatorClient()
storage_client = storage.Client()


# enter your bucket name

bucket_name = ""


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
graphs_url=[]
db = firestore.Client()


#enter your collection name
docs = db.collection([your collection name]).stream()


#####################################################
####___________#######################################

class TwitterClient(object):
    def __init__(self):
        # keys and tokens from the Twitter Dev Console
        consumer_key = ""
        consumer_secret = ""
        access_token = ""
        access_token_secret = ""
        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")
 
    def clean_tweet(self, tweet):
 
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
 
    def get_tweet_sentiment(self, tweet):

        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
        
    def get_tweet_sentiment_value(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        return analysis.sentiment.polarity
 
    def get_tweets(self, query, count = 1000):
        tweets = []
        tweet_value = []
 
        try:
            fetched_tweets = self.api.search(q = query, count = count)
            for tweet in fetched_tweets:
                parsed_tweet = {}
                if (tweet.metadata['iso_language_code'] == 'en'):               
                    parsed_tweet['text'] = tweet.text
                    parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
                    
                    print(parsed_tweet['text'])
                    if tweet.retweet_count > 0:
                        if parsed_tweet not in tweets:
                            tweets.append(parsed_tweet)
                    else:
                        tweets.append(parsed_tweet)
                tweet_value.append(self.get_tweet_sentiment_value(tweet.text))
            return tweets, tweet_value
 
        except tweepy.TweepError as e:
            print("Error : " + str(e))

#########################################################


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    if session:
        return render_template('home.html')
    else:
        return render_template('index.html')
    


@app.route('/about')
def about():
    if session:
        return render_template('about2.html')
    else:
        return render_template('about.html')

@app.route('/tag')
def tag():
    if session:
        return render_template('tag.html')
    else:
        return redirect(url_for('login'))

@app.route('/text')
def text():
    if session:
        return render_template('text.html')
    else:
        return redirect(url_for('login'))

@app.route('/contact')
def contact():
    if session:
        return render_template('contact2.html')
    else:
        return render_template('contact.html')


@app.route('/res')
def upload_form():
	return render_template('newupload2.html')

@app.route("/tw")
def indexi():
    return render_template('tw_analysis.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        print("did i come over here")
        username = request.form['username']
        password = request.form['password']
        temp=[]
        temp.clear()
        db = firestore.Client()
        docss = db.collection(u'users').stream()
        for doc in docss:
            temp=doc.to_dict()
            print("oh here!")
            print(temp)
        
            if temp['username']==username:
                if temp['password']==password:
                    session['loggedin'] = True
                    session['id'] = doc.id
                    session['username'] = temp['username']
                    return render_template('home.html')
                else:
                    msg = 'Incorrect username/password!'           
    return render_template('login.html',msg=msg)

@app.route('/pre',methods=['GET', 'POST'])
def payment():
    
    if request.headers['Content-Type'] == 'text/html':
        print(request.data)
        return render_template("login.html")
    return redirect(url_for('log'))
    
@app.route('/logout')
def log():
    session.pop('loggedin',None)
    session.pop('id',None)
    session.pop('username',None)
    return render_template('index.html')

@app.route('/feat')
def feat():
    session.pop('loggedin',None)
    session.pop('id',None)
    session.pop('username',None)
    return redirect(url_for('index'))

@app.route('/signup',methods=['GET', 'POST'])
def signup():
    msg = ''
    if request.method=='POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        cpassword = request.form['confirm-password']
        mobile = request.form['mobile']
        country = request.form['country']
        flag=0
        db = firestore.Client()
        docsss = db.collection(u'users').stream()
        for doc in docss:
            temp=doc.to_dict()
            if temp['username']==username:
                msg = 'Account already exists!'
                flag=1
                break
            else:
                msg = 'You have successfully registered!'
                data = {
                    u'username': username,
                    u'email': email,
                    u'password': password,
                    u'bussiness': "false",
                    u'mobile': mobile,
                    u'country':country
                    }
                flag=0               
        if flag==0:
            ussssse.add(data)
        return render_template('login.html',msg=msg)
                 
    return render_template('signup.html',msg=msg)


@app.route("/img1",methods=["POST"])
def searchimg1():
    search_tweet = request.form.get("search_query")
    t = []
    t.clear()
    hh=sentiment_twitter(search_tweet)
    t.append(hh)
    return jsonify({"success":True,"tweets":t})

@app.route("/img2",methods=["POST"])
def searchimg2():
    search_tweet = request.form.get("search_query")
    t = []
    t.clear()
    hh=analysse(search_tweet)
    t.append(hh)

    return jsonify({"success":True,"tweets":t})

@app.route("/search",methods=["POST"])
def search():
    search_tweet = request.form.get("search_query")
    t = []
    tweets = api.search(search_tweet, tweet_mode='extended')
    for tweet in tweets:
        polarity = TextBlob(tweet.full_text).sentiment.polarity
        subjectivity = TextBlob(tweet.full_text).sentiment.subjectivity
        t.append([tweet.full_text,polarity,subjectivity])
    return jsonify({"success":True,"tweets":t})


@app.route('/res', methods=['POST'])
def upload_file():    
    if request.form.getlist('obs'):
        ff=request.form.getlist('obs')
        if len(ff) == 0:
            return render_template("objres.html", name = urls,data=fin,user="commercial")
        for objects in ff:
            hashtags=HashSearch(objects)
            ss=[]
            single=[]
            for w in hashtags:
                if detect(w)=="en":
                    ss.append(w)
            for q in ss:
                if q not in single:
                    single.append(q)
            allt.append(single)
        str1 = ""
        uu=""
        for tt in urls:
            uu=uu+" "+tt+", "
        pic_urls=str.format(uu)
        for ele in fin: 
            for e in ele:
                str1=str1+" #"+e+" "
        dis=str.format(str1)
        allhash=""
        for r in allt:
            for t in r:
                allhash=allhash+" #"+e+" "
        oos=""
        for ty in res:
            oos=oos+" "+ty+", "
        data = {
            u'user': "commercial",
            u'time': dt_string,
            u'hashtag_g': dis,
            u'hashtag_obj_twitter':allhash,
            u'obj_identified':oos,
            u'img_urls':pic_urls
            }
        mydata.set(data)        
        return render_template("result.html", name = urls,data=fin,hashes=allt,user="commercial")

        
    if request.method == 'POST':
        fin.clear()
        res.clear()
        urls.clear()
        allt.clear()
        fff.clear()
        tts.clear()
        files = request.files.getlist('files[]')
        r=request.form.get('radio')       
        print(r)
        if request.form.get('radio') == '1':
           
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    fff.append(filename)
                    file.save(os.getcwd()+"/static/uploads/"+filename)
                    p=os.getcwd()+"/static/uploads/"+filename
                    global bucket_name
                    ur=upload_blob(bucket_name,p,filename)
                    urls.append(ur)
                    with io.open(p, 'rb') as image_file:
                        content = image_file.read()
                    image = vision.types.Image(content=content)
                    response = client.label_detection(image=image)
                    labels = response.label_annotations
                    print('Labels:')
                    for label in labels:
                        temp=label.description
                        y=temp.replace(" ","")
                        tts.append(y)
                    print(tts)
                    fin.append(tts)
                    vals=run_detector(detector, p)                  
                    for o in vals:
                        if o not in res:
                            res.append(o)

        else:
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    fff.append(filename)
                    file.save(os.getcwd()+"/static/uploads/"+filename)
                    p=os.getcwd()+"/static/uploads/"+filename
                    global bucket_name
                    ur=upload_blob(bucket_name,p,filename)
                    urls.append(ur)
                    with io.open(p, 'rb') as image_file:
                        content = image_file.read()
                    image = vision.types.Image(content=content)
                    response = client.label_detection(image=image)
                    labels = response.label_annotations
                    print('Labels:')
                    for label in labels:
                        temp=label.description
                        y=temp.replace(" ","")
                        tts.append(y)
                    print(tts)
                    fin.append(tts)
            str1 = ""
            uu=""
            for tt in urls:
                uu=uu+" "+tt+", "
            pic_urls=str.format(uu)
            for ele in fin: 
                for e in ele:
                    str1=str1+" #"+e+" "
            dis=str.format(str1)
            data = {
                u'user': "normal",
                u'time': dt_string,
                u'hashtag_g': dis, 
                u'pic_urls':pic_urls           
                }
            mydata.set(data)
            return render_template("result.html", name = urls,f=fin,user="normal")
        return render_template("result.html", name = urls,f=res,user="o_iden")


def listToString(s):  
    str1 = ""    
    for ele in s:  
        str1 += ele    
    return str1

def sentiment_twitter(name):
    api = TwitterClient()
    tweets, tweet_value = api.get_tweets(query = name, count = 100)
    file1 = open("data1.txt","w")
    x = np.arange(0,len(tweet_value),1)
    y = np.asarray(tweet_value)
    plt.plot(x,y)
    plt.ylim(-1,1)
    plt.ylabel('Sentiment value')
    plt.xlabel('Tweet Count')
    plt.title('Twitter sentiment analysis for ' + name)
    g_nn=str(current_milli_time())+".png"
    ppppp="static/images/"+g_nn
    plt.savefig(ppppp)
    global bucket_name
    g_url=upload_blob(bucket_name,ppppp,g_nn)
    plt.clf()
    graphs_url.append(g_url)
    return g_url


def analysse(name):
    graphs_url.clear()
    rr=TweetSearch(name)
    catego=[]
    catego_val=[]
    temp2=""
    for uy in rr:
        temp=clean_text(uy)
        temp1=[]
        temp1.append(temp)
        result = ml.classifiers.classify(model_id, temp1)
        res = list(map(itemgetter('classifications'), result.body)) 
        if res[0]=="None":
            print("fuckin error")
        try:
            res_tag_name=list(map(itemgetter('tag_name'),res[0]))
            trm_c=list(map(itemgetter('confidence'),res[0]))
        except:
            print("what to do if error occurs")
        if (res_tag_name[0] in catego):
            inf=catego.index(res_tag_name[0])
            temp=(float(catego_val[inf])+float(trm_c[0]))/2
            temp2=round(temp,2)           
            catego_val[inf]=temp2
            temp=0
        else:
            te=round(trm_c[0],2)               
            gret=str(te)
            catego.append(res_tag_name[0])
            catego_val.append(gret)
        temp1=[]         
    newval=[]
    for hy in catego_val:
        temp=float(hy)
        newval.append(temp)
    y_pos = np.arange(len(catego))
    plt.barh(y_pos, newval)
    plt.yticks(y_pos, catego)
    plt.xlabel('tweets analysed')
    plt.title('Recent Tweets categories')
    plt.rcParams['figure.figsize']=(20,12)
    g_nn=str(current_milli_time())+".png"
    ppppp="static/images/"+g_nn
    plt.savefig(ppppp)
    plt.clf()
    global bucket_name
    g_url=upload_blob(bucket_name,ppppp,g_nn)
    graphs_url.append(g_url)
    return g_url


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    blob.make_public()
    return blob.public_url

def clean_text(text):
    text = re.sub(r'\'+', '', text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    text = re.sub(r'(https?://[^\s]+)', ' ', text, flags=re.MULTILINE)
    text = re.sub('[$,?!\n]', ' ', text)
    text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())
    text = re.sub('[^A-Za-z0-9 ]+', ' ', text)
    return text


def draw_boxes(boxes, class_names, scores, max_boxes=10, min_score=0.1):
    objs=[]
    for i in range(min(boxes.shape[0], max_boxes)):
        if scores[i] >= min_score:
            ymin, xmin, ymax, xmax = tuple(boxes[i])
            display_str = "{}".format(class_names[i].decode("ascii"))
            objs.append(display_str)
            print(display_str)
    print(objs) 
    return objs


# here you can use your own pre tarined model which u want from tensorflow

module_handle = "https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1"
detector = hub.load(module_handle).signatures['default']

def load_img(path):
  img = tf.io.read_file(path)
  img = tf.image.decode_jpeg(img, channels=3)
  return img

def run_detector(detector, path):
    img = load_img(path)
    converted_img  = tf.image.convert_image_dtype(img, tf.float32)[tf.newaxis, ...]
    print(converted_img)
    start_time = time.time()
    result = detector(converted_img)
    end_time = time.time()
    result={key:value.numpy() for key,value in result.items()}
    print(result)
    print("Found %d objects." % len(result["detection_scores"]))
    print("Inference time: ", end_time-start_time)
    objarray = draw_boxes(result["detection_boxes"],
        result["detection_class_entities"], result["detection_scores"])
    
    return objarray


def sample_classify_text(text_content):

 
    client = language_v1.LanguageServiceClient()

    type_ = enums.Document.Type.PLAIN_TEXT
    


    language = "en"
    document = {"content": text_content, "type": type_, "language": language}

    response = client.classify_text(document)
    cats=[]

    for category in response.categories:
        cats.append(format(category.name))
        cats.append(format(category.confidence))
        print(u"Category name: {}".format(category.name))
        print(u"Confidence: {}".format(category.confidence))
    
    return cats



def HashSearch(hashtag):
    CONSUMER_KEY = ''
    CONSUMER_SECRET = ''
    OAUTH_TOKEN = ''
    OAUTH_TOKEN_SECRET = ''
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)
    twitter_api = twitter.Twitter(auth=auth)
    search_result = twitter_api.search.tweets(q=hashtag, count='100')
    statuses = search_result['statuses']
    for _ in range(5):
        try:
            counter = search_result['search_metadata']['next_results']
        except KeyError as e:
                break
    kwargs = dict([kv.split('=') for kv in unquote(counter[1:]).split("&")])
    search_results = twitter_api.search.tweets(**kwargs)
    statuses += search_results['statuses']
    status_texts = [status['text']
    for status in statuses]

    hashtags = [hashtag['text']
            for status in statuses
            for hashtag in status['entities']['hashtags']]

    return hashtags

def TweetSearch(tweet):
  CONSUMER_KEY = ''
  CONSUMER_SECRET = ''
  OAUTH_TOKEN = ''
  OAUTH_TOKEN_SECRET = ''
  auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                         CONSUMER_KEY, CONSUMER_SECRET)
  twitter_api = twitter.Twitter(auth=auth)
  search_result = twitter_api.search.tweets(q=tweet, count='10')
  statuses = search_result['statuses']
  for _ in range(5):
      try:
          counter = search_result['search_metadata']['next_results']
      except KeyError as e:
              break
  kwargs = dict([kv.split('=') for kv in unquote(counter[1:]).split("&")])
  search_results = twitter_api.search.tweets(**kwargs)
  statuses += search_results['statuses']
  status_texts = [status['text']
  for status in statuses]

  return status_texts



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0',port=8080)







