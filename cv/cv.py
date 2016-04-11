#!/usr/bin/env python
import argparse
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
    parser = argparse.ArgumentParser(
        description="""
Transforms JSON formatted CV into standalone html file.
""")
    parser.add_argument('--input', '-i', dest='input', type=str,
                        default="assets/cv.json",
                        help="input JSON file")
    parser.add_argument('--output', '-o', dest='output', type=str,
                        default='result.html',
                        help="output file")
    parser.add_argument('--stylesheets', '-s', dest='stylesheets', type=str,
                        default='assets/main.css',
                        help="file with stylesheets to be used")
    args = parser.parse_args()

    with open(args.input) as fd:
        data = urlize_data(escape_data(json.load(fd)))
    result = """
<!DOCTYPE HTML>
<html>
  <head>
    <title>{title}</title>
    <meta charset="utf-8">
    <style>
    {styles}
    </style>
  </head>
  <body>
  {body}
  </body>
</html>
"""
    with open(args.stylesheets) as fd:
        styles = fd.read()
    with open(args.output, 'w') as fd:
        fd.write(result.format(
            title="CV",
            body=data_to_html(data),
            styles=styles)
        )
    print("Finished!")
