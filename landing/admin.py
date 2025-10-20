from django.contrib import admin
from .models import (
    AboutBlock, Trailer, ProductInfo, Screenshot, Version,
    FPVMode, PurchaseOption, Footer, ContactForm, ScreenshotAlbum, AppScreenshot, PrivacyPolicy
)

class SingletonModelAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return self.model.objects.count() == 0

admin.site.register(AboutBlock, SingletonModelAdmin)
admin.site.register(Trailer, SingletonModelAdmin)
admin.site.register(ProductInfo, SingletonModelAdmin)
admin.site.register(FPVMode, SingletonModelAdmin)
admin.site.register(Footer, SingletonModelAdmin)

class ScreenshotInline(admin.TabularInline):
    model = Screenshot
    extra = 1

@admin.register(ScreenshotAlbum)
class ScreenshotAlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    inlines = [ScreenshotInline]

@admin.register(Screenshot)
class ScreenshotAdmin(admin.ModelAdmin):
    list_display = ('album', 'caption', 'image')
    list_filter = ('album',)

@admin.register(AppScreenshot)
class AppScreenshotAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'image')
    list_editable = ('order',)
    ordering = ['order']

@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(SingletonModelAdmin):
    list_display = ('title', 'last_updated')
    fields = ('title', 'content', 'last_updated')
    readonly_fields = ('last_updated',)

@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(PurchaseOption)
class PurchaseOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_custom')

@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'organization_name', 'email', 'phone', 'created_at')
    readonly_fields = ('full_name', 'phone', 'email', 'organization_name', 'comment', 'privacy_policy_accepted', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('full_name', 'organization_name', 'email')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
