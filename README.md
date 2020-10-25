# conda_flask-app
 
# Development

1. create an environment on anaconda with python 3.7.4
  1. conda create -n envname python=3.7.4
  2. conda activate envname
  3. conda install flask
  4. pip install gunicorn

2. To run the application, clone it on the local machine and run
  1. gunicorn --bind 0.0.0.0:5000 connector:app

3. To see all the installed pip libraries, run
  1. pip freeze requirements.txt

# Deployment:

1. create a buildpack on heroku app
  heroku buildpack:add heroku/python
  heroku buildpack:add https://github.com/heroku/heroku-buildpack-apt.git

2. If used any packages which are not installed with pip, then add those in "Aptfile"

# Hosted:
  Hosted on heroku
  URL: https://warm-beyond-68761.herokuapp.com/
