#!/usr/bin/python
import memcache
import boto3


def main():
    """
    Connects to the memcache first. Then puls the data from S3
    Stores the data pulled from S3 to the memcache instance.
    I just placed a cronjob for this to run once a day.
    """
    client = memcache.Client([('127.0.0.1', 11211)])

    s3 = boto3.resource('s3')
    bucket = s3.Bucket('api.ilmnuri.com')
    list_items = []
    dictionary = {'Abdulloh': {}, 'AbuNur': {}, 'Ayyubxon': {}}

    for key in bucket.objects.all():
        list_items.append(key.key)

    for item in list_items:
        s = item.split('/')
        if s[1] not in dictionary[s[0]]:
            dictionary[s[0]][s[1]] = []

    for item in list_items:
        s = item.split('/')
        if s[1] in dictionary[s[0]].keys():
            if s[2]:
                dictionary[s[0]][s[1]].append(s[2])

    client.set('album', dictionary)


if __name__ == '__main__':
    main()
