# weibo_api
It is a simple weibo api depend on cookies. I just use it to delete all my weibo post.

### Install
1. Install requirment modules. `$ sudo pip install -r requirements.txt`
2. Put your cookie to the file named *weibo.dat*
2. Execute *example.py*, it will test to post a message.


### Usage
```Python
weibo = Weibo()

# Post a new message
weibo.post("Test post. Enjoy it!")

# Delete your post with mid. TODO: the mid is your post id
weibo.del_post(1234567890)

# List all post in your weibo homepage. It will return the list of mid
weibo.list()

# Delete all posts
weibo.del_all_post()
```
