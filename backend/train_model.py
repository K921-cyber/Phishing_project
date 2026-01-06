import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
import joblib

# 1. CREATE A DUMMY DATASET (For demonstration)
# In a real capstone, you would load a CSV here: data = pd.read_csv("phishing_data.csv")
data = {
    'text': [
        "Urgent! Your account is suspended. Click here to verify.",
        "Hey, are we still on for lunch tomorrow?",
        "Security Alert: Unusual login detected. Reset password immediately.",
        "Attached is the project report for this semester.",
        "WINNER! You have won a lottery. Claim now!",
        "Meeting minutes from the board meeting attached."
    ],
    'label': [1, 0, 1, 0, 1, 0]  # 1 = Phishing, 0 = Safe
}
df = pd.DataFrame(data)

# 2. FEATURE EXTRACTION
# We turn text into numbers. 
# We look for "Urgency" and "Action" words.
vectorizer = CountVectorizer(stop_words='english', max_features=100)
X = vectorizer.fit_transform(df['text'])
y = df['label']

# 3. TRAIN THE MODEL
print("Training Random Forest Model...")
clf = RandomForestClassifier(n_estimators=10, random_state=42)
clf.fit(X, y)

# 4. SAVE THE BRAIN
# We save the model and the translator (vectorizer) to files so the app can use them.
joblib.dump(clf, 'phishing_model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')

print("Success! Model saved as 'phishing_model.pkl'")