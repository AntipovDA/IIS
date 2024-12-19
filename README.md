## **Описание проекта:**
Целью данного проекта является прогнозирование цен на подержаные автомобили. Для данной задачи используется набор данных Car Price prediction: https://www.kaggle.com/datasets/vijayaadithyanvg/car-price-predictionused-cars/data

В рамках данного проекта создается создается модель предсказания цен на подержаные автомобили, проводятся эксперименты по настройке модели с использованием MLFlow, создается микросервис предсказаний на основе FastApi. Также доступна возможность автоматической отправки запросов на сервис предсказаний и получения в ответ предикта. Есть возможность осуществлять мониторинг сервиса с помощью Prometheus и Grafana.

Список используемых библиотек: 
```
matplotlib
numpy
pandas
seaborn
bokeh
pickle4
mlflow
scikit-learn
mlxtend
optuna
fastapi
uvicorn
prometheus-fastapi-instrumentator
prometheus_client
requests
```

## **Запуск:**
```
git clone https://github.com/AntipovDA/IIS - клонирование репозитория
cd IIS - переход в склонированную папку
python3 -m venv .my_venv - установка виртуального окружения
source .my_venv/bin/activate - активация виртуального окружения
pip install -r requirements.txt - установкав в окружение всех требуемых библиотек
```
Запуск MlFlow:
```
cd mlflow - переход в папку со bash-скриптом, который запускает Mlflow
sh start_mlflow.sh - запуск mlflow
```
После запуска mlflow будет доступен по ссылке: http://localhost:5000/

## **Исследование данных:**
Находится в ```./eda/eda.ipynb.``` Основные результаты:
В ходе исследования был проведен анализ, который показал, что данные не обладают избыточностью, все записи валидны
В ходе анализа были выявлены следующие закономерности:

* Большая часть автомобилей продается через дилеров, а не частными лицами
* Преобладание механической коробки передач указывает на то, что в данных больше бюджетных моделей автомобилей, которые часто оснащаются механической трансмиссией
* Текущая цена автомобиля (Present_Price) является основным фактором, влияющим на цену его продажи (Selling_Price)
* Количество владельцев практически не влияет на остальные параметры, что может означать, что покупатели больше ориентируются на другие характеристики автомобиля, такие как текущая цена, пробег и возраст
* Большинство значений находится в нижнем диапазоне значений (до 15), что может указывать на преобладание автомобилей с низкой ценой.


## **Результаты исследования:**

Лучше всего показала себя модель 2 (RandonForestRegression) с трансформациями следующих столбцов входных данных: 

- к столбцам 'Selling_Price', 'Driven_kms' была применена полиномиальная функция PolynomialFeatures
- данные из столбцов 'Selling_Price', 'Driven_kms' были разбиты на 3 категории с помощью KBinsDiscretizer

Параметры модели: 

```
'n_estimators': 100
'max_depth': 20
'max_features': 0.8072727315456365
```

Результаты исследований приведены ниже: 

```
mae: 1,25
mape: 0,67
mse: 3,28
```
На вход модели подавались следующие признаки: 

```
 "Car_Name", "Selling_Price", "Driven_kms", "Fuel_Type", "Selling_type", "Transmission", "Owner"
```

Лучшая модель была обучена на всей выборке с тэгом Production. Run ID = 'c47d900173524e54a3c2d81582996146'

## **Описание разработанного сервиса предсказаний:**
1. ml_service - содержит в себе следующие файлы:
    * Dockerfile - содержит инструкцию по сборке образа и запуску контейнера
    * api_handler.py - содержит класс-обработчик запросов к API FastAPIHandler, который загружает обученную модель, принимает входные данные и выполняет предсказание с помощью загруженной модели
    * main.py - содержит скрипт, который разворачивает сервис для взаимодействия с моделью машинного обучения через API
    * requirements.txt - хранит зависимости, которые необходимы для работы сервиса


2. models - содержит в себе следующие файлы:
    * get_model.py - скрипт, который должен подключаться к mlflow, выгружать модель по её run_id и сохранять ее в файл model.pkl
  
```
docker build . --tag estate_model:0 - команда для создания образа
docker run -p 8001:8000 -v $(pwd)/../models:/models estate_model:0 - команда для запуска контейнера
```

