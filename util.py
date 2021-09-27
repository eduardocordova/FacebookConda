import re

# Parses a text to return the string containing the page id as first element.
def page_id_parser(page_source):
    result = re.search(r"(?<=pageID\":\")(.*)(?=\"\,\"tabName)", page_source)
    page_id = result.group(1).split("\"")[0]
    # print(f'page id is {page_id}')
    return page_id