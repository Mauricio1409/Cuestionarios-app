from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.subjects.models import Subject
from apps.quizzes.models import Quiz, Question, QuestionOption


SUBJECT_NAME = "Redes"
QUIZ_NAME = "1er Parcial Teórico RIN"


QUESTIONS_NEW = [
    {
        "statement": "Para la siguiente topología de red, determinar las direcciones IP que podrían usarse para satisfacer los requisitos de direcciones de host en la subred de Villa María. (falta imagen - archivo: Preguntas faltantes/Captura desde 2026-05-29 20-10-05.png)",
        "type": "multiple_choice",
        "options": [
            ("PC 1 VM → 192.168.16.226", True),
            ("PC 2 VM → 192.168.16.227", True),
            ("PC 3 VM → 192.168.16.238", True),
            ("PC 1 VM → 192.168.16.238", False),
            ("PC 2 VM → 192.168.16.241", False),
            ("PC 3 VM → 192.168.16.227", False),
        ],
        "explanation": "Las direcciones válidas deben pertenecer a la subred asignada a Villa María y no pueden ser ni la dirección de red ni la de broadcast. Por eso las IP correctas para los tres hosts son 192.168.16.226, 192.168.16.227 y 192.168.16.238.",
    },
    {
        "statement": "La siguiente es una captura de paquetes realizada mientras un host estaba navegando por Internet. En ella se puede observar que la dirección MAC del router de la LAN es ec:43:f6:b5:b4:f4. (falta imagen - archivo: Preguntas faltantes/Captura desde 2026-05-29 20-12-18.png)",
        "type": "single_choice",
        "options": [
            ("Verdadero", True),
            ("Falso", False),
        ],
        "explanation": "Cuando un host de una LAN navega hacia Internet, la trama Ethernet sale hacia la puerta de enlace local. Por eso la MAC que aparece como destino en la trama local corresponde al router/gateway de la LAN, no al servidor remoto.",
    },
    {
        "statement": "¿Cuál es el comando que permite observar la dirección MAC de la placa de red de un host en Windows?",
        "type": "single_choice",
        "options": [
            ("ipconfig/all", True),
            ("arp -a", False),
            ("ping", False),
            ("tracert", False),
        ],
        "explanation": "El comando ipconfig/all muestra la configuración completa de las interfaces de red en Windows, incluida la dirección física o dirección MAC de la placa.",
    },
    {
        "statement": "Para la siguiente topología de red, ¿cuáles podrían ser las direcciones de la puerta de enlace predeterminada de las subredes de Córdoba, Río Cuarto y Villa María? (falta imagen - archivo: Preguntas faltantes/Captura desde 2026-05-29 20-14-35.png)",
        "type": "multiple_choice",
        "options": [
            ("Córdoba → 192.168.16.1", True),
            ("Río Cuarto → 192.168.16.129", True),
            ("Villa María → 192.168.16.193", True),
            ("Río Cuarto → 192.168.16.1", False),
            ("Villa María → 192.168.16.1", False),
        ],
        "explanation": "La puerta de enlace predeterminada de cada subred debe estar dentro del rango de esa subred. En la topología, Córdoba usa la primera subred, Río Cuarto la siguiente y Villa María una subred posterior, por eso corresponden .1, .129 y .193 respectivamente.",
    },
    {
        "statement": "Respecto de una captura tomada mientras un host de una LAN navegaba por Internet, relacione las direcciones MAC observadas. (falta imagen - archivo: Preguntas faltantes/Captura desde 2026-05-29 20-15-31.png)",
        "type": "multiple_choice",
        "options": [
            ("Dirección MAC de la puerta de enlace de la LAN → EC:43:F6:B5:B4:F4", True),
            ("Dirección MAC del host que envía el mensaje → LiteonTe", True),
            ("Dirección MAC de Microsoft Azure → No se puede deducir de la captura", True),
            ("Dirección MAC de Microsoft Azure → EC:43:F6:B5:B4:F4", False),
            ("Dirección MAC de la puerta de enlace de la LAN → No se puede deducir de la captura", False),
        ],
        "explanation": "En una comunicación hacia Internet, la trama Ethernet solo contiene MACs del enlace local: la del host y la del gateway. La MAC del servidor remoto no viaja en la trama local y por eso no puede deducirse desde esa captura.",
    },
    {
        "statement": "Para la siguiente topología de red, determinar las máscaras que podrían usarse para satisfacer los requisitos de direcciones de host en cada subred. (falta imagen - archivo: Preguntas faltantes/Captura desde 2026-05-29 20-17-13.png)",
        "type": "multiple_choice",
        "options": [
            ("Villa María → /27", True),
            ("Río Cuarto → /26", True),
            ("Córdoba → /25", True),
            ("Enlaces WAN → /30", True),
            ("Todas las subredes → /24", False),
        ],
        "explanation": "Se usa VLSM: la subred con más hosts necesita una máscara más corta y las subredes pequeñas una máscara más larga. /25 alcanza para Córdoba, /26 para Río Cuarto, /27 para Villa María y /30 para enlaces punto a punto WAN.",
    },
    {
        "statement": "Si en una LAN se tienen 3 switches como los de la figura, interconectados de la forma indicada, ¿hasta cuántos dominios de colisión podría haber? (falta imagen - archivo: Preguntas faltantes/Captura desde 2026-05-29 20-17-34.png)",
        "type": "single_choice",
        "options": [
            ("82", True),
            ("72", False),
            ("24", False),
            ("3", False),
        ],
        "explanation": "Cada puerto de switch puede representar un dominio de colisión independiente. Al sumar los puertos de los switches y los enlaces de interconexión de la figura, el máximo posible indicado es 82.",
    },
    {
        "statement": "La siguiente es una captura de paquetes realizada mientras un host estaba navegando por Internet. En ella se puede observar que la dirección MAC del servidor de Microsoft es ec:43:f6:b5:b4:f4. (falta imagen - archivo: Preguntas faltantes/Captura desde 2026-05-29 20-25-43.png)",
        "type": "single_choice",
        "options": [
            ("Falso", True),
            ("Verdadero", False),
        ],
        "explanation": "En una captura Ethernet dentro de una LAN no se observa la MAC del servidor remoto de Internet. La MAC ec:43:f6:b5:b4:f4 corresponde al dispositivo local de salida, normalmente el gateway/router de la LAN.",
    },
    {
        "statement": "Las RFC (Request For Comments) son un conjunto de documentos que sirven de referencia para la comunidad de Internet, utilizados para la implementación, estandarización y discusión de normas, estándares, tecnologías y protocolos, emitidas por el IETF.",
        "type": "single_choice",
        "options": [
            ("Verdadero", True),
            ("Falso", False),
        ],
        "explanation": "Los RFC documentan protocolos, prácticas y estándares relacionados con Internet. Son la forma habitual en que se publican especificaciones técnicas dentro del ecosistema IETF.",
    },
    {
        "statement": "Un host conectado a la interfaz FastEthernet 0/5 de un switch recibe una trama. ¿Qué dirección agregará el switch en su tabla CAM correspondiente a dicho puerto 0/5? (falta imagen - archivo: Preguntas faltantes/Captura desde 2026-05-29 20-26-54.png)",
        "type": "single_choice",
        "options": [
            ("24:f5:aa:70:7e:1f", True),
            ("54 bytes", False),
            ("216.81.1.9", False),
            ("23.12.124.0", False),
        ],
        "explanation": "El switch aprende direcciones MAC observando la dirección MAC de origen de las tramas que ingresan por cada puerto. Por eso asocia el puerto FastEthernet 0/5 con la MAC de origen 24:f5:aa:70:7e:1f.",
    },
    {
        "statement": "¿Cuáles de las siguientes direcciones IP podrá utilizar un administrador de red si desea implementar un esquema de direccionamiento IP con 20 subredes, maximizando la cantidad de hosts por subred? (Seleccione dos)",
        "type": "multiple_choice",
        "options": [
            ("199.65.0.0/29", True),
            ("190.60.0.0/21", True),
            ("100.0.0.0/14", False),
            ("98.0.0.0/15", False),
            ("189.85.0.0/23", False),
            ("140.56.0.0/22", False),
        ],
        "explanation": "Para obtener al menos 20 subredes se necesitan 5 bits prestados, porque 2^5 = 32. Al comparar con la máscara por defecto de cada clase, las opciones válidas son las que reflejan ese préstamo de bits manteniendo la mayor cantidad posible de hosts por subred.",
    },
    {
        "statement": "La dirección 01:00:5E:00:04:C9 aparece en el campo destino de una trama. Indique cuál afirmación es correcta.",
        "type": "single_choice",
        "options": [
            ("La trama será procesada solo por un grupo de máquinas de la LAN", True),
            ("Es una dirección jerárquica", False),
            ("La trama será procesada solo por una PC", False),
            ("Todas las PC de la LAN procesarán la trama", False),
            ("Nunca puede aparecer esa dirección en el campo destino de una trama", False),
        ],
        "explanation": "Las direcciones MAC que comienzan con 01:00:5E corresponden a multicast IPv4 sobre Ethernet. Por eso la trama está destinada a un grupo de equipos y no a todos los hosts ni a uno solo.",
    },
    {
        "statement": "¿Cuáles de las siguientes afirmaciones son correctas con respecto a la arquitectura de Internet? (Seleccione dos)",
        "type": "multiple_choice",
        "options": [
            ("Las redes Tier 3 brindan servicio de conexión a Internet a los usuarios residenciales y a empresas", True),
            ("Las redes Tier 2 se conectan a las redes Tier 1 a través de conexiones de tránsito", True),
            ("Las redes Tier 3 ofrecen servicios de conectividad a los operadores Tier 2", False),
            ("Los IXP se conectan entre sí a través de conexiones de tránsito", False),
            ("Las redes Tier 2 brindan servicios de conexión a Internet a usuarios residenciales y empresas", False),
        ],
        "explanation": "En la jerarquía de Internet, los Tier 1 forman la red troncal, los Tier 2 compran tránsito o hacen peering, y los Tier 3 suelen vender acceso final a usuarios residenciales o empresas.",
    },
    {
        "statement": "En cuáles de los siguientes dispositivos se ejecuta el método de acceso al medio CSMA/CA. (Seleccione dos)",
        "type": "multiple_choice",
        "options": [
            ("Placas de red inalámbricas", True),
            ("Access Point", True),
            ("Hubs", False),
            ("Placas de red Ethernet", False),
            ("Switches", False),
            ("Cable UTP", False),
        ],
        "explanation": "CSMA/CA es usado por redes inalámbricas IEEE 802.11. Por eso intervienen tanto las placas Wi-Fi de los hosts como los Access Point.",
    },
    {
        "statement": "Una empresa está dividida en 10 áreas de trabajo. Si el administrador plantea un esquema de direccionamiento utilizando subredes:",
        "type": "single_choice",
        "options": [
            ("Todas las subredes deben poseer la misma máscara de subred", True),
            ("Las subredes pueden tener una máscara menor que la máscara por defecto", False),
            ("El administrador deberá reservar 3 bits para subredes", False),
            ("La máxima cantidad de bits que puede formar parte de la máscara es 31", False),
            ("Se permite que cada área posea su propia máscara de subred en función de la cantidad de hosts", False),
        ],
        "explanation": "Cuando se plantea un esquema de subnetting clásico, las subredes se definen con una misma máscara. Si cada área usara máscaras distintas, ya se estaría aplicando VLSM.",
    },
    {
        "statement": "Una empresa decide implementar un esquema de direccionamiento IP utilizando subredes. El administrador decide utilizar la IP 160.4.0.0/23. Ello implica que:",
        "type": "single_choice",
        "options": [
            ("Se pierden 512 direcciones IP del total del espacio de direccionamiento", True),
            ("Se ganan 256 direcciones IP del total del espacio de direccionamiento", False),
            ("Se pierden 128 direcciones IP del total del espacio de direccionamiento", False),
            ("Se pierden 510 direcciones IP del total del espacio de direccionamiento", False),
            ("Se ganan 510 direcciones IP del total del espacio de direccionamiento", False),
        ],
        "explanation": "La red 160.4.0.0 es de clase B por defecto. Al usar /23 se divide el espacio original en subredes de 512 direcciones cada una; por eso cada subred consume un bloque de 512 direcciones del espacio total.",
    },
    {
        "statement": "¿Cuál de las siguientes características corresponde al protocolo IPv4?",
        "type": "single_choice",
        "options": [
            ("Encamina cada paquete de manera independiente", True),
            ("Retransmite el paquete que no llegó correctamente", False),
            ("Reordena los paquetes en el destino", False),
            ("Utiliza direcciones de 48 bits", False),
            ("Utiliza números de secuencia", False),
        ],
        "explanation": "IPv4 trabaja con datagramas independientes. La retransmisión, el ordenamiento y los números de secuencia corresponden a funciones de transporte confiable como TCP.",
    },
    {
        "statement": "En el método de acceso al medio utilizado por las redes inalámbricas, los dispositivos cuando tienen que transmitir una trama:",
        "type": "single_choice",
        "options": [
            ("Escuchan el medio y si está libre, esperan un tiempo aleatorio y envían una trama RTS indicando dirección MAC origen y dirección MAC destino", True),
            ("Escuchan el medio y si está libre, envían los datos directamente hacia el medio de transmisión", False),
            ("Esperan que les llegue una trama token para poder transmitir", False),
            ("Garantizan que las tramas que colisionan sean confirmadas con ACK", False),
            ("Le avisan al emisor que están dispuestos a recibir mediante RTS", False),
        ],
        "explanation": "En CSMA/CA los dispositivos intentan evitar colisiones. Para ello escuchan el medio, esperan un tiempo aleatorio y pueden usar RTS/CTS antes de transmitir datos.",
    },
    {
        "statement": "Indique cuál es el tamaño mínimo de la cabecera de un paquete IPv4:",
        "type": "single_choice",
        "options": [
            ("20 bytes", True),
            ("15 bytes", False),
            ("6 bytes", False),
            ("25 bytes", False),
            ("40 bytes", False),
            ("60 bytes", False),
        ],
        "explanation": "La cabecera IPv4 mínima tiene 5 palabras de 32 bits. Como cada palabra son 4 bytes, 5 × 4 = 20 bytes.",
    },
    {
        "statement": "La dirección IPv4 127.1.1.1:",
        "type": "single_choice",
        "options": [
            ("Permite verificar la correcta instalación de la pila de protocolos TCP/IP", True),
            ("Es una dirección privada", False),
            ("El administrador la configura en un host en producción", False),
            ("Es la puerta de enlace de una LAN", False),
            ("Es una dirección multicast", False),
        ],
        "explanation": "Las direcciones 127.0.0.0/8 son de loopback. Sirven para probar la pila TCP/IP local sin salir a la red.",
    },
    {
        "statement": "Una placa de red FastEthernet recibe y procesa una trama si la dirección de destino es: (Seleccione dos)",
        "type": "multiple_choice",
        "options": [
            ("FF:FF:FF:FF:FF:FF", True),
            ("Su dirección MAC", True),
            ("Su dirección IP", False),
            ("La dirección del gateway", False),
            ("255.255.255.255", False),
        ],
        "explanation": "Una NIC procesa tramas dirigidas a su propia MAC y tramas broadcast Ethernet. Las direcciones IP se evalúan en capas superiores, no en el campo destino de la trama Ethernet.",
    },
    {
        "statement": "Mientras se intercambian datos entre una PC y un servidor, una NIC recibe desde UTP una trama y al calcular el CRC el resultado coincide con el valor que viene en dicha trama. ¿Qué hará la placa de red?",
        "type": "single_choice",
        "options": [
            ("Desencapsular y entregar a la capa superior", True),
            ("Encapsular y enviar la trama", False),
            ("Enviar confirmación de recepción al origen", False),
            ("Pedir retransmisión al origen", False),
            ("Descartar la trama", False),
        ],
        "explanation": "Si el CRC coincide, la trama se considera íntegra. Entonces la placa puede desencapsularla y entregar su contenido a la capa superior.",
    },
    {
        "statement": "A partir de las direcciones IP 200.15.43.0/24, 200.15.50.0/24 y 200.15.39.0/24, indique cuál es la superred correcta que debería publicar un ISP:",
        "type": "single_choice",
        "options": [
            ("200.15.32.0/19", True),
            ("200.15.32.0/18", False),
            ("200.15.38.0/19", False),
            ("200.15.32.0/20", False),
            ("200.15.48.0/19", False),
            ("200.15.48.0/20", False),
        ],
        "explanation": "La superred debe cubrir todos los bloques dados con el prefijo común más específico posible. Las redes 200.15.39.0, 200.15.43.0 y 200.15.50.0 quedan incluidas dentro de 200.15.32.0/19.",
    },
    {
        "statement": "A partir de la siguiente topología y tabla de direcciones MAC del switch, indique por cuáles puertos se transmitirá la trama si la máquina E le envía datos a la máquina B. (falta imagen - archivo: Preguntas faltantes/Captura desde 2026-05-29 21-04-02.png)",
        "type": "single_choice",
        "options": [
            ("Puertos 1, 3 y 8", True),
            ("Puerto 3", False),
            ("Puertos 1, 3, 5 y 8", False),
            ("Puertos 1, 2, 3, 4, 6, 7 y 8", False),
        ],
        "explanation": "Si el switch no conoce la MAC destino, realiza flooding por los puertos del mismo dominio excepto el puerto por donde entró la trama. Según la tabla y la topología, eso corresponde a los puertos 1, 3 y 8.",
    },
    {
        "statement": "La cantidad máxima de bits que se pueden pedir prestados para crear subredes en una dirección IP clase A es:",
        "type": "single_choice",
        "options": [
            ("22 bits", True),
            ("14 bits", False),
            ("6 bits", False),
            ("24 bits", False),
        ],
        "explanation": "En clase A hay 24 bits originalmente disponibles para host. Para que queden al menos 2 bits de host, se pueden pedir prestados como máximo 22 bits.",
    },
    {
        "statement": "La cantidad máxima de bits que se pueden pedir prestados para crear subredes en una dirección IP clase B es:",
        "type": "single_choice",
        "options": [
            ("14 bits", True),
            ("13 bits", False),
            ("7 bits", False),
            ("5 bits", False),
            ("16 bits", False),
        ],
        "explanation": "En clase B hay 16 bits de host. Dejando al menos 2 bits para hosts, se pueden pedir prestados como máximo 14 bits.",
    },
    {
        "statement": "Considerando la movilidad de los dispositivos, una red se puede clasificar en:",
        "type": "multiple_choice",
        "options": [
            ("Red fija o cableada", True),
            ("Red móvil o inalámbrica", True),
            ("Punto a punto", False),
            ("LAN", False),
            ("WAN", False),
            ("Red dispersa", False),
        ],
        "explanation": "Según la movilidad de los dispositivos, las redes se clasifican en fijas/cableadas o móviles/inalámbricas. LAN y WAN clasifican por cobertura, no por movilidad.",
    },
    {
        "statement": "Una red en la cual todos los dispositivos comparten el mismo canal de comunicación es una:",
        "type": "single_choice",
        "options": [
            ("Red de difusión", True),
            ("WAN", False),
            ("Símplex", False),
            ("Red punto a punto", False),
            ("MAN", False),
        ],
        "explanation": "En una red de difusión, todos los dispositivos comparten el mismo canal y las transmisiones pueden ser recibidas por todos los nodos del medio compartido.",
    },
    {
        "statement": "La sigla TCP significa:",
        "type": "single_choice",
        "options": [
            ("Transmission Control Protocol", True),
            ("Transport Control Protocol", False),
            ("Transfer Control Protocol", False),
            ("Terminal Control Protocol", False),
        ],
        "explanation": "TCP significa Transmission Control Protocol, protocolo de transporte confiable usado por la arquitectura TCP/IP.",
    },
]


class Command(BaseCommand):
    help = "Carga solo las preguntas nuevas/faltantes de Redes sin borrar las ya existentes."

    @transaction.atomic
    def handle(self, *args, **options):
        subject, _ = Subject.objects.get_or_create(
            name=SUBJECT_NAME,
            defaults={"description": "Materia de Redes / RIN"},
        )

        quiz, _ = Quiz.objects.get_or_create(
            subject=subject,
            name=QUIZ_NAME,
            defaults={
                "description": "Preguntas recopiladas para el primer parcial teórico de RIN.",
                "is_active": True,
            },
        )

        max_position = quiz.questions.order_by("-position").values_list("position", flat=True).first() or 0

        created_count = 0
        skipped_count = 0

        for offset, item in enumerate(QUESTIONS_NEW, start=1):
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
                position=max_position + offset,
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
                f"Listo. Preguntas nuevas creadas: {created_count}. Omitidas porque ya existían: {skipped_count}."
            )
        )
