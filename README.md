# hashtag generation 

The application aims to provide hashttags  for the image provided by the user and simple analysis 

  - prerequisite:
   python3
   gcloud sdk
   
   
   
 
  - step1: install the requirements( pip install -r requirements.txt)
  - step2: add key.json file for google cloud vision api
  - step3: add key2.json file for firestore database from firebase settings
  - step4: make the changes in main.py file seeing comments in that file
  - step5: run the command python3 main.py check at localhost:8080
  - step6: to deploy it to app engine use command gcloud app deploy

# optional

To containerize the application and run use docker commands:
  - docker build -t [container tag name] .

  - docker run -p8080 [container tag name]

