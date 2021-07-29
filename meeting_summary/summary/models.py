from django.db import models
from model_utils.models import TimeStampedModel
import uuid


class Meeting(TimeStampedModel):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    captions = models.JSONField(null=True)

    def __str__(self):
        return f"{self.id}"


# class Caption(models.Model):
#     id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
#     start = models.CharField("Start time", max_length=255)
#     end = models.CharField("End time", max_length=255)
#     name = models.CharField("User Name", max_length=255)
#     text = models.TextField("Text")
#     word_count = models.PositiveSmallIntegerField("Word Count")
#     index = models.PositiveSmallIntegerField("Index", null=True) 
#     meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)

#     def meeting_id(self):
#         return self.meeting.id

#     def __str__(self):
#         return f"{self.index} - {self.text}"


class Summary(TimeStampedModel):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, null=True)
    splits = models.JSONField()
    
    def __str__(self):
        return f"(Summary) id: {self.id} - Meeting id: {self.meeting.id}"


# class SummarySplit(models.Model):
#     models.JSONField()
#     id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
#     text = models.TextField("Text")
#     source_text = models.TextField("Source Text")
#     source_start = models.CharField("Source start time", max_length=255)
#     word_count = models.PositiveSmallIntegerField("Word Count")
#     summary = models.ForeignKey(Summary, on_delete=models.CASCADE)
    
#     def __str__(self):
#         return f"Text: {self.text} - Timestamp: {self.source_start}"

# [
#     {...},
#     {...},
#     {...}
# ]