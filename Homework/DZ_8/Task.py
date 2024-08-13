'''
1. Скачайте датасет House Prices Kaggle со страницы конкурса 
(https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques/data) 
и сохраните его в том же каталоге, что и ваш скрипт или блокнот Python.

2. Загрузите датасет в pandas DataFrame под названием df.

3.Выполните предварительную обработку данных, выполнив следующие шаги: 
    a. Определите и обработайте отсутствующие значения в датасете. 
        Определите, в каких столбцах есть отсутствующие значения, и решите, как их обработать 
        (например, заполнить средним, медианой или модой, или отбросить столбцы/строки с существенными отсутствующими значениями). 
    b. Проверьте и обработайте любые дублирующиеся строки в датасете. 
    c. Проанализируйте типы данных в каждом столбце и при необходимости преобразуйте их (например, из объектных в числовые типы).

4. Проведите разведочный анализ данных (EDA), ответив на следующие вопросы:
    a. Каково распределение целевой переменной 'SalePrice'? Есть ли какие-либо выбросы? 
    b. Исследуйте взаимосвязи между целевой переменной и другими характеристиками. Есть ли сильные корреляции? 
    c. Исследуйте распределение и взаимосвязи других важных характеристик, таких как 'OverallQual', 'GrLivArea', 'GarageCars' и т.д. 
    d. Визуализируйте данные, используя соответствующие графики (например, гистограммы, диаграммы рассеяния, квадратные диаграммы), 
        чтобы получить представление о датасете.

5.Выполните проектирование признаков путем реализации следующих преобразований: 
    a. Работайте с категориальными переменными, применяя one-hot encoding или label encoding, в зависимости от характера переменной. 
    b. При необходимости создайте новые характеристики, такие как общая площадь или возраст объекта недвижимости, путем объединения существующих характеристик.

6. Сохраните очищенный и преобразованный набор данных в новый CSV-файл под названием 'cleaned_house_prices.csv'.

'''

import pandas as pd # pandas - для обратки и анализа данных
import numpy as np # библиотека для работы с массивами данных
import matplotlib.pyplot as plt # matplotlib.pyplot - модуль для построения графиков
import seaborn as sns # seaborn - библиотека для визуализации данных, основания для matplotlib
from sklearn.preprocessing import LabelEncoder # инстумент, для кодирования категориальных переменных
from scipy import stats # библиотека для научных и математических вычислений
from scipy.stats import spearmanr
from sklearn.preprocessing import LabelEncoder

# Устанавливаем стиль графиков
sns.set(style='whitegrid')

# Загружаем данные
file_path = 'Homework/DZ_8/train.csv'
df = pd.read_csv(file_path)

# Выводим первые строки датасета, чтобы понять, какие данные перед нами
print('Первые строки датасета: ')
print(df.head())

# Получаем общую информацию о DataFrame
df.info()

'''
3.Выполните предварительную обработку данных, выполнив следующие шаги: 
    a. Определите и обработайте отсутствующие значения в датасете. 
        Определите, в каких столбцах есть отсутствующие значения, и решите, как их обработать 
        (например, заполнить средним, медианой или модой, или отбросить столбцы/строки с существенными отсутствующими значениями). 
    b. Проверьте и обработайте любые дублирующиеся строки в датасете. 
    c. Проанализируйте типы данных в каждом столбце и при необходимости преобразуйте их (например, из объектных в числовые типы).
'''
'''
 Пропущенные значения 
 3   LotFrontage    1201 non-null   float64 - 259  # среднее значение
 6   Alley          91 non-null     object - 1369  # Удалить более 80% пропущенных значений  # мода
 25  MasVnrType     588 non-null    object  - 872  # мода
 26  MasVnrArea     1452 non-null   float64 - 8    # медиана
 30  BsmtQual       1423 non-null   object - 37    # Not indicated
 31  BsmtCond       1423 non-null   object - 37    # Удалить не осообо важен
 32  BsmtExposure   1422 non-null   object - 38    # Not indicated
 33  BsmtFinType1   1423 non-null   object - 37    # Удалить не осообо важен
 35  BsmtFinType2   1422 non-null   object - 38    # Удалить не осообо важен
 42  Electrical     1459 non-null   object - 1     # мода
 57  FireplaceQu    770 non-null    object - 690   # мода
 58  GarageType     1379 non-null   object - 81    # Not indicated 
 59  GarageYrBlt    1379 non-null   float64 - 81   # среднее значение
 60  GarageFinish   1379 non-null   object - 81    # Not indicated
 63  GarageQual     1379 non-null   object - 81    # Not indicated
 64  GarageCond     1379 non-null   object - 81    # Not indicated
 72  PoolQC         7 non-null      object - 1453  # Удалить более 80% пропущенных значений 
 73  Fence          281 non-null    object - 1179  # Not indicated
 74  MiscFeature    54 non-null     object - 1406  # Удалить более 80% пропущенных значений 
'''

# Удаляем лишние пробелы из названий столбцов для упрощения работы с данными
df.columns = df.columns.str.strip()

