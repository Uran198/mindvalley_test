#!/usr/bin/env python
import json


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


if __name__ == "__main__":
    with open("cv.json") as fd:
        data = json.load(fd)
    result = """
<!DOCTYPE HTML>
<html>
  <head>
    <title>{title}</title>
    <meta charset="utf-8">
  </head>
  <body>
  {body}
  </body>
</html>
"""
    with open("result.html", 'w') as fd:
        fd.write(result.format(title="CV", body=data_to_html(data)))
    print("Finished!")
