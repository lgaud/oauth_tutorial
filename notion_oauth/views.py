from django.shortcuts import redirect
from django.conf import settings
from django.http import HttpResponse
import requests

from oauthlib.oauth2 import WebApplicationClient

server_url = "http://localhost:8000" # The URL of this server
redirect_uri = f"{server_url}/notion/redirect"

authorization_base_url = 'https://api.notion.com/v1/oauth/authorize'

token_url = 'https://api.notion.com/v1/oauth/token'

def notion_auth_start(request):
    client = WebApplicationClient(settings.NOTION_CLIENT_ID)
    authorize_request_url = client.prepare_request_uri(
        authorization_base_url, redirect_uri)
    return redirect(authorize_request_url)


def notion_redirect(request):
	# oauthlib needs the complete uri with host name    
    url = request.get_full_path()
		
    client = WebApplicationClient(settings.NOTION_CLIENT_ID)
    client.parse_request_uri_response(url) # Extracts the code from the url
    
	# Creates the URL, headers, and request body for the token request
    token_request_params = client.prepare_token_request(token_url, url, redirect_uri)

	# Makes a request for the token, authenticated with the client ID and secret
    auth = requests.auth.HTTPBasicAuth(
        settings.NOTION_CLIENT_ID, settings.NOTION_CLIENT_SECRET)
    response = requests.post(
        token_request_params[0], headers=token_request_params[1], data=token_request_params[2], auth=auth)

    return HttpResponse(response)