from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from news.cluster import get_nearest_clusters, cluster_news, id_gen
import numpy as np
import random
import datetime
from time import gmtime, strftime

from news.forms import createNewsform

flag = 0


def all_news(request):
    clusters = []
    cnt = 0
    cluster_batch = []
    random.shuffle(news_data)
    for news_row in news_data:
        cluster_batch.append(news_row)
        cnt += 1
        if cnt == 3:
            clusters.append(cluster_batch)
            cnt = 0
            cluster_batch = []
        if len(clusters) == 100:
            break
    batch_range = range(len(clusters))
    if request.method == "GET":
        return render(request, '../templates/news/all_news.html',
                      {'news': news, 'clusters': clusters, 'batch_range': batch_range})


def news(request, news_id):
    global flag
    if flag == 0:
        with open("C:/diploma/Web-proj/NewsRecs/data/my_clusters_final.json") as json_file:
            global news_data
            news_data = json.load(json_file)
            flag = 1

    for news_row in news_data:
        if news_row.get('id') == news_id:
            news = news_row
            break
    closest_clusters = get_nearest_clusters(news.get('cluster_id'))
    clusters = []
    for news_row in news_data:
        if news_row.get('cluster_id') in closest_clusters and news_row.get('id') != news.get('id'):
            clusters.append(news_row)
    clusters = sorted(clusters, key=lambda d: datetime.datetime.strptime(d['time'], "%m/%d/%Y"), reverse=True)
    if len(clusters) % 3 == 1:
        clusters = clusters[:-1]
    elif len(clusters) % 3 == 2:
        clusters = clusters[:-2]
    clusters = np.array_split(clusters, len(clusters) // 3)
    batch_range = range(len(clusters))
    if request.method == "GET":
        return render(request, '../templates/news/news.html',
                      {'news': news, 'clusters': clusters, 'closest_clusters':closest_clusters, 'batch_range': batch_range})


def news_add(request):
    if request.method == 'GET':
        form = createNewsform()
        return render(request, '../templates/news/create_news.html', {'form': form})
    elif request.method == 'POST':
        form = createNewsform(request.POST)
        if form.is_valid():
            body = request.POST.get("body")
            abstract = request.POST.get("abstract")
            subcategory = request.POST.get("subcategory")
            id = id_gen()
            time = strftime("%m/%d/%Y", gmtime())
            label = cluster_news(body, abstract, subcategory)
            news_data.append({"id": id, "subcategory": subcategory, "body":body, "abstract": abstract, "cluster_id":label, 'time':time})
            return redirect('/news/'+id)