from flask import Flask, request, jsonify, render_template,flash,redirect
import twitter
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
# from six.moves.urllib.request import urlopen
# from six import BytesIO
import numpy as np
from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps
from werkzeug.utils import secure_filename
from langdetect import detect
import re
from google.cloud import language_v1
from google.cloud.language_v1 import enums
from firebase_admin import credentials, firestore, initialize_app


# For measuring the inference time.
import time

global i

i=0

now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

allt=[]
fff=[]
res = []
tts=[]
fin=[]
urls=[]
app = Flask(__name__)

cred = credentials.Certificate('key2.json')
default_app = initialize_app(cred)
hashes = firestore.client().collection('fledge_used')
mydata = hashes.document()

app.secret_key = "secret key"
gt="submit"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=r"key.json"
client = vision.ImageAnnotatorClient()
storage_client = storage.Client()
bucket_name = "projectimages_christ"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/tag')
def tag():
    return render_template('tag.html')

@app.route('/text')
def text():
    return render_template('text.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/res')
def upload_form():
	return render_template('newupload2.html')




@app.route('/res', methods=['POST'])
def upload_file():
    
    if request.form.getlist('obs'):
        ff=request.form.getlist('obs')
        if len(ff) == 0:
            print("i came")
            print(fin)
            return render_template("objres.html", name = urls,data=fin,user="commercial")
        print(ff)
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
            # for ele in fin:
            #     str1=str1+" #"+ele+" "
            # dis=str.format(str1)
        
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
            
        return render_template("objres.html", name = urls,data=fin,hashes=allt,user="commercial")

        
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
            print("hey i m coming here")
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    fff.append(filename)
                    file.save(os.getcwd()+"/static/uploads/"+filename)
                    p=os.getcwd()+"/static/uploads/"+filename
                    ur=upload_blob("projectimages_christ",p,filename)
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
                    ur=upload_blob("projectimages_christ",p,filename)
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
            return render_template("objres.html", name = urls,f=fin,user="normal")
        return render_template("objres.html", name = urls,f=res,user="o_iden")

        
            


# @app.route('/business')
# def business():
#     return render_template("objupload.html")    

# @app.route('/objupload')
# def objupload():
#     return render_template("objupload.html")  

# @app.route('/objres', methods=['GET', 'POST'])
# def objres():  
#     if request.method == 'POST':  
#         f = request.files['file']       
#         f.save(os.getcwd()+"/uploads/"+f.filename)  
#         t=os.getcwd()+"/uploads/"+f.filename
#         with io.open(t, 'rb') as image_file:
#             content = image_file.read()
#         image = vision.types.Image(content=content)
#         response = client.label_detection(image=image)
#         labels = response.label_annotations
#         print('Labels:')
#         tt=[]
#         for label in labels:
#             temp=label.description
#             y=temp.replace(" ","")
#             tt.append(y)
#         vals=run_detector(detector, t)
#         res = []
#         for o in vals:
#             if o not in res:
#                 res.append(o)
#         for objects in res:
#             hashtags=HashSearch(objects)


#         return render_template("objres.html", name = f.filename,data=tt,tata=res)     
    
    

# @app.route('/elements')
# def elements():
#     return render_template('elements.html')



# @app.route('/keywords', methods=['GET', 'POST'])
# def keyword():
#     if request.method == 'POST':  
#         ddy = request.form['key']
#         rr=HashSearch(ddy)
#         return render_template('keyword.html',jj=rr)
#     return render_template('keyword.html')

# 
#  yet to be done below one 
# 
# 




# @app.route('/analyse')
# def analyse():
#     if request.method == 'POST':  
#         ddy = request.form['key']
#         rr=TweetSearch(ddy)
#         return render_template('keyword.html',jj=rr) 
# 	return render_template('keyword.html')

# @app.route('/analyse', methods=['GET', 'POST'])
# def tweet():
#     if request.method == 'POST':  
#         ddy = request.form['key']
#         rr=TweetSearch(ddy)
#         ff=[]
#         flag=1
#         cc=""
#         c1=""
#         c2=""
#         for nh in rr:
#             if nh[:2]=="RT":
#                 print("retweeted")
#             else:
#                 if nh not in ff:

#                     c1=clean_text(nh)
#                     # c2=c1
#                     leng=len(c2)
#                     if leng > 40:
#                         t=sample_classify_text(c2)
#                         c2=""
#                         print(t)
#                     else:
#                         c2=c2+c1
                        

                    

                    # g=clean_text(nh)
                    # cc=" "+g
                    # if flag == 1:
                    #     flag=2
                    #     c1=cc
                    # elif flag == 2:
                    #     flag=3
                    #     arg=cc+c1
                    # elif flag == 3:
                    #     flag=4
                    #     arg3=cc+arg
                    # elif flag==4:
                    #     print("i came")
                    #     flag=1
                    #     args=cc+arg3
                    #     print(args+"----"+len(args))
                    #     # dd=sample_classify_text()
                    #     ff.append(arg)
                    #     # print(dd)
                        


                #  anal_string=""
        # print(anal_string.join(ff))
    #     print(ff)
        
    #     return render_template('tweet.html',jj=ff)
    # return render_template('tweet.html')





