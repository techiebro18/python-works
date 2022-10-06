from django.contrib import admin
from .models import Product, Category, ProductImage, Brand, ProductTab
from import_export.admin import ImportExportModelAdmin

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'slug']

    class Meta:
        model = Category

admin.site.register(Category, CategoryAdmin)


class BrandAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'slug']

    class Meta:
        model = Brand

admin.site.register(Brand, BrandAdmin)


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage


@admin.register(Product)
#class ProductAdmin(admin.ModelAdmin):
class ProductAdmin(ImportExportModelAdmin):
    #list_display = ['__str__', 'sku', 'sale_price', 'price', 'quantity', 'category', 'brand']
    list_display = ['__str__', 'sku', 'sale_price', 'price', 'quantity', 'brand','product_image']
    search_fields = ('name', 'slug', 'description',)
    inlines = [ProductImageAdmin]

    class Meta:
        model = Product

    def get_queryset(self, obj):
        qs = super(ProductAdmin, self).get_queryset(obj)
        return qs.prefetch_related('productimage_set')

    def product_image(self, obj):
        return obj.productimage_set.all().first()

#admin.site.register(Product, ProductAdmin)


@admin.register(ProductImage)
class ProductImage(admin.ModelAdmin):
    pass


class ProducttabAdmin(admin.ModelAdmin):
    search_fields = ('product__name',)

    class Meta:
        model = ProductTab

admin.site.register(ProductTab, ProducttabAdmin)
