import requests
import time
import random

for i in range(50):
    params = {'flat_id': i}
    data = {
            "Car_Name": "Toyota Corolla",
            "Selling_Price": random.randint(1, 20),
            "Driven_kms": random.randint(1, 300000),
            "Fuel_Type": "Petrol",
            "Selling_type": "Dealer",
            "Transmission": "Manual",
            "Owner": 1
        } 
    response = requests.post('http://price-predict:8000/api/prediction', params=params, json=data)
    time.sleep(random.randint(1,5))
    print(response.json())