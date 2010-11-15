# mt2tumblr. A Tumblr importer.

Jaanus Kase, jaanuskase.com

This script imports blog entries from [Movable Type Import format](http://www.sixapart.com/movabletype/docs/mtimport) to Tumblr. [Related blog post.](http://jaanus.com/post/1451099140/mt2tumblr-import-blog-posts-fr)

## How to use

1. Download the script.
1. Go to your Movable Type installation and download the export file. In MT 4.34, this is under your blog, Tools, Export.
1. Edit mt2tumblrSettings.py: set your Tumblr username and password, your Tumblr site identifier and URL, and the name of file you got in previous step.
1. Run the script and observe the import.
1. If something goes wrong when running the script, you can run it many times until the import to Tumblr is complete.

## Changes

### Nov 14, 2010

The script didn’t work correctly when posting to an existing Tumblr site that had existing posts with non-text type (photo, video etc). Added an extra check to fix that.

## Motivation

I’ve had some blogs for a while that I’ve wanted to migrate from Movable Type to Tumblr. I contacted Tumblr a while ago and asked if they support importing from Movable Type. They said they don’t. But Tumblr has an [API.](http://www.tumblr.com/docs/en/api) I already knew a thing or two about MT import file format and so I thought, why not put it together and make a little importer. Maybe this is useful to others too.

The Movable Type import format is not perfect, but it has been around for a long time and has been adopted by many other platforms too. So if your blog can export to MT format, you will be able to import this content to Tumblr.

Interestingly, while I was putting the script together, [Six Apart announced that they are merging with another company](http://www.sixapart.com/blog/2010/09/say-hello.html). The future of Movable Type at this point is unclear, though the open source version will probably remain. This importer was in no way motivated by this news, though.

## How it works

The importer first connects to your Tumblr site and downloads the current posts through the API. This is necessary to avoid posting duplicate posts if something was already previously imported. A side effect of this is that all your posts need to have unique titles. If two posts have the same title, importing one of them will be skipped.

After downloading the current posts, the importer loads the posts to be potentially imported from the Movable Type import file. For each post from the file, it checks (by comparing titles) whether it already exists on your Tumblr site. If not, the post is posted to your Tumblr site.

What gets imported for each post:

* Title.
* Original date.
* Body. Tumblr doesn’t have “extended body” concept: both the body and extended body from Movable Type get lumped into one body.
* Approximate base name (slug).

What doesn’t get imported. (Mostly because Tumblr doesn’t support these features, and/or they are not present in the Movable Type import format.)

* Keywords, categories, tags.
* Excerpts.
* Comments, trackbacks.
* Multiple authors. All posts get posted under the name of whoever’s Tumblr credentials are used.
* Post status. All posts are posted right away. This is necessary, among other things, to preserve the original date.

## Random nuggets

Tumblr API has rate limiting. After posting many (100+) posts in a row, you may get a "400 slow down buddy" rate limiting message. If this happens, the importer pauses for 15 seconds, which seems to be enough in most situations. You can also abort and restart the import later.

The posts may not appear in the Tumblr site or backend right away, I observed small delays of a few seconds. For example, if you run the script twice in a row, the posts that you previously posted may not yet show up in the API when the importer fetches previous posts, and so importer thinks they don’t exist (whereas Tumblr just posts them with a delay), and you end up with duplicates. To avoid problems, take a small break between each running of the importer to give Tumblr some breathing time.

Tumblr editing backend doesn’t really scale to sites with large numbers of posts. It’s difficult to find a certain post, and the search does not always work. I entered a term that I knew for sure was in the post title or body, and the post did not show up. But the public archive is reliable and shows all posts. So to edit a post, the most reliable way I found was to just grab its url (mysite.tumblr.com/post/id/slug) and edit the url to be tumblr.com/edit/id.

## License (MIT)

Copyright (c) 2010 Jaanus Kase

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
