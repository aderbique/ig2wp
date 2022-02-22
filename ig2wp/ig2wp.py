import os
import lzma
import json
import re
import glob
import requests
from requests.auth import HTTPDigestAuth
from datetime import datetime
from configparser import ConfigParser
from requests_toolbelt.multipart.encoder import MultipartEncoder
from .structures import Post, Connection

class Ig2wp:
    """Instagram to Wordpress Class"""

    def __init__(self, directory, host,username, password):
        #self.connection = Connection(host,username,password)
        self.directory = directory
        self.host = host
        self.username = username
        self.password = password

        if username is None:
            print("Attempting to load config file")
            config_dir = "{}/.ig2wp".format(os.path.expanduser('~'))
            config_object = ConfigParser()
            config_object.read("{}/config.ini".format(config_dir))

            self.directory = config_object["INSTALOADERDIR"]["directory"]
            self.host = config_object["SERVERCONFIG"]["server"]
            self.username = config_object["USERINFO"]["username"]
            self.password = config_object["USERINFO"]["password"]


    def main(self):
        """Run the program"""
        if self.username is None or self.password is None or self.host is None or self.directory is None:
            raise Exception("Please refer to help page for instructions on necessary parameters.")            
        

        # The meat and bones. Start combing through for compressed json files
        # one json.xz file per post  
        for fname in glob.glob(os.path.join(self.directory, '*.json.xz')):
            f = os.path.join(self.directory, fname)
            post = self.get_post(f)
            #print(post.text)
            # Iterate through post media and upload
            # Add ID tag to post object
            base_name = fname.replace('.json.xz', '')
            for mname in glob.glob(os.path.join(self.directory, '{}*'.format(base_name))):
                if mname.endswith(".jpg") or mname.endswith(".mp4"):
                    id, link, f_type = self.upload_file(mname)
                    post.append_content(str(id),link,f_type)
            result = self.create_post(post)
            result.raise_for_status()

    def get_post(self, file_path):
        post = Post()
        with lzma.open(file_path, mode='r') as fp:
            data = fp.read()
            obj = json.loads(data)          
            post.text = obj['node']['edge_media_to_caption']['edges'][0]['node']['text']
            post.timestamp = obj['node']['taken_at_timestamp']
            post.shortcode = obj['node']['shortcode']

            # Not all posts have a location set
            try:
                post.location = obj['node']['location']['name']
                post.location_slug = obj['node']['location']['slug']
            except:
                print("Could not determine location for {}".format(file_path))
                post.location = "Lost in space"
                post.location_slug = "lost-in-space"
        return post
    
    def create_post(self, post):
        post_url = "{}/wp-json/wp/v2/posts".format(self.host)
        # Convert from Epoch into Wordpress friendly timestamp
        dt = datetime.fromtimestamp(post.timestamp)
        post_date = dt.strftime('%Y-%m-%dT%H:%M:%S')
        title_date = dt.strftime('%B %w, %Y')

        body = {
            "date": post_date,
            "date": post_date,
            "slug": post.location_slug,
            "status": "publish",
            "title":  post.text,
            "content": post.content,
            "author": post.author,
            "excerpt": post.text,
            "featured_media": post.featured_media,
            "comment_status": "open",
            "ping_status": "open",
            "format": "standard",
            "meta": [],
            "sticky": False,
            "template": "",
            "categories": [
            1
            ],
            "tags": []
        }

        x = requests.post(post_url, json=body, auth=(self.username, self.password))
        return x

    def upload_file(self, media_fp):
        media_url = '{}/wp-json/wp/v2/media'.format(self.host)
        data = open(media_fp, 'rb').read()
        fname = os.path.basename(media_fp)
        #last_modified= os.stat(media_fp).st_mtime
        #date = datetime.fromtimestamp(last_modified).strftime('%Y-%m-%dT%H:%M:%S')
        exp = '(\d{4}-\d{2}-\d{2})_(\d{2})-(\d{2})-(\d{2})'
        date, hour, minute, second =re.findall(exp,media_fp)[0]
        timestamp = "{date}T{hour}:{minute}:{second}".format(date=date,hour=hour,minute=minute,second=second)
        f_type = ''
        if (media_fp.endswith(".jpg")):
            f_type = 'image/jpg'
        elif (media_fp.endswith(".mp4")):
            f_type = 'video/mp4'
        else:
            raise Exception("The file {} is an unsupported File Type. Skipping...".format(media_fp))

        multipart_data = MultipartEncoder(
            fields={
                # a file upload field
                'file': (fname, open(media_fp, 'rb'), f_type),
                # plain text fields
                'date': timestamp,
                'description': 'Uploaded using IG2WP'
                #'post': '1',
            }
        )

        res = requests.post(url=media_url,
                            data=multipart_data,
                            headers={'Content-Type': multipart_data.content_type},
                            auth=(self.username, self.password))
        newDict=res.json()
        newID= newDict.get('id')
        link = newDict.get('guid').get("rendered")
        return newID, link, f_type

def ig2wp():
    ''' do it
    '''
    print("in main")
    Ig2wp().main()


if __name__ == '__main__':
    print("running stuff")
    Ig2wp().main()