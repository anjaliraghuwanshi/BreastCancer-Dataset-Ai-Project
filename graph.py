import matplotlib.pyplot as plt

def show_accuracy():

    labels = ["Correct", "Incorrect"]
    values = [97, 3]

    plt.bar(labels, values)
    plt.title("Model Accuracy Visualization")
    plt.show()