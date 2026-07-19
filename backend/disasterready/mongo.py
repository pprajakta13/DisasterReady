from mongoengine import connect

connect(
    db="disasterready",
    host="localhost",
    port=27017
)