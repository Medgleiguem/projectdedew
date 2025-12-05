#!/usr/bin/env python3
import os
import sys
import json
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

from compressors import save_image_variants
from cleaner import extract_used_classes_ids, fetch_and_clean_css
from minifier import minify_html_text, minify_css_text, minify_js_text

# -------------------------
# Helper functions
# -------------------------

def safe_mkdir(path):
    os.makedirs(path, exist_ok=True)

def download_bytes(url):
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        r.raise_for_status()
        return r.content
    except Exception:
        return None

# -------------------------
# Main optimizer function
# -------------------------

def optimize(url, out_dir, quality=72):
    safe_mkdir(out_dir)
    assets_dir = os.path.join(out_dir, 'assets')
    safe_mkdir(assets_dir)

    images_dir = os.path.join(assets_dir, 'images')
    css_dir = os.path.join(assets_dir, 'css')
    js_dir = os.path.join(assets_dir, 'js')
    for d in (images_dir, css_dir, js_dir):
        safe_mkdir(d)

    # Fetch HTML
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    html_before = r.text
    soup = BeautifulSoup(html_before, 'html.parser')

    used_classes, used_ids = extract_used_classes_ids(html_before)

    report = {'url': url, 'images': [], 'css': [], 'js': []}

    # -------------------------
    # Images
    # -------------------------
    for idx, img in enumerate(soup.find_all('img')):
        src = img.get('src') or img.get('data-src')
        if not src:
            continue
        full = urljoin(url, src)
        b = download_bytes(full)
        if not b:
            continue

        parsed = urlparse(full)
        name = os.path.basename(parsed.path) or f'image_{idx}.jpg'
        base = os.path.join(images_dir, os.path.splitext(name)[0])

        res = save_image_variants(b, base, quality=quality)
        res['original_url'] = full
        report['images'].append(res)

        if 'webp' in res:
            img['src'] = os.path.join('assets', 'images', os.path.basename(res['webp']))

    # -------------------------
    # CSS
    # -------------------------
    for link in soup.find_all('link', rel=lambda x: x and 'stylesheet' in x.lower()):
        href = link.get('href')
        if not href:
            continue

        full = urljoin(url, href)
        cleaned, removed = fetch_and_clean_css(url, full, used_classes, used_ids)
        if cleaned is None:
            continue

        minified = minify_css_text(cleaned)
        base_name = os.path.basename(urlparse(full).path) or f"style_{len(report['css'])}.css"
        out_path = os.p_
