from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import authentication, permissions

from .serializers import MeetingSerializer, CaptionSerializer
from .utils import super_algorithm, produce_summary
from .models import Summary

class CreateMeetingView(APIView):

    permission_classes = [permissions.AllowAny]
    
    def post(self, request, format=None):
        serializer = MeetingSerializer(data=request.data)
        if serializer.is_valid():
            meeting = serializer.save()
            print("Saving finished")
            caption_list = super_algorithm(meeting.id)
            # print("CAPTION_LIST:", caption_list)
            response = produce_summary(caption_list)
            summary = Summary.objects.create(
                meeting=meeting,
                splits=response
            )
            return Response(response, status=status.HTTP_200_OK)
            # return Response({}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

create_meeting_view = CreateMeetingView.as_view()
