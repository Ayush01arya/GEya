import numpy as np
import pickle
from sklearn.neighbors import KNeighborsClassifier

# Sample training data (X: Scores in different categories, y: Career labels)
X_train = np.array([
    [90, 70, 90, 80, 90],  # Data Science
    [50, 90, 70, 70, 75],  # Software Development
    [80, 50, 60, 90, 40],  # Management
    [60, 80, 50, 50, 80],  # Design
])

y_train = ["Data Scientist", "Software Developer", "Manager", "Designer"]

# Train a KNN classifier
model = KNeighborsClassifier(n_neighbors=1)
model.fit(X_train, y_train)

# Save the trained model
with open("career_predictor.pkl", "wb") as f:
    pickle.dump(model, f)
