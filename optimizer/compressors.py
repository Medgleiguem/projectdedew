from PIL import Image
from io import BytesIO
import os

def save_image_variants(img_bytes, out_basename, quality=75):
    """Save original, webp and avif variants. Returns dict with paths and sizes."""
    os.makedirs(os.path.dirname(out_basename), exist_ok=True)
    try:
        img = Image.open(BytesIO(img_bytes)).convert('RGB')
    except Exception as e:
        return {'error': str(e)}

    results = {}

    # Original
    orig_path = out_basename + os.path.splitext(out_basename)[1]
    with open(orig_path, 'wb') as f:
        f.write(img_bytes)
    results['original'] = orig_path

    # WebP
    webp_path = out_basename + '.webp'
    try:
        img.save(webp_path, 'WEBP', quality=quality, method=6)
        results['webp'] = webp_path
    except Exception as e:
        results['webp_error'] = str(e)

    # AVIF
    avif_path = out_basename + '.avif'
    try:
        img.save(avif_path, 'AVIF', quality=quality)
        results['avif'] = avif_path
    except Exception as e:
        results['avif_error'] = str(e)

    return results
