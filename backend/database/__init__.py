from mongoengine import connect, Document, StringField

# Replace the connection string with your actual connection string of mongodb atlas
# MONGO_URI = ""


def init_db():
    # client = connect(host=MONGO_URI) # for mongo db atlas
    client = connect(db="mydb", host="127.0.0.1", port=27017)
    print("\033[92mDatabase connected successfully\033[0m")
    # print("\033[94m{}\033[0m".format(client))
