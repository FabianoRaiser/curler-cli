"""HTML fixtures for parser tests."""

BLOG_HTML = """\
<!DOCTYPE html>
<html>
<head><title>My Blog Post</title></head>
<body>
  <h1>Hello World</h1>
  <p>First paragraph.</p>
  <p>Second paragraph.</p>
  <a href="/about">About us</a>
  <a href="https://example.com/contact">Contact</a>
  <script>console.log("ignored");</script>
  <style>.hidden { display: none; }</style>
</body>
</html>
"""

WIKI_HTML = """\
<!DOCTYPE html>
<html>
<head><title>Python (programming language) - Wikipedia</title></head>
<body>
  <h1>Python</h1>
  <p>Python is a programming language.</p>
  <a href="/wiki/Guido_van_Rossum">Guido van Rossum</a>
  <a href="#history">History</a>
  <a href="javascript:void(0)">Click me</a>
  <a href="mailto:info@example.com">Email</a>
</body>
</html>
"""

SPA_HTML = """\
<!DOCTYPE html>
<html>
<head><title>React App</title></head>
<body>
  <div id="root"></div>
  <script src="/static/bundle.js"></script>
</body>
</html>
"""

DUPLICATE_LINKS_HTML = """\
<!DOCTYPE html>
<html>
<head><title>Links</title></head>
<body>
  <a href="/page">Page</a>
  <a href="/page">Page again</a>
</body>
</html>
"""
