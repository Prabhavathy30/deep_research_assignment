from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveAPIView

from django.shortcuts import render, redirect, get_object_or_404

from .models import ResearchSession, UploadedDocument
from .serializers import (
    ResearchSessionSerializer,
    UploadedDocumentSerializer,
)
from .tasks import run_research_task

# ==========================
# API VIEWS (DRF)
# ==========================

class ResearchSessionCreateAPIView(APIView):
    def post(self, request):
        serializer = ResearchSessionSerializer(data=request.data)
        if serializer.is_valid():
            session = serializer.save()
            run_research_task.delay(session.id)
            return Response(
                ResearchSessionSerializer(session).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResearchSessionListAPIView(APIView):
    def get(self, request):
        sessions = ResearchSession.objects.all().order_by("-created_at")
        serializer = ResearchSessionSerializer(sessions, many=True)
        return Response(serializer.data)


class ResearchSessionDetailAPIView(RetrieveAPIView):
    queryset = ResearchSession.objects.all()
    serializer_class = ResearchSessionSerializer
    lookup_field = "id"


class UploadedDocumentCreateAPIView(APIView):
    def post(self, request):
        serializer = UploadedDocumentSerializer(data=request.data)
        if serializer.is_valid():
            document = serializer.save()
            return Response(
                UploadedDocumentSerializer(document).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ==========================
# UI VIEWS (HTML)
# ==========================

def home_view(request):
    if request.method == "POST":
        question = request.POST.get("question")
        if question:
            session = ResearchSession.objects.create(question=question)
            run_research_task.delay(session.id)
            return redirect("session-detail", session_id=session.id)

    sessions = ResearchSession.objects.all().order_by("-created_at")
    return render(request, "research/home.html", {"sessions": sessions})


def session_detail_view(request, session_id):
    session = get_object_or_404(ResearchSession, id=session_id)
    steps = session.steps.all()
    documents = session.documents.all()
    cost = getattr(session, "cost", None)
    return render(
        request,
        "research/session_detail.html",
        {"session": session, "steps": steps, "documents": documents, "cost": cost}
    )


def upload_document_view(request, session_id):
    session = get_object_or_404(ResearchSession, id=session_id)

    if request.method == "POST" and request.FILES.get("file"):
        UploadedDocument.objects.create(
            session=session,
            file=request.FILES["file"]
        )
        run_research_task.delay(session.id)

    return redirect("session-detail", session_id=session.id)


def continue_research_view(request, session_id):
    if request.method == "POST":
        parent_session = get_object_or_404(ResearchSession, id=session_id)
        query = request.POST.get("query")
        new_session = ResearchSession.objects.create(
            question=query,
            parent=parent_session
        )

        parent_summary = ""
        last_step = parent_session.steps.last()
        if last_step:
            parent_summary = last_step.output

        run_research_task.delay(new_session.id, parent_summary=parent_summary)
        return redirect("session-detail", session_id=new_session.id)
