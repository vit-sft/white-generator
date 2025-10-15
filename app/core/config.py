CSS_CONTENT = """
body { font-family: Arial, sans-serif; padding: 2em; max-width: 900px; margin: auto; background: #f9f9f9; }
h1 { margin-bottom: 0.5em; }
.meta { color: #555; margin-bottom: 1em; }
.screenshots { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 2em; }
.screenshots img { max-width: 220px; border-radius: 8px; box-shadow: 0 2px 8px #0002; }
.icon { max-width: 120px; border-radius: 16px; box-shadow: 0 2px 8px #0002; margin-bottom: 1em; }
footer { margin-top: 2em; color: #888; font-size: 0.9em; }
"""

JS_CONTENT = """
// JS placeholder
console.log('Site loaded');
"""

def render_html(data, screenshots_html):
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{data.get('title', '')}</title>
    <link rel="stylesheet" href="static/css/style.css">
</head>
<body>
    <img src="static/img/icon.webp" alt="App Icon" class="icon">
    <h1>{data.get('title', '')}</h1>
    <div class="screenshots">
        {screenshots_html}
    </div>
    <p>{data.get('description', '').replace('\n', '<br>')}</p>
    <footer><small>Data sourced from Google Play</small></footer>
    <script src="static/js/main.js"></script>
</body>
</html>
"""