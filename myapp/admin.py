from django.contrib import admin
from .models import Article,Slides,Test,TestResult,SlidesPdf,ArticlePdf

admin.site.register(Article)
admin.site.register(Slides)
admin.site.register(Test)
admin.site.register(TestResult)
admin.site.register(SlidesPdf)
admin.site.register(ArticlePdf)
# Register your models here.
