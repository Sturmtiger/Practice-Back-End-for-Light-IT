from requests import get
from flask import Flask, render_template, request

app = Flask(__name__)

appid = 'b38b555065898d619a06fb3af3303bbd'
cityID = None

###############################################################################################
def getCurrentWeather(cityID):
    res = get('http://api.openweathermap.org/data/2.5/weather',
              params={'id': cityID, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
    data = res.json()
    return render_template('cw.html', data=data)



def getWeatherForecastFor5days(cityID):
    res = get("http://api.openweathermap.org/data/2.5/forecast",
              params={'id': cityID, 'units': 'metric', 'lang': 'ru', 'APPID': appid}) #units - система измерения
    data = res.json()
    return render_template('wff5d.html', data=data)


def getWeather(typeOfData, town, country):
    global cityID
    location = f'{town.capitalize()},{country.upper()}' # ex "Zaporizhzhia,UA"
    if not location.split(',')[0] or not location.split(',')[1]:
        notCity = 'Произошла ошибка. Пожалуйста, укажите город и страну!'
        return render_template('menu.html', notCity=notCity)
    try:
        res = get('http://api.openweathermap.org/data/2.5/find',
                  params={'q': location, 'type': 'like', 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        cityID = data['list'][0]['id'] #ID нужного города
        if typeOfData == 'weather':
            return getCurrentWeather(cityID)
        return getWeatherForecastFor5days(cityID) # if typeOFData == 'forecast'
    except:
        err = 'Произошла ошибка. Пожалуйста, введите корректные данные!'
        return render_template('menu.html', error=err)
###############################################################################################

@app.route('/')
def menu():
    return render_template('menu.html')


@app.route('/city-weather-info', methods=['POST'])
def city_weather():
    city = request.form['city']
    country = request.form['country']
    typeOfData = request.form['typeOfData'] # тип данных, который нужно обработать
    return getWeather(typeOfData, city, country)

if __name__ == '__main__':
    app.run(debug=True)