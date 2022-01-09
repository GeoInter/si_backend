from http import HTTPStatus
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

import json

from app.models import Strategy

@csrf_exempt
@api_view(['POST'])
def get_action(request, format=json):
    payload = json.loads(request.body)
        
    p_cards = payload['player_cards'] # array
    d_card = payload['dealer_card'] # single element 2-10 or A
    nrDecks = payload['nrDecks'] # 1,2 or 4
    isSoft = payload['isSoft'] # boolean
    isDAS = payload['isDAS'] # boolean

    player_hand = ""
    if("A" in p_cards):
        # contains an ace
        print("found an ace")
        if p_cards.index("A") == 0:
            player_hand = "A-" + p_cards[1]
        else:
            player_hand = "A-" + p_cards[0]

    elif len(p_cards) != len(set(p_cards)):
        # contains at least one pair of the same value
        print("found a pair")
        player_hand = p_cards[0] + "-" + p_cards[1]
        
    else:
        sum = 0
        for card in p_cards:
            sum += int(card)
        if sum <= 7:
            player_hand = "5-7"
        else:
            player_hand = str(sum)
            print("sum = " + player_hand)
    

    isSoftInt = int(isSoft)
    isDASInt = int(isDAS)
    rulesetId = nrDecks * 100 + isSoftInt * 10 + isDASInt

    try:
        strategy = Strategy.objects.get(player_cards=player_hand, dealer_cards=d_card, rulesetId=rulesetId)
        message = { 'action': strategy.action}
        httpcode = HTTPStatus.OK
    except Strategy.DoesNotExist:
        message = { 'Error': 'No Strategy for this scenario found'}
        httpcode = HTTPStatus.INTERNAL_SERVER_ERROR
    except Strategy.MultipleObjectsReturned:
        message = { 'Error': 'Found multiple Strategies instead of one - database redundancy'}
        httpcode = HTTPStatus.INTERNAL_SERVER_ERROR
    except:
        message = { 'Error': 'Internal Server Error'}
        httpcode = HTTPStatus.INTERNAL_SERVER_ERROR
    response = JsonResponse(message)
    response.status_code = httpcode
    return response



@csrf_exempt
@api_view(['POST'])
def set_strat(request, format=json):
    payload = json.loads(request.body)
        # method to validate response?
        # how to request to db? 
            # for remote db?
        # map Queen, King, Jack to the value 10
    p_cards = payload['player_cards']
    d_card = payload['dealer_card']
    action = payload['action']
    nrDecks = payload['nrDecks']
    isSoft = payload['isSoft']
    isDAS = payload['isDAS']

    isSoftInt = int(isSoft)
    isDASInt = int(isDAS)
    rulesetId = nrDecks * 100 + isSoftInt * 10 + isDASInt

    try:
        strategy = Strategy(player_cards=p_cards, dealer_cards=d_card, action=action, rulesetId=rulesetId)
        strategy.save()

        message = { 'Success': 'cool'}
        httpcode = HTTPStatus.OK
    except:
        message = { 'Error': 'Internal Server Error'}
        httpcode = HTTPStatus.INTERNAL_SERVER_ERROR
    response = JsonResponse(message)
    response.status_code = httpcode
    return response