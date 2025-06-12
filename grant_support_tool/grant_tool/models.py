from django.db import models

class GrantDraft(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    analysis_results = models.JSONField(blank=True, null=True)  # NLP results

    def __str__(self):
        return self.title
