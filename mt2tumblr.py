#!/usr/bin/env python

import simplejson as json, urllib, urllib2, sys, time, codecs
from mt2tumblrSettings import tumblrEmail, tumblrPassword, tumblrSite, tumblrUrl, mtImportFile

# Clean up configuration just in case. The site should be just a hostname with no prefix/suffix.
tumblrSite = tumblrSite.replace("http://", "").strip("/")


# Import current posts from Tumblr from the API, so that we can avoid posting duplicates.

print "Downloading current posts from Tumblr..."

params = urllib.urlencode({"email": tumblrEmail, "password": tumblrPassword})

posts = []
startedDownload = False
postsTotal = 0

while not startedDownload or (len(posts) < postsTotal):
    try:
        request = urllib2.urlopen(tumblrUrl + '/api/read/json?num=50&start=' + str(len(posts)), params)
    except urllib2.HTTPError:
        print "Your Tumblr URL, email or password are wrong. Could not connect to Tumblr."
        sys.exit(0)
    
    # I don't know why Tumblr has to use this format instead of a regular JSON string. Hope they won't change it
    # and break this parser.
    jsonString = request.readlines()[0].replace('var tumblr_api_read = ', '').strip(";\n")
    postsFromApi = json.loads(jsonString)

    postsTotal = int(postsFromApi["posts-total"])

    for post in postsFromApi["posts"]:
        posts.append(post)
    
    startedDownload = True

    print "Downloaded", len(posts), "of", postsTotal
    sys.stdout.flush()


print "Done downloading current posts from Tumblr. Now parsing the Movable Type export file and posting to Tumblr."

# Map MovableType metadata fields to Tumblr post fields.
metadataMappings = {
    'DATE': 'date',
    'BASENAME': 'slug',
    'TITLE': 'title'
}

# Import the whole file as a bigass Unicode string and go from there. I tested that it works fine
# with a blog that contains UTF-8.
postsFromMt = codecs.open(mtImportFile, encoding='utf-8', mode='r').read().strip().split("--------\n")

print "Found", len(postsFromMt), "posts in Movable Type export file."
postIndex = 0

for mtPost in postsFromMt:
    postIndex += 1
    postPieces = mtPost.split("-----\n")
    post = {'body': '', 'email': tumblrEmail, 'password': tumblrPassword, 'type': 'regular', 'group': tumblrSite}
    
    for line in postPieces[0].splitlines():
        for field in metadataMappings:
            if line.startswith(field):
                post[metadataMappings[field]] = line.replace(field + ": ", "")
                if metadataMappings[field] == "slug":
                    post["slug"] = post["slug"].replace("_", "-") # Tumblr likes dashes better.
        if line.startswith('CONVERT BREAKS:'):
            if line.strip().endswith('skypeemo_with_mdsp') or line.strip().endswith('markdown') or line.strip().endswith('markdown_with_smartypants'):
                post["format"] = "markdown"
            else:
                post["format"] = "html"
    
    for piece in postPieces[1:]:
        if piece.startswith("BODY:\n") or piece.startswith("EXTENDED BODY:\n"):
            post['body'] += "\n".join(piece.splitlines()[1:]) + "\n\n"
        
    if len(post["body"]) > 0:
        print "Posting {0}/{1}:".format(postIndex, len(postsFromMt)), post["title"], "from", post["date"],
        sys.stdout.flush()
        
        alreadyExists = False
        
        for currentPost in posts:
            if (currentPost["type"] in ["text", "regular"]) and (currentPost["regular-title"] == post["title"]):
                alreadyExists = True
        if not alreadyExists:
            try:
                post["title"] = post["title"].encode('utf-8')
                post["body"] = post["body"].encode('utf-8')
                request = urllib2.urlopen('http://www.tumblr.com/api/write', urllib.urlencode(post))
                print "... ok."
            except urllib2.HTTPError, e:
                print "... posting failed. Check your configuration. Error:", e
                if e.code == 400:
                    print "Got error 400. This may mean we are posting too fast. Taking a little break for 15 seconds... or press Ctrl-C and try again later."
                    time.sleep(15)
        else:
            print "... skipping this post, already exists in Tumblr."
            
print "Done."
