## **Описание проекта:**
Целью данного проекта является прогнозирование цен на подержаные автомобили. Для данной задачи используется набор данных Car Price prediction: https://www.kaggle.com/datasets/vijayaadithyanvg/car-price-predictionused-cars/data

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
num__Selling_Price, num__Driven_kms, cat__Car_Name, cat__Fuel_Type, cat__Selling_type, cat__Transmission poly__1, poly__Selling_Price, poly__Driven_kms, poly__Selling_Price^2, poly__Selling_Price, Driven_kms, poly__Driven_kms^2, k_bin__Selling_Price, k_bin__Driven_kms
```

Лучшая модель была обучена на всей выборке с тэгом Production. Run ID = 4f48f48858094c48a0114ad0a4d9924a


