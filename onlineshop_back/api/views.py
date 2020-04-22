from api.models import Category, Product
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import sqlite3
from sqlite3 import Error
import requests

from api.serializers import ProductSerializer, CategorySerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated


@api_view(['GET', 'POST'])
def products_list(request):
    if request.method == 'GET':
        vacancies = Product.objects.all()
        serializer = ProductSerializer(vacancies, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors}, status=status.HTTP_501_NOT_IMPLEMENTED)


# @csrf_exempt
# def products_list(request):
#     global my_cursor, my_db
#     if request.method == 'GET':
#         products = Product.objects.all()
#         products_json = [product.to_json() for product in products]
#         return JsonResponse(products_json, safe=False)
#     elif request.method == 'POST':
#         try:
#             database = "db.sqlite3"
#             my_db = sqlite3.connect(database)
#             my_cursor = my_db.cursor()
#             sql = "INSERT INTO api_product(name, description, price, image, size, category_id) VALUES (?, ?, ?, ?, ?, ?)"
#             val = (
#                 "Walking Cradles Lynn",
#                 "Hit refresh with the easy and comfortable Walking Cradles® Lynn open-toed wedge mule. Smooth leather upper with soft microfiber linings and an open-cell, non-compacting latex footbed that features Tiny Pillows® for increased cushioning and support. Durable rubber outsole.",
#                 39500,
#                 "https://m.media-amazon.com/images/I/71D3K6s3QTL._SX700_.jpg",
#                 "39,40,41,42,43",
#                 2
#             )
#             my_cursor.execute(sql, val)
#             my_db.commit()
#         finally:
#             my_cursor.close()
#             my_db.close()
#         return JsonResponse({'product': 'to_json()'})


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, product_id):
    try:
        vacancies = Product.objects.get(id=product_id)
    except Product.DoesNotExist as e:
        return Response({'error': str(e)})

    if request.method == 'GET':
        s = ProductSerializer(vacancies)
        return Response(s.data)
    elif request.method == 'PUT':
        s = ProductSerializer(instance=vacancies, data=request.data)
        if s.is_valid():
            s.save()
            return Response(s.data)
        return Response({'error': s.errors})
    elif request.method == 'DELETE':
        vacancies.delete()
        return JsonResponse({'deleted': True})


# @csrf_exempt
# def product_detail(request, product_id):
#     database = "db.sqlite3"
#     my_db = sqlite3.connect(database)
#     my_cursor = my_db.cursor()
#
#     try:
#         products = Product.objects.get(id=product_id)
#     except Product.DoesNotExist as e:
#         return JsonResponse({'error': str(e)})
#
#     if request.method == 'GET':
#         return JsonResponse(products.to_json())
#     elif request.method == 'PUT':
#         try:
#             sql = "UPDATE api_product SET price = ? WHERE id = ?"
#             my_input = input()
#             new_price = int(my_input)
#             val = (new_price, 30)
#             my_cursor.execute(sql, val)
#             my_db.commit()
#         finally:
#             my_cursor.close()
#             my_db.close()
#         return JsonResponse({'price': val[0]})
#     elif request.method == 'DELETE':
#         try:
#             sql = "DELETE FROM api_product WHERE id = 30"
#             # product_id
#             val = 30
#             my_cursor.execute(sql)
#             my_db.commit()
#         finally:
#             my_cursor.close()
#             my_db.close()
#         return JsonResponse({'message': 'Product successfully deleted from database'})


def by_category(request, ctg):
    try:
        g = Category.objects.get(name=ctg)
    except Category.DoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False)

    products = g.product_set.all()
    products_json = [v.to_json() for v in products]
    if request.method == 'GET':
        return JsonResponse(products_json, safe=False)


def by_category_detail(request, ctg, product_id):
    try:
        g = Category.objects.get(name=ctg)
    except Category.DoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False)

    try:
        products = Product.objects.get(id=product_id)
    except Product.DoesNotExist as e:
        return JsonResponse({'error': str(e)})

    if request.method == 'GET':
        return JsonResponse(products.to_json())


