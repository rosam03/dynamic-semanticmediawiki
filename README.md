# dynamic-semanticmediawiki

Use this library to authenticate and make meaningful queries to a semantic mediawiki instance.

## requirements
- Python 2.7
- Libraries: requests, json `pip install requests json`
- Internet connection

## usage
- the url passed to the session must contain hostname only with prefix `http:// or https://`, not path nor `/api.php` extensions

```
def main():
    session = Session('www.mywiki.com', 'janedoe1', 'password123')
    if(session): # success

        response = session.get_pages('Category:Cities') # tuple of info returned
        if(response):
            count = response['query']['meta']['count']
            results = response['query']['results']
            print 'There are %d cities under the Cities category: /n %s' % (count, results)
        else:
            print('Failed to get pages - make sure you are authenticated')

        response = session.get_pages('Category:Cities|Is in North America::True') # tuple of info returned
        if(response):
            results = response['query']['results']
            print 'Here are the cities in North America: /n %s' % (results)

        if(session.get_edit_token()):
            edit_page('Vancouver','A city in beautiful British Columbia, Canada')

main()

```
