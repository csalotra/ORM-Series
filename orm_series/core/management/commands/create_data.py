from django.core.management.base import BaseCommand
from core.models import Restaurant, Ratings, Sale
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
from django.db import transaction
from dotenv import load_dotenv
import os
import random

load_dotenv()

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
DEFAULT_UPASSWORD = os.getenv("DEFAULT_UPASSWORD")

class Command(BaseCommand):
  help = "Helps create application data"

  def handle(self, *args, **options):
    #get or create an admin user

    admin = User.objects.filter(username = ADMIN_USERNAME)

    if not admin.exists():
      admin = User.objects.create_superuser(
        username= ADMIN_USERNAME,
        password= ADMIN_PASSWORD
      )
    else:
      self.stdout.write("Admin user already exists")

    usernames = ["john", "jane", "alice", "bob", "charlie", "david"]

    for user in usernames:
      if User.objects.filter(username=user).exists():
          self.stdout.write(f"User already exists: {user}")
          continue
      User.objects.create_user(
        username= user,
        password=DEFAULT_UPASSWORD
      )

    restaurants = [
      {"name":"Pizza Pizza","website":"https://pizzapizza.com","date_opened":timezone.now()-timezone.timedelta(days=2),"longitude":-45,"latitude":-12,"restaurant_type":Restaurant.TypeChoices.ITALIAN},
      {"name":"Spice Route","website":"https://spiceroute.com","date_opened":timezone.now()-timezone.timedelta(days=4),"longitude":-79.38,"latitude":43.65,"restaurant_type":Restaurant.TypeChoices.INDIAN},
      {"name":"Golden Dragon","website":"https://goldendragon.com","date_opened":timezone.now()-timezone.timedelta(days=6),"longitude":-123.12,"latitude":49.28,"restaurant_type":Restaurant.TypeChoices.CHINESE},
      {"name":"El Sombrero","website":"https://elsombrero.com","date_opened":timezone.now()-timezone.timedelta(days=8),"longitude":-99.13,"latitude":19.43,"restaurant_type":Restaurant.TypeChoices.MEXICAN},
      {"name":"Athens Grill","website":"https://athensgrill.com","date_opened":timezone.now()-timezone.timedelta(days=10),"longitude":23.72,"latitude":37.98,"restaurant_type":Restaurant.TypeChoices.GREEK},
      {"name":"Burger Hub","website":"https://burgerhub.com","date_opened":timezone.now()-timezone.timedelta(days=12),"longitude":-73.56,"latitude":45.50,"restaurant_type":Restaurant.TypeChoices.FASTFOOD},
      {"name":"Urban Bites","website":"https://urbanbites.com","date_opened":timezone.now()-timezone.timedelta(days=14),"longitude":-75.69,"latitude":45.42,"restaurant_type":Restaurant.TypeChoices.OTHER},
      {"name":"Bombay Palace","website":"https://bombaypalace.com","date_opened":timezone.now()-timezone.timedelta(days=16),"longitude":72.87,"latitude":19.07,"restaurant_type":Restaurant.TypeChoices.INDIAN},
      {"name":"Pasta Fresca","website":"https://pastafresca.com","date_opened":timezone.now()-timezone.timedelta(days=18),"longitude":12.49,"latitude":41.89,"restaurant_type":Restaurant.TypeChoices.ITALIAN},
      {"name":"Wok Express","website":"https://wokexpress.com","date_opened":timezone.now()-timezone.timedelta(days=20),"longitude":116.40,"latitude":39.90,"restaurant_type":Restaurant.TypeChoices.CHINESE},
      {"name":"Taco Fiesta","website":"https://tacofiesta.com","date_opened":timezone.now()-timezone.timedelta(days=22),"longitude":-103.35,"latitude":20.67,"restaurant_type":Restaurant.TypeChoices.MEXICAN},
      {"name":"Olympus Taverna","website":"https://olympustaverna.com","date_opened":timezone.now()-timezone.timedelta(days=24),"longitude":22.94,"latitude":40.64,"restaurant_type":Restaurant.TypeChoices.GREEK},
      {"name":"Fry Nation","website":"https://frynation.com","date_opened":timezone.now()-timezone.timedelta(days=26),"longitude":-118.24,"latitude":34.05,"restaurant_type":Restaurant.TypeChoices.FASTFOOD},
      {"name":"Daily Kitchen","website":"https://dailykitchen.com","date_opened":timezone.now()-timezone.timedelta(days=28),"longitude":-0.12,"latitude":51.50,"restaurant_type":Restaurant.TypeChoices.OTHER},
      {"name":"Curry Leaf","website":"https://curryleaf.com","date_opened":timezone.now()-timezone.timedelta(days=30),"longitude":77.59,"latitude":12.97,"restaurant_type":Restaurant.TypeChoices.INDIAN},
      {"name":"Trattoria Roma","website":"https://trattoriaroma.com","date_opened":timezone.now()-timezone.timedelta(days=32),"longitude":9.19,"latitude":45.46,"restaurant_type":Restaurant.TypeChoices.ITALIAN},
      {"name":"Dragon Pearl","website":"https://dragonpearl.com","date_opened":timezone.now()-timezone.timedelta(days=34),"longitude":121.47,"latitude":31.23,"restaurant_type":Restaurant.TypeChoices.CHINESE},
      {"name":"Casa Maya","website":"https://casamaya.com","date_opened":timezone.now()-timezone.timedelta(days=36),"longitude":-89.62,"latitude":20.97,"restaurant_type":Restaurant.TypeChoices.MEXICAN},
      {"name":"Santorini Eats","website":"https://santorinieats.com","date_opened":timezone.now()-timezone.timedelta(days=38),"longitude":25.46,"latitude":36.39,"restaurant_type":Restaurant.TypeChoices.GREEK},
      {"name":"Quick Buns","website":"https://quickbuns.com","date_opened":timezone.now()-timezone.timedelta(days=40),"longitude":-87.62,"latitude":41.88,"restaurant_type":Restaurant.TypeChoices.FASTFOOD},
      {"name":"Street Table","website":"https://streettable.com","date_opened":timezone.now()-timezone.timedelta(days=42),"longitude":139.69,"latitude":35.68,"restaurant_type":Restaurant.TypeChoices.OTHER},
      {"name":"Masala Street","website":"https://masalastreet.com","date_opened":timezone.now()-timezone.timedelta(days=44),"longitude":78.48,"latitude":17.38,"restaurant_type":Restaurant.TypeChoices.INDIAN},
      {"name":"Olive Gardenia","website":"https://olivegardenia.com","date_opened":timezone.now()-timezone.timedelta(days=46),"longitude":14.27,"latitude":40.85,"restaurant_type":Restaurant.TypeChoices.ITALIAN},
      {"name":"Red Lantern","website":"https://redlantern.com","date_opened":timezone.now()-timezone.timedelta(days=48),"longitude":114.16,"latitude":22.32,"restaurant_type":Restaurant.TypeChoices.CHINESE},
      {"name":"Burrito Bros","website":"https://burritobros.com","date_opened":timezone.now()-timezone.timedelta(days=50),"longitude":-111.89,"latitude":40.76,"restaurant_type":Restaurant.TypeChoices.MEXICAN},
      {"name":"Mykonos Plate","website":"https://mykonosplate.com","date_opened":timezone.now()-timezone.timedelta(days=52),"longitude":25.33,"latitude":37.44,"restaurant_type":Restaurant.TypeChoices.GREEK},
      {"name":"Snack Stop","website":"https://snackstop.com","date_opened":timezone.now()-timezone.timedelta(days=54),"longitude":-95.36,"latitude":29.76,"restaurant_type":Restaurant.TypeChoices.FASTFOOD},
      {"name":"Local Spoon","website":"https://localspoon.com","date_opened":timezone.now()-timezone.timedelta(days=56),"longitude":151.21,"latitude":-33.86,"restaurant_type":Restaurant.TypeChoices.OTHER},
      {"name":"Tandoor House","website":"https://tandoorhouse.com","date_opened":timezone.now()-timezone.timedelta(days=58),"longitude":73.85,"latitude":18.52,"restaurant_type":Restaurant.TypeChoices.INDIAN},
      {"name":"Bella Cucina","website":"https://bellacucina.com","date_opened":timezone.now()-timezone.timedelta(days=60),"longitude":11.25,"latitude":43.77,"restaurant_type":Restaurant.TypeChoices.ITALIAN},
      {"name":"Lotus Wok","website":"https://lotuswok.com","date_opened":timezone.now()-timezone.timedelta(days=62),"longitude":103.85,"latitude":1.29,"restaurant_type":Restaurant.TypeChoices.CHINESE},
      {"name":"Aztec Grill","website":"https://aztecgrill.com","date_opened":timezone.now()-timezone.timedelta(days=64),"longitude":-90.51,"latitude":14.64,"restaurant_type":Restaurant.TypeChoices.MEXICAN},
      {"name":"Hellas Kitchen","website":"https://hellaskitchen.com","date_opened":timezone.now()-timezone.timedelta(days=66),"longitude":21.82,"latitude":39.07,"restaurant_type":Restaurant.TypeChoices.GREEK},
      {"name":"Fast Cravings","website":"https://fastcravings.com","date_opened":timezone.now()-timezone.timedelta(days=68),"longitude":-84.39,"latitude":33.75,"restaurant_type":Restaurant.TypeChoices.FASTFOOD},
      {"name":"Open Fork","website":"https://openfork.com","date_opened":timezone.now()-timezone.timedelta(days=70),"longitude":-3.70,"latitude":40.41,"restaurant_type":Restaurant.TypeChoices.OTHER},
      {"name":"Royal Curry","website":"https://royalcurry.com","date_opened":timezone.now()-timezone.timedelta(days=72),"longitude":74.35,"latitude":31.52,"restaurant_type":Restaurant.TypeChoices.INDIAN},
      {"name":"Napoli Stone","website":"https://napolistone.com","date_opened":timezone.now()-timezone.timedelta(days=74),"longitude":14.26,"latitude":40.84,"restaurant_type":Restaurant.TypeChoices.ITALIAN},
      {"name":"Mandarin Bowl","website":"https://mandarinbowl.com","date_opened":timezone.now()-timezone.timedelta(days=76),"longitude":104.06,"latitude":30.67,"restaurant_type":Restaurant.TypeChoices.CHINESE},
      {"name":"Chili Loco","website":"https://chililoco.com","date_opened":timezone.now()-timezone.timedelta(days=78),"longitude":-106.48,"latitude":31.76,"restaurant_type":Restaurant.TypeChoices.MEXICAN},
      {"name":"Zeus Feast","website":"https://zeusfeast.com","date_opened":timezone.now()-timezone.timedelta(days=80),"longitude":24.94,"latitude":37.98,"restaurant_type":Restaurant.TypeChoices.GREEK},
      {"name":"Speedy Eats","website":"https://speedyeats.com","date_opened":timezone.now()-timezone.timedelta(days=82),"longitude":-122.41,"latitude":37.77,"restaurant_type":Restaurant.TypeChoices.FASTFOOD},
      {"name":"Plate & Co","website":"https://plateandco.com","date_opened":timezone.now()-timezone.timedelta(days=84),"longitude":-46.63,"latitude":-23.55,"restaurant_type":Restaurant.TypeChoices.OTHER},
      {"name":"Delhi Junction","website":"https://delhijunction.com","date_opened":timezone.now()-timezone.timedelta(days=86),"longitude":77.21,"latitude":28.61,"restaurant_type":Restaurant.TypeChoices.INDIAN},
      {"name":"Tuscan Yard","website":"https://tuscanyard.com","date_opened":timezone.now()-timezone.timedelta(days=88),"longitude":10.40,"latitude":43.72,"restaurant_type":Restaurant.TypeChoices.ITALIAN},
      {"name":"Jade Pavilion","website":"https://jadepavilion.com","date_opened":timezone.now()-timezone.timedelta(days=90),"longitude":113.26,"latitude":23.13,"restaurant_type":Restaurant.TypeChoices.CHINESE},
      {"name":"Rio Cantina","website":"https://riocantina.com","date_opened":timezone.now()-timezone.timedelta(days=92),"longitude":-43.17,"latitude":-22.90,"restaurant_type":Restaurant.TypeChoices.MEXICAN},
      {"name":"Greek Roots","website":"https://greekroots.com","date_opened":timezone.now()-timezone.timedelta(days=94),"longitude":23.73,"latitude":37.97,"restaurant_type":Restaurant.TypeChoices.GREEK},
      {"name":"Grab & Go","website":"https://grabngo.com","date_opened":timezone.now()-timezone.timedelta(days=96),"longitude":-71.06,"latitude":42.36,"restaurant_type":Restaurant.TypeChoices.FASTFOOD},
      {"name":"Common Table","website":"https://commontable.com","date_opened":timezone.now()-timezone.timedelta(days=98),"longitude":18.42,"latitude":-33.92,"restaurant_type":Restaurant.TypeChoices.OTHER},
    ]

    ## Create restaurants

    Restaurant.objects.all().delete() #delete data before inserting new 

    """
    Create restaurants 
    
    Method 1: Bulk Create, Efficient method with single query, 
    -> but it will not do save() override, 
    -> will not add many to many fields (needs to add manually), 
    -> In some cases will not return Auto fields like Ids(But depends on databse and dDjango version)
    -> It skips validators in the model fields

    """

    restaurants_list = [Restaurant(**data) for data in restaurants]

    # As bulk_create skips validators, we can add 

    for restaurant in restaurants_list:
      restaurant.full_clean()          # runs validators on each object

    with transaction.atomic():
      Restaurant.objects.bulk_create(restaurants_list)


    """
    Method 2: .create() for each record, it is inefficient method and will execute N database queries
    """

    # for data in restaurants:
    #   Restaurant.objects.create(**data)


    restaurants_retrieved = Restaurant.objects.all()
    users = User.objects.all()

    ## Create Ratings
    for _ in range(100):
      Ratings.objects.create(
        user = random.choice(users),
        restaurant = random.choice(restaurants_retrieved),
        rating = random.randint(1,5)
      )

    ## Create Sales
    for _ in range(100):
      Sale.objects.create(
        restaurant = random.choice(restaurants_retrieved),
        income = random.uniform(25, 500),
        datetime = timezone.now() - timezone.timedelta(days = random.randint(1,50))
      )


