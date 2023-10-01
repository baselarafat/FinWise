from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from core.models import Expense

def categorize_uncategorized_expenses():
    # Fetch expenses that aren't categorized
    uncategorized_expenses = Expense.objects.filter(category__isnull=True)

    # If there are no uncategorized expenses, return
    if not uncategorized_expenses.exists():
        return

    # Extract descriptions
    descriptions = [expense.description for expense in uncategorized_expenses]

    # Convert descriptions into numerical vectors using TF-IDF
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(descriptions)

    # Define the number of clusters
    num_clusters = 5  # Adjust based on your data

    # Apply KMeans clustering
    km = KMeans(n_clusters=num_clusters)
    km.fit(X)

    clusters = km.labels_.tolist()

    # Assign cluster numbers as categories
    for i, expense in enumerate(uncategorized_expenses):
        expense.category = f"Category {clusters[i]}"
        expense.save()
