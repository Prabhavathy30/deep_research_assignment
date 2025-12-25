from django.contrib import admin
from .models import ResearchSession, ResearchStep, UploadedDocument, CostUsage


class ResearchStepInline(admin.TabularInline):
    model = ResearchStep
    extra = 0
    readonly_fields = ("step_name", "output", "created_at")


class UploadedDocumentInline(admin.TabularInline):
    model = UploadedDocument
    extra = 0
    readonly_fields = ("file", "uploaded_at")


class CostUsageInline(admin.StackedInline):
    model = CostUsage
    readonly_fields = ("total_tokens", "total_cost_usd")
    can_delete = False
    max_num = 1


@admin.register(ResearchSession)
class ResearchSessionAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "status", "total_tokens", "total_cost_usd", "created_at")
    inlines = [ResearchStepInline, UploadedDocumentInline, CostUsageInline]
    list_filter = ("status",)
    readonly_fields = ("status", "created_at")

    def total_tokens(self, obj):
        return obj.cost.total_tokens if hasattr(obj, "cost") else 0

    def total_cost_usd(self, obj):
        return obj.cost.total_cost_usd if hasattr(obj, "cost") else 0.0


@admin.register(ResearchStep)
class ResearchStepAdmin(admin.ModelAdmin):
    list_display = ("id", "session", "step_name", "created_at")
    list_filter = ("session",)


@admin.register(UploadedDocument)
class UploadedDocumentAdmin(admin.ModelAdmin):
    list_display = ("id", "session", "file", "uploaded_at")
    list_filter = ("session",)


@admin.register(CostUsage)
class CostUsageAdmin(admin.ModelAdmin):
    list_display = ("id", "session", "total_tokens", "total_cost_usd")
    readonly_fields = ("total_tokens", "total_cost_usd")
