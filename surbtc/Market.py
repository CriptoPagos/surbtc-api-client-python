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

"""
Clase que representa un mercado genérico de SURBTC
@author Esteban De La Fuente Rubio, DeLaF (esteban[at]sasco.cl)
@version 2018-04-24
"""
class Market :

    _market = None # mercado para el cual se instanció el objeto
    client = None # Objeto que representa el cliente de la conexión a SURBTC

    def __init__ (self, market, Client = None) :
        self._market = market
        if Client != None :
            self.client = Client

    def getTicker (self) :
        return self.client.getTicker(self._market)

    def getBidQuote (self, amount) :
        return self.client.getQuote(self._market, amount, 'bid_given_size')

    def getAskQuote(self, amount) :
        return self.client.getQuote(self._market, amount, 'ask_given_size')

    def getBook (self) :
        return self.client.getBook(self._market)

    def getTrades (self, timestamp = None) :
        return self.client.getTrades(self._market, timestamp)

    def getOrders (self, state = None, minimun_exchanged = None, page = 1, per = None) :
        return self.client.getOrders(self._market, state, minimun_exchanged, page, per)

    def getReceivedOrders(self, minimun_exchanged = None, page = 1, per = None) :
        return self.client.getOrders(self._market, 'received', minimun_exchanged, page, per)

    def getPendingOrders(self, minimun_exchanged = None, page = 1, per = None) :
        return self.client.getOrders(self._market, 'pending', minimun_exchanged, page, per)

    def getTradedOrders(self, minimun_exchanged = None, page = 1, per = None) :
        return self.client.getOrders(self._market, 'traded', minimun_exchanged, page, per)

    def getCancelingOrders(self, minimun_exchanged = None, page = 1, per = None) :
        return self.client.getOrders(self._market, 'canceling', minimun_exchanged, page, per)

    def getCanceledOrders(self, minimun_exchanged = None, page = 1, per = None) :
        return self.client.getOrders(self._market, 'canceled', minimun_exchanged, page, per)

    def createBuyOrder (self, amount, limit = None, price_type = 'limit') :
        return self.client.createOrder(self._market, 'bid', amount, limit, price_type)

    def createSellOrder (self, amount, limit = None, price_type = 'limit') :
        return self.client.createOrder(self._market, 'ask', amount, limit, price_type)
