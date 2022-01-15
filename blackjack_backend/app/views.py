from http import HTTPStatus
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

import json
import re 

from app.models import Strategy

@csrf_exempt
@api_view(['POST'])
def get_action(request, format=json):
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return createResponse(HTTPStatus.BAD_REQUEST, {'Error': 'Transmitted JSON is invalid'})

    if(not is_JSON_valid(payload)):
        return createResponse(HTTPStatus.BAD_REQUEST, {'Error': 'Errors in transmitted JSON'})

    p_cards = payload['player_cards']
    d_card = payload['dealer_card']
    nrDecks = payload['nrDecks']
    isSoft = payload['isSoft']
    isDAS = payload['isDAS']

    # convert playerhand 
    player_hand = ""
    if(len(p_cards) != len(set(p_cards)) and len(p_cards) == 2):
        # contains at least one pair of the same value
        if("11" in p_cards):
            player_hand = "A-A"
        else:
            player_hand = p_cards[0] + "-" + p_cards[1]
    else:
        sum = 0
        if("A" in p_cards):
            aceIndex = p_cards.index("A")
        elif("11" in p_cards):
            aceIndex = p_cards.index("11")
        else:
            aceIndex = -1
        for i in range(len(p_cards)):
            if i != aceIndex: # skip ace for addition of values
                sum += int(p_cards[i])

        if("A" in p_cards or "11" in p_cards):
            player_hand = "A-" + str(sum)
        elif(sum <= 7): 
            player_hand = "5-7"
        elif(sum > 21):
            return createResponse(HTTPStatus.BAD_REQUEST, { 'Error': "player hand already exceeds 21 with a value of: " + str(sum)})
        elif(not isSoft and sum >= 18):
            player_hand = "18-21"
        elif(isSoft and sum >= 17):
            player_hand = "17-21"
        else:
            player_hand = str(sum)
    

    # convert dealer hand
    if("11" in d_card):
        dealer_hand = "A"
    else:
        dealer_hand = d_card


    isSoftInt = int(isSoft)
    isDASInt = int(isDAS)
    rulesetId = nrDecks * 100 + isSoftInt * 10 + isDASInt

    try:
        strategy = Strategy.objects.get(player_cards=player_hand, dealer_cards=dealer_hand, rulesetId=rulesetId)
        return createResponse(HTTPStatus.OK, { 'action': strategy.action})
    except Strategy.DoesNotExist:
        return createResponse(HTTPStatus.INTERNAL_SERVER_ERROR, { 'Error': 'No Strategy for this scenario found'})
    except Strategy.MultipleObjectsReturned:
        return createResponse(HTTPStatus.INTERNAL_SERVER_ERROR, { 'Error': 'Found multiple Strategies instead of one - database redundancy'})
    except:
        return createResponse(HTTPStatus.INTERNAL_SERVER_ERROR, { 'Error': 'Internal Server Error'})


def is_JSON_valid(payload):
    nrDeck = int(payload['nrDecks'])
    if(nrDeck == 3 or nrDeck < 1 or nrDeck > 4):
        return False
        
    dealer_hand = payload['dealer_card']
    pattern = re.compile('^([2-9]|10|A|11)$')
    if(not pattern.match(dealer_hand)):
        return False
    
    player_hand = payload['player_cards']
    if(len(player_hand) > 7):
        return False
    for i in range(len(player_hand)):
        if(not pattern.match(player_hand[i])):
            return False
        
    return True

def createResponse(httpcode, message):
    response = JsonResponse(message)
    response.status_code = httpcode
    return response
