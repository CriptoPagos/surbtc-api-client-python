#!/usr/bin/python
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
Ejemplo para crear una dirección para depósito de criptomonedas
@link http://api.surbtc.com/#dep-sito-criptomonedas
@author Esteban De La Fuente Rubio, DeLaF (esteban[at]sasco.cl)
@version 2017-11-26
"""

# credenciales
api_key = ''
api_secret = ''

# importar directamente del proyecto, sin instalar en el equipo, estas líneas no
# son necesarias cuando se instala con PIP el cliente, ya que en ese caso el
# módulo de surbtc quedará disponible en el sistema operativo
import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

# importar módulo del cliente
import surbtc

# crear cliente y moneda
Client = surbtc.Client(api_key, api_secret)
Currency = Client.getCurrency('ETH')

# crear dirección para depósito
address = Currency.createAddress()
print(address)

# obtener dirección a partir del ID
time.sleep(3)
print (Currency.getAddress(address['id']))
