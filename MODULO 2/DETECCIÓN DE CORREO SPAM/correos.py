# IMPORTACION DE LIBRERIAS NECESARIAS
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.metrics import accuracy_score, recall_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB



# CARGA Y PREPROCESAMIENTO DE LOS DATOS
# Cargamos los datos
data = pd.read_csv('spam_assassin.csv')
registros_iniciales = len(data)
print()
print('-' * 90)
print('Registros iniciales: ', registros_iniciales)

# Eliminacion de correos duplicados
data = data.drop_duplicates()
registros_unicos = len(data)
print('Registros sin duplicados: ', registros_unicos)
print("Registros eliminados: ", registros_iniciales - registros_unicos)

print('-' * 90)

# Imprimir el total de regostros que tienen 1 en la columna target
cantidad_spam = data['target'].sum()
print('Correos SPAM: ', cantidad_spam)
# Imprimir el total de regostros que tienen 0 en la columna target
cantidad_no_spam = len(data) - cantidad_spam
print('Correos NO SPAM: ', cantidad_no_spam)

print('-' * 90)

# PREPROCESAMIENTO DE LOS DATOS
# Convertir todo a minusculas
data['text'] = data['text'].str.lower()

# Eliminar caracteres especiales para mantener solo letras y numeros
data['text'] = data['text'].str.replace('[^a-zA-Z0-9 ]', '')
data['text'] = data['text'].str.split()

# Tokenizar y eliminar stopwords
stopwords = list(ENGLISH_STOP_WORDS)
data['text'] = data['text'].apply(lambda x: ' '.join([word for word in x if word not in stopwords]))


# EXTRAER CARACTERISTICAS DE LOS DATOS (TF, IDF, TF-IDF)

# Frecuencia de término (TF): Número de veces que una palabra aparece en un documento.
count_vectorizer = CountVectorizer(stop_words = 'english')
X_tf = count_vectorizer.fit_transform(data['text'])
tf_matrix = X_tf.toarray()
palabras = count_vectorizer.get_feature_names_out()

# Frecuencia de término inversa de documento (IDF): Mide la importancia de una palabra en un documento.
tfidf_transformer = TfidfTransformer(use_idf=True, norm=None, smooth_idf=True)
tfidf_transformer.fit(X_tf)
idf_values = tfidf_transformer.idf_
idf_dict = dict(zip(palabras, idf_values))

# TF-IDF: Multiplicación de TF y IDF para obtener la importancia de una palabra en un documento.
X_tfidf = tfidf_transformer.transform(X_tf).toarray()

vectorizer = TfidfVectorizer(stop_words = 'english')
X = vectorizer.fit_transform(data['text'])
print('X: ', X.shape)

# Definir las etiquetas (spam o no spam)
y = data['target']

# Dividir los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)
print('Datos de entrenamiento: ', X_train.shape)
print('Datos de prueba: ', X_test.shape)

print('-' * 90)


# ENTRENAMIENTO DEL MODELO
modelo_bayes = MultinomialNB()
modelo_bayes.fit(X_train, y_train)
y_pred = modelo_bayes.predict(X_test)

# CALCULO DE PROBABILIDADES
# Probabilidad de que sea spam
P_Spam = data['target'].sum() / len(data)
print('Probabilidad de que sea spam P(Spam): ', P_Spam, ' = ', round(P_Spam * 100, 2), '%')

# Probabilidad de que no sea spam
P_NoSpam = 1 - P_Spam
print("Probabilidad de que NO sea spam P(Spam)': ", P_NoSpam, ' = ', round(P_NoSpam * 100, 2), '%')

print('-' * 90)

# Calcular la probabilidad de las características del correo electrónico dado que es spam P(Características|Spam):
# Obtener los índices de las filas donde target == 1 (correos SPAM)
spam_indices = np.where(data['target'].to_numpy() == 1)[0]  # Convertir a índices numéricos

# Filtrar las filas correspondientes a correos SPAM en la matriz dispersa
X_spam = X[spam_indices]

# Calcular la probabilidad de las características dado que es spam
P_Caracteristicas_Spam = X_spam.sum(axis=0) / X_spam.sum()

