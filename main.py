
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename


import os
from datetime import datetime
import urllib.request
from openai import OpenAI

import api_key
import admin_details

from datetime import datetime
import pytz

import requests
import threading
from moviepy.editor import ImageClip, VideoFileClip, AudioFileClip
from mutagen.mp3 import MP3

import base64
import random

emergency_flag = False



###########################################################
#------------------1.CONFIG AREA---------------------------
###########################################################
app = Flask(__name__)

app.config['SECRET_KEY'] = b'\xb2\xab\x9d\xec\x8a\x98\xe7\x12\xd3\x14\x16\x94\xc3\x19\xa6\x18\x11\xb2\x1b\x10'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 5
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


admin_username = admin_details.get_admin_username
admin_mail = admin_details.get_admin_mail
admin_password = admin_details.get_admin_password

  

###########################################################
#------------------------CONFIG AREA End-------------------
###########################################################


#----------------------------------------------------------------------------------->





###########################################################
#---------------------2. Folder Creation part--------------
###########################################################


# Different upload folders for different types of files
app.config['UPLOAD_FOLDER_FILES'] = 'uploads/'  # For general file uploads
app.config['UPLOAD_FOLDER_IMAGES'] = 'static/Images'  # Specifically for image uploads
app.config['UPLOAD_FOLDER_PROFILE_IMAGE'] = 'static/upload_images'  

if not os.path.exists(app.config['UPLOAD_FOLDER_FILES']):
    os.makedirs(app.config['UPLOAD_FOLDER_FILES'])
    
if not os.path.exists(app.config['UPLOAD_FOLDER_IMAGES']):
    os.makedirs(app.config['UPLOAD_FOLDER_IMAGES'])

if not os.path.exists(app.config['UPLOAD_FOLDER_PROFILE_IMAGE']):
    os.makedirs(app.config['UPLOAD_FOLDER_PROFILE_IMAGE'])  
    




if not os.path.exists('static/imgs'):
    os.makedirs('static/imgs')

if not os.path.exists('static/img_gen'):
    os.makedirs('static/img_gen')
    
if not os.path.exists('static/AI_Voice'):
    os.makedirs('static/AI_Voice')

if not os.path.exists('static/Img_Video'):
    os.makedirs('static/Img_Video')

if not os.path.exists('static/AI_Caption_Video'):
    os.makedirs('static/AI_Caption_Video')


   

###########################################################
#---------------------Folder Creation End-----------------------------------
###########################################################


#----------------------------------------------------------------------------------->



###########################################################
#--------------------3. cache clear------------------------
###########################################################

def no_cache(response):
    """Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes."""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.after_request
def apply_no_cache(response):
    return no_cache(response)

###########################################################
#----------------------cache clear End---------------------
###########################################################


#----------------------------------------------------------------------------------->

###########################################################
#----------------------4. Data Base Creation--------------
###########################################################

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    ist = pytz.timezone('Asia/Kolkata')
    date_created = datetime.now(ist)
    account_created = db.Column(db.DateTime, default=date_created) # New column for account creation timestamp
    last_login = db.Column(db.DateTime)
    Logout_time = db.Column(db.DateTime)
    image_limit = db.Column(db.Integer, default=5)
    ai_caption_limit = db.Column(db.Integer, default=0)
    flag_check_freeze = db.Column(db.Integer, default=0)
    unique_key_pass = db.Column(db.Integer,default=123)
    password_changed = db.Column(db.Integer,default=0)
    password_changed_time = datetime.now(ist)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def unique_set_pass(self):
        self.unique_key_pass = random.randint(120, 500)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Create the database tables
with app.app_context():
    db.create_all()


###########################################################
#----------------------Data Base Creation End--------------
###########################################################

#----------------------------------------------------------------------------------->


###########################################################
#----------------------5. Main ROUTING PAGES---------------
###########################################################

@app.route('/')
def index():
    return redirect(url_for('GenAI'))#check with emergency flag
    #return redirect(url_for('shutdown')) # during working but website up
    
    #return redirect(url_for('closed_web')) # during working but website up
    
    
@app.route('/GenAI')
def GenAI():
    
    return render_template('landing_page.html')

@app.route('/shutdown')
def shutdown():
  
    return render_template('emergency_page.html')
    
@app.route('/closed_web')
def closed_web():
  
    return render_template('closed_web_page.html')

@app.route('/about_us')
def about_us():
    
    return render_template('about_us.html')  
    
    
@app.errorhandler(404)
def page_not_found(e):
    # your processing here
    return render_template('404.html'), 404

