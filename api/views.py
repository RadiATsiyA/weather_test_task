from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from api.serializers import SearchHistorySerializer
from weather.models import SearchHistory


class SearchHistoryAPIView(APIView):

    def get(self, request):
        session_key = request.session.session_key
        if not session_key:
            return Response({"detail": "Session not found"}, status=400)

        search_history = SearchHistory.objects.filter(session_key=session_key)
        serializer = SearchHistorySerializer(search_history, many=True)
        return Response(serializer.data)
