import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests

def extract_used_classes_ids(html):
    soup = BeautifulSoup(html, 'html.parser')
    classes, ids = set(), set()
    for tag in soup.find_all(True):
        cl = tag.get('class')
        if cl:
            if isinstance(cl, list):
                classes.update(cl)
            else:
                classes.update(str(cl).split())
        iid = tag.get('id')
        if iid:
            ids.add(iid)
    return classes, ids

def fetch_and_clean_css(url_base, css_url, used_classes, used_ids):
    try:
        r = requests.get(css_url, headers={"User-Agent":"Mozilla/5.0"}, timeout=10)
        r.raise_for_status()
    except Exception:
        return None, []
    
    css_text = r.text
    # Keep only selectors that exist in the HTML
    blocks = re.findall(r'([^{}]+)\{([^{}]+)\}', css_text, flags=re.DOTALL)
    cleaned = []
    removed = []
    for selector_group, rules in blocks:
        selectors = [s.strip() for s in selector_group.split(',')]
        keep = []
        for s in selectors:
            s_clean = s.split(':')[0].strip()
            if s_clean.startswith('.') and s_clean[1:] in used_classes:
                keep.append(s)
            elif s_clean.startswith('#') and s_clean[1:] in used_ids:
                keep.append(s)
            elif not s_clean.startswith(('.', '#')):
                keep.append(s)
            else:
                removed.append(s)
        if keep:
            cleaned.append(','.join(keep) + '{' + rules + '}')
    return '\n'.join(cleaned), list(set(removed))
