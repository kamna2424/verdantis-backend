from .models import Plant

def run():
    plants = [
        {
            "name": "Aloe Vera",
            "description": "A low-maintenance plant that thrives in sunlight and requires minimal watering.",
            "image_url": "https://i.imgur.com/z6dYx4m.jpeg",
            "ideal_temp": 25,
            "ideal_humidity": 40,
            "ideal_moisture": 20,
            "ideal_ph": 7
        },
        {
            "name": "Basil",
            "description": "A fragrant herb that prefers warm climates and consistently moist soil.",
            "image_url": "https://i.imgur.com/ppcBf4d.jpeg",
            "ideal_temp": 22,
            "ideal_humidity": 60,
            "ideal_moisture": 40,
            "ideal_ph": 6.5
        },
        {
            "name": "Snake Plant",
            "description": "Hardy plant that tolerates low light and irregular watering.",
            "image_url": "https://i.imgur.com/1G6sWZx.jpeg",
            "ideal_temp": 23,
            "ideal_humidity": 35,
            "ideal_moisture": 15,
            "ideal_ph": 6
        },
        # ---- Add more later ----
    ]

    for p in plants:
        Plant.objects.get_or_create(name=p["name"], defaults=p)

    print("🌱 Plant database seeded successfully!")
