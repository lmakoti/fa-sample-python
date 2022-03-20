from fastapi import FastAPI
from pydantic import BaseModel
import starlette.responses as _responses
import requests #get the data from the worldtime api


app = FastAPI()

db = [] #in-memory database, list

#define city model (structure)
class City(BaseModel):
	name: str
	timezone: str

#get_all
@app.get('/')
def index():
	return _responses.RedirectResponse("/docs")

#get cities
@app.get('/cities')
def get_cities():
	results = []
	for city in db:
		r = requests.get(f'http://worldtimeapi.org/api/timezone/{city["timezone"]}')
		#get specific items from the API [time, day, week number, utc]
		current_time = r.json()['datetime']
		current_day = r.json()['day_of_year']
		week_number = r.json()['week_number']
		utc_offset= r.json()['utc_offset']
		results.append({'name': city['name'], 'timezone': city['timezone'], 'current_time': current_time, 'utc_offset': utc_offset, 'week_number': week_number, 'current_day': current_day})
	return results

#get city (specific)
@app.get('/cities/{city_id:}')
def get_city(city_id: int):
	return db[city_id-1]

#add city
@app.post('/cities')
def create_city(city: City):
	db.append(city.dict()) #convert city to dict (key-value pair)
	return db[-1] #return last item in DB

#delete city
@app.delete('/cities/{city_id}')
def delete_city(city_id: int):
	db.pop(city_id-1)
	return {}