###########################################################
#---------------------Main ROUTING PAGES Ends--------------
###########################################################

if emergency_flag == False:
    #----------------------------------------------------------------------------------->


    ###############################################################
    #------------------6. USER SIDE -----------------------------------  
    ###############################################################

    client = OpenAI(api_key=api_key.openai_api_key)

    
    
    @app.route('/home')
    def home():
        if 'username' not in session:
            flash('You must be logged in to view the home page.')
            return redirect(url_for('login'))
        return render_template('home.html', username=session['username'])
        
    @app.route('/chat_assistance_info')
    def chat_assistance_info():
        if 'username' not in session:
            flash('You must be logged in to view the page.')
            return redirect(url_for('login'))
        return render_template('chat_assistance_info.html', username=session['username'])
    
    @app.route('/image_gen_info')
    def image_gen_info():
        if 'username' not in session:
            flash('You must be logged in to view the  page.')
            return redirect(url_for('login'))
        return render_template('image_gen_info.html')
    
    @app.route('/audio_transcript_info')
    def audio_transcript_info():
        if 'username' not in session:
            flash('You must be logged in to view the page.')
            return redirect(url_for('login'))
        return render_template('audio_transcript_info.html')
    
    @app.route('/ai_voice_info')
    def ai_voice_info():
        if 'username' not in session:
            flash('You must be logged in to view the  page.')
            return redirect(url_for('login'))
        return render_template('ai_voice_info.html')
    
    
    @app.route('/Account_hold')
    def Account_hold():
        
        return render_template('account_hold.html')


    #----------------------------6.1 chat bot-------------------------->
    @app.route('/chatbot')
    def chatbot():
        if 'username' not in session:
            flash('You must be logged in to view the chatbot.')
            return redirect(url_for('login'))
        
        return render_template('chatbot.html', username=session['username'])
     

    @app.route('/chat_with_bot', methods=['POST'])
    def chat_with_bot():
        user_message = request.json['message']

        response = client.chat.completions.create(
          model="gpt-3.5-turbo",
          messages=[
            {"role": "system", "content": "You are a helpful law and legal assistant ."},
            {"role": "user", "content": user_message}
          ]
        )

        
        ai_reply = response.choices[0].message.content


        return jsonify({'message': ai_reply})
         
    #----------------------------End chat bot-------------------------->


    #----------------------------------------------------------------------------------->

    #----------------------------6.2 Image generation-------------------------->
    @app.route('/image_generation', methods=['GET', 'POST'])
    def image_generation():
        if 'username' not in session:
            flash('You must be logged in to view the image generation page.')
            return redirect(url_for('login'))

        
        user = User.query.filter_by(username=session['username']).first()
        if user.image_limit <= 0:
            return redirect(url_for('limit_reached'))  

        
        user.image_limit -= 1
        db.session.commit()

        
        session['image_limit'] = user.image_limit

        image_size_options = ['1024x1024']
        generated_img_path = None

        if request.method == 'POST':
            img_description = request.form.get('img_description')
            image_size = request.form.get('image_size')
            
            generated_img_path = generate_image(session['username'], img_description, image_size)

        return render_template(
            'image_generation.html',
            user_limit_image=session['image_limit'],
            username=session['username'],
            image_size_options=image_size_options,
            generated_img_path=generated_img_path,
            
        )
        

    def generate_image(username, image_description, image_size):
        img_response = client.images.generate(
            model="dall-e-3",
            prompt=image_description,
            size=image_size,
            quality="standard",
            n=1,
        )
        
        filename = f'{username}.png'
        
        
        img_url = img_response.data[0].url
        image_path = f'static/img_gen/{filename}'
        urllib.request.urlretrieve(img_url, image_path)
        
        
        return image_path

    @app.route('/generated_image/<path:filename>')
    def get_generated_image(filename):
        return send_file(f'static/img_gen/{filename}', as_attachment=True)

    #----------------------------End Image generation-------------------------->

    #----------------------------------------------------------------------------------->

    #----------------------------6.3 Audio Transcript-------------------------->

    @app.route('/audio_transcript')
    def audio_transcript():
        if 'username' not in session:
            flash('You must be logged in to view the Audio Transcript')
            return redirect(url_for('login'))
        
            
        return render_template('audio_service_index.html', username=session['username'])
       
    @app.route('/transcribe_audio', methods=['POST'])
    def transcribe_audio():
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER_FILES'], filename)
            file.save(file_path)

            
            with open(file_path, "rb") as audio_file:
                
                transcript = client.audio.transcriptions.create(
                                  model="whisper-1",
                                  file=audio_file,
                                  response_format="text"
                                )

            
            os.remove(file_path)

            return jsonify({'transcript': transcript})

        return jsonify({'error': 'File not supported'}), 400
        



    #----------------------------End Audio Transcript-------------------------->

    #----------------------------------------------------------------------------------->
       
    #----------------------------6.4 Ai Audio Caption-------------------------->
    api_keys = api_key.openai_api_key

    @app.route('/ai_caption', methods=['GET', 'POST'])
    def ai_audio():

        if 'username' not in session:
            flash('You must be logged in to view the AI bytes.')
            return redirect(url_for('login'))
        
        user = User.query.filter_by(username=session['username']).first()
        
        if user.ai_caption_limit <= 0:
            return redirect(url_for('ai_caption_reached'))  

        
        user.ai_caption_limit -= 1
        db.session.commit()
        
        username = session['username']
        file_name = f'{username}.png'
        
        
        
        session['ai_caption_limit'] = user.ai_caption_limit

        video_generated = False
        
        if request.method == 'POST':
                if 'file' not in request.files:
                    return 'No file part'
                
                file = request.files['file']
        
                if file.filename == '':
                    return 'No selected file'
                
                if file:
                    
                    file.save(os.path.join('static/imgs', file_name))
                
                    
                image_url = r"static/imgs/"+ str(file_name)
                
                thread = threading.Thread(target=main_process, args=(image_url,session['username']))
                thread.start()
                thread.join()  # Wait for the processing to complete
                video_generated = True
                    
        return render_template('ai_bytes.html', video_generated=video_generated,username=session['username'])

        
    def get_mp3_duration(file_path):
        try:
            audio = MP3(file_path)
            return audio.info.length
        except Exception as e:
            print(f"Error in MP3 duration: {e}")
            return 0

    def create_video_from_image(image_path, duration, output_path):
        try:
            clip = ImageClip(image_path, duration=duration)
            clip.write_videofile(output_path, codec='libx264', fps=24)
        except Exception as e:
            print(f"Error in video creation: {e}")

    def text_speech(prompt,usrrname):
        
        
        try:
            
            usr_name = usrrname+".mp3"
            
            client = OpenAI(api_key=api_keys)
            
            response = client.audio.speech.create(
                model="tts-1",
                voice="onyx",
                input=prompt,
            )
            save_path_audio = "static/AI_Voice/"+str(usr_name)
            response.stream_to_file(str(save_path_audio))
            
        except Exception as e:
            print(f"Error in text to speech: {e}. Retrying...")

    def encode_image(image_path):
      with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

    def image_caption(image_path):
        
        try:
        

            # Getting the base64 string
            base64_image = encode_image(image_path)

            headers = {
              "Content-Type": "application/json",
              "Authorization": f"Bearer {api_keys}"
            }

            payload = {
              "model": "gpt-4-vision-preview",
              "messages": [
                {
                  "role": "user",
                  "content": [
                    {
                      "type": "text",
                      "text": "What’s in this image?"
                    },
                    {
                      "type": "image_url",
                      "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                      }
                    }
                  ]
                }
              ],
              "max_tokens": 300
            }

            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
            data = response.json()

            print(data['choices'][0]['message']['content'])
            return data['choices'][0]['message']['content']
        except Exception as e:
            print(f"Error in image captioning: {e}. ")

    def combine_ai(video_file_path, audio_file_path,usrrname):
        try:
            
            usr_name = usrrname+".mp4"
            save_path_video = "static/AI_Caption_Video/"+str(usr_name)
            
            video_clip = VideoFileClip(video_file_path)
            audio_clip = AudioFileClip(audio_file_path)
            final_clip = video_clip.set_audio(audio_clip)
            final_clip.write_videofile(str(save_path_video))
        
        except Exception as e:
            print(f"Error in combining AI: {e}")

    def main_process(image_path,ussr_name):
        print(image_path)
        
        usr_name = ussr_name
        file_path = image_path

        
        caption = image_caption(file_path)
        #print('caption done..\n\n\n')
        
        text_speech(caption,usr_name)
        
        #print('speech done..\n\n\n')
        
        set_ai_voice_path = "static/AI_Voice/"+str(usr_name)+".mp3"
        
        duration = get_mp3_duration(str(set_ai_voice_path))
        
        #print('duration done..\n\n\n')
        
        set_video_path = "static/Img_Video/"+str(usr_name)+".mp4"
        
        create_video_from_image(file_path, duration, str(set_video_path))
        
        #print('image video done..\n\n\n')
        
        combine_ai(str(set_video_path), str(set_ai_voice_path),usr_name)
        
        #print("Video creation complete.")



       
    #----------------------------End Ai Audio Caption-------------------------->

    #----------------------------------------------------------------------------------->


    #----------------------------------------------------------------------------------->


    ###############################################################
    #------------------End USER SIDE -----------------------------------  
    ###############################################################

    #----------------------------------------------------------------------------------->


    ###############################################################
    #------------------Profile View -----------------------------------  
    ###############################################################

    @app.route('/profile_view')
    def profile_view():
        if 'username' not in session:
            flash('You must be logged in to view the profile page.')
            return redirect(url_for('login'))
        
        
        user = User.query.filter_by(username=session['username']).first()
        if user is None:
            flash('User not found.')
            return redirect(url_for('login'))  
         
        user_details = {
            'email': user.email,
            'image_limits': user.image_limit,
            'last_login': user.last_login,
            'ai_caption_limit':user.ai_caption_limit
        }

        
        image_file = os.path.join(app.config['UPLOAD_FOLDER_PROFILE_IMAGE'], session['username'] + '.jpg')

        return render_template('profile_view.html', last_login=user_details['last_login'], username=session['username'], user_details=user_details['email'], user_image=user_details['image_limits'], user_ai_voice_limit=user_details['ai_caption_limit'],image_file=image_file)


    @app.route('/upload-image', methods=['POST'])
    def upload_image():
        
        username = session.get('username') or request.form.get('username')
        if not username:
            flash('Username not provided.')
            return redirect(url_for('login'))  

        image = request.files.get('profile_image')
        if image and image.filename:
            filename = username + '.jpg'  
            image.save(os.path.join(app.config['UPLOAD_FOLDER_PROFILE_IMAGE'], filename))
            return redirect(url_for('profile_view'))  

        return 'Failed to upload image'



    @app.route('/history_load')
    def history_load():
        if 'username' not in session:
            flash('You must be logged in to view the profile page.')
            return redirect(url_for('login'))
        
        
        return render_template('history_view.html', username=session['username'])

    ###############################################################
    #------------------Profile View -----------------------------------  
    ###############################################################


    #----------------------------------------------------------------------------------->

    ###############################################################
    #------------------Limit control pages------------------------- 
    ###############################################################


    @app.route('/limit_reached')
    def limit_reached():
        if 'username' not in session:
            flash('You must be logged in to view the  page.')
            return redirect(url_for('login'))
            
        return render_template('exceed.html')
        
    @app.route('/ai_caption_reached')
    def ai_caption_reached():
        if 'username' not in session:
            flash('You must be logged in to view the  page.')
            return redirect(url_for('login'))
            
        return render_template('ai_caption_exceed.html')
        

    ###############################################################
    #------------------End Limit control pages -----------------------------------  
    ###############################################################


    #----------------------------------------------------------------------------------->


    ###############################################################
    #------------------END USER SIDE -------------------------------
    ###############################################################








    ###############################################################
    #------------------ADMIN SIDE ---------------------------------
    ###############################################################



    @app.route('/admin_home')
    def admin_home():
        if 'username' not in session or session['username'] != admin_username:
                flash('only admin can view the page')
            
                return redirect(url_for('login'))
        
        
        user_details = User.query.all()  
        return render_template('admin_home.html',username=session['username'], user_details=user_details)




    @app.route('/user_details')
    def user_details():
        if 'username' not in session or session['username'] != admin_username:
            flash('Only admin can view this page.')
            return redirect(url_for('login'))

        user_details = User.query.all()
        return render_template('user_details.html', username=session['username'], user_details=user_details)
    
    @app.route('/reset_user_pass_view')
    def reset_user_pass_view():
        if 'username' not in session or session['username'] != admin_username:
            flash('Only admin can view this page.')
            return redirect(url_for('login'))

        user_details = User.query.all()
        return render_template('admin_reset_info.html', username=session['username'], user_details=user_details)

    @app.route('/forgot_pass')
    def forgot_pass():
        

        
        return render_template('reset_password.html')



    @app.route('/update_user_details', methods=['POST'])
    def update_user_details():
        if 'username' not in session or session['username'] != admin_username:
            flash('Only admin can perform this action.')
            return redirect(url_for('login'))

        user_id = request.form.get('user_id')
        
        new_image_limit = int(request.form.get('new_image_limit'))
        new_ai_voice_limit = int(request.form.get('new_ai_voice_limit'))
        flag_check = int(request.form.get('flag_check_freeze'))
        

        
        user = User.query.get(user_id)
        if user:
            user.image_limit = new_image_limit
            user.ai_caption_limit = new_ai_voice_limit
            user.flag_check_freeze = flag_check
            db.session.commit()
            
        else:
            flash('User not found.')

        return redirect(url_for('user_details'))



    @app.route('/delete_user/<int:user_id>', methods=['DELETE'])
    def delete_user(user_id):
        
        user_to_delete = User.query.get(user_id)
        if user_to_delete:
            db.session.delete(user_to_delete)
            db.session.commit()
            return jsonify(success=True)
        else:
            return jsonify(success=False), 404
            
            
            
    ###############################################################
    #------------------ADMIN SIDE END  ---------------------------- 
    ###############################################################







    ###############################################################
    #------------------FRONTEND  ------------------------------------ 
    ###############################################################


    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if 'username' in session:
            return redirect(url_for('home'))

        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            
            if not (4 <= len(password) <= 6) or not (password.isalpha() or password.isnumeric() or password.isalnum()):
                flash('Password must have between 4 - 6 characters and consist of plain alphabetic, plain numeric, or a combination of both.')
                return redirect(url_for('signup'))

            
            if not username or not email or not password:
                flash('Please fill out all fields')
                return redirect(url_for('signup'))

            user_email = User.query.filter_by(email=email).first()
            user_name = User.query.filter_by(username=username).first()
            
            if user_email:
                flash('Email address already exists')
                return redirect(url_for('signup'))
            if user_name:
                flash('username already exists')
                return redirect(url_for('signup'))
            
            

            new_user = User(username=username, email=email)
            new_user.set_password(password)
            new_user.unique_set_pass()
            
            db.session.add(new_user)
            db.session.commit()

            flash('Account created successfully, please log in.')
            return redirect(url_for('login'))
        return render_template('signup.html')




    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if 'username' in session:
            return redirect(url_for('home'))
        
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
         
            
            if email == admin_mail and password == admin_password:
                session['username'] = admin_username  
                
                return redirect(url_for('admin_home'))
            

            user = User.query.filter_by(email=email).first()
            
            if user and user.check_password(password):
            
                if user.flag_check_freeze != 1:
                    session['username'] = user.username
                    
                    ist = pytz.timezone('Asia/Kolkata')
                    session['login_time'] = datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S')  # Store login time in IST in session
                    return redirect(url_for('home'))
                else:
                    return redirect(url_for('Account_hold'))
                    
            else:
                flash('Invalid credentials')
        return render_template('login.html')




    @app.route('/logout')
    def logout():
        
        username = session.get('username')
        
        if username:
            user = User.query.filter_by(username=username).first()
            if user:
                
                login_time = datetime.strptime(session.get('login_time', datetime.now().strftime('%Y-%m-%d %H:%M:%S')), '%Y-%m-%d %H:%M:%S')
                user.last_login = login_time 
                user.Logout_time = datetime.now()
                
                db.session.commit()  
        
        session.pop('username', None)
        session.pop('image_limit', None)
        session.pop('limit_reduced', None)
        
        user = User.query.filter_by(username=session.get('username')).first()
        if user:
            user.last_login = session.get('login_time', datetime.now())  
            db.session.commit()  
        
        session.pop('login_time', None) 
        
        if username:
            flash(f'You have been logged out, {username}.')
        else:
            flash('You have been logged out.')
        
        return redirect(url_for('GenAI'))

    @app.route('/reset_password', methods=['POST'])
    def reset_password():
        data = request.get_json()
        email = data.get('email')
        unique_key = data.get('uniqueKey')
        new_password = data.get('newPassword')

        # Query the user by email
        user = User.query.filter_by(email=email).first()

        if user:
            # Check if the provided unique key matches the user's unique key
            
            if int(user.unique_key_pass) == int(unique_key):
                
                user.set_password(new_password)
                user.unique_key_pass = random.randint(120, 500)
                user.password_changed = user.password_changed + 1
                ist = pytz.timezone('Asia/Kolkata')
                user.password_changed_time = datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S')
                
                 
                db.session.commit()
                return jsonify({'success': True})
            else:
                return jsonify({'success': False, 'message': 'Unique key does not match'})
        else:
            return jsonify({'success': False, 'message': 'Email not found in database'})
         
     
    ###############################################################
    #------------------FRONTEND SIDE END  -------------------------   
    ###############################################################







    if __name__ == '__main__':
        app.run(debug=True)

if emergency_flag == True:
    if __name__ == '__main__':
        app.run(debug=True)
