from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from notion_oauth.models import NotionAuthorization
from utils.notion import NotionClient, NotionFormaters


@login_required
def home(request):
    # Get the authroization for the user, if it exists
    authorization = NotionAuthorization.objects.filter(
        user=request.user).first()
    if authorization is None:
        # If there's no NotionAuthorization, show the page where a user can add the authorization
        return render(request, 'notion_demo/home.html')
    else:
        client = NotionClient(authorization.access_token)
        formatter = NotionFormaters()
        search_response = client.search()
        if search_response.ok:
            notion_objects = formatter.simplify_search_response(search_response)
            return render(request, 'notion_demo/list.html', {'notion_objects': notion_objects})
        else:
            return render(request, 'notion_demo/list.html',
                          {'notion_objects': [],
                           'error_message': f"There was an error retrieving search results, status {search_response.status_code}"
                           })