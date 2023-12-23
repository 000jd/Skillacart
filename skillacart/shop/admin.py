from django.contrib import admin
from .models import ProductCategory, Product, ProductImage, ProductReview
from django.utils.html import format_html
from django.db.models import Q

class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['icon', 'name']
    list_filter = ['name']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_image', 'price', 'quantity', 'category']
    list_filter = ['name', 'price', 'category']
    search_fields = ['name', 'category__name', 'price', 'quantity'] 

    def get_search_fields(self, request):
        search_field = request.GET.get('search_field', 'name') 
        return [search_field]

    def display_image(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" width="50" height="50" />', obj.thumbnail.url)
        else:
            return 'No Image'
    display_image.short_description = 'Image'

class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['image', 'product']
    search_fields = ['image', 'product__name']  
    list_filter = ['image', 'product__name']

    def get_search_fields(self, request):
        search_field = request.GET.get('search_field', 'image')  
        return [search_field]
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'rating', 'created_at']
    search_fields = ['user__username', 'product__name', 'rating', 'created_at']
    list_filter = ['user__username', 'product__name', 'rating', 'created_at']

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        
        # Spliting the search term into words and prepare Q objects
        search_terms = search_term.split()
        q_objects = Q()

        for term in search_terms:
            q_objects |= Q(user__username__icontains=term)
            q_objects |= Q(product__name__icontains=term)
            q_objects |= Q(rating__icontains=term)
            q_objects |= Q(created_at__icontains=term)

        # Appling the Q objects to filter the queryset
        queryset |= self.model.objects.filter(q_objects)

        return queryset, use_distinct

admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)