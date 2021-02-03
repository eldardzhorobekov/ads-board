from django.contrib import admin
# from django.contrib.contenttypes.admin import GenericTabularInline
from mptt.admin import DraggableMPTTAdmin
from ad.models import Category


class SubCategoryInline(admin.TabularInline):
    model = Category
    extra = 14
    exclude = ('icon', 'slug')

class CategoryAdmin(DraggableMPTTAdmin):
    fieldsets = (
        ('Информация', {'fields': ('title', 'parent', 'icon', 'slug')}),
    )
    inlines = (SubCategoryInline,)

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