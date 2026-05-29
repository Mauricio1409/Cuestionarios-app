from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.subjects.models import Subject
from apps.quizzes.models import Quiz, Question, QuestionOption, QuestionType


SUBJECT_NAME = "Redes"
QUIZ_NAME = "1er Parcial Teórico Redes"


QUESTIONS = [
    {
        "statement": "Cuando utilizamos las redes de computadoras, encontramos distintos tipos de usos o aplicaciones para las mismas. (Elija dos)",
        "type": "multiple_choice",
        "options": [
            ("Usuarios fijos", True),
            ("Aplicaciones de negocios", True),
            ("Usuarios móviles", False),
            ("Procesamiento centralizado", False),
        ],
        "explanation": "Pregunta tomada de aPreguntas Teoricas Parcial 1 2 3.pdf, pág. 1.",
    },
    {
        "statement": "¿Cuál es la función de la máscara en una dirección IPv4?",
        "type": "single_choice",
        "options": [
            ("Determinar la porción de red", True),
            ("Determinar la dirección MAC", False),
            ("Determinar el protocolo de transporte", False),
            ("Determinar la puerta de enlace", False),
        ],
        "explanation": "Pregunta tomada de aPreguntas Teoricas Parcial 1 2 3.pdf, pág. 1.",
    },
    {
        "statement": "¿En qué capa del modelo OSI trabaja un switch?",
        "type": "single_choice",
        "options": [
            ("Física", False),
            ("Enlace de datos", True),
            ("Red", False),
            ("Transporte", False),
        ],
        "explanation": "Pregunta tomada de aPreguntas Teoricas Parcial 1 2 3.pdf, pág. 1.",
    },
    {
        "statement": "¿Cómo se determina la clase de una dirección IPv4?",
        "type": "single_choice",
        "options": [
            ("Por el valor del primer byte", True),
            ("Por la máscara de subred", False),
            ("Por la dirección MAC", False),
            ("Por el último octeto", False),
        ],
        "explanation": "Pregunta tomada de aPreguntas Teoricas Parcial 1 2 3.pdf, pág. 1.",
    },
    {
        "statement": "Hardware de la red. En las cuestiones técnicas en el diseño de red, existe la tecnología de transmisión que se utiliza mucho en la actualidad. (Elija dos)",
        "type": "multiple_choice",
        "options": [
            ("Punto a punto", True),
            ("Difusión", True),
            ("Token único", False),
            ("Circuito dedicado obligatorio", False),
        ],
        "explanation": "Pregunta tomada de aPreguntas Teoricas Parcial 1 2 3.pdf, pág. 2.",
    },
    {
        "statement": "¿En qué capa trabaja la placa de red?",
        "type": "single_choice",
        "options": [
            ("En la física y subcapa MAC", True),
            ("Solo en la capa de red", False),
            ("Solo en transporte", False),
            ("Aplicación", False),
        ],
        "explanation": "Pregunta tomada de aPreguntas Teoricas Parcial 1 2 3.pdf, pág. 2.",
    },
    {
        "statement": "¿Dónde encontraríamos las redes por el cableado eléctrico?",
        "type": "single_choice",
        "options": [
            ("LAN", True),
            ("WAN", False),
            ("PAN", False),
            ("MAN", False),
        ],
        "explanation": "Pregunta tomada de aPreguntas Teoricas Parcial 1 2 3.pdf, pág. 2.",
    },
    {
        "statement": "Ordene de menor a mayor la cobertura de las redes.",
        "type": "single_choice",
        "options": [
            ("PAN, LAN, MAN, WAN e Internet", True),
            ("LAN, PAN, MAN, WAN e Internet", False),
            ("WAN, MAN, LAN, PAN e Internet", False),
            ("Internet, WAN, MAN, LAN y PAN", False),
        ],
        "explanation": "Pregunta tomada de aPreguntas Teoricas Parcial 1 2 3.pdf, pág. 2.",
    },
    {
        "statement": "Teniendo la estructura N.N.H.H y necesito crear subredes minimizando la cantidad de subredes. ¿De dónde se piden prestados los bits?",
        "type": "single_choice",
        "options": [
            ("Del tercer octeto y de izquierda a derecha", True),
            ("Del primer octeto y de derecha a izquierda", False),
            ("Del cuarto octeto y de izquierda a derecha", False),
            ("De cualquier octeto indistintamente", False),
        ],
        "explanation": "Pregunta tomada de aPreguntas Teoricas Parcial 1 2 3.pdf, pág. 3.",
    },
    {
        "statement": "Un administrador de red tiene que configurar manualmente 5 puestos de trabajo de una red. Por error omitió poner la puerta de enlace en uno de ellos. ¿Se pueden comunicar entre ellas?",
        "type": "single_choice",
        "options": [
            ("Sí, todas se comunican entre ellas.", True),
            ("No, ninguna puede comunicarse.", False),
            ("Solo se comunica la PC sin puerta de enlace.", False),
            ("Solo se comunican si están en distintas redes.", False),
        ],
        "explanation": "La puerta de enlace no es necesaria para comunicarse dentro de la misma LAN. Fuente: aPreguntas Teoricas Parcial 1 2 3.pdf, pág. 3.",
    },
    {
        "statement": "¿Qué protocolos encontramos en la capa de aplicación del modelo TCP/IP? (Elija dos)",
        "type": "multiple_choice",
        "options": [
            ("SMTP", True),
            ("TELNET", True),
            ("IP", False),
            ("TCP", False),
        ],
        "explanation": "Pregunta tomada de aPreguntas Teoricas Parcial 1 2 3.pdf, pág. 3.",
    },
    {
        "statement": "¿Qué dispositivo divide dominios de colisión?",
        "type": "single_choice",
        "options": [
            ("Switch", True),
            ("Hub", False),
            ("Repetidor", False),
            ("Cable UTP", False),
        ],
        "explanation": "Pregunta tomada de aPreguntas Teoricas Parcial 1 2 3.pdf, pág. 3.",
    },
    {
        "statement": "Al trabajar en aplicaciones domésticas, encontramos un modelo que interactúan los dispositivos. ¿Cómo llamamos a este modelo?",
        "type": "single_choice",
        "options": [
            ("Cliente-Servidor", True),
            ("Punto a punto", False),
            ("De igual a igual", False),
            ("Ninguna de las opciones", False),
        ],
        "explanation": "Pregunta tomada de aPreguntas Teoricas Parcial 1 2 3.pdf, pág. 4.",
    },
    {
        "statement": "¿Cuántos bits tiene una dirección IPv4?",
        "type": "single_choice",
        "options": [
            ("32", True),
            ("8", False),
            ("48", False),
            ("64", False),
        ],
        "explanation": "Pregunta tomada de aPreguntas Teoricas Parcial 1 2 3.pdf, pág. 4.",
    },
    {
        "statement": "¿En qué capa del modelo OSI trabaja el puente?",
        "type": "single_choice",
        "options": [
            ("Física y enlace de datos", True),
            ("Solo física", False),
            ("Solo red", False),
            ("Transporte", False),
        ],
        "explanation": "Pregunta tomada de aPreguntas Teoricas Parcial 1 2 3.pdf, pág. 4.",
    },
    {
        "statement": "A un administrador de red le pidieron que instale una red inalámbrica en un edificio de cuatro pisos, para dar acceso a las 3 oficinas de cada piso. Decide instalar 4 AP para tener buena cobertura. ¿Cuántos ESS tiene esa arquitectura?",
        "type": "single_choice",
        "options": [
            ("1", True),
            ("4", False),
            ("12", False),
            ("48", False),
        ],
        "explanation": "Pregunta tomada de aPreguntas Teoricas Parcial 1 2 3.pdf, pág. 5.",
    },
    {
        "statement": "Se deben conectar tres edificios en un campus universitario. El edificio A está a 300 metros del B, C está a 250 metros del A y C está a 350 del B. ¿Cuál de las siguientes tecnologías se podría implementar?",
        "type": "single_choice",
        "options": [
            ("1000BASE-SX", True),
            ("100BASE-TX", False),
            ("10BASE-T", False),
            ("1000BASE-T", False),
        ],
        "explanation": "Pregunta tomada de aPreguntas Teoricas Parcial 1 2 3.pdf, pág. 5.",
    },
    {
        "statement": "Cuando utilizamos la conexión vía Bluetooth. ¿De qué tipo de red estamos hablando?",
        "type": "single_choice",
        "options": [
            ("PAN", True),
            ("LAN", False),
            ("MAN", False),
            ("WAN", False),
        ],
        "explanation": "Pregunta tomada de aPreguntas Teoricas Parcial 1 2 3.pdf, pág. 5.",
    },
    {
        "statement": "Un administrador de red necesita tener mucha velocidad en su LAN. ¿Qué técnica de conmutación deberá configurar en el switch?",
        "type": "single_choice",
        "options": [
            ("Cut-through", True),
            ("Almacenamiento y reenvío", False),
            ("Tabla CAM", False),
            ("Libre de fragmentos", False),
        ],
        "explanation": "Pregunta tomada de aPreguntas Teoricas Parcial 1 2 3.pdf, pág. 5.",
    },
    {
        "statement": "Un administrador de red desea garantizar que el switch conmute solo tramas correctas. Indique cuál de las siguientes técnicas deberá configurar:",
        "type": "single_choice",
        "options": [
            ("Almacenamiento y reenvío", True),
            ("Cut-through", False),
            ("Fast-switch", False),
            ("Tabla CAM", False),
            ("Libre de fragmentos", False),
        ],
        "explanation": "Pregunta repetida en varios PDFs; la respuesta marcada es almacenamiento y reenvío.",
    },
    {
        "statement": "Un switch de 24 bocas está conectado a un hub en el puerto 1, a otro hub en el puerto 2, a un router en el puerto 3 y a computadoras en el resto de los puertos. ¿Cuántos dominios de colisión existen?",
        "type": "single_choice",
        "options": [
            ("24", True),
            ("21", False),
            ("3", False),
            ("1", False),
        ],
        "explanation": "Pregunta tomada de aPreguntas Teoricas Parcial 1 2 3.pdf, pág. 6.",
    },
    {
        "statement": "¿Con qué direcciones se comunican los host dentro de una misma LAN?",
        "type": "single_choice",
        "options": [
            ("Direcciones MAC", True),
            ("Direcciones IP", False),
            ("Direcciones de puertos", False),
            ("Direcciones MAC e IP", False),
        ],
        "explanation": "Pregunta tomada de aPreguntas Teoricas Parcial 1 2 3.pdf, pág. 6.",
    },
    {
        "statement": "Dos máquinas de la misma red realizan una consulta fuera de su LAN. El primer paquete que llega al router es el de la máquina A y luego el de B, pero el router procesa primero el paquete de B y luego el de A. ¿En qué campo del datagrama IPv4 se fijó el router para realizar esa acción?",
        "type": "single_choice",
        "options": [
            ("Servicios Diferenciados", True),
            ("TTL", False),
            ("Versión", False),
            ("Protocolo", False),
        ],
        "explanation": "Pregunta tomada de aPreguntas Teoricas Parcial 1 2 3.pdf, pág. 7.",
    },
    {
        "statement": "¿Cómo se lleva a cabo la comunicación virtual en una arquitectura de protocolos entre las capas del mismo nivel?",
        "type": "single_choice",
        "options": [
            ("Horizontal", True),
            ("Vertical", False),
            ("De origen a destino", False),
            ("Ninguna de las anteriores", False),
        ],
        "explanation": "Pregunta tomada de aPreguntas Teoricas Parcial 1 2 3.pdf, pág. 7.",
    },
    {
        "statement": "Una persona vive en un pueblo y tiene su campo a 50 km de distancia; quiere controlar sus instalaciones vía internet. ¿Cuál de las siguientes tecnologías tendría que contratar?",
        "type": "single_choice",
        "options": [
            ("IEEE 802.16", True),
            ("IEEE 802.15", False),
            ("IEEE 802.5", False),
            ("WiFi", False),
        ],
        "explanation": "Pregunta tomada de aPreguntas Teoricas Parcial 1 2 3.pdf, pág. 7.",
    },
    {
        "statement": "¿A qué denominamos interfaz en una arquitectura de protocolos?",
        "type": "single_choice",
        "options": [
            ("Define las operaciones y servicios primitivos que pone la capa más baja a disposición de la capa superior inmediata", True),
            ("Define las aplicaciones del usuario", False),
            ("Define la capa física", False),
            ("Es el cable utilizado por la red", False),
        ],
        "explanation": "Pregunta tomada de aPreguntas Teoricas Parcial 1 2 3.pdf, pág. 8.",
    },
    {
        "statement": "¿Quién regula las telecomunicaciones internacionales?",
        "type": "single_choice",
        "options": [
            ("ITU", True),
            ("IEEE", False),
            ("IETF", False),
            ("ISO", False),
        ],
        "explanation": "Pregunta tomada de aPreguntas Teoricas Parcial 1 2 3.pdf, pág. 8.",
    },
    {
        "statement": "Al trabajar en aplicaciones de negocios, encontramos un modelo que interactúan los dispositivos. ¿Cómo llamamos a este modelo?",
        "type": "single_choice",
        "options": [
            ("Cliente-Servidor", True),
            ("Peer-to-peer", False),
            ("Punto a punto", False),
            ("De igual a igual", False),
        ],
        "explanation": "Pregunta tomada de aPreguntas Teoricas Parcial 1 2 3.pdf, pág. 9.",
    },
    {
        "statement": "¿Qué trama usa una estación de trabajo cuando quiere transmitir a otro puesto de trabajo utilizando CSMA/CA?",
        "type": "single_choice",
        "options": [
            ("RTS", True),
            ("CTS", False),
            ("ACK", False),
            ("RxBUSY", False),
        ],
        "explanation": "Pregunta tomada de aPreguntas Teoricas Parcial 1 2 3.pdf, pág. 9.",
    },
    {
        "statement": "¿Cuál de las siguientes características corresponde al protocolo IPv4?",
        "type": "single_choice",
        "options": [
            ("Es no orientado a conexión", True),
            ("Garantiza que los datos se entreguen ordenados en el destino", False),
            ("Encapsula una trama en un paquete", False),
            ("Utiliza direcciones de 48 bits", False),
        ],
        "explanation": "Pregunta tomada de aPreguntas Teoricas Parcial 1 2 3.pdf, pág. 9.",
    },
    {
        "statement": "¿Qué capa del modelo TCP/IP realiza la función de permitir que los host inyecten paquetes en cualquier red y que viajen de manera independiente hacia el destino?",
        "type": "single_choice",
        "options": [
            ("Interred", True),
            ("Transporte", False),
            ("Aplicación", False),
            ("Sesión", False),
        ],
        "explanation": "Pregunta tomada de aPreguntas Teoricas Parcial 1 2 3.pdf, pág. 9.",
    },
    {
        "statement": "Cuando se necesita un estándar, se discutía y después anunciaban el o los cambios formalmente. La comunicación se llevaba a cabo por informes técnicos llamados:",
        "type": "single_choice",
        "options": [
            ("RFC", True),
            ("Normas técnicas", False),
            ("OSI", False),
            ("ITU", False),
        ],
        "explanation": "Pregunta tomada de aPreguntas Teoricas Parcial 1 2 3.pdf, pág. 10.",
    },
    {
        "statement": "Un empleado en el primer piso le envía un mail a su supervisor que está en el cuarto piso. El primero usa una notebook conectada a un AP y el segundo una PC conectada a un switch. ¿Qué servicio está realizando el DS?",
        "type": "single_choice",
        "options": [
            ("Integración", True),
            ("Asociación", False),
            ("Distribución", False),
            ("Disociación", False),
        ],
        "explanation": "Pregunta tomada de aPreguntas Teoricas Parcial 1 2 3.pdf, pág. 10.",
    },
    {
        "statement": "¿Qué información se almacena en la tabla CAM?",
        "type": "single_choice",
        "options": [
            ("Puertos y MAC", True),
            ("Puertos y direcciones IP", False),
            ("MAC y direcciones IP", False),
            ("Ninguna de las opciones", False),
        ],
        "explanation": "Pregunta tomada de aPreguntas Teoricas Parcial 1 2 3.pdf, pág. 10.",
    },
    {
        "statement": "A un administrador de red le propusieron que configurara sumarización de rutas en el router. ¿Qué beneficio tiene?",
        "type": "single_choice",
        "options": [
            ("Reduce el tamaño de las tablas de encaminamiento", True),
            ("Tiene más opciones al router de elegir rutas", False),
            ("No necesita consultas estáticas", False),
            ("Se configuran automáticamente en el router", False),
        ],
        "explanation": "Pregunta tomada de aPreguntas Teoricas Parcial 1 2 3.pdf, pág. 10.",
    },
    {
        "statement": "¿Cómo sería la secuencia de encapsulamiento en el modelo TCP/IP?",
        "type": "single_choice",
        "options": [
            ("Datos, segmentos, paquetes, tramas y tren de bits", True),
            ("Datos, paquetes, segmentos, tramas y tren de bits", False),
            ("Tramas, paquetes, segmentos, datos y bits", False),
            ("Datos, segmentos, tren de bits y tramas", False),
        ],
        "explanation": "Pregunta tomada de aPreguntas Teoricas Parcial 1 2 3.pdf, pág. 11.",
    },
    {
        "statement": "¿Con qué direcciones trabaja el puente?",
        "type": "single_choice",
        "options": [
            ("MAC", True),
            ("IP", False),
            ("Puertos", False),
            ("Ninguna de las opciones", False),
        ],
        "explanation": "Pregunta tomada de aPreguntas Teoricas Parcial 1 2 3.pdf, pág. 11.",
    },
    {
        "statement": "Se necesita configurar 3 hosts con direcciones IP que puedan ser enrutadas a través de Internet. ¿Cuáles de las siguientes direcciones cumplen con lo solicitado?",
        "type": "multiple_choice",
        "options": [
            ("181.0.0.1", True),
            ("172.64.12.0", True),
            ("198.234.255.95", True),
            ("172.16.223.125", False),
            ("192.168.23.252", False),
            ("10.172.13.65", False),
        ],
        "explanation": "Pregunta tomada de Primer Parcial Teórico 4k4 2020 Merge.pdf, págs. 5 y 15.",
    },
    {
        "statement": "¿Cuál es la máxima tasa de bits a la que funcionará una LAN tipo Ethernet si el switch tiene 24 puertos de 1 Gb/s, dos puertos de fibra óptica de 10 Gb/s, cableado certificado categoría 6 y placas de red Fast Ethernet?",
        "type": "single_choice",
        "options": [
            ("100 Mb/s", True),
            ("1 Gb/s", False),
            ("2,4 Gb/s", False),
            ("22,4 Gb/s", False),
            ("24 Gb/s", False),
        ],
        "explanation": "La velocidad queda limitada por las placas Fast Ethernet. Fuente: Primer Parcial Teórico 4k4 2020 Merge.pdf, pág. 6.",
    },
    {
        "statement": "Una WLAN es una red: (seleccione las correctas)",
        "type": "multiple_choice",
        "options": [
            ("Inalámbrica", True),
            ("De difusión", True),
            ("Utiliza el protocolo CSMA/CA", True),
            ("WAN", False),
            ("Full Dúplex", False),
            ("Símplex", False),
        ],
        "explanation": "Pregunta tomada de Primer Parcial Teórico 4k4 2020 Merge.pdf, pág. 7.",
    },
    {
        "statement": "Si una estación de trabajo se encuentra a 180 mts del armario principal de la red:",
        "type": "single_choice",
        "options": [
            ("Podré colocar un switch en un punto intermedio para repetir la señal", True),
            ("Podré empalmar dos cables UTP de largo normalizado de 90 mts", False),
            ("Deberé ubicar a la estación de trabajo en otra VLAN", False),
            ("Reemplazaré el cable UTP por coaxil para conectar la PC al switch", False),
        ],
        "explanation": "Pregunta tomada de Primer Parcial Teórico 4k4 2020 Merge.pdf, pág. 13.",
    },
    {
        "statement": "Los mensajes ICMP se envían utilizando el encabezado IP básico.",
        "type": "single_choice",
        "options": [
            ("Verdadero", True),
            ("Falso", False),
        ],
        "explanation": "Pregunta tomada de Primer Parcial Teórico 4k4 2020 Merge.pdf, pág. 14.",
    },
    {
        "statement": "Identifique las distintas tecnologías de LAN.",
        "type": "multiple_choice",
        "options": [
            ("Red empresarial implementada con tecnología cableada → Ethernet", True),
            ("Red de campus universitario implementada con tecnología inalámbrica → Wi-Fi", True),
            ("Red empresarial implementada con tecnología cableada → Wi-Fi", False),
            ("Red de campus universitario implementada con tecnología inalámbrica → Wi-Max", False),
        ],
        "explanation": "Pregunta tomada de Primer Parcial Teórico 4k4 2020 Merge.pdf, pág. 14.",
    },
    {
        "statement": "Si hablamos de Internet, podemos decir que es una red:",
        "type": "multiple_choice",
        "options": [
            ("Conmutada por paquetes", True),
            ("Tolerante a fallas", True),
            ("Posee amplia cobertura geográfica", True),
            ("Basada en protocolos normalizados y públicos", True),
            ("Conmutada por circuitos", False),
            ("Basada en protocolos propietarios limitados", False),
        ],
        "explanation": "Pregunta tomada de Primer Parcial Teórico 4k4 2020 Merge.pdf, pág. 9.",
    },
    {
        "statement": "La red del campus de la UTN Facultad Regional Córdoba es una red MAN.",
        "type": "single_choice",
        "options": [
            ("Falso", True),
            ("Verdadero", False),
        ],
        "explanation": "Pregunta tomada de Primer Parcial Teórico 4k4 2020 Merge.pdf, pág. 19.",
    },
    {
        "statement": "Un administrador de red ha subneteado la red 172.16.0.0 usando la máscara 255.255.255.224. Accidentalmente duplicó la IP 172.16.2.121 en 2 equipos de la misma subred. ¿Cuál IP podría asignarse en reemplazo?",
        "type": "single_choice",
        "options": [
            ("172.16.2.100", True),
            ("172.16.2.127", False),
            ("172.16.2.128", False),
            ("172.16.2.64", False),
            ("172.16.1.80", False),
        ],
        "explanation": "Pregunta tomada de Primer Parcial Teórico 4k4 2020 Merge.pdf, pág. 19.",
    },
    {
        "statement": "Se dice que un ____ es un tipo de ____ porque interconecta redes cableadas que funcionan con el protocolo ____ con dispositivos inalámbricos que ejecutan ____.",
        "type": "multiple_choice",
        "options": [
            ("Access Point → Bridge → IEEE 802.3 → IEEE 802.11", True),
            ("Router → Bridge → PPP → IEEE 802.15", False),
            ("Switch → Router → IEEE 802.5 → IEEE 802.11", False),
            ("Access Point → Multiplexor → RS232-C → IEEE 802.3", False),
        ],
        "explanation": "Pregunta tomada de Primer Parcial Teórico 4k4 2020 Merge.pdf, pág. 20.",
    },
    {
        "statement": "Su ISP le asignó un espacio completo de clase C públicas. Debe armar 3 subredes que soporten 60 hosts cada una. ¿Cuáles son direcciones de red válidas?",
        "type": "multiple_choice",
        "options": [
            ("193.16.2.0", True),
            ("193.16.2.64", True),
            ("193.16.2.128", True),
            ("192.16.2.127", False),
            ("195.16.2.65", False),
            ("255.255.255.192", False),
        ],
        "explanation": "Pregunta tomada de Primer Parcial Teórico 4k4 2020 Merge.pdf, pág. 12.",
    },
    {
        "statement": "Su ISP le asignó un espacio completo de clase C públicas. Debe armar 3 subredes que soporten 60 hosts cada una. ¿Cuáles son direcciones de host válidas?",
        "type": "multiple_choice",
        "options": [
            ("193.16.2.1", True),
            ("193.16.2.65", True),
            ("193.16.2.120", True),
            ("192.16.2.65", False),
            ("255.255.255.192", False),
            ("255.255.255.224", False),
        ],
        "explanation": "Pregunta tomada de Primer Parcial Teórico 4k4 2020 Merge.pdf, pág. 20.",
    },
    {
        "statement": "Si tuviera que intercambiar datos entre un teléfono celular móvil y una PC con placas Ethernet y Wi-Fi, sin conexión a Internet en la oficina, lo podría hacer por:",
        "type": "multiple_choice",
        "options": [
            ("Wi-Fi", True),
            ("Bluetooth", True),
            ("Cable de red cruzado", False),
            ("Un switch", False),
            ("Ethernet", False),
        ],
        "explanation": "Pregunta tomada de Primer Parcial Teórico 4k4 2020 Merge.pdf, pág. 22.",
    },
    {
        "statement": "¿Cuándo un router descarta un paquete IP?",
        "type": "single_choice",
        "options": [
            ("Cuando su TTL llega a cero", True),
            ("Cuando su TTL llegó a 255", False),
            ("Cuando no trae la máscara de subred", False),
            ("Cuando el campo ToS no está marcado", False),
        ],
        "explanation": "Pregunta tomada de Primer Parcial Teórico 4k4 2020 Merge.pdf, pág. 23.",
    },
    {
        "statement": "La ARPANET estaba montada sobre una red de:",
        "type": "single_choice",
        "options": [
            ("Conmutación de paquetes", True),
            ("Conmutación de circuitos", False),
            ("Conmutación de celdas", False),
            ("Retransmisión de tramas", False),
        ],
        "explanation": "Pregunta tomada de Primer Parcial Teórico 4k4 2020 Merge.pdf, pág. 25.",
    },
    {
        "statement": "Indique los números de estándares IEEE que se corresponden con las siguientes tecnologías.",
        "type": "multiple_choice",
        "options": [
            ("Wi-Max → IEEE 802.16", True),
            ("Token Ring → IEEE 802.5", True),
            ("Bluetooth → IEEE 802.15", True),
            ("Wi-Fi → IEEE 802.11", True),
            ("Ethernet → IEEE 802.3", True),
            ("Ethernet → IEEE 802.16", False),
        ],
        "explanation": "Pregunta tomada de Primer Parcial Teórico 4k4 2020 Merge.pdf, pág. 28.",
    },
    {
        "statement": "El protocolo IP ____ prevé mecanismos de control de flujo extremo a extremo, como tampoco ____ de los mensajes, dejando estas funciones en protocolos de la capa de ____.",
        "type": "multiple_choice",
        "options": [
            ("NO → Secuenciación → Transporte", True),
            ("SÍ → Tipo de servicio → Red", False),
            ("NO → Tamaño máximo → Física", False),
            ("SÍ → Secuenciación → Acceso a Red", False),
        ],
        "explanation": "Pregunta tomada de Primer Parcial Teórico 4k4 2020 Merge.pdf, pág. 29.",
    },
    {
        "statement": "¿Cuál es el rango de direcciones privadas definidas en el RFC 1918? (Seleccione todas las aplicables)",
        "type": "multiple_choice",
        "options": [
            ("10.0.0.0 hasta 10.255.255.255", True),
            ("172.16.0.0 hasta 172.31.255.255", True),
            ("192.168.0.0 hasta 192.168.255.255", True),
            ("127.0.0.0 hasta 127.255.255.255", False),
            ("224.0.0.0 hasta 239.255.255.255", False),
        ],
        "explanation": "Pregunta tomada de Primer Parcial Teórico 4k4 2020 Merge.pdf, pág. 30.",
    },
    {
        "statement": "Indique cuáles de los siguientes son modos de funcionamiento de Access Point doméstico.",
        "type": "multiple_choice",
        "options": [
            ("Modo Access Point/Bridge", True),
            ("Modo repetidor", True),
            ("Modo Router", True),
            ("Modo Token Ring", False),
            ("Modo Frame Relay", False),
        ],
        "explanation": "Pregunta tomada de Primer Parcial Teórico 4k4 2020 Merge.pdf, pág. 30.",
    },
    {
        "statement": "Viendo una captura de tráfico con Wireshark realizada desde un host de una LAN, podemos afirmar que: (falta imagen - archivo: Primer Parcial Terórico 4k4 2020 Merge.pdf - página 31)",
        "type": "multiple_choice",
        "options": [
            ("El host poseía una configuración IP asignada dinámicamente por un servidor y la liberó", True),
            ("El host gestionó dinámicamente una nueva configuración con un servidor", True),
            ("El servidor de configuración IP está en la propia LAN", True),
            ("El administrador otorgó manualmente al host una nueva configuración", False),
            ("El servidor DHCP está en Internet", False),
        ],
        "explanation": "Requiere ver la captura de Wireshark. Fuente: Primer Parcial Teórico 4k4 2020 Merge.pdf, pág. 31.",
    },
    {
        "statement": "Es utilizado para enviar mensajes de error e información operativa, como por ejemplo:",
        "type": "multiple_choice",
        "options": [
            ("Un host no puede ser localizado", True),
            ("Un datagrama ya pasó por varios routers y al no encontrar el destino debe ser descartado", True),
            ("Un router avisa al host origen de algún problema en el procesamiento del datagrama", True),
            ("Un router no tiene suficiente espacio en memoria para alojar el datagrama y debe descartarlo", True),
            ("El destino recibió un paquete duplicado", False),
        ],
        "explanation": "Pregunta sobre ICMP tomada de Primer Parcial Teórico 4k4 2020 Merge.pdf, pág. 34.",
    },
    {
        "statement": "Un paquete para su correcta transmisión se divide en 3 fragmentos. ¿Cuál de las siguientes afirmaciones es correcta con respecto al protocolo IPv4?",
        "type": "single_choice",
        "options": [
            ("Todos los fragmentos tendrán el mismo origen, destino, protocolo e identificación", True),
            ("Todos los fragmentos tendrán distinto protocolo", False),
            ("Todos los fragmentos tendrán distinto origen y destino", False),
            ("Todos los fragmentos tendrán la misma suma de verificación", False),
        ],
        "explanation": "Pregunta tomada de 1º Parcial RIN - Preguntas.pdf, pág. 1.",
    },
    {
        "statement": "Si el tamaño de una trama inalámbrica es de 1554 bytes, determine la carga útil (datos) en el paquete IPv4.",
        "type": "single_choice",
        "options": [
            ("1500 bytes", True),
            ("1520 bytes", False),
            ("1480 bytes", False),
            ("Es una trama inválida", False),
        ],
        "explanation": "Pregunta tomada de 1º Parcial RIN - Preguntas.pdf, pág. 1.",
    },
    {
        "statement": "Dos dispositivos están separados entre sí por 8 routers. ¿Cuántas veces se calculará el algoritmo de la suma de verificación de un paquete IPv4?",
        "type": "single_choice",
        "options": [
            ("18", True),
            ("16", False),
            ("8", False),
            ("20", False),
        ],
        "explanation": "Pregunta tomada de Parcial REDES.pdf, pág. 3 y 1º Parcial RIN - Preguntas.pdf, pág. 2.",
    },
    {
        "statement": "Una trama Ethernet contiene en su carga útil (datos):",
        "type": "single_choice",
        "options": [
            ("Cabecera de la capa de red, cabecera de la capa de transporte y datos de la capa de aplicación", True),
            ("Datos de la capa de aplicación solamente", False),
            ("Cabecera de la capa de enlace y datos de aplicación", False),
            ("Cabecera de la capa física", False),
        ],
        "explanation": "Pregunta tomada de 1º Parcial RIN - Preguntas.pdf, pág. 4.",
    },
    {
        "statement": "Un usuario se queja de que la velocidad de su PC en la red es inapropiada, por ello el administrador decide actualizar la placa de red de la PC de 100 Mb/s a 1 Gb/s. ¿Qué es correcto?",
        "type": "multiple_choice",
        "options": [
            ("La velocidad de la placa será de 1000 Mbps", True),
            ("La PC tendrá otra dirección MAC", True),
            ("La velocidad ahora será 100 veces más rápida", False),
            ("Debe actualizarse la dirección IPv4 de la PC", False),
        ],
        "explanation": "Pregunta tomada de 1º Parcial RIN - Preguntas.pdf, pág. 5.",
    },
    {
        "statement": "Un router posee dos interfaces FastEthernet y una interfaz serial. Si recibe por una interfaz FastEthernet un paquete de 1000 bytes y debe encaminarlo a la interfaz serial cuya MTU es de 1500 bytes, ¿qué deberá hacer?",
        "type": "single_choice",
        "options": [
            ("Encapsular dicho paquete en una trama", True),
            ("Descartar siempre el paquete", False),
            ("Dividir el paquete en dos fragmentos", False),
            ("Descartar el paquete solo si el MF está activo", False),
        ],
        "explanation": "Pregunta tomada de 1º Parcial RIN - Preguntas.pdf, pág. 5.",
    },
    {
        "statement": "Determine a partir de la topología cuáles afirmaciones son correctas. (falta imagen - archivo: 1º Parcial RIN - Preguntas.pdf - página 6)",
        "type": "multiple_choice",
        "options": [
            ("Existen dos dominios de broadcast", True),
            ("Existen 6 dominios de colisión", True),
            ("Existe un dominio de broadcast", False),
            ("Existen 3 dominios de broadcast", False),
        ],
        "explanation": "Requiere ver la topología. Fuente: 1º Parcial RIN - Preguntas.pdf, pág. 6.",
    },
    {
        "statement": "Un router recibe por una de sus interfaces un paquete cuya dirección destino es 255.255.255.255. ¿Qué hará el router con dicho paquete?",
        "type": "single_choice",
        "options": [
            ("Lo descarta", True),
            ("Lo retransmite por todas sus interfaces", False),
            ("Se lo envía a todas las PC de la LAN", False),
            ("Lo encapsula en una trama", False),
        ],
        "explanation": "Pregunta tomada de Parcial REDES.pdf, pág. 3.",
    },
    {
        "statement": "¿Cuál de las siguientes es una organización voluntaria que emite estándares internacionales en cualquier ámbito científico y tecnológico?",
        "type": "single_choice",
        "options": [
            ("ISO", True),
            ("ITU", False),
            ("IEEE", False),
            ("IAB", False),
        ],
        "explanation": "Pregunta tomada de 1º Parcial RIN - Preguntas.pdf, pág. 8.",
    },
    {
        "statement": "Teniendo en cuenta la arquitectura TCP/IP, determine cuál de sus capas recibe paquetes, los encapsula y los entrega a dispositivos conectados a la misma red.",
        "type": "single_choice",
        "options": [
            ("Host a red", True),
            ("Interred", False),
            ("Transporte", False),
            ("Aplicación", False),
        ],
        "explanation": "Pregunta tomada de 1º Parcial RIN - Preguntas.pdf, pág. 9.",
    },
    {
        "statement": "Las tecnologías Ethernet, FastEthernet y GigaEthernet ejecutan funciones de las siguientes capas:",
        "type": "single_choice",
        "options": [
            ("Capa física y subcapa MAC de la capa de enlace", True),
            ("Capa física, capa de enlace y capa de red", False),
            ("Capa física y subcapa LLC de la capa de enlace", False),
            ("Capa física y capa de enlace", False),
        ],
        "explanation": "Pregunta tomada de Parcial REDES.pdf, pág. 4 y 1º Parcial RIN - Preguntas.pdf, pág. 10.",
    },
    {
        "statement": "Si se realiza un AND booleano entre una dirección IPv4 de una PC y una máscara de subred, se obtiene como resultado:",
        "type": "single_choice",
        "options": [
            ("La dirección de la subred a la cual pertenece la PC", True),
            ("La máscara de red", False),
            ("La dirección MAC de la PC", False),
            ("La clase a la cual pertenece la dirección IP", False),
        ],
        "explanation": "Pregunta tomada de 1º Parcial RIN - Preguntas.pdf, pág. 10.",
    },
    {
        "statement": "Los estándares desarrollados para redes LAN son definidos y administrados por una serie de autoridades reconocidas, entre las cuales se incluye:",
        "type": "single_choice",
        "options": [
            ("IEEE", True),
            ("IBM", False),
            ("Ethernet", False),
            ("IXP", False),
        ],
        "explanation": "Pregunta tomada de 1º Parcial RIN - Preguntas.pdf, pág. 12.",
    },
    {
        "statement": "Un switch de 24 bocas está conectado a un hub en el puerto 1, a un router en el puerto 2 y a computadoras en el resto de los puertos. Determine cuántos dominios de broadcast existen:",
        "type": "single_choice",
        "options": [
            ("1", True),
            ("2", False),
            ("3", False),
            ("24", False),
        ],
        "explanation": "Pregunta tomada de Parcial REDES.pdf, pág. 2 y 1º Parcial RIN - Preguntas.pdf, pág. 13.",
    },
    {
        "statement": "Determine cuáles de las siguientes direcciones IPv4 se podrían utilizar para que una computadora tenga conectividad en Internet. (Seleccione tres)",
        "type": "multiple_choice",
        "options": [
            ("172.32.60.90", True),
            ("11.10.10.10", True),
            ("194.168.10.6", True),
            ("10.10.12.14", False),
            ("172.29.0.90", False),
            ("192.168.32.48", False),
        ],
        "explanation": "Pregunta tomada de Parcial REDES.pdf, pág. 2 y 1º Parcial RIN - Preguntas.pdf, pág. 13.",
    },
    {
        "statement": "Indique cuál es el rango de direcciones IPv4 válidas de la subred 170.62.32.0/22:",
        "type": "single_choice",
        "options": [
            ("170.62.32.1 - 170.62.35.254", True),
            ("170.62.32.1 - 170.62.33.254", False),
            ("170.62.32.1 - 170.62.39.254", False),
            ("170.62.33.1 - 170.62.35.254", False),
        ],
        "explanation": "Pregunta tomada de 1º Parcial RIN - Preguntas.pdf, pág. 14.",
    },
    {
        "statement": "El prefijo /28 equivale a cuál de las siguientes máscaras de subred:",
        "type": "single_choice",
        "options": [
            ("255.255.255.240", True),
            ("255.255.255.248", False),
            ("255.255.255.224", False),
            ("255.255.248.0", False),
        ],
        "explanation": "Pregunta tomada de Parcial REDES.pdf, pág. 3 y 1º Parcial RIN - Preguntas.pdf, pág. 14.",
    },
    {
        "statement": "¿Cuáles de las siguientes afirmaciones describen el campo suma de verificación del protocolo IPv4? (Seleccione dos)",
        "type": "multiple_choice",
        "options": [
            ("Se calcula en el origen, el destino y dos veces en cada router", True),
            ("Permite detectar errores en la cabecera del paquete IPv4", True),
            ("Se utiliza para garantizar la integridad de todo el paquete IPv4", False),
            ("Lo calculan solo los routers para saber si encaminar o descartar el paquete", False),
        ],
        "explanation": "Pregunta tomada de Parcial REDES.pdf, pág. 1.",
    },
    {
        "statement": "Teniendo en cuenta la arquitectura TCP/IP, determine cuál de sus capas permite la comunicación de datos entre máquinas sobre una red de conmutación de paquetes, transportando la información de manera independiente:",
        "type": "single_choice",
        "options": [
            ("Interred", True),
            ("Transporte", False),
            ("Aplicación", False),
            ("Host a Red", False),
        ],
        "explanation": "Pregunta tomada de 1º Parcial RIN - Preguntas.pdf, pág. 15.",
    },
    {
        "statement": "Al administrador de red de una organización el ISP le asignó una dirección IPv4 pública clase B. Si se van a conectar como máximo 28 hosts por subred y se desea maximizar la cantidad de subredes:",
        "type": "single_choice",
        "options": [
            ("Se dejarán 5 bits para la parte de host y el prefijo de la máscara será /27", True),
            ("Se tomarán prestados 4 bits de la parte de host y el prefijo será /20", False),
            ("Se tomarán prestados 5 bits de la parte de red y el prefijo será /21", False),
            ("Se pedirán prestados 5 bits de la parte de host y el prefijo será /21", False),
        ],
        "explanation": "Pregunta tomada de Parcial REDES.pdf, pág. 4 y 1º Parcial RIN - Preguntas.pdf, pág. 15.",
    },
    {
        "statement": "El campo de la trama Ethernet que permite verificar la integridad de la trama es:",
        "type": "single_choice",
        "options": [
            ("Secuencia de verificación de trama (CRC o FCS)", True),
            ("Preámbulo", False),
            ("Tipo", False),
            ("Ninguno porque Ethernet no es fiable", False),
        ],
        "explanation": "Pregunta tomada de Cuestionario 1er Parcial RIN TEÓRICO.pdf, pág. 2.",
    },
    {
        "statement": "Una placa de red recibe una trama desde el medio de transmisión. Realiza el cálculo del CRC y el resultado no coincide con el valor que viene en dicha trama. ¿Qué hace la placa?",
        "type": "single_choice",
        "options": [
            ("Descarta la trama", True),
            ("Desencapsula la trama y la entrega a la capa superior", False),
            ("Pide retransmisión al origen", False),
            ("Descarta la trama e informa al origen", False),
        ],
        "explanation": "Pregunta tomada de Cuestionario 1er Parcial RIN TEÓRICO.pdf, pág. 2.",
    },
    {
        "statement": "Los Request for Comments (RFC) son:",
        "type": "single_choice",
        "options": [
            ("Documentos técnicos que describen el funcionamiento de los protocolos de Internet", True),
            ("Documentos técnicos establecidos por IEEE", False),
            ("Bases de datos que asocian dominios con direcciones IP", False),
            ("Estándares que definen la arquitectura de un sistema operativo", False),
        ],
        "explanation": "Pregunta tomada de Cuestionario 1er Parcial RIN TEÓRICO.pdf, pág. 3.",
    },
    {
        "statement": "Si el tamaño de una trama de Ethernet es de 1458 bytes, determine la carga útil (datos) en el paquete IPv4:",
        "type": "single_choice",
        "options": [
            ("1420 bytes", True),
            ("1440 bytes", False),
            ("1428 bytes", False),
            ("1400 bytes", False),
        ],
        "explanation": "Se resta encabezado Ethernet mínimo y cabecera IPv4. Fuente: Cuestionario 1er Parcial RIN TEÓRICO.pdf, pág. 3.",
    },
    {
        "statement": "Un mensaje ARP-reply se encapsula en:",
        "type": "single_choice",
        "options": [
            ("Una trama con dirección destino unicast", True),
            ("Un paquete con dirección destino 255.255.255.255", False),
            ("Una trama con dirección destino multicast", False),
            ("Una trama con dirección destino FF:FF:FF:FF:FF:FF", False),
        ],
        "explanation": "Pregunta tomada de Cuestionario 1er Parcial RIN TEÓRICO.pdf, pág. 3.",
    },
    {
        "statement": "La dirección MAC destino en una trama enviada desde una PC que está arrancando hacia un servidor DHCP es:",
        "type": "single_choice",
        "options": [
            ("FF-FF-FF-FF-FF-FF", True),
            ("0.0.0.0", False),
            ("Dirección IP del servidor DHCP", False),
            ("255.255.255.255", False),
        ],
        "explanation": "Pregunta tomada de Cuestionario 1er Parcial RIN TEÓRICO.pdf, pág. 5.",
    },
    {
        "statement": "Las tablas ARP:",
        "type": "single_choice",
        "options": [
            ("Pueden tener entradas dinámicas y estáticas", True),
            ("Tienen solo entradas dinámicas", False),
            ("Poseen solo entradas estáticas", False),
            ("Necesitan configuración de las entradas dinámicas", False),
        ],
        "explanation": "Pregunta tomada de Cuestionario 1er Parcial RIN TEÓRICO.pdf, pág. 5.",
    },
    {
        "statement": "¿Cuál protocolo permite que una PC obtenga una dirección IPv4 a partir de su dirección MAC, configurando tablas con mapas estáticos y permanentes en el servidor y requiriendo que la PC esté en la misma LAN que el servidor?",
        "type": "single_choice",
        "options": [
            ("Reverse Address Resolution Protocol", True),
            ("Address Resolution Protocol", False),
            ("Bootstrap Protocol", False),
            ("DHCP versión 6", False),
        ],
        "explanation": "Pregunta tomada de Cuestionario 1er Parcial RIN TEÓRICO.pdf, pág. 5.",
    },
    {
        "statement": "Si se quiere que una trama sea procesada por todos los dispositivos de una determinada LAN, la dirección de destino será:",
        "type": "single_choice",
        "options": [
            ("FF:FF:FF:FF:FF:FF", True),
            ("255.255.255.255", False),
            ("127.0.0.1", False),
            ("01:00:5E:98:76:54", False),
        ],
        "explanation": "Pregunta tomada de Cuestionario 1er Parcial RIN TEÓRICO.pdf, pág. 6.",
    },
    {
        "statement": "Dada la dirección de subred 189.45.8.0/25, determine cuál es un rango de direcciones válidas:",
        "type": "single_choice",
        "options": [
            ("189.45.8.1 - 189.45.8.126", True),
            ("189.45.8.1 - 189.45.8.254", False),
            ("189.45.8.0 - 189.45.8.255", False),
            ("189.45.8.1 - 189.45.11.254", False),
        ],
        "explanation": "Pregunta tomada de Cuestionario 1er Parcial RIN TEÓRICO.pdf, pág. 6.",
    },
    {
        "statement": "Una PC tiene que enviar un archivo de 5 Kbytes a través de Fast Ethernet. Si desea maximizar el uso de la MTU, enviará:",
        "type": "single_choice",
        "options": [
            ("4 tramas", True),
            ("1 trama", False),
            ("2 tramas", False),
            ("5 tramas", False),
        ],
        "explanation": "Ethernet permite transportar como máximo 1500 bytes de carga útil. Fuente: Cuestionario 1er Parcial RIN TEÓRICO.pdf, pág. 7.",
    },
    {
        "statement": "¿Qué significa un ping exitoso a la dirección IPv6 ::1?",
        "type": "single_choice",
        "options": [
            ("Los protocolos TCP/IP están instalados correctamente", True),
            ("La dirección de enlace local está bien configurada", False),
            ("El gateway está configurado correctamente", False),
            ("El switch funciona correctamente", False),
        ],
        "explanation": "Pregunta tomada de Cuestionario 1er Parcial RIN TEÓRICO.pdf, pág. 7.",
    },
    {
        "statement": "El ISP le asigna a una empresa la IP 190.45.96.0/22. Ello implica que se dispone de:",
        "type": "single_choice",
        "options": [
            ("1022 direcciones de hosts válidas", True),
            ("1024 direcciones de hosts válidas", False),
            ("510 direcciones de hosts válidas", False),
            ("2046 direcciones de hosts válidas", False),
        ],
        "explanation": "Pregunta tomada de Cuestionario 1er Parcial RIN TEÓRICO.pdf, pág. 7.",
    },
    {
        "statement": "El ISP le asigna a una empresa la IP 190.45.96.0/23. Ello implica que se dispone de:",
        "type": "single_choice",
        "options": [
            ("510 direcciones de hosts válidas", True),
            ("512 direcciones de hosts válidas", False),
            ("1022 direcciones de hosts válidas", False),
            ("256 direcciones de hosts válidas", False),
        ],
        "explanation": "Pregunta tomada de Cuestionario 1er Parcial RIN TEÓRICO.pdf, pág. 7.",
    },
    {
        "statement": "¿Cuál de las siguientes clasificaciones de redes es decreciente con respecto al área de cobertura?",
        "type": "single_choice",
        "options": [
            ("WAN - MAN - LAN - PAN", True),
            ("MAN - WAN - LAN - PAN", False),
            ("LAN - MAN - WAN - PAN", False),
            ("PAN - LAN - MAN - WAN", False),
        ],
        "explanation": "Pregunta tomada de Cuestionario 1er Parcial RIN TEÓRICO.pdf, pág. 7.",
    },
    {
        "statement": "El agente relay Dynamic Host Configuration Protocol se ejecuta cuando:",
        "type": "single_choice",
        "options": [
            ("Cliente y servidor DHCP se encuentran en diferentes subredes", True),
            ("Cliente y servidor DHCP están en la misma subred", False),
            ("Existe un servidor DHCP en cada subred", False),
            ("Cliente y servidor web se encuentran en diferentes subredes", False),
        ],
        "explanation": "Pregunta tomada de Cuestionario 1er Parcial RIN TEÓRICO.pdf, pág. 8.",
    },
    {
        "statement": "Los campos de la cabecera del Internet Control Message Protocol son:",
        "type": "single_choice",
        "options": [
            ("Tipo, código y suma de verificación", True),
            ("Origen, destino y TTL", False),
            ("Puerto origen y puerto destino", False),
            ("Preámbulo, tipo y FCS", False),
        ],
        "explanation": "Pregunta tomada de Cuestionario 1er Parcial RIN TEÓRICO.pdf, pág. 8.",
    },
    {
        "statement": "¿Cuáles de las siguientes características corresponden a VLSM? (Seleccione dos)",
        "type": "multiple_choice",
        "options": [
            ("Permite tomar una subred y volverla a dividir en subredes más pequeñas", True),
            ("Permite crear para pocos hosts máscaras largas", True),
            ("Exige que todas las áreas posean la misma máscara", False),
            ("Se implementa especialmente con direcciones privadas", False),
        ],
        "explanation": "Pregunta tomada de Cuestionario 1er Parcial RIN TEÓRICO.pdf, págs. 2 y 9.",
    },
    {
        "statement": "El algoritmo para determinar el checksum de IPv4 se calcula:",
        "type": "single_choice",
        "options": [
            ("En el origen, en el destino y dos veces en cada salto", True),
            ("En el origen, en el destino y una vez en cada salto", False),
            ("Solo en el origen", False),
            ("Solo en los routers", False),
        ],
        "explanation": "Pregunta tomada de Cuestionario 1er Parcial RIN TEÓRICO.pdf, pág. 9.",
    },
    {
        "statement": "En el método de acceso CSMA/CA, el mensaje RTS contiene:",
        "type": "single_choice",
        "options": [
            ("Direcciones MAC del dispositivo origen y destino", True),
            ("Direcciones IP del dispositivo origen y destino", False),
            ("Número de puerto origen y destino", False),
            ("Relación IP-MAC del dispositivo destino", False),
        ],
        "explanation": "Pregunta tomada de Cuestionario 1er Parcial RIN TEÓRICO.pdf, pág. 9.",
    },
    {
        "statement": "¿Cuál de los siguientes campos pertenece a la cabecera de un paquete IPv4? (Seleccione dos)",
        "type": "multiple_choice",
        "options": [
            ("Longitud de cabecera (IHL)", True),
            ("Time To Live (TTL)", True),
            ("Longitud de carga útil", False),
            ("Límite de salto", False),
        ],
        "explanation": "Pregunta tomada de Cuestionario 1er Parcial RIN TEÓRICO.pdf, pág. 9.",
    },
    {
        "statement": "Determine cuáles de las siguientes direcciones IP son públicas.",
        "type": "multiple_choice",
        "options": [
            ("172.14.60.8", True),
            ("190.168.21.56", True),
            ("11.10.10.16", True),
            ("192.168.255.16", False),
            ("172.28.56.90", False),
            ("10.28.5.10", False),
        ],
        "explanation": "Pregunta tomada de Cuestionario 1er Parcial RIN TEÓRICO.pdf, pág. 10.",
    },
    {
        "statement": "El mensaje utilizado en DHCP que tiene por objeto solicitar los parámetros de configuración es:",
        "type": "single_choice",
        "options": [
            ("Request", True),
            ("Offer", False),
            ("Discover", False),
            ("Ack", False),
        ],
        "explanation": "Pregunta tomada de Cuestionario 1er Parcial RIN TEÓRICO.pdf, pág. 10.",
    },
    {
        "statement": "En el método de acceso CSMA/CA, el mensaje RTS lo envía:",
        "type": "single_choice",
        "options": [
            ("El dispositivo de origen", True),
            ("El dispositivo destino", False),
            ("El switch", False),
            ("El hub", False),
        ],
        "explanation": "Pregunta tomada de Cuestionario 1er Parcial RIN TEÓRICO.pdf, pág. 11.",
    },
    {
        "statement": "La dirección IPv4 0.0.0.0:",
        "type": "single_choice",
        "options": [
            ("Se utiliza en la dirección origen del paquete DHCP Discover", True),
            ("Representa una puerta de enlace de la LAN", False),
            ("Representa todos los hosts de una LAN", False),
            ("Puede aparecer en la dirección origen de una trama", False),
        ],
        "explanation": "Pregunta tomada de Cuestionario 1er Parcial RIN TEÓRICO.pdf, págs. 11 y 12.",
    },
    {
        "statement": "¿Cuál de las siguientes es la dirección de broadcast de la subred 190.10.24.0/23?",
        "type": "single_choice",
        "options": [
            ("190.10.25.255", True),
            ("190.10.24.255", False),
            ("190.10.25.254", False),
            ("190.10.31.255", False),
        ],
        "explanation": "Pregunta tomada de Cuestionario 1er Parcial RIN TEÓRICO.pdf, pág. 12.",
    },
    {
        "statement": "Una dirección MAC es:",
        "type": "single_choice",
        "options": [
            ("Física, plana, es independiente de la ubicación dentro de la organización", True),
            ("Lógica, jerárquica, depende de la ubicación dentro de la organización", False),
            ("Física, jerárquica, depende de la ubicación dentro de la organización", False),
            ("Lógica, plana, es independiente de la ubicación", False),
        ],
        "explanation": "Pregunta tomada de Cuestionario 1er Parcial RIN TEÓRICO.pdf, pág. 12.",
    },
    {
        "statement": "Un mensaje ARP-request se encapsula en:",
        "type": "single_choice",
        "options": [
            ("Una trama con dirección destino FF:FF:FF:FF:FF:FF", True),
            ("Un paquete con dirección destino 255.255.255.255", False),
            ("Una trama con dirección destino multicast", False),
            ("Una trama con dirección origen FF:FF:FF:FF:FF:FF", False),
        ],
        "explanation": "Pregunta tomada de Cuestionario 1er Parcial RIN TEÓRICO.pdf, pág. 13.",
    },
    {
        "statement": "¿Cuál de las siguientes es una desventaja de las redes inalámbricas?",
        "type": "single_choice",
        "options": [
            ("Velocidad", True),
            ("Movilidad", False),
            ("Flexibilidad", False),
            ("Costo de instalación", False),
        ],
        "explanation": "Pregunta tomada de Cuestionario 1er Parcial RIN TEÓRICO.pdf, pág. 13.",
    },
    {
        "statement": "Determine cuáles de las siguientes direcciones IPv4 son privadas. (Seleccione tres)",
        "type": "multiple_choice",
        "options": [
            ("172.28.10.9", True),
            ("192.168.150.78", True),
            ("10.20.10.18", True),
            ("172.33.60.95", False),
            ("194.168.50.18", False),
            ("14.40.60.5", False),
        ],
        "explanation": "Pregunta tomada de Cuestionario 1er Parcial RIN TEÓRICO.pdf, pág. 14.",
    },
    {
        "statement": "La dirección MAC origen en una trama enviada desde una PC que está arrancando hacia el servidor DHCP es:",
        "type": "single_choice",
        "options": [
            ("MAC de la PC", True),
            ("FF-FF-FF-FF-FF-FF", False),
            ("0.0.0.0", False),
            ("255.255.255.255", False),
        ],
        "explanation": "Pregunta tomada de Cuestionario 1er Parcial RIN TEÓRICO.pdf, pág. 14.",
    },
    {
        "statement": "El tipo de mensaje ICMP que se utiliza para informar al origen que reduzca la tasa de transmisión es:",
        "type": "single_choice",
        "options": [
            ("Source quench", True),
            ("Tiempo de vida excedido", False),
            ("Problema de parámetro", False),
            ("Packet too big", False),
        ],
        "explanation": "Pregunta tomada de Cuestionario 1er Parcial RIN TEÓRICO.pdf, pág. 14.",
    },
    {
        "statement": "La red del campus de la Facultad Regional Córdoba es una red:",
        "type": "single_choice",
        "options": [
            ("LAN", True),
            ("MAN", False),
            ("WAN", False),
            ("PAN", False),
        ],
        "explanation": "Pregunta tomada de Cuestionario 1er Parcial RIN TEÓRICO.pdf, pág. 15.",
    },
    {
        "statement": "La sigla WAN significa:",
        "type": "single_choice",
        "options": [
            ("Wide Area Network", True),
            ("Wall Area Network", False),
            ("Wise Area Network", False),
            ("Wonderful Area Network", False),
        ],
        "explanation": "Pregunta tomada de Cuestionario 1er Parcial RIN TEÓRICO.pdf, pág. 15.",
    },
    {
        "statement": "Según la direccionalidad de los datos, una red se puede clasificar en:",
        "type": "multiple_choice",
        "options": [
            ("Símplex", True),
            ("Semi Dúplex o Half Dúplex", True),
            ("Dúplex o Full Dúplex", True),
            ("Difusión", False),
            ("Punto a punto", False),
        ],
        "explanation": "Pregunta tomada de Cuestionario 1er Parcial RIN TEÓRICO.pdf, pág. 16.",
    },
    {
        "statement": "La capa de la arquitectura TCP/IP que brinda un servicio de comunicación de datos extremo a extremo entre aplicaciones es:",
        "type": "single_choice",
        "options": [
            ("Transporte", True),
            ("Interred", False),
            ("Host a red", False),
            ("Aplicación", False),
        ],
        "explanation": "Pregunta tomada de Cuestionario 1er Parcial RIN TEÓRICO.pdf, pág. 17.",
    },
    {
        "statement": "Indique el orden correcto de las capas o niveles de la arquitectura TCP/IP:",
        "type": "single_choice",
        "options": [
            ("Aplicación – Transporte – Interred – Host a red", True),
            ("Aplicación – Interred – Transporte – Host a red", False),
            ("Transporte – Aplicación – Interred – Host a red", False),
            ("Aplicación – Host a red – Transporte – Interred", False),
        ],
        "explanation": "Pregunta tomada de Cuestionario 1er Parcial RIN TEÓRICO.pdf, pág. 17.",
    },
    {
        "statement": "La arquitectura TCP/IP tiene más capas o niveles que el Modelo OSI:",
        "type": "single_choice",
        "options": [
            ("Falso", True),
            ("Verdadero", False),
        ],
        "explanation": "Pregunta tomada de Cuestionario 1er Parcial RIN TEÓRICO.pdf, pág. 17.",
    },
    {
        "statement": "La arquitectura TCP/IP surgió en:",
        "type": "single_choice",
        "options": [
            ("EEUU", True),
            ("Europa", False),
            ("Asia", False),
            ("Japón", False),
        ],
        "explanation": "Pregunta tomada de Cuestionario 1er Parcial RIN TEÓRICO.pdf, pág. 17.",
    },
    {
        "statement": "Indique cuáles de los siguientes protocolos pertenecen a la capa de aplicación del modelo TCP/IP:",
        "type": "multiple_choice",
        "options": [
            ("HTTP", True),
            ("DNS", True),
            ("DHCP", True),
            ("UDP", False),
            ("TCP", False),
            ("IP", False),
        ],
        "explanation": "Pregunta tomada de Cuestionario 1er Parcial RIN TEÓRICO.pdf, pág. 17.",
    },
    {
        "statement": "Dos dispositivos están intercambiando datos entre sí. ¿Cuál protocolo garantiza que la información llegue completa, ordenada e íntegra?",
        "type": "single_choice",
        "options": [
            ("TCP", True),
            ("UDP", False),
            ("ICMP", False),
            ("DNS", False),
        ],
        "explanation": "Pregunta tomada de Cuestionario 1er Parcial RIN TEÓRICO.pdf, pág. 17.",
    },
    {
        "statement": "Indique cuáles de los siguientes protocolos pertenecen a la capa de transporte del modelo TCP/IP:",
        "type": "multiple_choice",
        "options": [
            ("TCP", True),
            ("UDP", True),
            ("HTTP", False),
            ("IP", False),
            ("DNS", False),
        ],
        "explanation": "Pregunta tomada de Parcial REDES.pdf, pág. 2 y Cuestionario 1er Parcial RIN TEÓRICO.pdf, pág. 18.",
    },
]


