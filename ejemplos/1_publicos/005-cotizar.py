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
Ejemplo para cotizar una cantidad de criptomoneda

Este ejemplo no utiliza credenciales para hacer la consulta, sin embargo se
recomienda usarlas ya que que al estar autenticado (api_key), los fee serán
el correspondiente al volumen transado. Si no (sin api_key), los fee serán
los máximos.

@author Esteban De La Fuente Rubio, DeLaF (esteban[at]sasco.cl)
@version 2018-04-24
"""

# credenciales
api_key = None
api_secret = None

# importar directamente del proyecto, sin instalar en el equipo, estas líneas no
# son necesarias cuando se instala con PIP el cliente, ya que en ese caso el
# módulo de surbtc quedará disponible en el sistema operativo
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# importar módulo del cliente
import surbtc

# crear cliente y mercado
Client = surbtc.Client(api_key, api_secret)
Market = Client.getMarket('ETH-CLP')

# cotizar BID de 1 ETH
print(Market.getBidQuote(1))

# cotizar ASK de 1 ETH
print(Market.getAskQuote(1))
