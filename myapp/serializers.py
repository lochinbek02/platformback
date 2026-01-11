from rest_framework import serializers
from .models import Article,Slides,Test,TestResult,SlidesPdf,ArticlePdf,VideoLessons,Questions, UserSettings, SubjectInfoPdf, InnovativeSchemePdf, CustomPlotExampleDefault, LimitGraphDefault
from django.contrib.auth.models import User

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id','title', 'content', 'image','mincontent'] 
class SlideSerializer(serializers.ModelSerializer):
    class Meta:
        model =Slides
        fields=['id','title','file']

class TestSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Test
        fields=['id','title','file']


class TestResultSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True) 

    class Meta:
        model = TestResult
        fields = ['user', 'test', 'score', 'total_questions']
class SlidesPdfSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlidesPdf
        fields=['id','title','file']

class ArticlePdfSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticlePdf
        fields=['id','title','file']
class VideoLessonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoLessons
        fields=['id','title','file','uploaded_at']

class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields=['id','name','email','question']

class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = ['dark_mode', 'language', 'notifications_enabled', 'username', 'email']

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'is_superuser']

class SubjectInfoPdfSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectInfoPdf
        fields = ['id', 'title', 'file', 'uploaded_at']

class InnovativeSchemePdfSerializer(serializers.ModelSerializer):
    class Meta:
        model = InnovativeSchemePdf
        fields = ['id', 'title', 'file', 'uploaded_at']


class CustomPlotExampleDefaultSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomPlotExampleDefault
        fields = ['id', 'title', 'description', 'video', 'epsilon', 'x_end', 'uploaded_at', 'is_active']


class LimitGraphDefaultSerializer(serializers.ModelSerializer):
    class Meta:
        model = LimitGraphDefault
        fields = ['id', 'title', 'description', 'video', 'epsilon', 'uploaded_at', 'is_active']