from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render
from django.db import transaction

from square.client import Client
from square.configuration import Configuration

import json
import requests
import uuid

from donation_test import settings
from .models import CardPayment

client = Client(
    access_token=settings.SQUARE_ACCESS_TOKEN,
)

payments_api = client.payments

def payment_form(request):
    if request.method != 'GET':
        raise SuspiciousOperation('Wrong method for payment form')

    fixed = request.GET.get('amount', '')
    custom = request.GET.get('custom', '')

    if custom != '':
        amount = int(custom)
    elif fixed != '':
        amount = int(fixed)
    else:
        amount = 5 # give up

    if amount < 5 or amount > 200:
        raise SuspiciousOperation('Wrong params for payment form')

    context = {
        'sq_app_id': settings.SQUARE_APP_ID,
        'amount': amount,
    }
    return render(request, 'payment_form.html', context)

def process_payment(request):
    if request.method != 'POST':
        raise SuspiciousOperation('Wrong method for payment processing')

    try:
        request_params = json.loads(request.body)

        # length of idempotency_key should be less than 45
        idempotency_key = str(uuid.uuid1())

        amount = request_params['amount']
        if amount < 5 or amount > 200:
            raise SuspiciousOperation('Wrong params for payment processing')

        body = {
            'source_id': request_params['nonce'],
            'amount_money': {
                'amount': amount * 100,
                'currency': 'AUD',
            },
            'idempotency_key': idempotency_key,
        }

        # setup Square payment manually
        endpoint = 'https://connect.squareupsandbox.com/v2/payments'
        access_token = settings.SQUARE_ACCESS_TOKEN
        headers = {
            'Square-Version': '2020-04-22',
            'Authorization': 'Bearer {}'.format(access_token),
            'Content-Type': 'application/json',
        }

        result = requests.post(endpoint, headers=headers, json=body)

        if result.status_code == 200:
            # actually commit to payment, now
            with transaction.atomic():
                # credit the user's account
                balance_obj = request.user.attendee_info.balance
                balance_obj.balance += amount
                balance_obj.cumulative += amount
                balance_obj.save()

                # and record the transaction
                pay_record = CardPayment(
                    amount=amount,
                    idempotency_key=idempotency_key,
                    attendee_payer=request.user.attendee_info,
                )
                pay_record.save()

            return JsonResponse({
                'title': 'Payment Successful',
                'result': result.json(),
            })
        else:
            return JsonResponse({
                'title': 'Payment Failure',
                'result': result.json(),
            }, status=500)

    except (KeyError, ValueError):
        raise SuspiciousOperation('Wrong params for payment processing')
