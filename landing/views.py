from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404, StreamingHttpResponse
import os
import mimetypes
from django.utils.http import http_date
from django.utils.timezone import now

from .models import (
    AboutBlock, Trailer, ProductInfo, ScreenshotAlbum, Version,
    FPVMode, PurchaseOption, Footer, AppScreenshot, PrivacyPolicy, PageSettings
)


def index(request):
    context = {
        'about_block': AboutBlock.load(),
        'trailer': Trailer.load(),
        'product_info': ProductInfo.load(),
        'screenshot_albums': ScreenshotAlbum.objects.prefetch_related('screenshots').all(),
        'app_screenshots': AppScreenshot.objects.all().order_by('order'),
        'versions': Version.objects.all(),
        'fpv_mode': FPVMode.load(),
        'purchase_options': PurchaseOption.objects.all(),
        'footer': Footer.load(),
        'page_settings': PageSettings.load(),
    }
    return render(request, 'landing/index.html', context)

def privacy_policy(request):
    privacy_policy = PrivacyPolicy.load()
    return render(request, 'landing/privacy_policy.html', {'privacy_policy': privacy_policy})


def stream_video(request, filename):
    # Раздаём только из MEDIA_ROOT/videos/
    video_dir = os.path.join(settings.MEDIA_ROOT, 'videos')
    file_path = os.path.join(video_dir, filename)
    if not os.path.isfile(file_path):
        raise Http404()

    file_size = os.path.getsize(file_path)
    range_header = request.headers.get('Range')
    content_type = 'video/mp4'

    def file_iterator(start, end, chunk_size=8192):
        with open(file_path, 'rb') as f:
            f.seek(start)
            remaining = end - start + 1
            while remaining > 0:
                chunk = f.read(min(chunk_size, remaining))
                if not chunk:
                    break
                remaining -= len(chunk)
                yield chunk

    if range_header:
        try:
            _, range_val = range_header.split('=')
            start_str, end_str = (range_val.split('-') + [''])[:2]
            start = int(start_str) if start_str else 0
            end = int(end_str) if end_str else file_size - 1
            end = min(end, file_size - 1)
        except Exception:
            start, end = 0, file_size - 1
        length = end - start + 1
        response = StreamingHttpResponse(file_iterator(start, end), status=206, content_type=content_type)
        response['Content-Length'] = str(length)
        response['Content-Range'] = f'bytes {start}-{end}/{file_size}'
        response['Accept-Ranges'] = 'bytes'
        response['Last-Modified'] = http_date(os.path.getmtime(file_path))
        response['Cache-Control'] = 'public, max-age=86400'
        response['Date'] = http_date(now().timestamp())
        return response

    response = StreamingHttpResponse(file_iterator(0, file_size - 1), content_type=content_type)
    response['Content-Length'] = str(file_size)
    response['Accept-Ranges'] = 'bytes'
    response['Last-Modified'] = http_date(os.path.getmtime(file_path))
    response['Cache-Control'] = 'public, max-age=86400'
    response['Date'] = http_date(now().timestamp())
    return response
