from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Order, Job
from .serializer import OrderSerializers, JobSerializes
from .helper import parse_duration, create_coordinate, calculate_duration, sort_orders

@api_view(['GET'])
def list_order(req):
    queryset = Order.objects.all()
    filter_params = {
        'name': 'name__icontains',
        'phone': 'phone__icontains',
        'status': 'status__iexact',
        'price': 'price',
        'address': 'address__icontains',
    }
    
    for param, lookup in filter_params.items():
        val = req.query_params.get(param)
        if val:
            queryset = queryset.filter(**{lookup: val})
            
    order_fields = []
    for order_param in ['order_by_price', 'order_by_status', 'order_by_name', 'order_by_duration']:
        order_direction = req.query_params.get(order_param)
        if order_direction == 'asc':
            if order_param == 'order_by_duration':
                queryset = sorted(queryset, key=lambda x: parse_duration(x.duration))
            else:
                order_fields.append(order_param.split('_')[2]) 
        elif order_direction == 'desc':
            if order_param == 'order_by_duration':
                queryset = sorted(queryset, key=lambda x: parse_duration(x.duration), reverse=True)
            else:
                order_fields.append(f'-{order_param.split("_")[2]}')
    if order_fields:
        queryset = queryset.order_by(*order_fields)
        
    serializer = OrderSerializers(queryset, many=True)
    return Response({'data': serializer.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_order(req):
    coordinate = create_coordinate(req.data.get('address'))
    if not coordinate:
        return Response({'message': 'Invalid address. Could not retrieve coordinates.'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        job = Job.objects.get(id=req.data.get('job_id'))
    except Job.DoesNotExist:
        return Response({'message': 'Job not found'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        duration = calculate_duration(
            (coordinate.latitude, coordinate.longitude),
            (job.coordinate.latitude, job.coordinate.longitude)
            )
    except ValueError as e:
        return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    data = {**req.data, 'coordinate': coordinate.id, 'duration': duration}
    serializer = OrderSerializers(data=data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT'])
def update_order(req, id):
    try:
        order = Order.objects.get(id=id)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
    if req.method == 'GET':        
        return Response({ 'data' : OrderSerializers(order).data})

    serializer = OrderSerializers(order, data=req.data, partial=True)  # Use partial=True to allow partial updates
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_job(req):
    coordinate = create_coordinate(req.data.get('address'))
    if not coordinate:
        return Response({'message': 'Invalid address. Could not retrieve coordinates.'}, status=status.HTTP_400_BAD_REQUEST)
    serializer = JobSerializes({**req.data, coordinate: coordinate.id })
    if serializer.is_valid():
        serializer.save()
        return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
    return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def sort_orders():
    queryset = Order.objects.all()
    return Response({ 'data': sort_orders(OrderSerializers(queryset, many=True).data)})