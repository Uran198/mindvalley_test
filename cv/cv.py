#!/usr/bin/env python
import json
from html import escape

from jinja2.utils import urlize


def data_to_html(data, html_class=None):
    """
    Converts python data got from json files into html string.
    Escapes nothing. To be secure escape your data as needed yourself
    """
    result = ""
    if html_class:
        classes = ' class="{}"'.format(html_class)
    else:
        classes = ''
    if isinstance(data, list):
        result += "<ul{}>".format(classes)
        for value in data:
            result += "<li>{}</li>".format(data_to_html(value))
        result += "</ul>"
    elif isinstance(data, dict):
        result += "<div{}>".format(classes)
        for key, value in data.items():
            result += data_to_html(value, html_class=key)
        result += "</div>"
    else:
        result += "<p{}>{}</p>".format(classes, data)
    return result


def escape_data(data):
    """
    Returns new data with all keys and values escaped using html.escape
    function.
    """
    if isinstance(data, list):
        return [escape_data(value) for value in data]
    if isinstance(data, dict):
        return {escape(key): escape_data(value) for key, value in data.items()}
    return escape(data)


def urlize_data(data):
    """
    Returns new data with all values urlized.
    """
    if isinstance(data, list):
        return [urlize_data(value) for value in data]
    if isinstance(data, dict):
        return {key: urlize_data(value) for key, value in data.items()}
    return urlize(data)


if __name__ == "__main__":
    with open("assets/cv.json") as fd:
        data = urlize_data(escape_data(json.load(fd)))
    result = """
<!DOCTYPE HTML>
<html>
  <head>
    <title>{title}</title>
    <meta charset="utf-8">
    <link rel="stylesheet" href="assets/main.css">
  </head>
  <body>
  {body}
  </body>
</html>
"""
    with open("result.html", 'w') as fd:
        fd.write(result.format(title="CV", body=data_to_html(data)))
    print("Finished!")
