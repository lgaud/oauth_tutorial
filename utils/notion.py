import requests
from urllib.parse import urljoin

class NotionClient():
    def __init__(self, notion_key):
        self.notion_key = notion_key
        self.default_headers = {'Authorization': f"Bearer {self.notion_key}",
                                'Content-Type': 'application/json', 'Notion-Version': '2022-06-28'}
        self.session = requests.Session()
        self.session.headers.update(self.default_headers)
        self.NOTION_BASE_URL = "https://api.notion.com/v1/"


    def search(self, query=None, sort=None, filter=None, start_cursor=None, page_size=None):
        request_url = urljoin(self.NOTION_BASE_URL, 'search')

        data = {}
        if query is not None:
            data["query"] = query
        if sort is not None:
            data["sort"] = sort

        if filter is not None:
            data["filter"] = filter

        if start_cursor is not None:
            data["start_cursor"] = start_cursor

        if page_size is not None:
            data["page_size"] = page_size
        response = self.session.post(request_url, json=data)

        return response

class NotionFormaters():
    def get_text(self, text_object):
	    # Concatenates an object with a text array into plain text
        text = ""
        obj_type = text_object.get("type")
        if obj_type in ["rich_text", "title"]:
            for rt in text_object.get(obj_type):
                text += rt.get("plain_text")
            return text

    def simplify_search_response(self, search_response):
        # Process the search response to make it easier to handle
        notion_objects = search_response.json().get("results")
        simplified_results = []
        for item in notion_objects:
            # Create an object with the properties we care about and a default value for title
            simplified_item = {"title": "Untitled", "url": item.get("url"), "id": item.get("id")}
            properties = item.get("properties")
            # Find the title property and set it on the simplified item
            if properties is not None:
                for _, value in properties.items():
                    if value.get("type") == "title":
                        text = self.get_text(value)
                        if text is not None and text != "":
                            simplified_item["title"] = text
                        break
            simplified_results.append(simplified_item)
        return simplified_results