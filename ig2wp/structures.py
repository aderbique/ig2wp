




class Post:
   """Base class to hold details of each post"""

   def __init__(self, text=None, location=None,location_slug=None, timestamp=None, shortcode=None, images=None,author=None):
      self.text = text
      self.location = location
      self.location_slug = location_slug
      self.timestamp = timestamp
      self.shortcode = shortcode
      self.images = images
      self.author = '1'
      self.featured_media = None
      self.content = ''
      if self.text is not None:
         self.content = "<p>Location: {}</p>".format(self.location)

   def add_image(self, image_fp):
      self.images.append(image_fp)


   def append_content(self,id,link,f_type):
      print(id)

      if self.featured_media is None:
         self.featured_media = id
      if f_type == 'image/jpg':
         print("JPG")
         html = '<!-- wp:image {"id":' + id + ',"sizeSlug":"large","linkDestination":"none"} -->\n<figure class="wp-block-image size-large"><img src="' + link + ' alt="" class="wp-image-' + id + '"/></figure>\n<!-- /wp:image -->'
      elif f_type == 'video/mp4':
         html = '<!-- wp:video {"id":' + id + ' -->\n<figure class="wp-block-video"><video controls src="' + link + '"></video></figure>\n<!-- /wp:video -->'
      else:
         raise Exception("Unsupported Media Type")
      self.content += "\n{html}".format(html=html)

class Connection:
   """Base Class to hold connection string details to Wordpress"""

   def __init__(self, host, username, password):
      self.host = host
      self.username = username
      self.password = password

      if host is None or username is None or password is None:
         raise Exception("Sorry, you must supply all login details.")
