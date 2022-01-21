from rest_framework import views, response
from .models import Audio, Section
from .serializers import AudioLatinSerializer, AudioCyrillicSerializer, SectionSerializer
from django.http import Http404

class SectionAPIView(views.APIView):
    def get(self, request):
        query = Section.objects.all()
        serializer = SectionSerializer(query, many=True)
        return response.Response(serializer.data)


class AudioLatinAPIView(views.APIView):
    def get(self, request, pk, *args, **kwargs):
        queryset = self.get_object(pk)
        query = Audio.objects.filter(section_id=queryset.pk)
        serializer = AudioLatinSerializer(query, many=True)
        return response.Response(serializer.data)


    def get_object(self, pk):
        try:
            return Section.objects.get(pk=pk)
        except Section.DoesNotExist:
            raise Http404


class AudioCyrillicAPIView(views.APIView):
    def get(self, request, pk, *args, **kwargs):
        queryset = self.get_object(pk)
        query = Audio.objects.filter(section_id=queryset.pk)
        serializer = AudioCyrillicSerializer(query, many=True)
        return response.Response(serializer.data)


    def get_object(self, pk):
        try:
            return Section.objects.get(pk=pk)
        except Section.DoesNotExist:
            raise Http404


