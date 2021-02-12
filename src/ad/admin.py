from django.contrib import admin
# from django.contrib.contenttypes.admin import GenericTabularInline
from mptt.admin import DraggableMPTTAdmin
from ad.models import City, \
    Category, AdvertisementImage, Advertisement


class SubCategoryInline(admin.TabularInline):
    model = Category
    extra = 14
    exclude = ('icon', 'slug')

class CategoryAdmin(DraggableMPTTAdmin):
    fieldsets = (
        ('Информация', {'fields': ('title', 'parent', 'icon', 'slug')}),
    )
    inlines = (SubCategoryInline,)


class AdvertisementImageInline(admin.TabularInline):
    model = AdvertisementImage
    extra = 3
    fieldsets = (
        ('Основные поля', {'fields': ('id', 'image', 'is_main') }),
    )

    
class AdvertisementAdmin(admin.ModelAdmin):
    inlines = (AdvertisementImageInline,)
    fieldsets = (
        ('Основные поля', {'fields': ('category', 'description', 'price', 'currency', 'city') }),
        ('Контакты', {'fields': ('author', 'phone_number', 'hide_phone_number', 'email')}),
        ('Остальное', {'fields': ('likes', 'views', 'created_at', 'updated_at')})
    )
    readonly_fields = ('created_at','updated_at')
    list_display = ('id', 'description','category', 'count_images')

    def count_images(self, obj):
        return obj.images.count()

class CityAdmin(admin.ModelAdmin):
    pass

admin.site.register(City, CityAdmin)
admin.site.register(Advertisement, AdvertisementAdmin)
admin.site.register(
    Category,
    CategoryAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
        'icon',
        'slug'
    ),
    list_display_links=(
        'indented_title',
    ))