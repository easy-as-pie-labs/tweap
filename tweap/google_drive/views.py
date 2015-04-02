from django.shortcuts import render


def GetCodeCredentials(self):
    """Create OAuth 2.0 credentials by extracting a code and performing OAuth2.0.

    The authorization code is extracted form the URI parameters. If it is absent,
    None is returned immediately. Otherwise, if it is present, it is used to
    perform step 2 of the OAuth 2.0 web server flow.

    Once a token is received, the user information is fetched from the userinfo
    service and stored in the session. The token is saved in the datastore against
    the user ID received from the userinfo service.

    Args:
      request: HTTP request used for extracting an authorization code and the
               session information.
    Returns:
      OAuth2.0 credentials suitable for authorizing clients or None if
      Authorization could not take place.
    """
    # Other frameworks use different API to get a query parameter.
    code = self.request.get('code')
    if not code:
        # returns None to indicate that no code was passed from Google Drive.
        return None

    # Auth flow is a controller that is loaded with the client information,
    # including client_id, client_secret, redirect_uri etc
    oauth_flow = self.CreateOAuthFlow()

    # Perform the exchange of the code. If there is a failure with exchanging
    # the code, return None.
    try:
        creds = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        return None

    # Create an API service that can use the userinfo API. Authorize it with our
    # credentials that we gained from the code exchange.
    users_service = CreateService('oauth2', 'v2', creds)

    # Make a call against the userinfo service to retrieve the user's information.
    # In this case we are interested in the user's "id" field.
    userid = users_service.userinfo().get().execute().get('id')

    # Store the user id in the user's cookie-based session.
    session = sessions.LilCookies(self, SESSION_SECRET)
    session.set_secure_cookie(name='userid', value=userid)

    # Store the credentials in the data store using the userid as the key.
    StorageByKeyName(Credentials, userid, 'credentials').put(creds)
    return creds


def GetSessionCredentials(self):
    """Get OAuth 2.0 credentials for an HTTP session.

    If the user has a user id stored in their cookie session, extract that value
    and use it to load that user's credentials from the data store.

    Args:
      request: HTTP request to use session from.
    Returns:
      OAuth2.0 credentials suitable for authorizing clients.
    """
    # Try to load  the user id from the session
    session = sessions.LilCookies(self, SESSION_SECRET)
    userid = session.get_secure_cookie(name='userid')
    if not userid:
        # return None to indicate that no credentials could be loaded from the
        # session.
        return None

    # Load the credentials from the data store, using the userid as a key.
    creds = StorageByKeyName(Credentials, userid, 'credentials').get()

    # if the credentials are invalid, return None to indicate that the credentials
    # cannot be used.
    if creds and creds.invalid:
        return None

    return creds


ALL_SCOPES = (
    'https://www.googleapis.com/auth/drive.file '
    'email '
    'profile'
)


def RedirectAuth(self):
    """Redirect a handler to an authorization page.

    Used when a handler fails to fetch credentials suitable for making Drive API
    requests. The request is redirected to an OAuth 2.0 authorization approval
    page and on approval, are returned to application.

    Args:
      handler: webapp.RequestHandler to redirect.
    """
    flow = self.CreateOAuthFlow()

    # Manually add the required scopes. Since this redirect does not originate
    # from the Google Drive UI, which authomatically sets the scopes that are
    # listed in the Developers Console.
    flow.scope = ALL_SCOPES

    # Create the redirect URI by performing step 1 of the OAuth 2.0 web server
    # flow.
    uri = flow.step1_get_authorize_url(flow.redirect_uri)

    # Perform the redirect.
    self.redirect(uri)


def CreateService(service, version, creds):
    """Create a Google API service.

    Load an API service from the Discovery API and authorize it with the
    provided credentials.

    Args:
      service: Request service (e.g 'drive', 'oauth2').
      version: Version of the service (e.g 'v2').
      creds: Credentials used to authorize service.
    Returns:
      Authorized Google API service.
    """
    # Instantiate an Http instance
    http = httplib2.Http()

    # Authorize the Http instance with the passed credentials
    creds.authorize(http)

    # Build a named service from the Discovery API
    return build(service, version, http=http)


def CreateOAuthFlow(self):
    """Create OAuth2.0 flow controller

    This controller can be used to perform all parts of the OAuth 2.0 dance
    including exchanging an Authorization code.

    Args:
      request: HTTP request to create OAuth2.0 flow for
    Returns:
      OAuth2.0 Flow instance suitable for performing OAuth2.0.
    """
    flow = flow_from_clientsecrets('client-debug.json', scope='')
    # Dynamically set the redirect_uri based on the request URL. This is extremely
    # convenient for debugging to an alternative host without manually setting the
    # redirect URI.
    flow.redirect_uri = self.request.url.split('?', 1)[0].rsplit('/', 1)[0]
    return flow


class DriveState(object):
    """Store state provided by Drive."""

    def __init__(self, state):
        """Create a new instance of drive state.

        Parse and load the JSON state parameter.

        Args:
          state: State query parameter as a string.
        """
        state_data = json.loads(state)
        self.action = state_data['action']
        self.ids = map(str, state_data.get('ids', []))

    @classmethod
    def FromRequest(cls, request):
        """Create a Drive State instance from an HTTP request.

        Args:
          cls: Type this class method is called against.
          request: HTTP request.
        """
        return DriveState(request.get('state'))


def get(self):
    """Called when HTTP GET requests are received by the web application.

    Use the query parameter file_id to fetch the required file's metadata then
    content and return it as a JSON object.

    Since DrEdit deals with text files, it is safe to dump the content directly
    into JSON, but this is not the case with binary files, where something like
    Base64 encoding is more appropriate.
    """
    # Create a Drive service
    service = self.CreateDrive()
    if service is None:
        return
    try:
        # Requests are expected to pass the file_id query parameter.
        file_id = self.request.get('file_id')
        if file_id:
            # Fetch the file metadata by making the service.files().get method of
            # the Drive API.
            f = service.files().get(fileId=file_id).execute()
            downloadUrl = f.get('downloadUrl')
            # If a download URL is provided in the file metadata, use it to make an
            # authorized request to fetch the file ontent. Set this content in the
            # data to return as the 'content' field. If there is no downloadUrl,
            # just set empty content.
            if downloadUrl:
                resp, f['content'] = service._http.request(downloadUrl)
            else:
                f['content'] = ''
        else:
            f = None
        # Generate a JSON response with the file data and return to the client.
        self.RespondJSON(f)
    except AccessTokenRefreshError:
        # Catch AccessTokenRefreshError which occurs when the API client library
        # fails to refresh a token. This occurs, for example, when a refresh token
        # is revoked. When this happens the user is redirected to the
        # Authorization URL.
        self.RedirectAuth()

