from django.db import models

class ResearchSession(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("RUNNING", "Running"),
        ("COMPLETED", "Completed"),
        ("FAILED", "Failed"),
    ]

    question = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    trace_id = models.CharField(max_length=255, null=True, blank=True)
    # Parent session for continuation
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children'
    )

    def __str__(self):
        return f"ResearchSession {self.id}"


class ResearchStep(models.Model):
    session = models.ForeignKey(
        ResearchSession,
        on_delete=models.CASCADE,
        related_name="steps"
    )
    step_name = models.CharField(max_length=100)
    output = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.step_name} - Session {self.session.id}"


class CostUsage(models.Model):
    session = models.OneToOneField(
        ResearchSession,
        on_delete=models.CASCADE,
        related_name="cost"
    )
    total_tokens = models.IntegerField(default=0)
    total_cost_usd = models.FloatField(default=0.0)


class UploadedDocument(models.Model):
    session = models.ForeignKey(
        ResearchSession,
        on_delete=models.CASCADE,
        related_name="documents",
    )
    file = models.FileField(upload_to="documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document {self.id} for Session {self.session.id}"
