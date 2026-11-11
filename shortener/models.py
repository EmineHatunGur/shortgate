from django.db import models


class Link(models.Model):
    original_url = models.URLField(max_length=2048)
    code = models.CharField(max_length=16, unique=True)
    click_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.code} -> {self.original_url}"
