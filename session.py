import requests
import json

class session(object):

  # constructor
  def __init__(self, host, username, password):
    self.url = host + '/api.php?'
    self.auth_state = False # default state unauthenticated
    self.token = ""
    self.edit_token = ""
    self.cookies = ""

    self.auth(username, password)


  """
  Purpose: Authenticate a client into a semantic mediawiki
        instance by obtaining a log in token and cookie
        to enable future queries in the same session. The
        authentication process has two steps, 1) Makes the
        login request to obtain a token, and 2)
        authenticate with the token.
  Params
    username : username of an account in the semantic mediawiki
        instance
    password : corresponding password
  """
  def auth(self, username, password):
    payload =  {'action': 'login', 'lgname': username, 'lgpassword': password, 'format': 'json'}
    # initiate authentication
    response, _, _ = self.query(payload) # returns a 3-tuple, discard extra info for auth
    # get auth token and cookie
    if 'token' in response.json()['login']:
      self.token = response.json()['login']['token']
      payload['lgtoken'] = self.token
      self.cookies = response.cookies
      try:
        # attempt log in
        response, _, _ = self.query(payload)
      except:
        print("Login token confirmation failed.")
      if response.json()['login']['result'] == 'Success':
        print("Authentication Success")
        self.auth_state = True
      else:
        print("Authentication Failed")
        self.auth_state = False


  """
  Purpose: Gets a list of pages in the database that match
    the given condition. Returns a 3-tuple containing all
    response details, response results, and results count.
    Returns false if session is invalid.
  Params
    conditions : the condition to query on in the database

  """
  def get_pages(self, payload):
    if self.auth_state is False and payload['action'] != 'login':
      return False
    else:
      payload = {'action': 'askargs', 'conditions': conditions, 'format': 'json'}
      response = requests.post(self.url, data=payload, cookies=self.cookies)
      if result.status_code == 200:
          response = response.json()
          count = response['query']['meta']['count']
          results = response['query']['results']
          return response, count, results
      else:
          return False


  """
  Purpose: Gets an edit token for page editing type requests
  """
  def get_edit_token(self):

    payload = {'action': 'query', 'format': 'json', 'meta':'tokens', 'continue':""}

    try:
        response = requests.post(self.url, data=payload, cookies=self.cookies)
        self.edit_token = response.json()['query']['tokens']['csrftoken']
        return True
    except:
        print ("Failure: could not get edit token")
        return False


    """
    Purpose: Gets the wikitext of a page specified by title
    Note: Limitations of the API only allow to retrieve content
        by providing a page id. The only way to get a page id
        is by making a page edit request. The trade-off with this
        feature is that it will create a new page even if it doesnt
        exist.
    Params
      title : the page title to get content for
    """
  def get_page_content(self, title):

      # get page id
      payload = {'action': 'edit', 'format': 'json', 'utf8': '', 'bot': '', 'appendtext': '', 'title': title, 'token': self.edit_token}

      try:
          response = requests.post(self.url, data=payload, cookies=self.cookies)
          page_id = str(response.json()['edit']['pageid'])
      except:
          print ("Failure: could not get page id")
          return False

      # get wikitext
      payload = {'action': 'query', 'prop': 'revisions', 'rvprop':'content','format': 'json', 'titles': title, 'utf8': ''}

      try:
          response = requests.post(self.url, data=payload, cookies=self.cookies)
          result = response.json()['query']['pages'][page_id]['revisions'][0]['*']
          print ("Success: got " + title + ' content')
          return result
      except:
          print ("Failure: could not get " + title + ' content ')
          return False


  """
  Purpose: Rewrites a pages wikitext. To modify a pages content ,
    first use get_page_content() and modify the content as desired,
    then pass in the modified text to the 'text' parameter.
  Params
    text: the text to write to the page
    title: the title of the page to edit
  """
  def edit_page(self, text, title) :

    payload = {'action': 'edit', 'assert': 'user', 'format': 'json', 'utf8': '', 'bot': '', 'text': text, 'title': title, 'token': edit_token}

    try:
        response = requests.post(self.url, data=payload, cookies=self.cookies)
        print ("Success: edited " + title)
        return True
    except:
        print ("Failure: could not edit " + title)
        return False
