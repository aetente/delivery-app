# delivery-app

It is a delivery application backend written in Django.

To preload timeslots run:

```
python .\gen_timeslots.py
```

It will create fixtures json in deliveryapp/fixtures/timeslots.json
And then run:

```
python .\manage.py loaddata .\deliveryapp\fixtures\timeslots.json
```

I couldn't really find any specific "courier API", that would be useful generating timeslots or something like this,
so I made my own timeslots generation.

You will need environmental varibles called "GOOGLE_API" and "HOLIDAY_API"
for google gecoding and holiday api: https://holidayapi.com/docs

About the concurrent requests, I think that Django resolves request in a thread and not in paralell,
so if two consumers try to reserve one slot, it would first process one of them
and then based on the changes which were made, it would process the second request

# Methods

● POST /resolve-address - resolves a single line address into a structured address(See ‘Address’ model)

{

“searchTerm”: {SINGLE LINE ADDRESS}

}

● POST /timeslots - retrieve all available timeslots(See ‘Timeslot’ model) for a formatted address

{

“address”: {FORMATTED ADDRESS}

}

● POST /deliveries - book a delivery

{

“user”: {USER},

“timeslotId”: {TIMESLOT_ID}

}

● POST /deliveries/{DELIVERY_ID}/complete - mark a delivery as completed

● DELETE /deliveries/{DELIVERY_ID} - cancel a delivery

● GET /deliveries/daily - retrieve all today’s deliveries

● GET /deliveries/weekly - retrieve the deliveries for current week
