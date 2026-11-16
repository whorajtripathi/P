import java.util.*;

public class Fibo{

    static void nonRecursive(int n){
        int a=0,b=1,c;
        System.out.println("Non-Recursive!!");
        for(int i=0;i<n;i++){
            System.out.print(a+" ");
            c=a+b;
            a=b;
            b=c;
        }
        System.out.println();
    }

    static int Recursive(int n){
        if(n<=1){
            return n;
        }

        return Recursive(n-1)+Recursive(n-2);
    }

    public static void main(String[] args){

        Scanner sc=new Scanner(System.in);

        System.out.print("Enter n:");
        int n=sc.nextInt();

        if(n<0){
            System.out.println("Please enter non-negative n!!!!!!!!!!!");
            return;
        }
        nonRecursive(n);

        System.out.println("Recursive!!");
        for(int i=0;i<n;i++){
            System.out.print(Recursive(i)+" ");
        }

        sc.close();
    }
}