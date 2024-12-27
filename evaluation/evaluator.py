from app.services.current_service import generate_synonyms as current_generate_synonyms
from app.services.new_service import generate_synonyms as new_generate_synonyms
from langsmith import Tracker
import json

# Load test dataset
with open("app/evaluation/test_dataset.json", "r") as f:
    dataset = json.load(f)

# Calculate accuracy
def calculate_accuracy(generated, ground_truth):
    intersection = set(generated).intersection(set(ground_truth))
    return len(intersection) / len(ground_truth) if ground_truth else 0

# Compare services
def evaluate_services():
    tracker = Tracker("synonym_service_comparison")

    results = []
    for example in dataset:
        word = example["word"]
        ground_truth = example["ground_truth"]

        # Test current service
        current_output = current_generate_synonyms(word)
        current_accuracy = calculate_accuracy(current_output, ground_truth)

        # Test new service
        new_output = new_generate_synonyms(word)
        new_accuracy = calculate_accuracy(new_output, ground_truth)

        # Log results
        tracker.log({
            "word": word,
            "ground_truth": ground_truth,
            "current_output": current_output,
            "current_accuracy": current_accuracy,
            "new_output": new_output,
            "new_accuracy": new_accuracy
        })

        results.append({
            "word": word,
            "ground_truth": ground_truth,
            "current_accuracy": current_accuracy,
            "new_accuracy": new_accuracy
        })

    return results
