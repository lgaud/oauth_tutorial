import secrets

from django.shortcuts import redirect, reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

import requests

from oauthlib.oauth2 import WebApplicationClient

from .models import NotionAuthorization

server_url = "http://localhost:8000" # The URL of this server
redirect_uri = f"{server_url}/notion/redirect"

authorization_base_url = 'https://api.notion.com/v1/oauth/authorize'

token_url = 'https://api.notion.com/v1/oauth/token'

STATE_SESSION_KEY = "notion_state"

@login_required
def notion_auth_start(request):
    client = WebApplicationClient(settings.NOTION_CLIENT_ID)

    state = generate_state()
    request.session[STATE_SESSION_KEY] = state

    authorize_request_url = client.prepare_request_uri(
        authorization_base_url, redirect_uri)
    return redirect(authorize_request_url)

@login_required
def notion_redirect(request):
	# oauthlib needs the complete uri with host name    
    url = request.get_full_path()
		
    client = WebApplicationClient(settings.NOTION_CLIENT_ID)
    state = request.session.pop(STATE_SESSION_KEY)
    client.parse_request_uri_response(url, state=state)
    
	# Creates the URL, headers, and request body for the token request
    token_request_params = client.prepare_token_request(token_url, url, redirect_uri)

	# Makes a request for the token, authenticated with the client ID and secret
    auth = requests.auth.HTTPBasicAuth(
        settings.NOTION_CLIENT_ID, settings.NOTION_CLIENT_SECRET)
    response = requests.post(
        token_request_params[0], headers=token_request_params[1], data=token_request_params[2], auth=auth)

    if response.ok:
        token_response = client.parse_request_body_response(response.text)

        authorization = NotionAuthorization.objects.create(
            user = request.user,
            access_token = token_response.get("access_token"),
            bot_id = token_response.get("bot_id"),
            duplicated_template_id = token_response.get("duplicated_template_id", None),
            workspace_name = token_response.get("workspace_name"),
            workspace_icon = token_response.get("workspace_icon"),
            workspace_id = token_response.get("workspace_id"),
            owner = token_response.get("owner")
        )
        authorization.save()

    return HttpResponseRedirect(reverse('notion_demo:home'))

def generate_state():
    return secrets.token_urlsafe(8)