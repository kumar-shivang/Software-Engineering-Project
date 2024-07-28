from mongoengine import connect


def init_db():
    client = connect(db="mydb", host="127.0.0.1", port=27017)
    print("\033[92mDatabase connected successfully\033[0m")
    print("\033[94m{}\033[0m".format(client))
