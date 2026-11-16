
import java.util.Scanner;
import java.util.Arrays;

class Item {
    int weight;
    int profit;
    double ratio;

    Item(int weight, int profit) {
        this.weight = weight;
        this.profit = profit;
        this.ratio = (double) profit / weight;
    }
}

public class FractionalKnapsack {

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        System.out.print("Enter number of items: ");
        int n = sc.nextInt();

        Item[] items = new Item[n];

        // Input item details
        for (int i = 0; i < n; i++) {

            System.out.print("Enter weight of item " + (i + 1) + ": ");
            int weight = sc.nextInt();

            System.out.print("Enter profit of item " + (i + 1) + ": ");
            int profit = sc.nextInt();

            items[i] = new Item(weight, profit);
        }

        System.out.print("Enter knapsack capacity: ");
        int capacity = sc.nextInt();

        // Sort items by profit/weight ratio
        Arrays.sort(items, (a, b) ->
            Double.compare(b.ratio, a.ratio)
        );

        double totalProfit = 0;

        // Greedy selection
        for (int i = 0; i < n; i++) {

            if (capacity == 0) {
                break;
            }

            if (items[i].weight <= capacity) {

                totalProfit += items[i].profit;
                capacity -= items[i].weight;

            } else {

                double fraction = (double) capacity / items[i].weight;

                totalProfit += items[i].profit * fraction;

                capacity = 0;
            }
        }

        System.out.println("Maximum Profit = " + totalProfit);

        sc.close();
    }
}


// Enter number of items: 3

// Enter weight of item 1: 10
// Enter profit of item 1: 60

// Enter weight of item 2: 20
// Enter profit of item 2: 100

// Enter weight of item 3: 30
// Enter profit of item 3: 120

// Enter knapsack capacity: 50

// Maximum Profit = 240.0