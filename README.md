# conda_flask-app
 
create an environment on anaconda with python 3.7.4
  conda create -n envname python=3.7.4
  conda activate envname
  conda install flask
  pip install gunicorn

To run the application, clone it on the local machine and run
  gunicorn --bind 0.0.0.0:5000 connector:app
