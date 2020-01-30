import requests, json, datetime, urllib.parse

import pprint

apikey = 'P0mrHHtqMfKcHnUZDvVafKGfRX1iRJ02'
mapboxapikey = 'pk.eyJ1IjoidGViYXN4IiwiYSI6ImNrNXIwM2FjajA4MTIza25zdTB3cmNveWEifQ.7OGAmEOXAOGj4Hjx36VBoQ'
semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sabado', 'Domingo']
dias = [0, 1, 2, 3, 4, 5, 6]
x = y = 0

def GetCoordinates():
    r = requests.get('http://www.geoplugin.net/json.gp')

    if r.status_code != 200:
        print('Nao foi possivel obter a localizacao!')
        print(r.status_code)
        return None
    else:
        try:
            localizacao = json.loads(r.text)
            coordinates = {}
            coordinates['long'] = str(localizacao['geoplugin_longitude'])
            coordinates['lat'] = str(localizacao['geoplugin_latitude'])
            return coordinates
        except:
            return None

def PesquisarLocal(cidade):
    _cidade = urllib.parse.quote(cidade)
    mapboxURL = 'https://api.mapbox.com/geocoding/v5/mapbox.places/' + _cidade + '.json?access_token=' + mapboxapikey
    r = requests.get(mapboxURL)
    if r.status_code != 200:
        print('nao foi possivel encontrar o codigo do local digitado. =(')
        return None
    else:
        try:
            mapboxresponse = json.loads(r.text)
            #pprint.pprint(mapboxresponse)
            coordinates = {}
            coordinates['long'] = str(mapboxresponse['features'][0]['center'][0])
            coordinates['lat'] = str(mapboxresponse['features'][0]['center'][1])
            return coordinates
        except:
            return None


def GetLocalCode(lat, long):
    local_url = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?' \
                + 'apikey=' + apikey + '&q=' + lat + '%2C' + long + '&language=pt-br'

    r = requests.get(local_url)
    if r.status_code != 200:
        print('nao foi possivel encontrar o codigo do local. =(')
        return None
    else:
        try:
            locationResponse = json.loads(r.text)
            localinfo = {}

            localinfo["nomelocal"] = locationResponse['LocalizedName'] + ', ' + locationResponse['AdministrativeArea'][
                'LocalizedName'] \
                                     + ', ' + locationResponse['Country']['LocalizedName']
            localinfo["codigolocal"] = locationResponse['Key']
            return localinfo
        except:
            return None


def GetWeather(codigolocal, nomelocal):
    CurentConditionsURL = 'http://dataservice.accuweather.com/currentconditions/v1/' + codigolocal + '?' \
                          + 'apikey=' + apikey + '&language=pt-br'
    r = requests.get(CurentConditionsURL)
    if r.status_code != 200:
        print('nao foi possivel encontrar o clima do local. =(')
        return None
    else:
        try:
            CurentConditionsResponse = json.loads(r.text)
            #print(pprint.pprint(CurentConditionsResponse))
            weatherinfo = {}
            weatherinfo["TextoClima"] = CurentConditionsResponse[0]['WeatherText']
            weatherinfo['temperatura'] = CurentConditionsResponse[0]['Temperature']['Metric']['Value']
            weatherinfo['localname'] = nomelocal
            return weatherinfo
        except:
            return None

## buscando previsão dos proximos 5 dias

def FiveDays(codigolocal, localname):
    fivedays_Url = "http://dataservice.accuweather.com/forecasts/v1/daily/5day/" + codigolocal + "?apikey=" + apikey + "&language=pt-br"
    r = requests.get(fivedays_Url)
    if r.status_code !=200:
        print('não foi possivel encontrar a previsão para o local atual.')
        return None
    else:
        previsao = json.loads(r.text)
        day_count = [0,1,2,3,4]
        week = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sabado', 'Domingo']
        index = datetime.date.weekday(datetime.date.today())

        print('\n Previsão para os proximo 5 dias em: ' + weather['localname'] + '\n')
        for d in day_count:
            proxdias = {}
            proxdias['frasedia'] = previsao['DailyForecasts'][d]['Day']['IconPhrase']
            proxdias['frasenoite'] = previsao['DailyForecasts'][d]['Night']['IconPhrase']
            proxdias['max'] = previsao['DailyForecasts'][d]['Temperature']['Maximum']['Value']
            proxdias['min'] = previsao['DailyForecasts'][d]['Temperature']['Minimum']['Value']
            proxdias['max'] = (proxdias['max'] - 32) * 5 / 9
            proxdias['min'] = (proxdias['min'] - 32) * 5 / 9
            dia_semana = week[index]
            if index == 6:
                index = 0
            else:
                index += 1

            print(dia_semana + ': \n' + proxdias['frasedia'] + ' durante o dia e ' \
                      + proxdias['frasenoite'] + ' no periodo da noite.'
                      '\nTemperatura maxima: ' + str(round(proxdias['max'], 2)) + '\xb0' + 'C. E minima: ' \
                      + str(round(proxdias['min'], 2)) + '\xb0' + 'C.\n')


##mapbox
## progan begins

while x == 0:

    while y == 0:
        r = int(input('Desaja consultar o clima em seu local atual ou pesquisar uma cidade?\n'
                  '[1] Local atual. \n'
                  '[2] Pesquisar uma cidade.\n'
                  ':'))

        if r == 1:
            latlong = GetCoordinates()
            y = 1

        elif r == 2:
            cidade = input('\nDigite o nome e o estado da cidade. \n')
            latlong = PesquisarLocal(cidade)
            y = 1

        else:
            print('\nOpção invalida, por favor digite o numero de uma das opçoes do menu. \n'
                  '*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*# \n')
            y = 0

    a = int(input('\nDigite qual opção deseja pesquisar: \n'
              '[1] Clima agora. \n'
              '[2] previsão dos proximos 5 dias.\n'
              ':'))
    if a == 1:
        try:
            local = GetLocalCode(latlong['lat'], latlong['long'])
            weather = GetWeather(local['codigolocal'], local['nomelocal'])
            print("\n")
            print('clima agora em ' + weather['localname'])
            print(weather['TextoClima'])
            print('Temperatura ' + str(weather['temperatura']) + "\xb0" + "C")
            print(
                '\n *#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*## \n')


        except:
            print('Não foi possivel obeter o clima atual. Entre em contato com o suporte')
            print(
                '*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*# \n')
        y = 1

    elif a == 2:
        try:
            local = GetLocalCode(latlong['lat'], latlong['long'])
            weather = GetWeather(local['codigolocal'], local['nomelocal'])
            FiveDays(local['codigolocal'], local['nomelocal'])
        except:
            print('Não foi possivel obeter o a previsão. Entre em contato com o suporte')
            print(
                '*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*# \n')
    else:
        print('Opção invalida, por favor digite o numero de uma das opçoes do menu. \n'
              '*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*# \n')
    y = 0