from django.contrib import admin
from .models import (Supporter, SupporterPromo, Country,
                     PromoImpressions, GeoFilter)


DEFAULT_EXCLUDES = ['BD', 'CN', 'TF', 'GT', 'IN', 'ID',
                    'IR', 'PK', 'PH', 'RU', 'TW', 'TH', 'TR', 'UA', 'VN']


def set_default_countries(modeladmin, request, queryset):
    for project in queryset:
        filter = project.geo_filters.create(filter_type='exclude')
        for country in Country.objects.filter(country__in=DEFAULT_EXCLUDES):
            filter.countries.add(country)
set_default_countries.short_description = "Add default exclude countries to this Promo"


class GeoFilterAdmin(admin.ModelAdmin):
    model = GeoFilter
    filter_horizontal = ('countries',)


class GeoFilterInline(admin.TabularInline):
    model = GeoFilter
    filter_horizontal = ('countries',)
    extra = 0


class SupporterAdmin(admin.ModelAdmin):
    model = Supporter
    raw_id_fields = ('user',)
    list_display = ('name', 'email', 'dollars', 'public')
    list_filter = ('name', 'email', 'dollars', 'public')


class ImpressionInline(admin.TabularInline):
    model = PromoImpressions
    readonly_fields = ('date', 'promo', 'offers', 'views', 'clicks', 'view_ratio', 'click_ratio')
    extra = 0
    can_delete = False
    max_num = 15

    def view_ratio(self, instance):
        return instance.view_ratio * 100

    def click_ratio(self, instance):
        return instance.click_ratio * 100


class SupporterPromoAdmin(admin.ModelAdmin):
    model = SupporterPromo
    save_as = True
    list_display = ('name', 'live', 'click_ratio', 'sold_impressions',
                    'total_views', 'total_clicks')
    list_filter = ('live', 'display_type')
    list_editable = ('live', 'sold_impressions')
    readonly_fields = ('total_views', 'total_clicks')
    inlines = [ImpressionInline, GeoFilterInline]
    actions = [set_default_countries]

    def view_ratio(self, instance):
        return instance.view_ratio() * 100

    def click_ratio(self, instance):
        return instance.click_ratio() * 100

    def total_views(self, instance):
        return sum(imp.views for imp in instance.impressions.all())

    def total_clicks(self, instance):
        return sum(imp.clicks for imp in instance.impressions.all())

admin.site.register(Supporter, SupporterAdmin)
admin.site.register(SupporterPromo, SupporterPromoAdmin)
admin.site.register(GeoFilter, GeoFilterAdmin)
