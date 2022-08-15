from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth, messages
from django import forms
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict
from django.db.models import QuerySet, Sum
from django.utils import timezone
import json
import datetime

from ...models import EUser, Material, MaterialItem, Stock, StockHistory
from ..auxiliary import *

@login_required
def search_material(request: HttpRequest):
    post = request.POST
    mname = getRegex(post.get('mname'))
    mType = getRegex(post.get('mType'))
    industrySector = getRegex(post.get('industrySector'))
    materials = Material.objects.filter(
        mname__regex=mname, mType__regex=mType, industrySector__regex=industrySector
    )
    return HttpResponse(serializers.serialize('json', list(materials)))

@login_required
def search_item(request: HttpRequest):
    post = request.POST
    mid = post.get('mid')
    if mid == '':
        mname = getRegex(post.get('mname'))
        mType = getRegex(post.get('mType'))
        industrySector = getRegex(post.get('industrySector'))
        stock_name = getRegex(post.get('plant'))
        sloc = getRegex(post.get('sloc'))
        uid = getPk(post.get('uid'), 'U')
        items = MaterialItem.objects.filter(
            material__mname__regex=mname, material__mType__regex=mType, 
            material__industrySector__regex=industrySector, stock__name__regex=stock_name,
            sloc__regex=sloc, material__euser__id__regex=uid
        )
    else:
        stock_name = post.get('plant')
        sloc = post.get('sloc')
        items = MaterialItem.objects.filter(
            material__id__exact=int(mid), stock__name__exact=stock_name, sloc__exact=sloc
        )
    items_list = json.loads(serializers.serialize('json', list(items)))
    for i, item in enumerate(items):
        material: Material = Material.objects.get(pk__exact=item.material.pk)
        stock: Stock = Stock.objects.get(pk__exact=item.stock.pk)
        user: EUser = EUser.objects.get(pk__exact=item.material.euser.pk)
        items_list[i]['material'] = model_to_dict(material)
        items_list[i]['stock'] = model_to_dict(stock)
        items_list[i]['user'] = model_to_dict(user)
    return HttpResponse(json.dumps(items_list, default=str))

@login_required
def update_item(request: HttpRequest):
    post = request.POST
    material_id = getPkExact(post.get('material_id'), 'M')
    mname = post.get('mname')
    mType = post.get('mType')
    meaunit = post.get('meaunit')
    netWeight = post.get('netWeight')
    weightUnit = post.get('weightUnit')
    transGrp = post.get('transGrp')
    loadingGrp = post.get('loadingGrp')
    industrySector = post.get('industrySector')
    mGroup = post.get('mGroup')
    sloc = post.get('sloc')
    sOrg = post.get('sOrg')
    distrChannel = post.get('distrChannel')
    companyCode = post.get('companyCode')
    pOrg = post.get('pOrg')
    pGrp = post.get('pGrp')
    stock_name = post.get('name')
    materials: QuerySet = Material.objects.filter(id__exact=material_id)
    items: QuerySet = MaterialItem.objects.filter(
        material__id__exact=material_id, stock__name__exact=stock_name, sloc__exact=sloc
    )
    if len(materials) != 1:
        return HttpResponse(json.dumps({'status':0, 'message':"物料相关信息错误！"}))
    if len(items) != 1:
        return HttpResponse(json.dumps({'status':0, 'message':"物料条目相关信息错误！"}))
    material: Material = materials.first(); item: MaterialItem = items.first()
    item.distrChannel=distrChannel; item.sOrg=sOrg
    try:
        item.full_clean()
    except ValidationError as e:
        error_fields = list(e.error_dict.keys())
        return HttpResponse(json.dumps({'status':0, 'message':"表单填写错误！", 'fields':error_fields}))
    item.save()
    material.mname=mname; material.mType=mType; material.meaunit=meaunit; material.netWeight=netWeight
    material.weightUnit=weightUnit; material.transGrp=transGrp; material.loadingGrp=loadingGrp
    material.industrySector=industrySector; material.mGroup=mGroup
    try:
        material.full_clean()
    except ValidationError as e:
        error_fields = list(e.error_dict.keys())
        return HttpResponse(json.dumps({'status':0, 'message':"表单填写错误！", 'fields':error_fields}))
    material.save()
    return HttpResponse(json.dumps({'status':1, 'message':"商品信息已更新！"}))

@login_required
def search_stock(request: HttpRequest):
    post = request.POST
    client = getRegex(post.get('client'))
    companyCode = getRegex(post.get('companyCode'))
    pOrg = getRegex(post.get('pOrg'))
    pGrp = getRegex(post.get('pGrp'))
    stocks = Stock.objects.filter(
        client__regex=client, companyCode__regex=companyCode, pOrg__regex=pOrg, pGrp__regex=pGrp
    )
    return HttpResponse(serializers.serialize('json', list(stocks)))

@login_required
def search_stock_history(request: HttpRequest):
    MONTH_NUM = 6
    post = request.POST
    material_id = getPkExact(post.get('material_id'), 'M')
    stock_name = post.get('plant')
    sloc = post.get('sloc')
    items: QuerySet = MaterialItem.objects.filter(
        material__id__exact=material_id, stock__name__exact=stock_name, sloc__exact=sloc
    )
    if len(items) != 1:
        return HttpResponse(json.dumps({'status':0, 'message':"物料条目相关信息错误！"}))
    item: MaterialItem = items.first()
    init_ununrestrictUse = item.unrestrictUse
    init_qltyInspection = item.qltyInspection
    init_blocked = item.blocked
    now = timezone.now()
    history = StockHistory.objects.filter(
        item__id=item.id, time__range=[now+datetime.timedelta(days=-40*MONTH_NUM), now]
    ).values_list(
        'time__year', 'time__month'
    ).annotate(Sum('unrestrictUse'), Sum('qltyInspection'), Sum('blocked'))
    history_list = list(history)
    history_list.sort(key=lambda x:x[0]*100+x[1], reverse=True)
    history_list = history_list[:MONTH_NUM]
    result = [[now.year, now.month, init_ununrestrictUse, init_qltyInspection, init_blocked, item.transit]]
    for his in history_list:
        temp_date1 = datetime.date(year=his[0], month=his[1], day=1)
        temp_date2 = temp_date1 + datetime.timedelta(days=-1)
        result.append([temp_date2.year, temp_date2.month, result[-1][2] - his[2], result[-1][3] - his[3], result[-1][4] - his[4]])
    return HttpResponse(json.dumps({'status':1, 'message':result}, default=str))