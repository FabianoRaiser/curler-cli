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

HEADINGS_HTML = """\
<!DOCTYPE html>
<html>
<head><title>Docs</title></head>
<body>
  <h1>Getting Started</h1>
  <h2>Installation</h2>
  <h3>Requirements</h3>
  <p>Need Python 3.10+.</p>
</body>
</html>
"""

LISTS_HTML = """\
<!DOCTYPE html>
<html>
<head><title>Lists</title></head>
<body>
  <ul>
    <li>Gmail</li>
    <li>Imagens</li>
  </ul>
  <ol>
    <li>Passo 1</li>
    <li>Passo 2</li>
  </ol>
</body>
</html>
"""

NESTED_LIST_HTML = """\
<!DOCTYPE html>
<html>
<head><title>Nested</title></head>
<body>
  <ul>
    <li>One</li>
    <li>Two
      <ul>
        <li>Two A</li>
      </ul>
    </li>
  </ul>
</body>
</html>
"""

LIST_WITH_LINK_HTML = """\
<!DOCTYPE html>
<html>
<head><title>Nav</title></head>
<body>
  <ul>
    <li><a href="/docs">Docs</a></li>
  </ul>
</body>
</html>
"""

INLINE_MARKUP_HTML = """\
<!DOCTYPE html>
<html>
<head><title>Markup</title></head>
<body>
  <p>Use <strong>curl</strong> and <code>python</code>.</p>
  <blockquote>A note.</blockquote>
</body>
</html>
"""
