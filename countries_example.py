import datetime
from datetime import date
from diary.py import *

conn = get_conn()
prepare_schema(conn)

name = "Adam"
country = "Great Britain"
place = "London"
date_from = date(2019,4,5)
date_to = date(2019,4,16)
text = "London is the capital and largest city of England and the United Kingdom. The city stands on the River Thames in" \
       " the south-east of England, at the head of its 50-mile (80 km) estuary leading to the North Sea. London has been" \
       " a major settlement for two millennia."
insert_diary_record(conn,name,country,place,date_from,date_to,text)
print (list_diary_records_countries(conn,country))


"""Country  2"""
name = "Eva"
country = "Great Britain"
place = "Exeter"
date_from = date(2020,8,5)
date_to = date(2019,8,20)
text = " Exeter is a city in Devon, England, on the River Exe 36 miles (58 km) northeast of Plymouth and 65 miles (105 km) " \
       "southwest of Bristol. It is the county town of Devon, and home to Devon County Council and the University of " \
       "Exeter."
insert_diary_record(conn,name,country,place,date_from,date_to,text)
print (list_diary_records_countries(conn,country))
"""Country  1"""
name = "Paul"
country = "Great Britain"
place = "Leicester"
date_from = date(2018,7,5)
date_to = date(2018,7,16)
text = "Leicester is a city and unitary authority area in the East Midlands of England, and the county town of" \
       " Leicestershire. The city lies on the River Soar and close to the eastern end of the National Forest."
insert_diary_record(conn,name,country,place,date_from,date_to,text)
print (list_diary_records_countries(conn,country))
"""Country  2"""
name = "Susan"
country = "Angola"
place = "Angola"
date_from = date(2018,4,5)
date_to = date(2018,4,16)
text = " Angola large country, Angola takes in a broad variety of landscapes, including the semidesert Atlantic littoral " \
       "bordering Namibia's “Skeleton Coast,” the sparsely populated rainforest interior, the rugged highlands of the " \
       "south, the Cabinda exclave in the north, and the densely settled towns and cities of the northern coast"
insert_diary_record(conn,name,country,place,date_from,date_to,text)
print (list_diary_records_countries(conn,country))
"""Country  3"""
name = "Peter"
country = "Canada"
place = "Montreal"
date_from = date(2018,2,5)
date_to = date(2018,2,16)
text = "Montreal is a city in the country of Canada. It is the largest city in the province of Quebec and the " \
       "second-largest city in Canada. It is the second-largest French-speaking city in the world after Paris." \
       " Montreal is built on an island sitting in the Saint Lawrence River."
insert_diary_record(conn,name,country,place,date_from,date_to,text)
print (list_diary_records_countries(conn,country))

"""Country  5"""
name = "James"
country = "Czech Republic"
place = "Prague"
date_from = date(2020,2,5)
date_to = date(2020,2,16)
text = "Situated in the northwest of the country on the Vltava River, Prague is the capital and the largest city of " \
       "the Czech Republic. This magical city of bridges, cathedrals, gold-tipped towers and church spires is also " \
       "the fourteenth largest city in the European Union."
insert_diary_record(conn,name,country,place,date_from,date_to,text)
print (list_diary_records_countries(conn,country))
"""Country  6"""
name = "James"
country = "Italy"
place = "Venice"
date_from = date(2019,3,5)
date_to = date(2019,7,16)
text ="Venice is unique environmentally, architecturally, and historically, and in its days as a republic the city " \
      "was styled la serenissima (“the most serene” or “sublime”). It remains a major Italian port in the northern" \
      " Adriatic Sea and is one of the world's oldest tourist and cultural centres."
insert_diary_record(conn,name,country,place,date_from,date_to,text)
print (list_diary_records_countries(conn,country))
"""Country  7"""
name = "Lily"
country = "Japan"
place = "Tokio"
date_from = date(2020,9,5)
date_to = date(2020,9,16)
text ="Japan's capital and the world's most populous metropolis. It is also one of Japan's 47 prefectures, consisting" \
      " of 23 central city wards and multiple cities, towns and villages west of the city center. The Izu and Ogasawara" \
      " Islands are also part of Tokyo. Prior to 1868, Tokyo was known as Edo"
insert_diary_record(conn,name,country,place,date_from,date_to,text)
print (list_diary_records_countries(conn,country))
"""Country  8"""
name = "Lily"
country = "Russia"
place = "Petersburg"
date_from = date(2019,9,8)
date_to = date(2019,9,16)
text ="St. Petersburg is a mecca of cultural, historical, and architectural landmarks. Founded by Tsar Peter I " \
      "(the Great) as Russia's “window on Europe,” it bears the unofficial status of Russia's cultural capital and" \
      " most European city, a distinction that it strives to retain in its perennial competition with Moscow."
insert_diary_record(conn,name,country,place,date_from,date_to,text)
print (list_diary_records_countries(conn,country))
"""Country  9"""
name = "Sirius"
country = "Slovakia"
place = "Martin"
date_from = date(2019,12,8)
date_to = date(2019,12,16)
text = "Martin is a city in the northern Central Slovakia. It is the center of the Turiec region." \
       " It is on the Turiec river, between the Little Fatra and Great Fatra mountains. The population numbers " \
       "approximately 60,000, which makes it the eighth largest city in Slovakia."
insert_diary_record(conn,name,country,place,date_from,date_to,text)
print (list_diary_records_countries(conn,country))
"""Country  10"""
name = "Sirius"
country = "US"
place = "grand canyon"
date_from = date(2018,3,9)
date_to = date(2018,3,15)
text ="Grand Canyon is considered one of the finest examples of arid-land erosion in the world. " \
      "Incised by the Colorado River, the canyon is immense, averaging 4,000 feet deep for its entire 277 miles. " \
      "It is 6,000 feet deep at its deepest point and 18 miles at its widest"
print ("all")
print (list_diary_records_all(conn))
print ("random")
print (list_diary_records_random(conn))