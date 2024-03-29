# conda_flask-app

# apt installs
sudo apt install python3-pyaudio
sudo apt-get install portaudio19-dev
 
# Development

1. create an environment on anaconda with python 3.7.4
  1. conda create -n envname python=3.7.4
  2. conda activate envname
  3. conda install flask
  4. pip install gunicorn

2. To run the application, clone it on the local machine and run
  1. gunicorn --bind 0.0.0.0:5000 connector:app

3. To see all the installed pip libraries, run
  1. pip freeze > requirements.txt

# Deployment:

Note: all the below process should run in conda environment

1. Run pip freeze > requirements.txt to see if there are any changes on requirements.txt

2. If needed, create a buildpack on heroku app
  heroku buildpacks:add heroku/python
  <!-- used to read the "Aptfile" of our project -->
  heroku buildpacks:add https://github.com/heroku/heroku-buildpack-apt.git
  heroku buildpacks:add --index 1 heroku-community/apt

3. If used any packages which are not installed with pip, then add those in "Aptfile"

4. git push heroku master

5. to check logs use "heroku logs --tail"

# Hosted:
  Hosted on heroku
  URL: https://warm-beyond-68761.herokuapp.com/