class Command(BaseCommand):
    help = "Carga la materia Redes y el cuestionario del 1er Parcial Teórico RIN con preguntas deduplicadas."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Borra las preguntas existentes del cuestionario antes de cargar.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        subject, _ = Subject.objects.get_or_create(
            name=SUBJECT_NAME,
            defaults={"description": "Materia de Redes / RIN"},
        )

        quiz, created = Quiz.objects.get_or_create(
            subject=subject,
            name=QUIZ_NAME,
            defaults={
                "description": "Preguntas recopiladas para el primer parcial teórico de RIN.",
                "is_active": True,
            },
        )

        if options["reset"]:
            quiz.questions.all().delete()
            self.stdout.write(self.style.WARNING("Preguntas anteriores eliminadas."))

        created_count = 0
        skipped_count = 0

        for index, item in enumerate(QUESTIONS, start=1):
            normalized_statement = " ".join(item["statement"].split())

            if quiz.questions.filter(statement__iexact=normalized_statement).exists():
                skipped_count += 1
                continue

            question = Question.objects.create(
                quiz=quiz,
                statement=normalized_statement,
                question_type=item["type"],
                score=Decimal("1.00"),
                explanation=item.get("explanation", ""),
                position=index,
            )

            for option_index, (text, is_correct) in enumerate(item["options"], start=1):
                QuestionOption.objects.create(
                    question=question,
                    text=text,
                    is_correct=is_correct,
                    position=option_index,
                )

            created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Listo. Quiz: {quiz.name}. Creadas: {created_count}. Omitidas por duplicado: {skipped_count}."
            )
        )