# @app.route('/tweet', methods=['GET', 'POST']) #allow both GET and POST requests
# def form_example1():
#     if request.method == 'POST': #this block is only entered when the form is submitted
#         dd = request.form['data']
#         dy=TweetSearch(dd)
#         return render_template("res.html",dates=dy)
#     return '''<form method="POST">
#                   enter Keyword whose trending tweet u want: <input type="text" name="data"><br>
#                   <input type="submit" value="Submit"><br>
#               </form>'''

# @app.route('/send', methods=['GET', 'POST']) #allow both GET and POST requests
# def form_example2():
#     if request.method == 'POST': #this block is only entered when the form is submitted
#         dd = request.form['data']
#         dy=HashSearch(dd)
#         return render_template("res.html",dates=dy)

    # return '''<form method="POST">
    #               Keyword: <input type="text" name="data"><br>
    #               <input type="submit" value="Submit"><br>
    #           </form>'''


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



# def draw_bounding_box_on_image(image,
#                                ymin,
#                                xmin,
#                                ymax,
#                                xmax,
#                                color,
#                                font,
#                                thickness=4,
#                                display_str_list=()):
#   """Adds a bounding box to an image."""
#   draw = ImageDraw.Draw(image)
#   im_width, im_height = image.size
#   (left, right, top, bottom) = (xmin * im_width, xmax * im_width,
#                                 ymin * im_height, ymax * im_height)
#   draw.line([(left, top), (left, bottom), (right, bottom), (right, top),
#              (left, top)],
#             width=thickness,
#             fill=color)

#   display_str_heights = [font.getsize(ds)[1] for ds in display_str_list]
#   # Each display_str has a top and bottom margin of 0.05x.
#   total_display_str_height = (1 + 2 * 0.05) * sum(display_str_heights)

#   if top > total_display_str_height:
#     text_bottom = top
#   else:
#     text_bottom = bottom + total_display_str_height
#   # Reverse list and print from bottom to top.
#   for display_str in display_str_list[::-1]:
#     text_width, text_height = font.getsize(display_str)
#     margin = np.ceil(0.05 * text_height)
#     draw.rectangle([(left, text_bottom - text_height - 2 * margin),
#                     (left + text_width, text_bottom)],
#                    fill=color)
#     draw.text((left + margin, text_bottom - text_height - margin),
#               display_str,
#               fill="black",
#               font=font)
#     text_bottom -= text_height - 2 * margin


def draw_boxes(image, boxes, class_names, scores, max_boxes=10, min_score=0.1):
    objs=[]
    for i in range(min(boxes.shape[0], max_boxes)):
        if scores[i] >= min_score:
            ymin, xmin, ymax, xmax = tuple(boxes[i])
            display_str = "{}".format(class_names[i].decode("ascii"))
            objs.append(display_str)
            print(display_str)
    print(objs) 
    return objs

module_handle = "https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1"
detector = hub.load(module_handle).signatures['default']

def load_img(path):
  img = tf.io.read_file(path)
  img = tf.image.decode_jpeg(img, channels=3)
  return img

def run_detector(detector, path):
    img = load_img(path)
    converted_img  = tf.image.convert_image_dtype(img, tf.float32)[tf.newaxis, ...]
    start_time = time.time()
    result = detector(converted_img)
    end_time = time.time()
    result = {key:value.numpy() for key,value in result.items()}
    print("Found %d objects." % len(result["detection_scores"]))
    print("Inference time: ", end_time-start_time)
    objarray = draw_boxes(
        img.numpy(), result["detection_boxes"],
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

        print(u"Category name: {}".format(category.name))

        print(u"Confidence: {}".format(category.confidence))

    return cats



def HashSearch(hashtag):
    CONSUMER_KEY = 'qAZXMRvttjWaq4Ns8hR6KtIG7'
    CONSUMER_SECRET = 'XTBuR26hXrJFc4qwL7EzvtWMIq5dq7pnB01FAWfsRa0ViMDcGx'
    OAUTH_TOKEN = '497030183-5XWr6IF688dxPXKyF7Xx12eJ6PDSX4uNNaewc3fx'
    OAUTH_TOKEN_SECRET = 'JlZOhLs923LQp6LZ82OgWWPUAA9x9xb2YoWulPECvUEOI'
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
  #  print(json.dumps(hashtags[0:10], indent=1))
    return hashtags

def TweetSearch(tweet):
  CONSUMER_KEY = 'qAZXMRvttjWaq4Ns8hR6KtIG7'
  CONSUMER_SECRET = 'XTBuR26hXrJFc4qwL7EzvtWMIq5dq7pnB01FAWfsRa0ViMDcGx'
  OAUTH_TOKEN = '497030183-5XWr6IF688dxPXKyF7Xx12eJ6PDSX4uNNaewc3fx'
  OAUTH_TOKEN_SECRET = 'JlZOhLs923LQp6LZ82OgWWPUAA9x9xb2YoWulPECvUEOI'
  auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                         CONSUMER_KEY, CONSUMER_SECRET)
  twitter_api = twitter.Twitter(auth=auth)
  search_result = twitter_api.search.tweets(q=tweet, count='100')
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

#  print(json.dumps(hashtags[0:10], indent=1))
  return status_texts


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0',port=8080)