# Заполняем пропущенные значения средним значением
df['LotFrontage'] = df['LotFrontage'].fillna(df['LotFrontage'].mean())
df['GarageYrBlt'] = df['GarageYrBlt'].fillna(df['GarageYrBlt'].mean())

# Заполняем пропущенные значения модой
if 'MasVnrType' in df.columns:
    df['MasVnrType'] = df['MasVnrType'].fillna(df['MasVnrType'].mode()[0])
if 'Electrical' in df.columns:
    df['Electrical'] = df['Electrical'].fillna(df['Electrical'].mode()[0]) 
if 'FireplaceQu' in df.columns:
    df['FireplaceQu'] = df['FireplaceQu'].fillna(df['FireplaceQu'].mode()[0])

# Заполняем пропущенные значения медианой.
if 'MasVnrArea' in df.columns:
    df['MasVnrArea'] = df['MasVnrArea'].fillna(df['MasVnrArea'].median())

# Для других столбцов, где отсутствуют данные, заполняем их значением "не указано"('Not indicated')
cols_not_indicated = ['BsmtQual', 'BsmtExposure', 'GarageType', 'GarageFinish', 
                      'GarageQual', 'GarageCond', 'Fence']
for col in cols_not_indicated:
    if col in df.columns:
        df[col] = df[col].fillna('Not indicated')

# Удаляем столбцы, в которых более 80% данных отсутствует 
columns_to_drop = ['Alley', 'BsmtCond', 'BsmtFinType1', 'BsmtFinType2', 'PoolQC', 'MiscFeature']
df.drop(columns=[col for col in columns_to_drop if col in df.columns], inplace=True)

# Проверяем наличие дублирующихся строк в датасете и выводим их количеств
duplicates = df.duplicated().sum()
print(f'Количество дублирующихся строк: {duplicates}')
# Если такие строки присутствуют, удаляем их из DataFrame.
df.drop_duplicates(inplace=True)

# Проверяем типы данных в каждом столбце и выводим результат.
print(df.dtypes)
#Получаем все столбцы с категориальными данными
categorical_cols = df.select_dtypes(include=['object']).columns

# Сначала округляем значения
df['LotFrontage'] = df['LotFrontage'].round()
# Заполняем пропущенные значения нулями и преобразуем его в целочисленный тип данных.
df['LotFrontage'] = df['LotFrontage'].fillna(0).astype(int)
df['MasVnrArea'] = df['MasVnrArea'].fillna(0).astype(int)
df['GarageYrBlt'] = df['GarageYrBlt'].fillna(0).astype(int) 
# Проверяем уникальные значения в обновленных столбцах
df['LotFrontage'].unique()
df['MasVnrArea'].unique()
df['GarageYrBlt'].unique()

# Дополнительная проверка на наличие дублирующихся строк в датасете.
duplicates = df.duplicated().sum()
print(f'Количество дублирующихся строк: {duplicates}')


'''
4. Проведите разведочный анализ данных (EDA), ответив на следующие вопросы:
    a. Каково распределение целевой переменной 'SalePrice'? Есть ли какие-либо выбросы? 
    b. Исследуйте взаимосвязи между целевой переменной и другими характеристиками. Есть ли сильные корреляции? 
    c. Исследуйте распределение и взаимосвязи других важных характеристик, таких как 'OverallQual', 'GrLivArea', 'GarageCars' и т.д. 
    d. Визуализируйте данные, используя соответствующие графики (например, гистограммы, диаграммы рассеяния, квадратные диаграммы), 
        чтобы получить представление о датасете.
'''
df.info()

# Создаем ящичковую диаграмму
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, y='SalePrice')
plt.title('Ящичковая диаграмма SalePrice')
plt.ylabel('Цена')
plt.show()
### На диаграмме мы можем наблюдать выбросы, их обработка в соответствии с заданием не требуется. 



# Создаем гистограмму
plt.figure(figsize=(10, 6))
sns.histplot(df["SalePrice"], kde=True)
plt.xlabel("Цена продажи")
plt.ylabel("Количество")
plt.title('Распределение SalePrice')
plt.show()

# Рассчитываем асимметрию и эксцесс для характеристики распределения цен продажи
skewness = df['SalePrice'].skew()
kurtosis = df['SalePrice'].kurt()
print(f"Асимметрия: {skewness}")
print(f"Эксцесс: {kurtosis}")

# Выполняем тест нормальности (тест Шапиро-Уилка) для проверки отклонения распределения от нормального
shapiro_test = stats.shapiro(df['SalePrice'])
print(f"Тест Шапиро-Уилка: статистика = {shapiro_test.statistic}, p-значение = {shapiro_test.pvalue}")

### Распределение 'SalePrice' явно указывает на отклонение от нормального распределения. 
# Это подтверждается результатами теста Шапиро-Уилка, где p-значение, существенно ниже критического значения.



