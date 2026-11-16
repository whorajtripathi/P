
import java.util.PriorityQueue;
import java.util.Scanner;

// Node class
class Node {
    char ch;
    int freq;

    Node left, right;

    Node(char ch, int freq) {
        this.ch = ch;
        this.freq = freq;
        left = right = null;
    }
}

public class Huffman {

    // Generate Huffman Codes
    static void printCodes(Node root, String code) {

        if (root == null) {
            return;
        }

        // If leaf node, print character and code
        if (root.left == null && root.right == null) {
            System.out.println(root.ch + " : " + code);
            return;
        }

        printCodes(root.left, code + "0");
        printCodes(root.right, code + "1");
    }

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        System.out.print("Enter number of characters: ");
        int n = sc.nextInt();

        PriorityQueue<Node> pq = new PriorityQueue<>(
            (a, b) -> a.freq - b.freq
        );

        // Input characters and frequencies
        for (int i = 0; i < n; i++) {

            System.out.print("Enter character: ");
            char ch = sc.next().charAt(0);

            System.out.print("Enter frequency: ");
            int freq = sc.nextInt();

            pq.add(new Node(ch, freq));
        }

        // Build Huffman Tree
        while (pq.size() > 1) {

            Node left = pq.poll();
            Node right = pq.poll();

            Node parent = new Node(
                '-', left.freq + right.freq
            );

            parent.left = left;
            parent.right = right;

            pq.add(parent);
        }

        // Generate Huffman Codes
        Node root = pq.poll();

        System.out.println("\nHuffman Codes:");
        printCodes(root, "");
        
        sc.close();
    }
}


// Enter number of characters: 6

// Enter character: A
// Enter frequency: 5

// Enter character: B
// Enter frequency: 9

// Enter character: C
// Enter frequency: 12

// Enter character: D
// Enter frequency: 13

// Enter character: E
// Enter frequency: 16

// Enter character: F
// Enter frequency: 45

// Huffman Codes:
// F : 0
// C : 100
// D : 101
// A : 1100
// B : 1101
// E : 111