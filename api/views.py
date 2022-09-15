from rest_framework import viewsets, serializers, status, permissions
from rest_framework.response import Response
from django.db import transaction

from api.models import Coin, Product
from api.serializers import CoinSerializer, LoginSerializer, ProductSerializer

class LoginView(viewsets.ViewSet):
    serializer_class = LoginSerializer

    def login(self, request):
        try:
            data={'username': request.data['username'], 'password': request.data['password']}
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data
            return Response({'Success': True, 'data': user, 'message':'Authenticated successfully'}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'Success': False, 'message':'Authentication Failed'}, status=status.HTTP_401_UNAUTHORIZED)

# products view
class ProductView(viewsets.ViewSet):
    serializer_class = ProductSerializer
    
    # fetch products and serialize 
    def list(self):
        try:
            products = Product.objects.all()
            serializer = self.serializer_class(products, many=True)
            return Response({
                'success': True, 
                'message':'products fetched successfully', 
                'data': serializer.data
                })

        except Exception as e:
            print(e)
            return Response({
                'success': False, 
                'message':'Failed to fetch products', 
            }, status=500 )



class ProductActionsView(viewsets.ViewSet):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    # add Products
    def create(self, request):
        try:
            with transaction.atomic():
                data = request.data.copy()
                serializer = self.serializer_class(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({'success': True, 'message':'Product added successfully', 'data': serializer.data})

        except serializers.ValidationError as ve:
            print(ve)
            return Response({'success':False, "message":'Some field(s) are incorrect'}, status=status.HTTP_400_BAD_REQUEST )
        
        except Exception as e:
            print(e)
            return Response({'success':False, "message":'Failed to add product'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR )
    
   
    # update product
    def update(self, request, *args, **kwargs):
        try:
            product = Product.objects.get(id=request.data['id'])
            serializer = self.serializer_class(product, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'success':True, 'message': 'Updated Product Successfully', 'data':serializer.data})
        
        except serializers.ValidationError as ve:
            print('product update err', ve)
            return Response({'success':False, 'message': 'Encountered field(s) error...'},status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print('update failed',e)
            return Response({'success':False, 'message': 'Product update Failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# coins view
class CoinView(viewsets.ViewSet):
    serializer_class = CoinSerializer

    # fetch coins and serialize 
    def list(self, request):
        try:
            coins = Coin.objects.all()
            serializer = self.serializer_class(coins, many=True)
            return Response({
                'success': True, 
                'message':'coins fetched successfully', 
                'data': serializer.data
                })

        except Exception as e:
            print(e)
            return Response({
                'success': False, 
                'message':'Failed to fetch coins', 
            }, status=500 )



class CoinActionsView(viewsets.ViewSet):
    serializer_class = CoinSerializer   
    permission_classes = [permissions.IsAuthenticated]

    # add coins
    def create(self, request):
        try:
            with transaction.atomic():
                data = request.data.copy()
                serializer = self.serializer_class(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({'success': True, 'message':'coin type added successfully', 'data':serializer.data})

        except serializers.ValidationError as ve:
            print(ve)
            return Response({'success':False, "message":'Some field(s) are incorrect'}, status=status.HTTP_400_BAD_REQUEST )
        
        except Exception as e:
            print(e)
            return Response({'success':False, "message":'Failed to add coin'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR )

    
    # update coin
    def update(self, request, *args, **kwargs):
        try:
            coin = Coin.objects.get(id=request.data['id'])
            serializer = self.serializer_class(coin, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'success':True, 'message': 'Updated Coin Successfully', 'data':serializer.data})
        
        except serializers.ValidationError as ve:
            print('coin update err', ve)
            return Response({'success':False, 'message': 'Encountered field(s) error...'},status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print('coin failed',e)
            return Response({'success':False, 'message': 'Coin update Failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class PurchaseProductView(viewsets.ViewSet):
    # purchase product
    def purchase(self, request):
        try:
            data = request.data.copy()
            coins = Coin.objects.all()
            product = Product.objects.get(id=int(data.get('product')))
            
            # check if product exists and is in stock
            if product and product.num > 0:

                coin_type = coins.get(id=int(data.get('coin_type')))
                num_of_coins = data.get('num_of_coins')  # number of coin user input
                user_coin_value = int(num_of_coins) * coin_type.value  # calculate user input coin value
                change = user_coin_value - product.price  # calculate change

                if change > 0:
                    try:
                        with transaction.atomic():
                            coins_list = []
                            coins_init_state = []
                            __change = change
                            for coin in coins:
                                if coin.value < __change:   # check coin value to less than change
                                    coins_to_return = {}
                                    unit_coin_init_state_dict = {}

                                    __change_remainder = __change % coin.value    # get the remaining change value
                                    returnable_coins_count = (__change - __change_remainder) / coin.value  # number of coin to return

                                    coins_to_return['coin type'] = coin.type    
                                    coins_to_return['number of coins'] = int(returnable_coins_count)
                                    coins_list.append(coins_to_return)      # coins to return list

                                    unit_coin_init_state_dict['id'] = coin.id        # store coins id
                                    unit_coin_init_state_dict['num'] = coin.num        # store initial coins count
                                    coins_init_state.append(unit_coin_init_state_dict)

                                    __change = __change_remainder
                                    coin.num -= returnable_coins_count      # update number of coins
                                    coin.save()

                            if __change == 0:
                                product.num -= 1    # update number of coins
                                product.save()
                                return Response({'success': True, 'Message':'Transaction Complete Successfully', 'data':coins_list})

                            else:
                                # reverse coins to their initial count if the change is not divisible by the coins value available
                                for coin in coins:
                                    for item in coins_init_state:
                                        if int(item['id']) == coin.id:
                                            coin.num = int(item['num'])
                                            coin.save()

                                return Response({'success': False, 'Message':'Sorry... cannot process the exact coins change'})

                    except Exception as e:
                        print('update coins',e)
                        return Response({'success': False, 'Message':'Sorry... cannot process the exact coins change'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR )

                else:
                    return Response({'success':False, "message":'Amount paid is less than the actual product price'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR )

            else:
                return Response({'success':False, "message":'Product is out of stock'}, status=status.HTTP_204_NO_CONTENT )


        except Exception as e:
            print(e)
            return Response({'success':False, "message":'Failed to buy product'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR )
 
