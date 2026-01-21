import uuid
from datetime import datetime, timedelta, timezone
from urllib.parse import urljoin, urlparse
from pathlib import Path
from io import BytesIO

import jwt
import PIL
from flask import current_app, flash, redirect, request, url_for
from jwt.exceptions import InvalidTokenError
from PIL import Image


def generate_token(user, operation, expiration=3600, **kwargs):
    payload = {
        'id': user.id,
        'operation': operation.value,
        'exp': datetime.now(timezone.utc) + timedelta(seconds=expiration)
    }
    payload.update(**kwargs)
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')


def parse_token(user, token, operation):
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
    except InvalidTokenError:
        return {}

    if operation.value != payload.get('operation') or user.id != payload.get('id'):
        return {}
    return payload


def rename_image(old_filename):
    ext = Path(old_filename).suffix
    new_filename = uuid.uuid4().hex + ext
    return new_filename


def resize_image(image, filename, base_width):
    ext = Path(filename).suffix
    img = Image.open(image)
    if img.size[0] <= base_width:
        return filename
    w_percent = base_width / float(img.size[0])
    h_size = int(float(img.size[1]) * float(w_percent))
    img = img.resize((base_width, h_size), PIL.Image.LANCZOS)

    filename += current_app.config['MOMENTS_PHOTO_SUFFIXES'][base_width] + ext
    img.save(current_app.config['MOMENTS_UPLOAD_PATH'] / filename, optimize=True, quality=85)
    return filename


def validate_image(filename):
    ext = Path(filename).suffix.lower()
    allowed_extensions = current_app.config['DROPZONE_ALLOWED_FILE_TYPE'].split(',')
    return '.' in filename and ext in allowed_extensions


def get_blip_model_and_processor():
    """Load ViT+GPT2 image captioning model."""
    from transformers import ViTImageProcessor, AutoTokenizer, VisionEncoderDecoderModel
    import torch
    
    model_name = "nlpconnect/vit-gpt2-image-captioning"
    processor = ViTImageProcessor.from_pretrained(model_name)
    model = VisionEncoderDecoderModel.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model.to("cpu").eval()
    return processor, model, tokenizer


def generate_image_metadata(image_path):
    """Extract description and keywords from image. Returns (description, keywords_str)."""
    try:
        import torch
        from transformers import CLIPProcessor, CLIPModel
        
        processor, model, tokenizer = get_blip_model_and_processor()
        img = Image.open(image_path).convert('RGB')
        img.thumbnail((384, 384))
        with torch.no_grad():
            pixel_values = processor(images=img, return_tensors="pt").pixel_values
            output_ids = model.generate(pixel_values, max_length=16)
        description = tokenizer.decode(output_ids[0], skip_special_tokens=True).strip()
        
        clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        candidates = ["person", "dog", "cat", "car", "building", "tree", "water", "sky", "food", "nature", 
                     "outdoor", "indoor", "beach", "mountain", "sunset", "animal", "people", "landscape"]
        inputs = clip_processor(text=candidates, images=img, return_tensors="pt", padding=True)
        
        with torch.no_grad():
            outputs = clip_model(**inputs)
            scores = outputs.logits_per_image[0].softmax(dim=-1)
            top_indices = scores.topk(5).indices
        keywords = ', '.join([candidates[i] for i in top_indices])
        
        return description, keywords
    except Exception as e:
        current_app.logger.error(f"Image metadata extraction failed: {e}")
        return "", ""


def generate_description_from_image(image_path):
    """Generate image description using ViT+GPT2 ML model."""
    description, _ = generate_image_metadata(image_path)
    return description


def extract_image_keywords(image_path, num_keywords=5):
    """Extract object keywords from image using CLIP model."""
    _, keywords = generate_image_metadata(image_path)
    return keywords.split(', ') if keywords else []


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_back(default='main.index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


def generate_alt_text(filename):
    """Generate alt text from filename. Returns 'Photo' for unrecognizable names."""
    name = Path(filename).stem.replace('_', ' ').replace('-', ' ')
    words = [w for w in name.split() if not (len(w) >= 8 and all(c in '0123456789abcdef' for c in w))]
    return ' '.join(words).title() if words else 'Photo'


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'Error in the {getattr(form, field).label.text} field - {error}')
