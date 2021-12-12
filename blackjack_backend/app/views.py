from http import HTTPStatus
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import json

from app.models import Action1

@csrf_exempt
def get_action(request):
    if request.method == 'POST':
        payload = json.loads(request.body)
        # method to validate response?
        # how to request to db? 
            # for remote db?
        # map Queen, King, Jack to the value 10
        p_cards = payload['player_cards']  # refactor because array, instead of single value
        d_card = payload['dealer_card']

        # Action1.objects.get(player_cards=p_cards, dealer_cards=d_card)

        try:
            message = { 'action': 'post on reddit'}
            httpcode = HTTPStatus.OK
        except:
            message = { 'Error': 'Internal Server Error'}
            httpcode = HTTPStatus.INTERNAL_SERVER_ERROR
    else:
        message = { 'Error': 'Method Not Allowed'}
        httpcode = HTTPStatus.METHOD_NOT_ALLOWED
    response = JsonResponse(message)
    response.status_code = httpcode
    return response