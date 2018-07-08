"""Views for the webmap app."""
# from django.views.generic import TemplateView

from django import http
from django.contrib.gis.shortcuts import render_to_kml
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page, never_cache
from django.views.decorators.gzip import gzip_page
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

from djgeojson.views import GeoJSONLayerView

from . import models


@gzip_page
@never_cache              # don't cache KML in browsers
@cache_page(24 * 60 * 60)  # cache in memcached for 24h
def kml_view(request, layer_name):
    # find layer by slug or throw 404
    v = get_object_or_404(models.Layer, slug=layer_name, status__show=True)

    # all enabled pois in this layer
    points = models.Poi.visible.filter(marker__layer=v)
    return render_to_kml(
        "webmap/gis/kml/layer.kml", {
            'places': points,
            'markers': models.Marker.objects.all(),
            'site': get_current_site(request).domain,
        },
    )


def search_view(request, query):
    if len(query) < 3:
        return http.HttpResponseBadRequest('Insufficient query lenght')

    # first by name
    name_qs = models.Poi.visible.filter(Q(name__icontains=query))
    # then by description, address and marker name if not done before
    extra_qs = models.Poi.visible.filter(
        Q(desc__icontains=query) |
        Q(address__icontains=query) |
        Q(marker__name__icontains=query),
    ).exclude(id__in=name_qs)
    # union qs doesn't hold order, so transform to lists and join
    points = list(name_qs) + list(extra_qs)
    return render_to_kml(
        "webmap/gis/kml/layer.kml",
        {
            'places': points,
            'site': get_current_site(request).domain,
        },
    )


class PopupView(DetailView):
    @method_decorator(gzip_page)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    template_name = "popup.html"
    model = models.Poi

    def get_context_data(self, *args, **kwargs):
        return {
            'poi': self.object,
            'fotky': self.object.photos.filter(status__show=True),
            'can_change': self.request.user.has_perm('webmap.change_poi'),  # and poi.has_change_permission(request.user),
        }


class LeafletIncludeView(TemplateView):
    template_name = "webmap/leaflet_include.js"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['markers'] = models.Marker.objects.all()
        context['layers'] = models.OverlayLayer.objects.all()
        return context


class WebmapGeoJsonView(GeoJSONLayerView):
    model = models.Poi
    properties = (
        'marker',
        'popup_url',
        'name',
    )

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(marker__layer__slug=self.kwargs['layer_slug'])


class FullWebmapView(TemplateView):
    template_name = "webmap/map.html"

    def get_context_data(self, preset_slug=None, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['markers'] = models.Marker.objects.all()
        context['layers'] = models.OverlayLayer.objects.all()
        context['base_layers'] = models.BaseLayer.objects.all()
        context['preset'] = models.MapPreset.objects.get(slug=preset_slug)
        context['presets'] = models.MapPreset.objects.all()
        return context

