from django.contrib import admin
from .models import Article,Slides,Test,TestResult,SlidesPdf,ArticlePdf,VideoLessons,Questions, UserSettings, SubjectInfoPdf, InnovativeSchemePdf, CustomPlotExampleDefault, LimitGraphDefault

@admin.register(SubjectInfoPdf)
class SubjectInfoPdfAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')

@admin.register(InnovativeSchemePdf)
class InnovativeSchemePdfAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')

@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'dark_mode', 'language', 'notifications_enabled')
    search_fields = ('user__username',)


@admin.register(CustomPlotExampleDefault)
class CustomPlotExampleDefaultAdmin(admin.ModelAdmin):
    list_display = ('title', 'epsilon', 'x_end', 'is_active', 'uploaded_at')
    list_filter = ('is_active', 'uploaded_at')
    search_fields = ('title', 'description')
    list_editable = ('is_active',)
    ordering = ['-uploaded_at']
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('title', 'description', 'video')
        }),
        ('Parametrlar', {
            'fields': ('epsilon', 'x_end', 'is_active')
        }),
    )


@admin.register(LimitGraphDefault)
class LimitGraphDefaultAdmin(admin.ModelAdmin):
    list_display = ('title', 'epsilon', 'is_active', 'uploaded_at')
    list_filter = ('is_active', 'uploaded_at')
    search_fields = ('title', 'description')
    list_editable = ('is_active',)
    ordering = ['-uploaded_at']
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('title', 'description', 'video')
        }),
        ('Parametrlar', {
            'fields': ('epsilon', 'is_active')
        }),
    )


admin.site.register(Article)
admin.site.register(Slides)
admin.site.register(Test)
admin.site.register(TestResult)
admin.site.register(SlidesPdf)
admin.site.register(ArticlePdf)
admin.site.register(VideoLessons)
admin.site.register(Questions)
# Register your models here.
