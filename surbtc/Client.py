# -*- coding: utf-8 -*-

"""
Cliente para servicios web de SURBTC
Copyright (C) SASCO SpA (https://sasco.cl)

Este programa es software libre: usted puede redistribuirlo y/o modificarlo
bajo los términos de la GNU Lesser General Public License (LGPL) publicada
por la Fundación para el Software Libre, ya sea la versión 3 de la Licencia,
o (a su elección) cualquier versión posterior de la misma.

Este programa se distribuye con la esperanza de que sea útil, pero SIN
GARANTÍA ALGUNA; ni siquiera la garantía implícita MERCANTIL o de APTITUD
PARA UN PROPÓSITO DETERMINADO. Consulte los detalles de la GNU Lesser General
Public License (LGPL) para obtener una información más detallada.

Debería haber recibido una copia de la GNU Lesser General Public License
(LGPL) junto a este programa. En caso contrario, consulte
<http://www.gnu.org/licenses/lgpl.html>.
"""

# módulos que se usan en el cliente
import sys, requests, urllib, time, hashlib, hmac, json, base64
from .Market import Market
from .Currency import Currency

"""
Clase principal con el cliente de SURBTC
@author Esteban De La Fuente Rubio, DeLaF (esteban[at]sasco.cl)
@version 2017-11-26
"""
class Client:

    _url = 'https://www.buda.com' # URL base para las llamadas a la API
    _version = 'api/v2' # Versión de la API con la que funciona este SDK
    default_per = 300 # Límite por defecto a usar en consultas paginadas (se usa el máximo por defecto)
    api_key = None # API key para autenticación
    api_secret = None # API secret para autenticación
    response = None # Objeto con la respuesta del servicio web de SURBTC

    def __init__ (self, api_key = None, api_secret = None, test = False) :
        if api_key != None and api_secret != None :
            self.api_key = api_key
            self.api_secret = api_secret
        if test :
            self._url = 'https://stg.buda.com'

    def getMarket(self, market) :
        return Market(market, self)

    def getCurrency(self, currency) :
        return Currency(currency, self)

    def getMarkets (self) :
        url = self.createUrl('/markets')
        self.response = self.consume(url)
        body = self.response.json()
        if self.response.status_code != 200 :
            raise requests.ConnectionError('No fue posible obtener el listado de mercados: ' + body['message'])
        return body['markets']

    def getTicker (self, market = '') :
        url = self.createUrl('/markets/' + market + '/ticker')
        self.response = self.consume(url)
        body = self.response.json()
        if self.response.status_code != 200 :
            raise requests.ConnectionError('No fue posible obtener el ticker del mercado ' + market + ': ' + body['message'])
        return body['ticker']

    def getBook (self, market) :
        url = self.createUrl('/markets/' + market + '/order_book')
        self.response = self.consume(url)
        body = self.response.json()
        if self.response.status_code != 200 :
            raise requests.ConnectionError('No fue posible obtener el libro del mercado ' + market + ': ' + body['message'])
        return body['order_book']

    def getTrades (self, market, timestamp = None) :
        if timestamp == None :
            timestamp = time.time() - 60*60*24 # se solicita por defecto las últimas 24 horas
        url = self.createUrl('/markets/' + market + '/trades', {'timestamp': timestamp})
        self.response = self.consume(url)
        body = self.response.json()
        if self.response.status_code != 200 :
            raise requests.ConnectionError('No fue posible obtener los intercambios del mercado ' + market + ': ' + body['message'])
        return body['trades']

    def getOrders (self, market, state = None, minimun_exchanged = None, page = 1, per = None) :
        if per == None :
            per = self.default_per
        params = {'page': page, 'per': per}
        if state :
            params['state'] = state
        if minimun_exchanged :
            params['minimun_exchanged'] = minimun_exchanged
        url = self.createUrl('/markets/' + market + '/orders', params)
        self.response = self.consume(url)
        body = self.response.json()
        if self.response.status_code != 200 :
            raise requests.ConnectionError('No fue posible obtener las ordenes activas del mercado ' + market + ': ' + body['message'])
        return body['orders']

    def getBalance (self, currency = None) :
        if currency == None :
            url = self.createUrl('/balances')
        else :
            url = self.createUrl('/balances/' + currency)
        self.response = self.consume(url)
        body = self.response.json()
        if self.response.status_code != 200 :
            raise requests.ConnectionError('No fue posible obtener el balance de las billeteras: ' + body['message'])
        if currency == None :
            return body['balances']
        else :
            return body['balance']

    def createOrder (self, market, type, amount, limit = None, price_type = 'limit') :
        url = self.createUrl('/markets/' + market + '/orders')
        data = {'order': {'type': type, 'price_type': price_type, 'amount': amount}}
        if limit :
            data['order']['limit'] = limit
        self.response = self.consume(url, data)
        body = self.response.json()
        if self.response.status_code != 201 :
            raise requests.ConnectionError('No fue posible crear la orden en el mercado ' + market + ': ' + body['message'])
        return body['order']

    def getOrder (self, id) :
        url = self.createUrl('/orders/' + str(id))
        self.response = self.consume(url)
        body = self.response.json()
        if self.response.status_code != 200 :
            raise requests.ConnectionError('No fue posible obtener la orden ' + str(id) + ': ' + body['message'])
        return body['order']

    def cancelOrder (self, id) :
        url = self.createUrl('/orders/' + str(id))
        self.response = self.consume(url, {'state': 'canceling'}, method='PUT')
        body = self.response.json()
        if self.response.status_code != 200 :
            raise requests.ConnectionError('No fue posible cancelar la orden ' + id + ' en el mercado: ' + body['message'])
        return body['order']

    def getHistory (self, currency, type) :
        url = self.createUrl('/currencies/' + currency + '/' + type)
        self.response = self.consume(url)
        body = self.response.json()
        if self.response.status_code != 200 :
            raise requests.ConnectionError('No fue posible obtener el historial de ' + type + ' para ' + currency + ': ' + body['message'])
        return body[type]

    def getAddresses (self, currency) :
        url = self.createUrl('/currencies/' + currency + '/receive_addresses')
        self.response = self.consume(url)
        body = self.response.json()
        if self.response.status_code != 200 :
            raise requests.ConnectionError('No fue posible obtener el listado de direcciones para ' + currency + ': ' + body['message'])
        return body['receive_addresses']

    def createAddress (self, currency) :
        url = self.createUrl('/currencies/' + currency + '/receive_addresses')
        self.response = self.consume(url, {'receive_address':{}}, method='POST')
        body = self.response.json()
        if self.response.status_code != 201 :
            raise requests.ConnectionError('No fue posible crear una dirección para ' + currency + ': ' + body['message'])
        return body['receive_address']

    def getAddress (self, currency, id) :
        url = self.createUrl('/currencies/' + currency + '/receive_addresses/' + str(id))
        self.response = self.consume(url)
        body = self.response.json()
        if self.response.status_code != 200 :
            raise requests.ConnectionError('No fue posible obtener la dirección para ' + currency + ' con ID ' + str(id) + ': ' + body['message'])
        return body['receive_address']

    def deposit(self, currency, amount) :
        url = self.createUrl('/currencies/' + currency + '/deposits')
        data = {'deposit': {'amount': [amount, currency]}}
        self.response = self.consume(url, data)
        body = self.response.json()
        if self.response.status_code != 201 :
            raise requests.ConnectionError('No fue posible realizar el depósito de ' + str(amount) + ' '+ currency + ': ' + body['message'])
        return body['deposit']

    def withdrawal (self, currency, target_address, amount = None) :
        # si no hay monto se transfiere todo el balance
        if not amount :
            balance = self.getBalance(currency)
            amount = float(balance['available_amount'][0]) * 0.98 # WARNING: se saca el 98% del balance (falta saber cual es el máximo que se puede retirar)
        # realizar retiro
        url = self.createUrl('/currencies/' + currency + '/withdrawals')
        data = {'withdrawal': {'amount': amount, 'currency': currency, 'withdrawal_data': {'target_address': target_address} }}
        self.response = self.consume(url, data)
        body = self.response.json()
        if self.response.status_code != 201 :
            raise requests.ConnectionError('No fue posible realizar el retiro de ' + str(amount) + ' '+ currency + ' a la dirección ' + target_address + ': ' + body['message'])
        return body['withdrawal']

    def createUrl (self, recurso, params = None) :
        url = self._url + '/' + self._version + recurso
        if params == None :
            return url
        if sys.version_info[0] == 2 :
            query = urllib.urlencode(params)
        else :
            query = urllib.parse.urlencode(params)
        return '{0}?{1}'.format(url, query)

    def consume (self, url, data = None, method = None) :
        # definir método si no se indicó
        if method == None :
            method = 'POST' if data else 'GET'
        # preparar cabeceras
        if self.api_key != None and self.api_secret != None :
            timestamp = int(time.time() * 1E6)
            path = url.replace(self._url, '')
            msg = method + ' ' + path
            if data :
                data = json.dumps(data).encode('utf-8')
                msg += ' ' + base64.standard_b64encode(data).decode('utf-8')
            msg += ' ' + str(timestamp)
            if sys.version_info[0] == 2 :
                hashed = hmac.new(self.api_secret, msg, hashlib.sha384)
            else :
                hashed = hmac.new(bytes(self.api_secret, 'utf-8'), bytes(msg, 'utf-8'), hashlib.sha384)
            headers = {
                'X-SBTC-APIKEY': self.api_key,
                'X-SBTC-NONCE': str(timestamp),
                'X-SBTC-SIGNATURE': hashed.hexdigest(),
                'Content-Type': 'application/json'
            }
        else :
            headers = {}
        # método POST
        if method == 'POST' :
            return requests.post(url, data=data, headers=headers)
        # método PUT
        elif method == 'PUT' :
            return requests.put(url, data=data, headers=headers)
        # método GET
        else :
            return requests.get(url, headers=headers)
