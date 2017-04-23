from pymongo import MongoClient
from django.utils.text import slugify
import gridfs
from django.http import StreamingHttpResponse


def get_mongodb_client():
    return MongoClient()


def create_or_get_database_name(user):
    client = get_mongodb_client()
    db = client[slugify(user.username)]
    return slugify(user.username)


def get_collection(instance):
    client = get_mongodb_client()
    db = create_or_get_database_name(instance.user)
    database = client[db]
    instance.database = db
    instance.save()
    return database[instance.collection]


def drop_files(instance,options):
    client = get_mongodb_client()
    file_name = instance.file_name
    db = (client[create_or_get_database_name(instance.user)])
    collection = db.fs.files
    result = collection.find_one({'filename': file_name})
    files_id = result['_id']
    fs = gridfs.GridFS(db)
    fs.delete(files_id)

def create_collection(instance):
    client = get_mongodb_client()
    name = instance.name
    instance.collection = name
    instance.save()
    fs = gridfs.GridFS(client[create_or_get_database_name(instance.user)])
    fs.put(instance.file, filename=instance.file_name)
    return name
