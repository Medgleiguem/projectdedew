import minify_html
import csscompressor
import rjsmin

def minify_html_text(html: str) -> str:
    try:
        return minify_html.minify(
            html.encode("utf-8"),
            minify_js=False,
            minify_css=False
        ).decode("utf-8")
    except Exception:
        return " ".join(html.split())

def minify_css_text(css: str) -> str:
    try:
        return csscompressor.compress(css)
    except Exception:
        return " ".join(css.split())

def minify_js_text(js: str) -> str:
    try:
        return rjsmin.jsmin(js)
    except Exception:
        return " ".join(js.split())
