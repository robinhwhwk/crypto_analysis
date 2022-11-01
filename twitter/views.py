from importlib.metadata import distribution
from re import template
from typing import Any, Optional
from urllib import response
import pandas as pd
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from .models import Ratings

import tweepy
from . import tweet_analysis
from . import coins

# Create your views here.
# views functions takes a request and returns a response
# request handler
# action


class IndexView(View):
    def get(self, request, *args, **kwargs):
        template = loader.get_template('index.html')
        ratings = Ratings.objects.all().values()
        context = {
            'ratings': ratings,
        }
        return HttpResponse(template.render(context, request))


class SearchView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('query',).lower()
        template = loader.get_template('index.html')

        rating = tweet_analysis.getRating(query)
        positive, negative, neutral = tweet_analysis.getDistribution(
            tweet_analysis.getDataframe(query))
        piechart = tweet_analysis.getPiechart(query)
        wordcloud = tweet_analysis.getWordcloud(query)
        pricechart = coins.getPriceChart(query)
        context = {
            'name': query,
            'rating': rating,
            'positive': positive,
            'negative': negative,
            'neutral': neutral,
            'piechart': piechart,
            'wordcloud': wordcloud,
            'pricechart': pricechart,
        }
        rating = Ratings(name=query, rating=rating,
                         positive=positive, negative=negative, neutral=neutral)
        rating.save()

        return HttpResponse(template.render(context, request))
