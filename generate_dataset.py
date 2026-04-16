import random
import pandas as pd

positive_phrases = [
    "The product is excellent and works perfectly",
    "I am very satisfied with the quality and performance",
    "This is a great product and worth the money",
    "Amazing experience using this product",
    "Highly recommend this to everyone",
    "The performance is smooth and reliable",
    "Very good quality and easy to use",
    "Fantastic product with great features",
    "I love this product and its design",
    "The results are accurate and fast"
]

negative_phrases = [
    "The product is very poor and disappointing",
    "I am not satisfied with the quality",
    "This is a waste of money",
    "Very bad experience using this product",
    "I would not recommend this to anyone",
    "Performance is slow and unstable",
    "The quality is cheap and not durable",
    "Terrible product with many issues",
    "I hate this product and its design",
    "The results are inaccurate and unreliable"
]

modifiers = [
    "overall", "honestly", "in my opinion", "after using it for a while",
    "based on my experience", "personally", "to be frank"
]

data = []

# Generate 500 positive + 500 negative
for _ in range(500):
    sentence = random.choice(modifiers) + ", " + random.choice(positive_phrases)
    data.append([sentence, "positive"])

for _ in range(500):
    sentence = random.choice(modifiers) + ", " + random.choice(negative_phrases)
    data.append([sentence, "negative"])

# Shuffle dataset
random.shuffle(data)

# Save to CSV
df = pd.DataFrame(data, columns=["review", "sentiment"])
df.to_csv("sentiment_dataset_1000.csv", index=False)

print("Dataset generated successfully!")