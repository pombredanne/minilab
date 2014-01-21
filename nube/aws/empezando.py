import boto
s3 = boto.connect_s3()
bucket = s3.create_bucket('xmn.net')  # bucket names must be unique
key = bucket.new_key('data/data.csv')
key.set_contents_from_filename('data/source-data.csv')
key.set_acl('public-read')
