from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.permissions import IsAuthenticated
from apps.accounts.permissions import IsAllowedAction

MOCK_ARTICLES = [
    {"id": 1, "title": "Как настроить Django", "author": "admin"},
    {"id": 2, "title": "Docker для начинающих", "author": "user"},
]

class ArticleListView(APIView):
    permission_classes = [IsAuthenticated, IsAllowedAction]
    resource = "article"
    action = "read"  # Исправлено: "list" -> "read"

    @extend_schema(responses={200: {"type": "array", "items": {"type": "object"}}})
    def get(self, request):
        return Response(MOCK_ARTICLES, status=200)

class ArticleDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAllowedAction]
    resource = "article"
    action = "read"

    @extend_schema(
        parameters=[OpenApiParameter(name='id', type=int, location=OpenApiParameter.PATH)],
        responses={200: {"type": "object"}}
    )
    def get(self, request, pk):
        article = next((a for a in MOCK_ARTICLES if a["id"] == int(pk)), None)
        if not article:
            return Response({"detail": "Not found"}, status=404)
        return Response(article, status=200)

class ArticleCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAllowedAction]
    resource = "article"
    action = "create"

    @extend_schema(
        request={"type": "object", "properties": {"title": {"type": "string"}}},
        responses={201: {"type": "object"}}
    )
    def post(self, request):
        new_article = {"id": len(MOCK_ARTICLES) + 1, "title": request.data.get("title", "Untitled"), "author": request.user.email}
        return Response(new_article, status=201)

class ReportListView(APIView):
    permission_classes = [IsAuthenticated, IsAllowedAction]
    resource = "report"
    action = "read"

    @extend_schema(responses={200: {"type": "array", "items": {"type": "object"}}})
    def get(self, request):
        return Response([{"id": 1, "name": "Monthly Stats", "restricted": True}], status=200)