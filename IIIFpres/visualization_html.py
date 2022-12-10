# -*- coding: UTF-8 -*-.
import tempfile
import webbrowser
import time


def show_error_in_browser(myjson, getHTML=False):
    """Get display a dict in the browser highlighting Recommended and Required
    fields.

    Args:
        myjson (dict): A dictionary representing the JSON object.
        getHTML (bool, optional): if True returns the HTML as string.
             Defaults to False.
    """
    html_page = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Visualization errors of the manifest</title>
    </head>
    <body>
    <script>
        function output(inp) {
        document.body.appendChild(document.createElement('pre')).innerHTML = inp;
    }

    function showerror(json) {
    json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    json = json.replace(/Recommended/g, function (match) {
        return '⚠️<span style="background-color: orange">' + match + '</span>';
    });
    return json.replace(/Required/g, function (match) {
        return '❌<span style="background-color: #FF3C3C">' + match + '</span>';
    });
    }


    var obj = %s;
    var str = JSON.stringify(obj, undefined, 4);

    output(showerror(str));
    </script>
    </body>
    </html>
    """ % myjson
    if getHTML:
        return html_page
    else:
        with tempfile.NamedTemporaryFile('r+', suffix='.html') as f:
            f.write(html_page)
            webbrowser.open('file://' + f.name)
            f.seek(0)
            time.sleep(1)