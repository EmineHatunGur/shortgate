from django.db import IntegrityError, transaction
from django.db.models import F
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Link
from .serializers import ShortenSerializer
from .utils import generate_code

MAX_CODE_ATTEMPTS = 5


@api_view(["POST"])
def shorten(request):
    serializer = ShortenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    url = serializer.validated_data["url"]

    for _ in range(MAX_CODE_ATTEMPTS):
        try:
            with transaction.atomic():
                link = Link.objects.create(original_url=url, code=generate_code())
        except IntegrityError:
            continue  # kod çakıştı, yenisini dene
        return Response(
            {"code": link.code, "short_url": request.build_absolute_uri(f"/{link.code}")},
            status=status.HTTP_201_CREATED,
        )
    return Response(
        {"detail": "Could not generate a unique code."},
        status=status.HTTP_503_SERVICE_UNAVAILABLE,
    )


def redirect_view(request, code: str):
    link = get_object_or_404(Link, code=code)
    Link.objects.filter(pk=link.pk).update(click_count=F("click_count") + 1)
    return HttpResponseRedirect(link.original_url)


def health(request):
    return JsonResponse({"status": "ok"})
