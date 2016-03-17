<h1>Twitter Streaming App</h1>

<p>
<b>Twitter Streaming App</b> is a twitter streaming data fetching django application using <b>twitter tweepy module</b>. The API used for the twitter app is Streaming Api. <b>Django Celery</b> is used for running twitter streaming data fetching operation. Database is used for storing twitter json data is <b>Pymongo</b>, which is a python based NoSQL MongoDB Database.
</p>

<h3>Django Celery</h3>

<p>Celery is an asynchronous task queue based on distributed message passing. Celery requires a solution to send and receive messages; usually this comes in the form of a separate service
called a message broker. Here we are using RabbitMQ as Broker.
</p>

<h3>MongoDB</h3>
<p>MongoDB is an open-source document database, and leading NoSQL database. MongoDB is written in JavaScript, C, C++.</p>


<h4>Installation</h4>

<div>Create a new Virtual Environment

<p>	<b>$virtualenv env</b></p>
</div>


<div> Activate virtualenv

<p><b> $source ./env/bin/activate</b></p>
</div>

<div>Enter the app location and Install the requirements for twitterapp

<p><b>$pip install -r requirements.txt</b></p>
</div>

<div>After installation, run the django celery worker server

<p><b>$celery -A streamapi worker -l info</b></p>
</div>