from django.contrib import admin
from .models import Article,Slides,Test,TestResult,SlidesPdf,ArticlePdf,VideoLessons,Questions

admin.site.register(Article)
admin.site.register(Slides)
admin.site.register(Test)
admin.site.register(TestResult)
admin.site.register(SlidesPdf)
admin.site.register(ArticlePdf)
admin.site.register(VideoLessons)
admin.site.register(Questions)
# Register your models here.
