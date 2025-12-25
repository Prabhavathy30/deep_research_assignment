from django.urls import path
from . import views

urlpatterns = [
    # UI Views
    path('', views.home_view, name='home'),
    path('session/<int:session_id>/', views.session_detail_view, name='session-detail'),
    path('session/<int:session_id>/upload/', views.upload_document_view, name='upload_document'),
    path('session/<int:session_id>/continue/', views.continue_research_view, name='continue_research'),

    # API Views (DRF)
    path('api/create-session/', views.ResearchSessionCreateAPIView.as_view(), name='api-create-session'),
    path('api/research-sessions/', views.ResearchSessionListAPIView.as_view(), name='api-list-sessions'),
    path('api/research-sessions/<int:id>/', views.ResearchSessionDetailAPIView.as_view(), name='api-session-detail'),
    path('api/upload-document/', views.UploadedDocumentCreateAPIView.as_view(), name='api-upload-document'),
]
