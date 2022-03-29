from main import redis, Order
import time

key = 'refund_order'
group = 'order-group'

try:
    redis.xgroup_create(key, group)
except:
    print('Group already exist')

while True:
    try:
        results = redis.xreadgroup(group, key, {key: '>'}, None)

        if results != []:
            for result in results:
                obj = result[1][0][1]
                product = Order.get(obj['product_id'])
                
                if product:
                    product.quantity = product.quantity - int(obj['quantity'])
                    product.save()
                else:
                    redis.xadd('refund_order', obj, "*")
        print(result)
    except Exception as e:
        print(str(e))
    time.sleep(1)