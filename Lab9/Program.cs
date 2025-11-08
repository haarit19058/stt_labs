using System;

namespace LAB_9
{
    // Main program class
    class Program
    {
        static void Main(string[] args)
        {
            //Calculator calc = new Calculator();

            //// Accepting user input
            //Console.Write("Enter the first number: ");
            //double num1 = Convert.ToDouble(Console.ReadLine());

            //Console.Write("Enter the second number: ");
            //double num2 = Convert.ToDouble(Console.ReadLine());

            //// Performing operations
            //double sum = calc.Add(num1, num2);
            //double diff = calc.Subtract(num1, num2);
            //double prod = calc.Multiply(num1, num2);
            //double div = calc.Divide(num1, num2);

            //// Displaying results
            //Console.WriteLine("\n--- Results ---");
            //Console.WriteLine($"Addition: {sum}");
            //Console.WriteLine($"Subtraction: {diff}");
            //Console.WriteLine($"Multiplication: {prod}");
            //Console.WriteLine($"Division: {div}");

            //// Check if sum is even or odd
            //if (sum % 2 == 0)
            //    Console.WriteLine("The sum is even.");
            //else
            //    Console.WriteLine("The sum is odd.");

            ArrayOperations arrOps = new ArrayOperations();

            int[] numbers = { 5, 3, 8, 1, 4 };
            Console.WriteLine("\nOriginal array:");
            arrOps.PrintArray(numbers);
            arrOps.BubbleSort(numbers);
            Console.WriteLine("Sorted array:");
            arrOps.PrintArray(numbers);

            int[,] matrix = { { 1, 2, 3 }, { 4, 5, 6 } };
            Console.WriteLine("\nOriginal 2D array:");
            arrOps.PrintMatrix(matrix);
            Console.WriteLine("Row-major order:");
            arrOps.PrintArray(arrOps.RowMajor(matrix));
            Console.WriteLine("Column-major order:");
            arrOps.PrintArray(arrOps.ColumnMajor(matrix));

            int[,] A = { { 1, 2 }, { 3, 4 } };
            int[,] B = { { 5, 6 }, { 7, 8 } };
            Console.WriteLine("\nMatrix A:");
            arrOps.PrintMatrix(A);
            Console.WriteLine("Matrix B:");
            arrOps.PrintMatrix(B);
            Console.WriteLine("Matrix A × B:");
            int[,] C = arrOps.MultiplyMatrices(A, B);
            arrOps.PrintMatrix(C);
        }
    }
}