# Convertir a un arreglo plano para usarlo en el DataFrame
P_Caracteristicas_Spam = np.asarray(P_Caracteristicas_Spam).flatten()

# Crear el DataFrame con las probabilidades
df_Caracteristicas_Spam = pd.DataFrame(P_Caracteristicas_Spam.T, columns=['Probabilidad'])
df_Caracteristicas_Spam['Palabra'] = palabras
df_Caracteristicas_Spam = df_Caracteristicas_Spam[['Palabra', 'Probabilidad']]

# Imprimir el resultado
print('Probabilidad de las características del correo electrónico dado que es spam P(Caracteristicas | Spam):\n', df_Caracteristicas_Spam)

print('-' * 90)

# Obtener los índices de las filas donde target == 0 (correos NO SPAM)
no_spam_indices = np.where(data['target'].to_numpy() == 0)[0]  # Convertir a índices numéricos

# Filtrar las filas correspondientes a correos NO SPAM en la matriz dispersa
X_no_spam = X[no_spam_indices]

# Calcular la probabilidad de las características dado que no es spam
P_Caracteristicas_NoSpam = X_no_spam.sum(axis=0) / X_no_spam.sum()

# Convertir a un arreglo plano para usarlo en el DataFrame
P_Caracteristicas_NoSpam = np.asarray(P_Caracteristicas_NoSpam).flatten()

# Crear el DataFrame con las probabilidades
df_Caracteristicas_NoSpam = pd.DataFrame(P_Caracteristicas_NoSpam.T, columns=['Probabilidad'])
df_Caracteristicas_NoSpam['Palabra'] = palabras
df_Caracteristicas_NoSpam = df_Caracteristicas_NoSpam[['Palabra', 'Probabilidad']]

# Imprimir el resultado
print('Probabilidad de las características del correo electrónico dado que NO es spam P(Caracteristicas | NoSpam):\n', df_Caracteristicas_NoSpam)

print('-' * 90)

# Calcular la probabilidad posterior de que el correo electrónico sea spam P(Spam|Caracteristicas):
P_Spam_Caracteristicas = (P_Spam * P_Caracteristicas_Spam) / (P_Spam * P_Caracteristicas_Spam + P_NoSpam * P_Caracteristicas_NoSpam)

df_Spam_Caracteristicas = pd.DataFrame(P_Spam_Caracteristicas.T, columns=['Probabilidad'])
df_Spam_Caracteristicas['Palabra'] = palabras
df_Spam_Caracteristicas = df_Spam_Caracteristicas[['Palabra', 'Probabilidad']]
print('Probabilidad posterior de que el correo electrónico sea spam P(Spam | Caracteristicas):\n', df_Spam_Caracteristicas)

print('-' * 90)

# Calculamos la probabilidad posterior de que el correo electrónico no sea spam P(NoSpam|Caracteristicas):
P_NoSpam_Caracteristicas = (P_NoSpam * P_Caracteristicas_NoSpam) / (P_Spam * P_Caracteristicas_Spam + P_NoSpam * P_Caracteristicas_NoSpam)

df_NoSpam_Caracteristicas = pd.DataFrame(P_NoSpam_Caracteristicas.T, columns=['Probabilidad'])
df_NoSpam_Caracteristicas['Palabra'] = palabras
df_NoSpam_Caracteristicas = df_NoSpam_Caracteristicas[['Palabra', 'Probabilidad']]
print('Probabilidad posterior de que el correo electrónico NO sea spam P(NoSpam | Caracteristicas):\n', df_NoSpam_Caracteristicas)

print('-' * 90)

# Clasificación:
# Un correo electrónico se clasificara como 'spam' si P(Spam|Caracteristicas) > P(NoSpam|Caracteristicas):
clasificaciones = np.where(P_Spam_Caracteristicas > P_NoSpam_Caracteristicas, "Spam", "No Spam")
print('Clasificaciones: ', clasificaciones)

print('-' * 90)

# EVALUACION DEL MODELO
# Evaluamos las predicciones del modelo de Naive Bayes estándar
precision = accuracy_score(y_test, y_pred)

print('Precisión: ', precision, ' = ', round(precision * 100, 2), '%')
