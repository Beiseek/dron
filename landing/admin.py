from django.contrib import admin
from .models import (
    AboutBlock, Trailer, ProductInfo, Screenshot, Version,
    FPVMode, PurchaseOption, Footer, ScreenshotAlbum, AppScreenshot, PrivacyPolicy,
    PageSettings
)

class SingletonModelAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return self.model.objects.count() == 0

@admin.register(Footer)
class FooterAdmin(SingletonModelAdmin):
    fieldsets = (
        ('Блок "Свяжитесь с нами"', {
            'fields': ('contact_title', 'contact_subtitle', 'address', 'email', 'phone')
        }),
        ('Логотипы в футере', {
            'fields': ('our_logo', 'partner_logo'),
            'classes': ('collapse',)
        }),
    )

admin.site.register(AboutBlock, SingletonModelAdmin)
admin.site.register(PageSettings, SingletonModelAdmin)

@admin.register(Trailer)
class TrailerAdmin(SingletonModelAdmin):
    fields = ('title', 'subtitle', 'local_video', 'video_url')

@admin.register(ProductInfo)
class ProductInfoAdmin(SingletonModelAdmin):
    fields = ('title', 'description', 'image')

@admin.register(FPVMode)
class FPVModeAdmin(SingletonModelAdmin):
    list_display = ('title',)
    fields = ('title', 'description', 'image')

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
    fields = ('name', 'price', 'features', 'is_custom')