class CategoryList(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        cs = Category.objects.all()
        serializer = CategorySerializer(cs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def main():
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()

    products = [
        (
            1,
            "Walking Cradles Lynn",
            "Hit refresh with the easy and comfortable Walking Cradles® Lynn open-toed wedge mule. Smooth leather upper with soft microfiber linings and an open-cell, non-compacting latex footbed that features Tiny Pillows® for increased cushioning and support. Durable rubber outsole.",
            39500,
            "https://m.media-amazon.com/images/I/71D3K6s3QTL._SX700_.jpg",
            "red, blue, white, pink",
            "39,40,41,42,43",
            2

        ),
        (
            2,
            "UGG Lennox",
            "The UGG® Lennox faux-patent open-toe sandal sets the bar with a chic and modern tone for the summer.Crisscrossing elastic heel strap features an adjustable buckle at ankle.    Smooth synthetic linings with a cushioned, leather-lined Imprint by UGG™ footbed.",
            38000,
            "https://m.media-amazon.com/images/I/71GRYTgYhPL._SX700_.jpg",
            "red, yellow, white, pink",
            "39, 41",
            2

        ),

        (
            3,
            "UGG Kids. Fluff Yeah Slide (Toddler/Little Kid)",
            "Crafted from rows of plush shearling, and featuring an open-toe silhouette with an easy-on brand-marked elasticized heel strap, these UGG® Kids Fluff Yeah Slide slippers will embrace your little one from the toes up!Luxuriously lined with UGGpure™ wool for a breathable and warm environment.",
            25000,
            "https://m.media-amazon.com/images/I/71NOD24J0BL._SX700_.jpg",
            "black, purple, white, pink",
            "29,31,32,33,34,35,36",
            3

        ),
        (
            4,
            "UGG Kids.  Cozy II (Toddler/Little Kid/Big Kid)",
            "Exclusive colors Black Rainbow, Navy, and Navy Multi available only on Zappos. Whether youre in the comfort of your home or out on the town, the UGG® Fluff Yeah Slide gets you style and comfort thats out of this world! Soft and plush sheepskin uppers with an open toe.",
            18000,
            "https://m.media-amazon.com/images/I/81N11m3ww+L._SX700_.jpg",
            "brown, white, black",
            "31,33,35,36,37",
            3

        ),
        (
            5,
            "Giesswein. Veitsch",
            "The Giesswein® Veitsch slippers feel so good, youll never want to take them off. 100% boiled wool construction offers a breathable wear thats also naturally water resistant. Cushioned footbed with arch support can be removed to accommodate your custom orthotics.",
            67000,
            "https://m.media-amazon.com/images/I/91rbeBXAkXL._SX700_.jpg",
            "brown, grey, white, black",
            "41,42,43,44,45,46",
            1

        ),
        (
            6,
            "New Balance.  MID626v2",
            "Keep feet from feeling weary, even if you are pulling a double shift, with the New Balance® MID626v2 work sneaker.  Durable leather uppers.  Lace-up closure.",
            73000,
            "https://m.media-amazon.com/images/I/81tp-ij+YML._SX700_.jpg",
            "grey, white, black",
            "41,43,45,46",
            1

        ),
        (
            7,
            "Timberland PRO.  Ridgework Composite Safety Toe Waterproof Mid",
            "Something here",
            89000,
            "https://m.media-amazon.com/images/I/81fD0EleeVL._SX700_.jpg",
            "brown, grey, black",
            "36,37,39,40,41,42,44,45",
            1

        ),
        (
            8,
            "Haflinger. Sassy",
            "Something here",
            46000,
            "https://m.media-amazon.com/images/I/81vSL0h7nrL._SX700_.jpg",
            "grey, purple, pink, white",
            "36,37,38,39,40,42,44",
            2

        ),
        (
            9,
            "Giesswein.  Ammern Classic",
            "The Giesswein® Ammern Classic transforms your standard slipper into a houseshoe that can be worn for both work and play. 100% boiled-wool construction wicks away moisture while helping to regulate temperature and is never itchy or scratchy so it feels soft against your feet.",
            33500,
            "https://m.media-amazon.com/images/I/81CidFoU9LL._SX700_.jpg",
            "brown, black",
            "40,41,42,44,45",
            1
        ),
        (
            10,
            "Haflinger.  Olivia",
            "Soft, natural 100% boiled wool upper with an owl on each shoe. Easy slip-on style.  Wool-covered latex sock liner conforms to your foot for optimal comfort.  Felt outsole.",
            24000,
            "https://m.media-amazon.com/images/I/81WwUm+-IAL._SX700_.jpg",
            "grey, blue, pink",
            "31,33,35,36,37",
            3

        ),
        (
            11,
            "Haflinger.  Coffee",
            "Cozy up with your morning brew and your new favorite slippers with these warm and comfy Haflinger® slippers. Boiled wool upper is naturally soft, sturdy, and machine washable. Coffee-inspired appliqués adorn the front of each slipper.",
            19000,
            "https://m.media-amazon.com/images/I/81VrkQ-uz+L._SX700_.jpg",
            "brown",
            "31,32,33,34,35,36,37",
            3

        ), (
            12,
            "Nike. Free RN 5.0",
            "The Nike® Free RN 5.0 running shoes have returned to form with its newest iteration, ideal for low-mileage runs around the track or at the gym.",
            74500,
            "https://m.media-amazon.com/images/I/71UcWegbPcL._SX700_.jpg",
            "grey, blue, red, white, black",
            "39,42,43,44,45,46,47",
            2

        ),
        (
            13,
            "Nike.  Flex Experience Run 9",
            "Built for natural motion, the Nike® Flex Experience Run 9 running shoes provide ideal levels of support and cushioning for any activity.",
            63000,
            "https://m.media-amazon.com/images/I/613Y8MbQ71L._SX700_.jpg",
            "white, black",
            "39,41,42,44,45,47",
            1

        ),
        (
            14,
            "Nike.  Flex Control 4",
            "Breathable mesh uppers combined with synthetic overlays to ensure long-lasting wear. Rounded-toe design with synthetic reinforcement. Lace-up closure with medial strap holds your foot in place.",
            51000,
            "https://m.media-amazon.com/images/I/81KY77cketL._SX700_.jpg",
            "blue, red, orange, white, black",
            "39,42,43,44,46,47",
            1

        ),
        (
            15,
            "Under Armour. Charged Commit TR 2.0",
            "Get back on the grind and stay on it with the Under Armour® Charged Commit TR 2.0 trainers. Leather heel saddle provides comfortable, custom fitting support for lifting and resistance with mesh under layer for breathability.",
            69000,
            "https://m.media-amazon.com/images/I/71AjhPnMRCL._SX700_.jpg",
            "orange, red, pink, white",
            "39,40,41,42,43,44",
            2

        ),
        (
            16,
            "CL By Laundry. Caring",
            "Your chic sense of style shows when you step out in the CL By Laundry® Caring booties featuring an animal pattern throughout in a synthetic upper. Slip-on, pointed-toe silhouette with V-cutout design. Synthetic lining and cushioned footbed.",
            108000,
            "https://m.media-amazon.com/images/I/71B5iLbbfFL._SX700_.jpg",
            "beige snake, beige dot cheetah, black",
            "38,39,40,41,42,43,44",
            2

        ),
        (
            17,
            "Sam Edelman. Patti Ankle Strap Heeled Sandal",
            "With an adjustable ankle strap and single vamp strap, the Sam Edelman® Patti sandals are a sexy shoe choice thatll take an outfit from ho-hum to va-va-voom.",
            83000,
            "https://m.media-amazon.com/images/I/81f1a0q4viL._SX700_.jpg",
            "sand leopard, black patent, classic nude, light gold leather",
            "39,40,41,42,43,44",
            2
        ),

        (
            18,
            "Clarks. Annadel Eirwyn",
            "Darling, show em whatcha got in the flattering Annadel Eirwyn wedge by Clarks®. Combination upper depending on the color you choose. Hook-and-loop closure.",
            61000,
            "https://m.media-amazon.com/images/I/81MZ8neRQKL._SX700_.jpg",
            "classic nude, sand, black nubuck, gold metallic",
            "39,40,41,42,43,44",
            2
        ),

        (
            19,
            "Steve Madden. Irenee Sandal",
            "DNNDNDNDNDNNDNDNDND",
            91000,
            "https://m.media-amazon.com/images/I/71T88gTjHCL._SX700_.jpg",
            "black, white, bone croco, clear, fuchsia, gold snake",
            "39,40,41,42,43,44",
            2

        ),

        (
            20,
            "Steve Madden. Catia Wedge Sandal",
            "Espadrille sandal features a leather upper. Ankle strap with adjustable buckle closure. Open-toe silhouette.",
            67500,
            "https://m.media-amazon.com/images/I/71JBWboI4gL._SX700_.jpg",
            "natural leather, black leather, snake, white",
            "39,40,41,42,43,44",
            2
        ),

        (
            21,
            "Crocs. Monterey Diamante Slip-On Wedge",
            "QGGQGQGQGQGGQGQGQGQ",
            21000,
            "https://m.media-amazon.com/images/I/71DadOYQnzL._SX700_.jpg",
            "navy, black",
            "39,40,41,42,43,44",
            2
        ),

        (
            22,
            "Blue by Betsey Johnson. Mari Heeled Sandal",
            "Upper made of fabric with sparkling rhinestone detail. Buckle closure at ankle. Synthetic lining.",
            121000,
            "https://m.media-amazon.com/images/I/71Rht5kwNVL._SX700_.jpg",
            "black, white, pink, pink 2, green, navy, blue, gold",
            "39,40,41,42,43,44",
            2

        ),

        (
            23,
            "UGG Kids. Kolding (Infant/Toddler)",
            "Faux-leather upper with multi-colored straps for added fun. Adjustable hook-and-loop strap provides a comfortable fit.",
            14000,
            "https://m.media-amazon.com/images/I/81viaOMJASL._SX700_.jpg",
            "white, navy",
            "16,18,19,20",
            3

        ),

        (
            24,
            "UGG Kids. Allairey (Infant/Toddler)",
            "Shell be ready for carefree days with the Allairey sandal from UGG® Kids.",
            19000,
            "https://m.media-amazon.com/images/I/81CD5HgAiAL._SX700_.jpg",
            "pink, yellow, red, white",
            "16,18,19,20,21,22",
            3

        ),

        (
            25,
            "UGG Kids Fluff Yeah Slide (Infant/Toddler)",
            "Just like Mommy! From parties to playdates, keep those tiny tootsies toastie with the adorable UGG® Kids Fluff Yeah Slide slipper sandal!",
            33000,
            "https://m.media-amazon.com/images/I/71CTLljiSML._SX700_.jpg",
            "black, ribbon red, charcoal",
            "16,17,18,19,20",
            3

        ),

        (
            26,
            "UGG Kids. Roos (Infant/Toddler)",
            "The UGG® Kids Roos booties will spoil their tiny toes with soft suede and the coziest fleece. Suede upper with printed UGG® logo across vamp. Medial and lateral hook-and-loop closure straps for easy on and off. Elastic gore",
            29000,
            "https://m.media-amazon.com/images/I/81EsV6X2J8L._SX700_.jpg",
            "black, white, pink, fuchsia",
            "16,18,19,20",
            3

        ),

        (
            27,
            "Livie & Luca. Fleur (Infant)",
            "Perfect for this season, the Livie & Luca® Fleur bootie will support your little love while she explores the world of first steps. Crafted from a shimmering suede leather upper with scalloped detailing. A wide hook-and-loop closure strap secures little feet.",
            36000,
            "https://m.media-amazon.com/images/I/711wj7mvQtL._SX700_.jpg",
            "desert rose, black, white",
            "16,18,19,20,21,22,23",
            3

        ),

        (
            28,
            "Nike. Air Monarch IV",
            "Get the royal treatment every time you train in the Air Monarch IV from Nike®.",
            53000,
            "https://m.media-amazon.com/images/I/81wTP6n94lL._SX700_.jpg",
            "black, white, cool grey, navy",
            "39,40,41,42,43,44",
            1

        ),

        (
            29,
            "Vans. Classic Slip-On™ Core Classics",
            "Vans Classic Slip-On™ Core Classics are True To Size. These Vans may feel tight at first, but the material is expected to stretch. They are manufactured only for Medium Width, so if you have wider feet, we recommend going a 1/2 size up",
            58000,
            "https://m.media-amazon.com/images/I/81Ba5XgUvOL._SX700_.jpg",
            "charcoal, canvas, black, black and white checker",
            "39,40,41,42,43,44",
            1

        ),

        (
              30,
              "Vans. Authentic™",
              "With roots firmly entrenched in So.Cal surf and skate style but embraced around the world, stay true with the clean, classic, and uncompromising aesthetic of the Vans® Authentic™ shoe!",
              49000,
              "https://m.media-amazon.com/images/I/81pVbGzmvWL._SX700_.jpg",
              "black, white, marshmallow, gum, parisian night, multi, ebony",
              "39,40,41,42",
              1
        )
    ]

    c.executemany(
        'INSERT INTO api_product(id, name, description, price, image, color, size, category_id)'
        'VALUES(?,?,?,?,?,?,?,?);', products)
    conn.commit()
    conn.close()
