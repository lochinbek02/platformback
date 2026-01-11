# models.py
from django.db import models
from django.contrib.auth.models import User

class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="test_results")
    test = models.ForeignKey("Test", on_delete=models.CASCADE, related_name="results")  # Test modeli bilan bog'lash
    score = models.IntegerField()  # To‘g‘ri javoblar soni
    total_questions = models.IntegerField()  # Umumiy savollar soni
    created_at = models.DateTimeField(auto_now_add=True)  # Test ishlangan vaqti

    def __str__(self):
        return f"{self.user.username} - {self.test.title} - {self.score}/{self.total_questions}"
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()  # CKEditordan keladigan ma'lumot
    mincontent = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)  # Rasmni qo'shish
    

    def __str__(self):
        return self.title
    
class Slides(models.Model):
    title=models.CharField(max_length=200)
    file=models.FileField(upload_to='uploads/')
    uploaded_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
class SlidesPdf(models.Model):
    title=models.CharField(max_length=250)
    file=models.FileField(upload_to='uploads/pdf')
    uploaded_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

    
class Test(models.Model):
    title=models.CharField(max_length=250)
    file=models.FileField(upload_to='uploads/test/')
    uploaded_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
class ArticlePdf(models.Model):
    title=models.CharField(max_length=250)
    file=models.FileField(upload_to='uploads/pdf')
    uploaded_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
class VideoLessons(models.Model):
    title=models.CharField(max_length=300)
    file=models.FileField(upload_to='uploads/videolessons')
    uploaded_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
class Questions(models.Model):
    name=models.CharField(max_length=250)
    email=models.EmailField()
    question=models.TextField()
    
    def __str__(self):
        return self.question

class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')
    username = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    dark_mode = models.BooleanField(default=False)
    language = models.CharField(max_length=10, default='uz')
    notifications_enabled = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.username} settings"

class SubjectInfoPdf(models.Model):
    title = models.CharField(max_length=250)
    file = models.FileField(upload_to='uploads/subject_info/')
    uploaded_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

class InnovativeSchemePdf(models.Model):
    title = models.CharField(max_length=250)
    file = models.FileField(upload_to='uploads/innovative_scheme/')
    uploaded_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title


class CustomPlotExampleDefault(models.Model):
    """CustomPlotExample uchun default video saqlanadigan model"""
    title = models.CharField(max_length=300, verbose_name="Video nomi")
    description = models.TextField(blank=True, null=True, verbose_name="Tavsif")
    video = models.FileField(upload_to='uploads/default_videos/custom_plot/', verbose_name="Video fayl")
    epsilon = models.FloatField(default=1.0, verbose_name="Epsilon qiymati")
    x_end = models.IntegerField(default=20, verbose_name="X oxiri")
    uploaded_at = models.DateTimeField(auto_now=True, verbose_name="Yuklangan vaqt")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.title} (ε={self.epsilon})"


class LimitGraphDefault(models.Model):
    """LimitGraph uchun default video saqlanadigan model"""
    title = models.CharField(max_length=300, verbose_name="Video nomi")
    description = models.TextField(blank=True, null=True, verbose_name="Tavsif")
    video = models.FileField(upload_to='uploads/default_videos/limit_graph/', verbose_name="Video fayl")
    epsilon = models.FloatField(default=0.5, verbose_name="Epsilon qiymati")
    uploaded_at = models.DateTimeField(auto_now=True, verbose_name="Yuklangan vaqt")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.title} (ε={self.epsilon})"