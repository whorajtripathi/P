
import java.util.Scanner;

public class Knapsackzero {

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        System.out.print("Enter number of items: ");
        int n = sc.nextInt();

        int[] weight = new int[n];
        int[] profit = new int[n];

        // Input weights
        System.out.println("Enter weights:");
        for (int i = 0; i < n; i++) {
            weight[i] = sc.nextInt();
        }

        // Input profits
        System.out.println("Enter profits:");
        for (int i = 0; i < n; i++) {
            profit[i] = sc.nextInt();
        }

        System.out.print("Enter knapsack capacity: ");
        int W = sc.nextInt();

        // Create DP table
        int[][] dp = new int[n + 1][W + 1];

        // Dynamic Programming
        for (int i = 1; i <= n; i++) {

            for (int j = 0; j <= W; j++) {

                if (weight[i - 1] <= j) {

                    dp[i][j] = Math.max(
                        profit[i - 1] + dp[i - 1][j - weight[i - 1]],
                        dp[i - 1][j]
                    );

                } else {

                    dp[i][j] = dp[i - 1][j];
                }
            }
        }

        System.out.println("Maximum Profit = " + dp[n][W]);

        sc.close();
    }
}


// Enter number of items: 3

// Enter weights:
// 10
// 20
// 30

// Enter profits:
// 60
// 100
// 120

// Enter knapsack capacity: 50

// Maximum Profit = 220