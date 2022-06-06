import gspread, json, time, requests, math
from oauth2client.service_account import ServiceAccountCredentials
from alive import keep_alive

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("key.json", scope)

client = gspread.authorize(creds)

sheet = client.open("ZTrade Price List").sheet1

rate = 0.5

univ = (100-rate)/100

items = [('186', 'Sheep Plushie', 'Plushie', (2, 2), None),
         ('187', 'Teddy Bear Plushie', 'Plushie', (3, 2), None), 
         ('215', 'Kitten Plushie', 'Plushie', (4, 2), None), 
         ('258', 'Jaguar Plushie', 'Plushie', (5, 2), None), 
         ('261', 'Wolverine Plushie', 'Plushie', (6, 2), None), 
         ('266', 'Nessie Plushie', 'Plushie', (7, 2), None), 
         ('268', 'Red Fox Plushie', 'Plushie', (8, 2), None), 
         ('269', 'Monkey Plushie', 'Plushie', (9, 2), None), 
         ('273', 'Chamois Plushie', 'Plushie', (10, 2), None), 
         ('274', 'Panda Plushie', 'Plushie', (11, 2), None), 
         ('281', 'Lion Plushie', 'Plushie', (12, 2), None), 
         ('384', 'Camel Plushie', 'Plushie', (13, 2), None), 
         ('618', 'Stingray Plushie', 'Plushie', (14, 2), None), 
         
         ('260', 'Dahlia', 'FLower', (2, 5), None), 
         ('263', 'Crocus', 'FLower', (3, 5), None), 
         ('264', 'Orchid', 'FLower', (4, 5), None), 
         ('267', 'Heather', 'FLower', (5, 5), None), 
         ('271', 'Ceibo Flower', 'FLower', (6, 5), None), 
         ('272', 'Edelweiss', 'FLower', (7, 5), None), 
         ('276', 'Peony', 'FLower', (8, 5), None), 
         ('277', 'Cherry Blossom', 'FLower', (9, 5), None), 
         ('282', 'African Violet', 'FLower', (10, 5), None), 
         ('385', 'Tribulus Omanense', 'FLower', (11, 5), None), 
         ('617', 'Banana Orchid', 'FLower', (12, 5), None), 
         
         ('530', 'Can of Munster', 'Energy Drink', (5, 8), 3),
         ('532', 'Can of Red Cow', 'Energy Drink', (6, 8), 3),
         ('533', 'Can of Taurine Elite', 'Energy Drink', (7, 8), 3),
         ('553', 'Can of Santa Shooters', 'Energy Drink', (8, 8), 3),
         ('554', 'Can of Rockstar Rudolph', 'Energy Drink', (9, 8), 3),
         ('555', 'Can of X-MASS', 'Energy Drink', (10, 8), 3),
         ('985', 'Can of Goose Juice', 'Energy Drink', (11, 8), 3),
         ('986', 'Can of Damp Valley', 'Energy Drink', (12, 8), 3),
         ('987', 'Can of Crocozade', 'Energy Drink', (13, 8), 3),
         
         ('206', 'Xanax', 'Drug', (22, 2), 2),
         
         ('367', 'Feathery Hotel Coupon', 'Booster', (19, 2), 2),
         ('366', 'Erotic DVD', 'Booster', (18, 2), 2),
         
         ('180', 'Bottle of Beer', 'Alcohol', (17, 5), None), 
         ('181', 'Bottle of Champagne', 'Alcohol', (18, 5), 2), 
         ('294', 'Bottle of Sake', 'Alcohol', (19, 5), 2), 
         ('426', 'Bottle of Tequila', 'Alcohol', (20, 5), 2), 
         ('531', 'Bottle of Pumpkin Brew', 'Alcohol', (21, 5), 2), 
         ('541', 'Bottle of Stinky Swamp Punch', 'Alcohol', (22, 5), 2), 
         ('542', 'Bottle of Wicked Witch', 'Alcohol', (23, 5), 2), 
         ('550', 'Bottle of Kandy Kane', 'Alcohol', (24, 5), 2), 
         ('551', 'Bottle of Minty Mayhem', 'Alcohol', (25, 5), 2), 
         ('552', 'Bottle of Mistletoe Madness', 'Alcohol', (26, 5), 2), 
         ('638', 'Bottle of Christmas Cocktail', 'Alcohol', (27, 5), 2), 
         ('873', 'Bottle of Green Stout', 'Alcohol', (28, 5), 2), 
         ('924', 'Bottle of Christmas Spirit', 'Alcohol', (29, 5), 2), 
         ('984', 'Bottle of Moonshine', 'Alcohol', (30, 5), 2), 

         ('818', 'Six Pack of Alcohol', 'Supply', (19, 8), 3),
         
         ('283', 'Donator Pack', 'Supply', (20, 8), 2),

         ('35', 'Box of Chocolate Bars', 'Candy', (23, 8), 3),
         ('36', 'Big Box of Chocolate Bars', 'Candy', (24, 8), 3),
         ('37', 'Bag of Bon Bons', 'Candy', (25, 8), 3),
         ('38', 'Box of Bon Bons', 'Candy', (26, 8), 3),
         ('39', 'Box of Extra Strong Mints', 'Candy', (27, 8), 3),
         ('151', 'Pixie Sticks', 'Candy', (28, 8), 4),
         ('209', 'Box of Sweet Hearts', 'Candy', (29, 8), 3),
         ('210', 'Bag of Chocolate Kisses', 'Candy', (30, 8), 3),
         ('310', 'Lollipop', 'Candy', (31, 8), 2),
         ('527', 'Bag of Candy Kisses', 'Candy', (32, 8), 3),
         ('528', 'Bag of Tootsie Rolls', 'Candy', (33, 8), 3),
         ('529', 'Bag of Chocolate Truffles', 'Candy', (34, 8), 3),
         ('556', 'Bag of Reindeer Droppings', 'Candy', (35, 8), 3),
         ('586', 'Jawbreaker', 'Candy', (36, 8), 4),
         ('587', 'Bag of Sherbet', 'Candy', (37, 8), 3),
         ('634', 'Bag of Bloody Eyeballs', 'Candy', (38, 8), 3),
         ('1028', 'Birthday Cupcake', 'Candy', (39, 8), 4),
         ('1039', 'Bag of Humbugs', 'Candy', (40, 8), 3),
         
         
         ]



keep_alive()
def main():
  while True:
    try:
      for i in items:

        response = requests.get(f'https://api.torn.com/market/{i[0]}?selections=bazaar,itemmarket&key=8oGWP17leHxNlh4g').json()

        nres = requests.get(f'https://api.torn.com/torn/{i[0]}?selections=items&key=8oGWP17leHxNlh4g').json()

        bprice = response['bazaar'][0]['cost']
        iprice = response['itemmarket'][0]['cost']
        value = nres['items'][i[0]]['market_value']


        if not bprice: bprice = 0
        if not iprice: iprice = 0
        if not value: value = 0
        priceOrd = [bprice,iprice, value]
        priceOrd.sort()
        price = min(bprice,iprice,value)
        price = max(price, 0.9*value)
        rateItem = univ
        if i[4]:
          rateItem = (100 - i[4])/100

        price = "{:,}".format(math.ceil(rateItem*price))
        row, column = i[3]
        sheet.update_cell(row,column, price)
        print(i)
        time.sleep(3)

      time.sleep(300)

    except:
      time.sleep(60)
      print('Error')
      print(i)
      continue
      
 
if __name__ == "__main__":
  main()
    