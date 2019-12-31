# Gcloud Deploy Notes

Go to Google Cloud Platform, select or create the project we want to build.
Click on the Gcloud shell button (top right area, looks like a terminal icon).
Git clone the desired repository (or, if it is already cloned, git pull origin master)
We should see at least the following files: app.yaml, main.py, and requirements.txt .
We need a virtual environment. So in the Gcloud shell,type:
  `virtualenv --python python3 ~/envs/project_name` replacing project_name as appropriate.
Activate the environment: `source ~/envs/hello_world/bin/activate`
Install dependencies: `pip install -r requirements.txt`
Run the app: `python main.py`

Deploying to App Engine:
If not already done, we need to create an gcloud app: `gcloud app create`
Deploy the app: `gcloud app deploy app.yaml --project fb-test-251219`
replacing project name as appropriate.

-- End of Document --
