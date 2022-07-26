from scipy.integrate import simps

def ranking_extraction_es(alpha, name_dataset, name_algorithm, accuracy_scores, completeness_scores, consistency_scores):

    #exponential smoothing y= a*x(t) + (1-a)*y(t-1)
    def compute_exponential_smoothing(scores):
        area_es = 0
        for i in range(0,9):
            a = scores[i]
            b = scores[i+1]
            y = [a,b]
            area_es += alpha*simps(y, dx=10) + (1-alpha)*area_es
        return area_es

    Consistency = compute_exponential_smoothing(consistency_scores)
    Accuracy = compute_exponential_smoothing(accuracy_scores)
    Completeness = compute_exponential_smoothing(completeness_scores)

    areas = [Consistency, Accuracy, Completeness]
    areas.sort()

    def print_dimension_with_value(dimension):
        string = []
        if dimension == Consistency:
            print(f"{Consistency=}\n")
        if dimension == Completeness:
            print(f"{Completeness=}\n")
        if dimension == Accuracy:
            print(f"{Accuracy=}\n")

    def print_dimension(dimension):
        string = []
        if dimension == Consistency:
            string.append("Consistency\n")
        if dimension == Completeness:
            string.append("Completeness\n")
        if dimension == Accuracy:
            string.append("Accuracy\n")
        return "".join([str(item) for item in string])

    string = []
    string.append("Ranking for " + name_dataset + " - " + name_algorithm + "\n")

    for dimension in areas:
        string.append(print_dimension(dimension))
        #print_dimension_with_value(dimension)

    string.append("\n\n")
    print("".join([str(item) for item in string]))
    return "".join([str(item) for item in string])