# Указываем переменную, для которой будем рассчитывать корреляцию
variable = 'SalePrice'
# Выбираем только числовые переменные из DataFrame
quantitative_vars = df.select_dtypes(include=['int64', 'float64'])
# Создаем словарь для хранения результатов
results = {}
if variable in quantitative_vars.columns:
    for col in quantitative_vars.columns:
        if col != variable: # Исключаем саму переменную 'SalePrice' при вычислении корреляции
            try:
                spearman_corr, p_value = spearmanr(df[variable], df[col]) # Рассчитываем коэффициент корреляции Спирмена и p-значение
                results[col] = {'Spearman_corr': spearman_corr, 'p_value': p_value}
            except Exception as e:
                print(f"Ошибка при расчете для {col}: {e}")

    # Преобразуем словарь результатов в DataFrame для удобства представления
    results_df = pd.DataFrame.from_dict(results, orient='index')

    print(f"Коэффициенты Спирмена и p-значения для переменной '{variable}':")
    print(results_df)
else:
    print(f"Переменная '{variable}' не найдена в DataFrame.")

# Выбираем только числовые переменные из DataFrame
numeric_df = df.select_dtypes(include=[np.number])

# Проверяем наличие числовых переменных
if not numeric_df.empty:
    plt.figure(figsize=(20, 20))
    try:
        correlation_matrix = numeric_df.corr() # Вычисляем корреляционную матрицу для всех числовых переменных

       # Визуализируем корреляционную матрицу с помощью тепловой карты
        sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm',
                    square=True, linewidths=0.5, cbar_kws={"shrink": .8},
                    annot_kws={"size": 10}, center=0)
        
        plt.title('Корреляционная матрица', fontsize=20)
        plt.xticks(rotation=45, ha='right', fontsize=12)
        plt.yticks(rotation=0, fontsize=12)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"Ошибка при визуализации корреляционной матрицы: {e}")
else:
    print("Нет числовых переменных для вычисления корреляционной матрицы.")


# Выбор важных переменных для дальнейшего анализа
important = ['OverallQual', 'GrLivArea', 'GarageCars']
df[important].describe().round(2)  # Получаем описательную статистику для выбранных переменных

# Отрисовка гистограмм распределения выбранных переменных
num_rows = 1
num_cols = 3

# Создаем подграфики для визуализации гистограмм
fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 5))
axes = axes.flatten()

for i, col in enumerate(important):
    sns.histplot(data=df[col], kde=True, ax=axes[i], color='skyblue', bins=20, alpha=0.7)
    
    mean_value = df[col].mean() # Добавление вертикальной линии для отображения среднего значения переменной
    axes[i].axvline(mean_value, color='red', linestyle='--', label=f'Среднее: {mean_value:.2f}')
    
    axes[i].set_title(f'Гистограмма {col}', fontsize=14)
    axes[i].set_xlabel('Значение', fontsize=12)
    axes[i].set_ylabel('Частота', fontsize=12)
    axes[i].legend()

plt.tight_layout()
plt.show()

'''
5.Выполните проектирование признаков путем реализации следующих преобразований: 
    a. Работайте с категориальными переменными, применяя one-hot encoding или label encoding, в зависимости от характера переменной. 
    b. При необходимости создайте новые характеристики, такие как общая площадь или возраст объекта недвижимости, путем объединения существующих характеристик.
'''
# Список столбцов для Label Encoding
label_encoding_cols = ['ExterQual', 'KitchenQual', 'BsmtQual', 'GarageQual']
'''# Список столбцов для One-Hot Encoding
one_hot_encoding_cols = ['MSZoning', 'Street', 'LotShape', 'LandContour', 
                         'Utilities', 'LotConfig', 'LandSlope', 
                         'Neighborhood', 'Condition1', 'Condition2', 
                         'BldgType', 'HouseStyle', 'RoofStyle', 
                         'RoofMatl', 'Exterior1st', 'Exterior2nd', 
                         'MasVnrType', 'Foundation', 'Heating', 
                         'HeatingQC', 'CentralAir', 'Electrical', 
                         'Functional', 'FireplaceQu', 'GarageType', 
                         'GarageFinish', 'PavedDrive', 'Fence', 
                         'SaleType', 'SaleCondition']
'''
# Применяем Label Encoding
for col in label_encoding_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])

'''# Применяем One-Hot Encoding
df = pd.get_dummies(df, columns=one_hot_encoding_cols, drop_first=True)'''

# 1. Общая площадь (сумма всех жилых и нежилых площадей)
df['TotalSF'] = df['TotalBsmtSF'] + df['1stFlrSF'] + df['2ndFlrSF']
# 2. Возраст дома (разница между годом продажи и годом постройки)
df['HouseAge'] = df['YrSold'] - df['YearBuilt']
# 3. Возраст ремонта (разница между годом продажи и годом последнего ремонта)
df['RemodelAge'] = df['YrSold'] - df['YearRemodAdd']
# 4. Общее количество ванных комнат (с учетом полноценных и половинных ванных комнат)
df['TotalBath'] = df['FullBath'] + (0.5 * df['HalfBath']) + df['BsmtFullBath'] + (0.5 * df['BsmtHalfBath'])

print(df.head())  # Вывод первых нескольких строк для проверки корректности
print(df.describe())


df.to_csv('Homework/DZ_8/cleaned_house_prices.csv', index=False)