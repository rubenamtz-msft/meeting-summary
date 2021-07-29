Intelligent Meeting Summary
===========================

## Description
--------
We all have a lot of meetings every day, but we cannot divide ourselves into multiple meetings. What if we missed an important meeting and the meeting was not recorded? Boomer😢, even if it was, 30 minutes of your free time watching a meeting? I don't think so 👀. Hey but you still have the transcripts... okey, that's even more exhausting. Also, time is money, let’s save that one hour to spend with our family and use this awesome Text Meeting Summary Tool so that you don’t miss anything.

Disclaimer: You will need to have the meeting captions 😜

## Requirements
--------
The Dockerfile installs all the dependencies at building stage. However, if you would like to setup your local environment create and activate a virtual enviroment and run
```
$ pip install -r requirements/base.txt -f https://download.pytorch.org/whl/torch_stable.html
```

Also consider that you will need your docker and wsl2 installed in your computer.

## What to expect
--------
This repository is intended for demo purposes and it only supports text in English. It uses Django and Postgres and a Transformer-based Machine Learning model for abstractive text summarization. For more information about the model []().The summarization model is exposed at `POST http://127.0.0.1:5000/api/summary/`.

The working demo has the summarization model exposed at `POST http://summarizer-api.westus.azurecontainer.io:5000/api/model/summary/`.

The expected body in your request should have the following data contract:
```JSON
{
    "captions": [
        {
            "start": "00:00:00.000",
            "end": "00:00:02.850",
            "text": "Hello, this is sample text",
            "name": "Elon Musk"
        },
        {
            "start": "00:00:03.000",
            "end": "00:00:07.800",
            "text": "Talking non-sense, Talking non-sense, Talking non-sense, Talking non-sense, Talking non-sense, Talking non-sense, Talking non-sense, more non-sense and more non-sense.",
            "name": "Anonymous"
        },
         {
            "start": "00:00:08.000",
            "end": "00:00:11.500",
            "text": "Here I go again, talking non-sense, Talking non-sense, Talking non-sense, Talking non-sense, Talking non-sense, Talking non-sense, Talking non-sense, more non-sense and more non-sense.",
            "name": "Anonymous"
        },
     ]
}
```
Where each element in the list represents a new caption block from within the same "conversation".

You should expect an answer with the following data contract:
```JSON
[
    {
        "id": "c9da5061-cbdd-43ce-b3ab-ee90f92e40a7",
        "summary": "Hello, this is sample text",
        "properties": {
            "source": {
                "id": "c936b8cf-75b0-4e4c-8617-796dc68df54d",
                "text": "Hello, this is sample text",
                "start": "00:00:00.000"
            },
            "words_count": 5,
            "name": "Elon Musk"
        }
    },
    {
        "id": "94c5b2b4-aed3-4f60-b210-c55148794bf1",
        "summary": "A bunch of non-sense",
        "properties": {
            "source": {
                "id": "bee951cb-ffef-42fe-a33e-a8a5920d15da",
                "text": "Talking non-sense, Talking non-sense, Talking non-sense, Talking non-sense, Talking non-sense, Talking non-sense, Talking non-sense, more non-sense and more non-sense. Here I go again, talking non-sense, Talking non-sense, Talking non-sense, Talking non-sense, Talking non-sense, Talking non-sense, Talking non-sense, more non-sense and more non-sense.",
                "start": "00:00:03.000"
            },
            "words_count": 17,
            "name": "Anonymous"
        }
    },
]
```
Where each element in the list represents either:
- A summary split based off a single caption block *or*
- A summary split based off multiple caption blocks.

A list of caption blocks' 'line break' is influenced by two factors:
- _Everytime a new person speaks_, as we want to only summarize text from the same person and to also keep the chronological order of dialog exchanged.
- _Everytime we reach a limit of 500 words_, as the ML model only allows for 500 tokens as input.

Notice that the first summary split is exactly as the input text. We decided to not try to summarize inputs with less than 50 words as they might already contain summarized information by default.

Notice that a `start` property is also return, this corresponds to the timestamp of the first appended caption block out of all the appended blocks to produce this particular summary element. This is used to help the user navigate to different points in the actual caption file in the search for extra context.


Basic Commands
--------------

### Build the containers (local and production environments)

-   There are two different environments that are able to build, a local and a production environment. The local environment will hold two services, Django and postgres. It will expose Django through the port 8000. To build the environment run:
```
$ docker-compose -f local.yml build
```
-   The production environment should no longer expose Django (as of today the service is still exposed for debuggin purposes) and it will not hold a postgres services (it is actually configured to work with an external postgres server, but the config files are not present in the project for security reasons). To build the production environment run:
```
$ docker-compose -f production.yml build
```
To produce the hidden Django and postgres server configuration files just copy the structure of .envs/.local and call it .production and fill it up with the respective values.

### Running the containers

To run either container environment run:
```
$ docker-compose -f <env_file_name>.yml up
```

### Create a superuser

To access your local database you will need to first create a superuser:
```
$ docker-compose -f local.yml run django python manage.py createsuperuser
```

### Committing changes to the database

For the local environment you will have to run:
```
$ docker-compose -f local.yml run django python manage.py makemigrations
$ docker-compose -f local.yml run django python manage.py migrate
```
For the production environment you will only have to run:
```
$ docker-compose -f local.yml run django python manage.py migrate
```

## Deployment
----------

Remember that your production container image is setup to connect to an external DB, please set it up before deploying your container. For more info please refer to: [Creating a Postgres server in Azure](https://docs.microsoft.com/en-us/azure/postgresql/quickstart-create-server-database-portal)
  
### Publish the container image
To push the image to Azure Image Registry you will need to first create a container registry in your Azure Subscription. 

### Log in to your registry  
```
$ az acr login --name <your_registry_name>
```

### Tag your image (create an alias)
```
$ docker tag <your_local_image_name> <your_registry_name>.azurecr.io/<version_number> 
```

### Push your image to your registry  
```
$ docker push <your_registry_name>.azurecr.io/<version_number>
```
For more info: [Push an image](https://docs.microsoft.com/en-us/azure/container-registry/container-registry-get-started-docker-cli?tabs=azure-cli)  

## Deploy your registered container image
  
Please following this tutorial: [Deploy a container instance using the Azure portal](https://docs.microsoft.com/en-us/azure/container-instances/container-instances-quickstart-portal)

> Important note: It is recommended to setup your environment variables at instance creation time even if they are set in your code base. Also, to be able to debug select "Never" for the Restart policy, otherwise if something fails you won't be able to see the logs. This is cubersome but necessary, once you finish debugging you can delete your instance and recreate it again with a more suitable Restart policy.