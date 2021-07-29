from rest_framework import serializers
from .models import Meeting


class CaptionSerializer(serializers.Serializer):
    start = serializers.CharField(max_length=255)
    end = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255)
    text = serializers.CharField()


class MeetingSerializer(serializers.Serializer):
    captions = CaptionSerializer(many=True)

    def create(self, validated_data):
        # print(validated_data)
        # for caption in validated_data["captions"]
        meeting = Meeting.objects.create(
            captions=validated_data["captions"]
        )
        # captions = []
        # for i, item in enumerate(validated_data["captions"]):
        #     word_count = len(item["text"].split(sep=" "))

        #     caption = Caption(**item, word_count=word_count, meeting=meeting, index=i)
        #     captions.append(caption)

        # Caption.objects.bulk_create(captions)
        return meeting

# create a serializer for the response