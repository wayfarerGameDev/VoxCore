import urllib.request
import datetime
import json
from enum import Enum

# Update Categories
class UpdateCat(Enum):
    LOCATION = 0
    WEATHER = 1
    SPACE_WEATHER = 2
    SPACE_CELESTIALS = 3
    SPACE_PERSONNEL = 4
    SPACE_ASTEROIDS = 5
    SPACE_EQUIPMENT = 6

class TaskOutputWeatherUniversal:
    command = "--task_output_enviorment_web_universal"
        
    def __init__(self, command_router_function, flags=None):
        self.route_command = command_router_function
        self.flags = flags if flags is not None else {}
        self.imperial_system_enabled = False
        self.data = {
            # Location
            "region": "N/A", 
            "city": "N/A", 
            "longitude": "N/A", 
            "latitude": "N/A", 
            "elevation": "N/A", 
            
            # Weather
            "temperature": "N/A", 
            "windspeed": "N/A", 
            "winddirection": "N/A", 
            "weathercode": "N/A",
            "aqi": "N/A",
            "aqi_status": "N/A",
            "uv_index": "N/A",
            "uv_status": "N/A",
            
            # Space
            "sunrise": "N/A", 
            "sunset": "N/A", 
            "moonrise": "N/A", 
            "moonset": "N/A", 
            "moonphase": "N/A", 
            "daylight": "N/A", 
            "is_day": "N/A",
            "kp_index": "N/A",
            "space_alert": "N/A",
            "iss_lat": "N/A",
            "iss_lon": "N/A",
            "iss_country": "N/A",
            "personnel_details": "N/A",
            "asteroid_details": "N/A",
            "next_launch": "N/A",
            "solar_flare": "N/A"
        }

    def boot(self):
        self.route_command("--ui_header Task booted: Output_Enviorment_Web_Universal")

    def terminate(self):
        self.route_command("--ui_header Task terminated: Output_Enviorment_Web_Universal")

    def run(self, delta_time: float):
        pass

    def on_command(self, command: str) -> bool:
        args = command.lower().split()
        if not args: return False
        cmd, force = args[0], (len(args) > 1 and args[1] == "1")

        # Enviorment Update
        if cmd == "--enviorment_update":
            for cat in UpdateCat: self._update(cat)
            return True
        
         # Enviorment Update
        if cmd == "--enviorment_units_switch":
            self.imperial_system_enabled = not self.imperial_system_enabled
            self._update(UpdateCat.WEATHER)
            return True
        
        # Location
        if cmd == "--enviorment_location":
            if force or self.data["city"] == "N/A": self._update(UpdateCat.LOCATION)
            self.route_command(f"--ui_widget Enviorment Location -> Region: {self.data['region']} | City: {self.data['city']} | Latitude: {self.data['latitude']} | Longitude: {self.data['longitude']} | Elevation: {self.data['elevation']} {'ft' if self.imperial_system_enabled else 'm'}")
            return True
   
        # Weather
        if cmd == "--enviorment_weather":
            if force or self.data["city"] == "N/A": self._update(UpdateCat.LOCATION)
            if force or self.data["temperature"] == "N/A": self._update(UpdateCat.WEATHER)
            self.route_command(f"--ui_widget Enviorment Weather -> Temp: {self.data['temperature']}{'°F' if self.imperial_system_enabled else '°C'} | Condition: {self.data['weathercode']} | Wind: {self.data['windspeed']} {'mph' if self.imperial_system_enabled else 'kph'} | AQI: {self.data['aqi']} ({self.data['aqi_status']}) | UV: {self.data['uv_index']} ({self.data['uv_status']})")
            return True 
     
        # Space (Personal)
        if cmd == "--enviorment_space_personnel":
            if force or self.data["personnel_details"] == "N/A": self._update(UpdateCat.SPACE_PERSONNEL)
            self.route_command(f"--ui_widget Enviorment Space Personnel -> Humans in Orbit:\n{self.data['personnel_details']}")
            return True
        
        # Space (Equiptment)
        if cmd == "--enviorment_space_equiptment":
            if force or self.data["iss_lat"] == "N/A": self._update(UpdateCat.SPACE_EQUIPMENT)
            self.route_command(f"--ui_widget Enviorment Space Equiptment -> ISS: {self.data['iss_country']}")
            return True
        
        # Space (Celestials)
        if cmd == "--enviorment_space_celestials":
            if force or self.data["city"] == "N/A": self._update(UpdateCat.LOCATION)
            if force or self.data["temperature"] == "N/A": self._update(UpdateCat.WEATHER)
            if force or self.data["moonrise"] == "N/A": self._update(UpdateCat.SPACE_CELESTIALS)
            self.route_command(f"--ui_widget Enviorment Space Celestials -> Status: {self.data['is_day']} | Moon: {self.data['moonphase']} | Sun: {self.data['sunrise']} to {self.data['sunset']}")
            return True
        
       # Space (Astroids)
        if cmd == "--enviorment_space_asteroids":
            if force or self.data["asteroid_details"] == "N/A": self._update(UpdateCat.SPACE_ASTEROIDS)
            self.route_command(f"--ui_widget Enviorment Space Asteroids -> Today's Near-Earth Objects:\n{self.data['asteroid_details']}")
            return True

        # Space (weather)
        if cmd == "--enviorment_space_weather":
            if force or self.data["city"] == "N/A": self._update(UpdateCat.LOCATION)
            if force or self.data["kp_index"] == "N/A": self._update(UpdateCat.SPACE_WEATHER)
            if force or self.data["sunrise"] == "N/A": self._update(UpdateCat.WEATHER)
            self.route_command(f"--ui_widget Enviorment Space Weather -> Space Weather: Kp {self.data['kp_index']} ({self.data['space_alert']}) | Solar Activity: {self.data['solar_flare']}")
            return True
           
        return False
    

    def _update(self, category: UpdateCat):
        
        # Hour converter
        def to_12h(time_string):
            if time_string == "N/A": return "N/A"
            return datetime.datetime.strptime(time_string[:5], "%H:%M").strftime("%I:%M %p").lstrip("0")

        # Location
        if category == UpdateCat.LOCATION or self.data["latitude"] == "N/A":
            try:
                with urllib.request.urlopen("http://ip-api.com/json/") as response: data = json.loads(response.read()); self.data["region"], self.data["city"], self.data["longitude"], self.data["latitude"] = data.get("region"), data.get("city"), data.get("lon"), data.get("lat")
            # Error
            except: pass

        # Weather | Space
        elif category == UpdateCat.WEATHER:
            WEATHER_CODES = {0: "Clear", 1: "Mainly Clear", 2: "Partly Cloudy", 3: "Overcast", 45: "Foggy", 48: "Rime Fog", 51: "Light Drizzle", 53: "Drizzle", 55: "Heavy Drizzle", 56: "Light Freezing Drizzle", 57: "Freezing Drizzle", 61: "Light Rain", 63: "Rain", 65: "Heavy Rain", 66: "Light Freezing Rain", 67: "Freezing Rain", 71: "Light Snow", 73: "Snow", 75: "Heavy Snow", 77: "Snow Grains", 80: "Light Showers", 81: "Showers", 82: "Heavy Showers", 85: "Light Snow Showers", 86: "Snow Showers", 95: "Thunderstorm", 96: "Thunderstorm with Hail", 99: "Heavy Thunderstorm with Hail"}
            try:
                with urllib.request.urlopen(url=f"https://api.open-meteo.com/v1/forecast?latitude={self.data['latitude']}&longitude={self.data['longitude']}&current_weather=true&daily=sunrise,sunset,daylight_duration&timezone=auto") as response:
                    data = json.loads(response.read()); data_weather = data.get("current_weather", {}); data_day = data.get("daily", {})
                    # Weather
                    self.data["elevation"] = data.get("elevation") if not self.imperial_system_enabled else round(float(data.get("elevation")) * 3.28084, 2)
                    self.data["temperature"] = data_weather.get("temperature") if not self.imperial_system_enabled else round((float(data_weather.get("temperature")) * 9/5) + 32, 2)
                    self.data["windspeed"] = data_weather.get("windspeed") if not self.imperial_system_enabled else round(float(data_weather.get("windspeed")) / 1.60934, 2)
                    self.data["winddirection"], self.data["weathercode"] = data_weather.get("winddirection"), WEATHER_CODES.get(int(data_weather.get("weathercode")), "Unknown")
                    # Space
                    self.data["is_day"] = "day" if data_weather.get("is_day") == 1 else "night"
                    self.data["sunrise"], self.data["sunset"] = to_12h(data_day.get("sunrise", ["N/A"])[0].split("T")[-1]), to_12h(data_day.get("sunset", ["N/A"])[0].split("T")[-1])
                    sec = data_day.get("daylight_duration", [0])[0]; self.data["daylight"] = f"{int(sec // 3600)}h {int((sec % 3600) // 60)}m"
            # Error
            except: pass

            # Air Quality & UV
            try:
                req = urllib.request.Request(url=f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={self.data['latitude']}&longitude={self.data['longitude']}&current=european_aqi,uv_index&timezone=auto", headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req) as response:
                    aq_data = json.loads(response.read()).get("current", {}); aqi_val, uv_val = float(aq_data.get("european_aqi", 0)), float(aq_data.get("uv_index", 0))
                    self.data["aqi"], self.data["uv_index"] = str(aqi_val), str(uv_val)
                    self.data["aqi_status"] = "Extremely Poor" if aqi_val >= 100 else "Very Poor" if aqi_val >= 80 else "Poor" if aqi_val >= 60 else "Moderate" if aqi_val >= 40 else "Fair" if aqi_val >= 20 else "Good"
                    self.data["uv_status"] = "Extreme" if uv_val >= 11 else "Very High" if uv_val >= 8 else "High" if uv_val >= 6 else "Moderate" if uv_val >= 3 else "Low"
            # Error
            except Exception as e: pass

        # Space (Weather)
        elif category == UpdateCat.SPACE_WEATHER:
            try:
                with urllib.request.urlopen(urllib.request.Request(url="https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json", headers={"User-Agent": "Mozilla/5.0"})) as response:
                    space_data = json.loads(response.read()); kp_val = next((float(row["Kp"]) for row in reversed(space_data) if row.get("Kp") is not None), 0.0)
                    self.data["kp_index"] = str(kp_val)
                    self.data["space_alert"] = "Extreme Storm" if kp_val >= 9 else "Severe Storm" if kp_val >= 8 else "Strong Storm" if kp_val >= 7 else "Moderate Storm" if kp_val >= 6 else "Minor Storm" if kp_val >= 5 else "Active" if kp_val >= 4 else "Quiet"
            except: pass
            try:
                with urllib.request.urlopen(f"https://api.nasa.gov/DONKI/FLR?startDate={(datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')}&api_key=DEMO_KEY") as response: flares = json.loads(response.read()); self.data["solar_flare"] = f"{flares[-1]['classType']} Class" if flares else "Quiet"
            except: pass

        # Space (Celestials)
        elif category == UpdateCat.SPACE_CELESTIALS:
            PHASES = ["New Moon", "Waxing Crescent", "First Quarter", "Waxing Gibbous", "Full Moon", "Waning Gibbous", "Last Quarter", "Waning Crescent"]
            try:
                with urllib.request.urlopen(urllib.request.Request(url=f"https://api.met.no/weatherapi/sunrise/3.0/moon?lat={self.data['latitude']}&lon={self.data['longitude']}", headers={"User-Agent": "EnvTask/1.0"})) as response:
                    astro = json.loads(response.read()).get("properties", {}); cycle_position = ((datetime.datetime.now() - datetime.datetime(2000, 1, 6)).days % 29.53) / 29.53
                    self.data["moonphase"] = PHASES[int(cycle_position * 8) % 8]
                    self.data["moonrise"] = to_12h(astro.get("moonrise").get("time", "N/A").split("T")[-1].split("+")[0])
                    self.data["moonset"] = to_12h( astro.get("moonset").get("time", "N/A").split("T")[-1].split("+")[0])
            # Error
            except Exception as e: pass 

        # Space (Equiptment)
        elif category == UpdateCat.SPACE_EQUIPMENT:
            try:
                with urllib.request.urlopen("http://api.open-notify.org/iss-now.json") as response: iss_data = json.loads(response.read()).get("iss_position", {}); self.data["iss_lat"], self.data["iss_lon"] = str(round(float(iss_data.get("latitude", 0)), 2)), str(round(float(iss_data.get("longitude", 0)), 2))
                with urllib.request.urlopen(f"https://api.bigdatacloud.net/data/reverse-geocode-client?latitude={self.data['iss_lat']}&longitude={self.data['iss_lon']}&localityLanguage=en") as response: geo_data = json.loads(response.read()); self.data["iss_country"] = geo_data.get("countryName") if geo_data.get("countryName") else "International Waters"
            except: pass
            
        # Space (Personnel)
        elif category == UpdateCat.SPACE_PERSONNEL:
            try:
                with urllib.request.urlopen("http://api.open-notify.org/astros.json") as response: data = json.loads(response.read()); self.data["personnel_details"] = "\n".join([f"• {p['name']} ({p['craft']})" for p in data.get("people", [])])
            except: pass

        # Space (Astroids)
        elif category == UpdateCat.SPACE_ASTEROIDS:
            try:
                today = datetime.datetime.now().strftime('%Y-%m-%d')
                with urllib.request.urlopen(f"https://api.nasa.gov/neo/rest/v1/feed?start_date={today}&end_date={today}&api_key=DEMO_KEY") as response: data = json.loads(response.read()); self.data["asteroid_details"] = "\n".join([f"• {a['name']} ({round(a['estimated_diameter']['meters']['estimated_diameter_max'])}m | {round(float(a['close_approach_data'][0]['miss_distance']['lunar']), 1)} LD away) {'[HAZARDOUS]' if a['is_potentially_hazardous_asteroid'] else ''}" for a in data.get("near_earth_objects", {}).get(today, [])])
            except: pass

        # Space (Upcoming rocket launches)
        # try:
        #    with urllib.request.urlopen("https://lldev.thespacedevs.com/2.2.0/launch/upcoming/?limit=1") as response: launch = json.loads(response.read())['results'][0]; self.data["next_launch"] = f"{launch['name']} ({launch['pad']['location']['name']})"
        # except: pass