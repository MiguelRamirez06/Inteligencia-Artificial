from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt
import numpy as np

# Datos de ejemplo
X = np.array([[16], [20], [13], [45], [10], [18]])
y = np.array([0, 1, 0, 1, 0, 1])

# Crear el modelo
model = DecisionTreeClassifier()

# Entrenar el modelo
model.fit(X, y)

# Hacer una predicción
prediction = model.predict([[17]])
print("¿Puede votar una persona de 17 años?", "Sí" if prediction[0] == 1 else "No")

# Dibujar el árbol
plt.figure(figsize=(10, 6))
plot_tree(model, filled=True, feature_names=["Edad"], class_names=["No puede votar", "Puede votar"])
plt.show()
