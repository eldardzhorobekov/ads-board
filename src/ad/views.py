from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model

from ad.models import Category, Advertisement, AdvertisementImage
from ad.forms import AdvertisementForm, AdvertisementImageInlineFormset


CustomUser = get_user_model()

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'ads/category-details.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        return context


class AdvertisementDetailView(DetailView):
    model = Advertisement
    template_name = 'ads/ads-details.html'
    context_object_name = 'ad'

    def get_context_data(self, **kwargs):
        context = super(AdvertisementDetailView, self).get_context_data(**kwargs)
        context['images'] = self.object.images.order_by('id')
        return context


class AdvertisementUpdateView(LoginRequiredMixin, UpdateView):
    model = Advertisement
    template_name = 'ads/ads-edit.html'
    form_class = AdvertisementForm

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context.get('formset')

        if formset.is_valid():
            form.save()
            formset.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))
    def get_context_data(self, **kwargs):
        context = super(AdvertisementUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = AdvertisementImageInlineFormset(
                data=self.request.POST,
                files=self.request.FILES,
                instance=self.object,
                queryset=self.object.images.all()
            )
        else:
            context['formset'] = AdvertisementImageInlineFormset(instance=self.object)
        return context

class AdvertisementCreateView(LoginRequiredMixin, CreateView):
    model = Advertisement
    form_class = AdvertisementForm
    template_name = 'ads/ads-edit.html'

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context.get('formset')

        if formset.is_valid():
            form.instance.author = self.request.user
            self.object = form.save()
            # formset.instance = self.object
            for form in formset:
                form.instance.advertisement = self.object
                form.instance.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(AdvertisementCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = AdvertisementForm(self.request.POST)
            context['formset'] = AdvertisementImageInlineFormset(self.request.POST, self.request.FILES)
        else:
            initial_values = {
                'phone_number': self.request.user.phone_number or '',
                'email': self.request.user.email or '',
            }
            context['form'] = AdvertisementForm(initial=initial_values)
            context['formset'] = AdvertisementImageInlineFormset()
        return context


class UserAdvertisementListView(LoginRequiredMixin, ListView):
    template_name = 'ads/user-ads-list.html'
    model = Advertisement
    context_object_name = 'ads'
    def get_queryset(self):
        return Advertisement.objects.with_counts().filter(author=self.request.user)