Тело запроса: 
```
{
 "Car_Name": "sx4",
 "Selling_Price": 4.87,
 "Driven_kms": 48923,
 "Fuel_Type": 1,
 "Selling_type": "Petrol",
 "Transmission": "Manual",
 "Owner": 1
}
```

## **Проверка работоспособности сервиса:**
1. Собрать Docker-образ (команда по сборке и запуску находится выше)
2. Запустить контейнер
3. Откройте адрес активированного сервиса в браузере и перейдите по маршруту /docs. С помощью интерфейса Swagger UI протестируйте доступные эндпоинты (в нашем случае это api/prediction)


## **Сервис отправки запросов:**
В папке requests находится скрипт req.py, который отправляет запросы к основному сервису предсказаний с ипользованием случайной генерации полей входных данных "Selling_Price" и "Driven_kms" в случайные промежутки времени.

## **Сервис по сбору метрик Prometheus:**
Prometheus регулярно запрашивает метрики у сервиса предсказаний, чтобы в дальнейшем была возможность визуализировать их на графиках. Обработка данных происходит с помощью команд на языке запросов PromQL. Файл prometheus.yml содержит информацию о том, какие цели (экспортёры) опрашивать, как часто, и с какими параметрами.

## **Сервис по сбору метрик Grafana:**
Grafana позволяет установить соединение с Prometheus в качестве источника данных. Пользователь настраивает панели , которые отображают метрики в виде графиков, таблиц и других визуализаций. Для каждой панели можно задать собственный запрос к данным и тип отображения.

## **Веб-интерфейс запускается по адресу:**
```
http://localhost:8000 - для веб-интерфейса сервиса предсказаний
http://localhost:9090 - для запуска Prometheus
http://localhost:3000 - для запуска Grafana
```

Запуск compose-проекта осуществляется командой ```docker compose up```

## **Графики (Prometheus)**
* гистограма предсказаний модели
![image](https://github.com/AntipovDA/IIS/blob/main/services/prometheus/Screenshot%20from%202024-12-19%2014-21-45.png)

* частота (rate) запросов к основному сервису в минуту
![image](https://github.com/AntipovDA/IIS/blob/main/services/prometheus/Screenshot%20from%202024-12-19%2014-22-10.png)

* Количество запросов к сервису с кодами ошибок 4** и 5**
![image](https://github.com/AntipovDA/IIS/blob/main/services/prometheus/Screenshot%20from%202024-12-19%2014-23-07.png)


## **Дашборд (Grafana)**
![image](https://github.com/AntipovDA/IIS/blob/main/services/grafana/Screenshot%20from%202024-12-19%2015-12-43.png)

На данном дашборде отображены 5 графиков мониторинга сервиса предсказаний: 
* Memory - отображены данные, связанные с метрикой process_resident_memory_bytes, которая показывает объем потребляемой памяти (в байтах) процессом. Относится к инфраструктурному уровню мониторинга.
* CPU Seconds Total - на данном графике отображена метрика process_cpu_seconds_total, которая показывает общее количество процессорного времени (в секундах), использованного процессом. Относится к инфраструктурному уровню мониторинга.
* Preediction Bucket - на графике отображена метрика prediction_metric_histogram_bucket, представляющая гистограмму значений, сгруппированных по различным "корзинам". Все линии на графике монотонно растут, что говорит о накоплении количества выполненных предсказаний в каждой из корзин. Линейный рост во всех "корзинах" говорит о том, что процесс предсказаний работает стабильно, без резких изменений в скорости выполнения. Относится к уровню мониторинга качества работы модели.
* Requests - на графике изображены метрики запросов в приложении, сгруппированные по различным параметрам. График позволяет оценить работоспособность эндпоинтов и выявить потенциальные проблемы, например, наличие ошибок (4xx, 5xx). Относится к прикладному уровню мониторинга
* Rate Status Request - на графике показан темп (rate) запросов с ошибками для эндпоинта /api/prediction (метод POST) с разделением по статусам ошибок: 4xx (клиентские ошибки) и 5xx (серверные ошибки). Относится к прикладному уровню мониторинга
