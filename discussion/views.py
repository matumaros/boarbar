from django.views.generic import View

from django.shortcuts import render


class AddWordDiscussionView(View):
    http_methods_name = ['get']


class WordDiscussionView(View):
    http_methods_name = ['get']
