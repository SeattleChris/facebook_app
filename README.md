# facebook_app

**Author**: Chris L Chapman
**Version**: 0.1.0
<!-- (increment the patch/fix version number up if you make more commits past your first submission) -->

## Deploy notes

We are currently deploying on google cloud (gcloud), with a flask server. Gcloud is expecting a pip requirements file (requirements.txt), an app.yaml file (indicating what python version to use), and a main.py file for our server code file. Gcloud also allows an ignore file (.gcloudignore) which follows the same concepts from .gitignore files. Locally we are using pipenv to help us track dependencies and packages only needed in the development environment. However, the Pipfile and Pipfile.lock files should be in the ignore file for uploading to gcloud.

Deployed site:
[https://fb-test-251219.appspot.com/](https://fb-test-251219.appspot.com/)

## Overview

<!-- What is this project for? What does it do? -->

## Getting Started

<!-- What are the steps that a user must take in order to build this app on their own machine and get it running? -->

## Architecture

<!-- Provide a detailed description of the application design. What technologies (languages, libraries, etc) you're using, and any other relevant design information. This is also an area which you can include any visuals; flow charts, example usage gifs, screen captures, etc.-->

## API

<!-- Provide detailed instructions for your applications usage. This should include any methods or endpoints available to the user/client/developer. Each section should be formatted to provide clear syntax for usage, example calls including input data requirements and options, and example responses or return values. -->

## Change Log

<!-- Ctrl+Shift+I (on Win & Linux) Inserts current DateTime, -->
