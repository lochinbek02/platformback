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