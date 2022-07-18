import json

from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore

from liqpay.liqpay3 import LiqPay

from bookshop.models import Book, CustomerOrder
from e_shop import settings


class PayView(TemplateView):
    template_name = 'bookshop/liqpay_api.html'

    def get(self, request, *args, **kwargs):
        ordering_data = self.request.session.get('ordering_data')
        cart = self.request.session.get('cart')
        liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)

        info_data = {
            'mail': ordering_data['mail'],
            'city': ordering_data['city'],
            'post_department': ordering_data['post_department'],
            'phone_number': ordering_data['phone_number'],
            'session_key': ordering_data['session_key']
        }

        user_active = self.request.user.is_active
        if user_active:
            info_data['pk'] = self.request.user.pk

        amount, description, info_body = 0, 'Оплата зи книги:', ''

        for k, v in cart.items():
            amount += v['quantity'] * v['price']
            current_book = Book.objects.get(pk=int(k))
            description += f'\nНазва книги: {current_book.title}, кількість: {v["quantity"]} шт.'
            info_body += f'Назва книги: ' \
                         f'{current_book.title}, ' \
                         f'кількість: {v["quantity"]} шт, код товару({current_book.code_product}).'
        info_body += f'\nЗагальна вартість: {str(amount)} грн'

        info_data['total_price'] = amount
        info_data['info_body'] = info_body

        params = {
            'action': 'pay',
            'amount': amount,
            'currency': 'UAH',
            'description': description,
            'version': '3',
            'sandbox': 0,  # sandbox mode, set to 1 to enable it
            'server_url': 'https://9fae-217-30-192-161.eu.ngrok.io/payment/pay-callback/',  # url to callback view
            'result_url': 'https://9fae-217-30-192-161.eu.ngrok.io/booklover/',
            'info': json.dumps(info_data),
        }

        signature = liqpay.cnb_signature(params)
        data = liqpay.cnb_data(params)

        return render(request, self.template_name, {'signature': signature, 'data': data})


@method_decorator(csrf_exempt, name='dispatch')
class PayCallbackView(View):
    def post(self, request, *args, **kwargs):
        liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
        data = request.POST.get('data')
        signature = request.POST.get('signature')
        sign = liqpay.str_to_sign(settings.LIQPAY_PRIVATE_KEY + data + settings.LIQPAY_PRIVATE_KEY)

        if sign == signature:
            response = liqpay.decode_data_from_str(data)
            business_data = json.loads(response['info'])

            order = CustomerOrder(
                order_items=business_data['info_body'],
                mail=business_data['mail'],
                city=business_data['city'],
                post_department=business_data['post_department'],
                total_price=business_data['total_price'],
                phone_number=business_data['phone_number']
            )

            if response['status'] == 'success':
                order.status_success = True
                s = Session.objects.get(pk=business_data['session_key'])
                session_dict = s.get_decoded()
                del session_dict['cart']
                session_dict = encode(s, session_dict)
                s.session_data = session_dict
                s.save()
            else:
                order.status_success = False

            if business_data.get('pk'):
                order.user = User.objects.get(pk=business_data.get('pk'))

            order.save()

        return HttpResponse('')


def encode(self, session_dict):
    return SessionStore().encode(session_dict)
