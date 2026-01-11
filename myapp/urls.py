from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import create_video,create_custom_plot_video,MyTokenObtainPairView,ProtectedView,ArticleCreateView,ArticleListAPIView, ArticleDetailView,MyModelRetrieveDestroyView
from .views import SlideRetrieveDestroyView,SlideDetailView,SlideListAPIView, SlideCreateView
from .views import TestCreateView,TestDetailView,TestListAPIView,TestRetrieveDestroyView,SaveTestResultView,TestResultListView,SlideUploadPdfView,ArticleUploadPdfView,ArticleListPdfView,SlideListPdfView
from .views import PdfRetrieveDestroyView
from .views import *
urlpatterns = [

    # nazariya
    path('articles-view/', ArticleListAPIView.as_view(), name='article-list'),
    path('articles/<int:id>/', ArticleDetailView.as_view(), name='article-detail'),
    path('articles/', ArticleCreateView.as_view(), name='article-create'),
    path('delete-item/<int:pk>/', MyModelRetrieveDestroyView.as_view(), name='delete-item'),
    path('delete-item-pdf/<int:pk>/', PdfRetrieveDestroyView.as_view(), name='delete-item'),
    path('upload-articlepdf/', ArticleUploadPdfView.as_view(), name='upload-articlepdf'),
    path('see-upload-articlepdf/', ArticleListPdfView.as_view(), name='upload-articlepdf'),

    # taqdimot
    path('slides-view/', SlideListAPIView.as_view(), name='slide-list'),
    path('slides/<int:id>/', SlideDetailView.as_view(), name='slide-detail'),
    path('slides/', SlideCreateView.as_view(), name='slide-create'),
    path('delete-slide/<int:pk>/', SlideRetrieveDestroyView.as_view(), name='delete-slide'),
    path('upload-pdf/', SlideUploadPdfView.as_view(), name='upload-pdf'),
    path('see-upload-pdf/', SlideListPdfView.as_view(), name='see-upload-pdf'),
    # test
    path('test-view/', TestListAPIView.as_view(), name='test-list'),
    path('test/<int:id>/', TestDetailView.as_view(), name='test-detail'),
    path('tests/', TestCreateView.as_view(), name='test-create'),
    path('delete-test/<int:pk>/', TestRetrieveDestroyView.as_view(), name='delete-test'),
    path('save_test_result/', SaveTestResultView.as_view(), name='save_test_result'),
    path('test-results/', TestResultListView.as_view(), name='test-results'),
    # login
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('some_protected_route/', ProtectedView.as_view(), name='protected'),
    # Model yaratish
    path('create-video/', create_video, name='create_video'),
    path('create_custom_plot_video/',create_custom_plot_video, name='create_custom_plot_video'),
    # video lessons
    path('video-lessons/', VideoLessonsListAPIView.as_view(), name='video-lessons'),
    path('video-lessons/<int:id>/', VideoLessonsDetailView.as_view(), name='video-lessons-detail'),
    path('video-lessons-create/', VideoLessonsCreateView.as_view(), name='video-lessons-create'),
    path('delete-video-lessons/<int:pk>/', VideoLessonsRetrieveDestroyView.as_view(), name='delete-video-lessons'),
    # questions
    path('questions/', QuestionsCreateView.as_view(), name='questions'),
    
    # user management and settings
    path('users/list/', UserListView.as_view(), name='user-list'),
    path('users/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('user/settings/', UserSettingsView.as_view(), name='user-settings'),
    path('user/update-profile/', UserSettingsView.as_view(), name='update-profile'),

    # Subject Info PDFs
    path('subject-info-pdfs/', SubjectInfoPdfListAPIView.as_view(), name='subject-info-pdf-list'),
    path('upload-subject-pdf/', SubjectInfoPdfCreateView.as_view(), name='subject-info-pdf-create'),
    path('delete-subject-info-pdf/<int:pk>/', SubjectInfoPdfRetrieveDestroyView.as_view(), name='subject-info-pdf-delete'),

    # Innovative Scheme PDFs
    path('innovative-scheme-pdfs/', InnovativeSchemePdfListAPIView.as_view(), name='innovative-scheme-pdf-list'),
    path('upload-innovative-pdf/', InnovativeSchemePdfCreateView.as_view(), name='innovative-scheme-pdf-create'),
    path('delete-innovative-scheme-pdf/<int:pk>/', InnovativeSchemePdfRetrieveDestroyView.as_view(), name='innovative-scheme-pdf-delete'),

    # CustomPlotExample Default Video (faqat GET)
    path('custom-plot-default-video/', CustomPlotExampleDefaultListAPIView.as_view(), name='custom-plot-default'),

    # LimitGraph Default Video (faqat GET)
    path('limit-graph-default-video/', LimitGraphDefaultListAPIView.as_view(), name='limit-graph-default'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)