from http import HTTPStatus
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import json

@csrf_exempt
def get_action(request):
    if request.method == 'POST':
        payload = json.loads(request.body)
        player_card = payload['player']
        dealer_card = payload['dealer']
        try:
            message = { 'action': 'cum'}
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