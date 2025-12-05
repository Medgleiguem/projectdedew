import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import subprocess
import json
import re
import os

def analyze(url):
    try:
        response = requests.get(url, timeout=10)
        html = response.text
        html_size = len(response.content) / 1024  # KB
    except Exception as e:
        return {"error": f"Failed to fetch URL: {e}"}

    soup = BeautifulSoup(html, 'html.parser')

    # -------------------------------
    # COUNT RESOURCES
    # -------------------------------
    resources = soup.find_all(['img', 'script', 'link'])
    requests_count = len(resources)

    # -------------------------------
    # TOTAL IMAGE SIZE
    # -------------------------------
    total_image_size = 0
    for img in soup.find_all("img"):
        src = img.get("src") or img.get("data-src")
        if src:
            img_url = urljoin(url, src)
            try:
                img_data = requests.get(img_url, timeout=5)
                total_image_size += len(img_data.content) / 1024
            except:
                continue

    # -------------------------------
    # DEAD CSS / JS DETECTION
    # -------------------------------
    used_classes = set()
    for cls_list in re.findall(r'class="([^"]+)"', html):
        used_classes.update(cls_list.split())

    used_ids = set(re.findall(r'id="([^"]+)"', html))

    dead_css = []
    dead_js = []

    for link in soup.find_all("link", rel="stylesheet"):
        href = link.get("href")
        if not href:
            continue
        css_url = urljoin(url, href)
        try:
            css = requests.get(css_url, timeout=5).text
            selectors = re.findall(r'([.#][\w\-]+)', css)
            for sel in selectors:
                if sel.startswith(".") and sel[1:] not in used_classes:
                    dead_css.append(sel)
                if sel.startswith("#") and sel[1:] not in used_ids:
                    dead_css.append(sel)
        except:
            continue

    for script in soup.find_all("script", src=True):
        src = script.get("src")
        if src:
            js_url = urljoin(url, src)
            try:
                js = requests.get(js_url, timeout=5).text
                if "function" in js and js.count("(") < 2:
                    dead_js.append(js_url)
            except:
                continue

    # -------------------------------
    # ECOINDEX SCORE
    # -------------------------------
    ecoindex = 100 - (
        (html_size / 1000) * 30 +
        (requests_count / 100) * 30 +
        (total_image_size / 1000) * 40
    )
    ecoindex = round(max(0, min(100, ecoindex)), 2)

    # -------------------------------
    # LIGHTHOUSE PERFORMANCE (optional)
    # -------------------------------
    try:
        result = subprocess.run(
            ["lighthouse", url, "--output=json", "--quiet", '--chrome-flags="--headless"'],
            capture_output=True,
            text=True,
            check=True
        )
        lighthouse = json.loads(result.stdout)
        performance = lighthouse.get("categories", {}).get("performance", {}).get("score", None)
        if performance is not None:
            performance *= 100
    except:
        performance = "Lighthouse not installed"

    return {
        "url": url,
        "page_size_kb": round(html_size, 2),
        "requests": requests_count,
        "images_size_kb": round(total_image_size, 2),
        "dead_css": dead_css[:20],  # limit for readability
        "dead_js": dead_js[:20],
        "ecoindex_score": ecoindex,
        "lighthouse_performance": performance
    }

# -------------------------------
# MAIN: save report to reports/report.json
# -------------------------------
if __name__ == "__main__":
    site = input("Entrer l'URL du site : ").strip()
    os.makedirs("reports", exist_ok=True)

    # Optional: generate safe filename based on URL
    safe_name = site.replace("https://", "").replace("http://", "").replace("/", "_")
    report_file = os.path.join("reports", f"{safe_name}.json")

    report = analyze(site)
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)

    print(f"Report saved to: {report_file}")
