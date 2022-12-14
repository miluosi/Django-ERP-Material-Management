import json
from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth, messages
from django import forms
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict

from ..models import *
from .auxiliary import *

@login_required
def create_invoice(request: HttpRequest):
    if request.method == 'GET':
        return render(
            request=request,
            template_name='../templates/invoice/create.html'
        )
    else:
        return HttpResponse(status=405)

@login_required
def search_invoice(request: HttpRequest):
    if request.method == 'GET':
        return render(
            request=request,
            template_name='../templates/invoice/search.html'
        )
    else:
        return HttpResponse(status=405)

@login_required
def payment(request: HttpRequest):
    if request.method == 'GET':
        return render(
            request=request,
            template_name='../templates/invoice/pay.html'
        )
    else:
        return HttpResponse(status=405)

@login_required
def display_invoice(request: HttpRequest):
    get = request.GET
    orderID = get.get('orderID')
    itemID = get.get('itemID')
    item: OrderItem = get_object_or_404(OrderItem, po__id__exact=orderID, itemId__exact=itemID)
    invoice = Invoice.objects.get(orderItem__id__exact=item.id)
    item_dict = model_to_dict(item)
    materialItem: MaterialItem = get_object_or_404(MaterialItem, id__exact=item.meterialItem.id)
    material: Material = get_object_or_404(Material, id__exact=materialItem.material.id)
    stock: Stock = get_object_or_404(Stock, id__exact=materialItem.stock.id)
    po: PurchaseOrder = get_object_or_404(PurchaseOrder, id__exact=item.po.id)
    vendor: Vendor = get_object_or_404(Vendor, vid__exact=po.vendor.vid)
    gr: GoodReceipt = get_object_or_404(GoodReceipt, orderItem__id__exact=item.id)
    item_dict['po'] = model_to_dict(po)
    item_dict['materialItem'] = model_to_dict(materialItem)
    item_dict['material'] = model_to_dict(material)
    item_dict['stock'] = model_to_dict(stock)
    item_dict['invoice'] = model_to_dict(invoice)
    item_dict['vendor'] = model_to_dict(vendor)
    item_dict['gr'] = model_to_dict(gr)
    return render(
        request=request,
        template_name='../templates/invoice/display.html',
        context={'context': item_dict}
    )

@login_required
def load_order_item(request: HttpRequest):
    get = request.GET
    orderID = get.get('orderID')
    itemID = get.get('itemID')
    item: OrderItem = get_object_or_404(OrderItem, po__id__exact=orderID, itemId__exact=itemID)
    item_dict = model_to_dict(item)
    materialItem: MaterialItem = get_object_or_404(MaterialItem, id__exact=item.meterialItem.id)
    material: Material = get_object_or_404(Material, id__exact=materialItem.material.id)
    stock: Stock = get_object_or_404(Stock, id__exact=materialItem.stock.id)
    po: PurchaseOrder = get_object_or_404(PurchaseOrder, id__exact=item.po.id)
    item_dict['po_'] = model_to_dict(po)
    item_dict['materialItem_'] = model_to_dict(materialItem)
    item_dict['material_'] = model_to_dict(material)
    item_dict['stock_'] = model_to_dict(stock)
    return render(
        request=request,
        template_name='../templates/invoice/create2.html',
        context={'context': item_dict}
    )