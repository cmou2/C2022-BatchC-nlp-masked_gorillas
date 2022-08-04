# import requirements needed
from flask import Flask, render_template, request, redirect, url_for
from utils import get_base_url
import openai
import requests
openai.api_key = "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"
from nltk.tokenize import sent_tokenize

# setup the webserver
# port may need to be changed if there are multiple flask servers running on same server
port = 12346
base_url = get_base_url(port)

# if the base url is not empty, then the server is running in development, and we need to specify the static folder so that the static files are served
if base_url == '/':
    app = Flask(__name__)
else:
    app = Flask(__name__, static_url_path=base_url+'static')

    
    
    
    
    
    
    
    
# set up the routes and logic for the webserver
@app.route(f'{base_url}/try-our-model', methods = ['POST', 'GET'])
def try_our_model():
    if request.method == 'GET':
        return render_template('get-a-quote.html', title='try-our-model')
    else:
        #handle the post request
        try:
            #print out user input
            user_input = request.form['userInput'] + '\n\n###\n\n'
            print('USER INPUT:', user_input)
            reply = ''


            #get a reply\
            reply = str(openai.Completion.create(
                model="ada:ft-personal-2022-07-31-18-04-47",
                prompt = user_input,max_tokens=150)['choices'][0]['text'])

            #split the reply into different paragraphs
            paragraphs = reply.split('###')
            selected_par = [-1,0] #index, len

            for i in range(len(paragraphs)):
                par = paragraphs[i]
                #if it's bigger, select it.
                if len(par) > selected_par[1]:
                    selected_par[0] = i
                    selected_par[1] = len(par)

            #select the final one
            reply = paragraphs[selected_par[0]]
            sentences = sent_tokenize(reply)[:-1]

            #format the reply
            reply = ''
            for sent in sentences:
                reply += (sent + ' ')

            return reply
    
        #catch the error and return to the user
        except Exception as e:
            return "ERROR: " +str(e)


#Load main page and redirects



@app.route(f'{base_url}')
def home():
    return render_template('index.html')

@app.route(f'{base_url}/static/index.html')
def home2():
    return redirect(f'{base_url}')

@app.route(f'{base_url}/index.html')
def home3():
    return redirect(f'{base_url}')


#@app.route(f'{base_url}/static/assets/img/<img>)
#def get_img(img):
#    return

# define additional routes here
# for example:
# @app.route(f'{base_url}/team_members')
# def team_members():
#     return render_template('team_members.html') # would need to actually make this page

if __name__ == '__main__':
    # IMPORTANT: change url to the site where you are editing this file.
    website_url = 'cocalc13.ai-camp.dev'
    
    print(f'Try to open\n\n    https://{website_url}' + base_url + '\n\n')
    app.run(host = '0.0.0.0', port=port, debug=True)
