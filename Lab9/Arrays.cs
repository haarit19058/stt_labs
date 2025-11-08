using System;

namespace LAB_9
{
    class ArrayOperations
    {
        // 1. Bubble Sort
        public void BubbleSort(int[] arr)
        {
            int n = arr.Length;
            for (int i = 0; i < n - 1; i++)
            {
                for (int j = 0; j < n - i - 1; j++)
                {
                    if (arr[j] > arr[j + 1])
                    {
                        // Swap
                        int temp = arr[j];
                        arr[j] = arr[j + 1];
                        arr[j + 1] = temp;
                    }
                }
            }
        }

        // 2. Store 2D array into 1D array (Row Major Order)
        public int[] RowMajor(int[,] matrix)
        {
            int rows = matrix.GetLength(0);
            int cols = matrix.GetLength(1);
            int[] result = new int[rows * cols];
            int index = 0;

            for (int i = 0; i < rows; i++)
            {
                for (int j = 0; j < cols; j++)
                {
                    result[index++] = matrix[i, j];
                }
            }
            return result;
        }

        // 3. Store 2D array into 1D array (Column Major Order)
        public int[] ColumnMajor(int[,] matrix)
        {
            int rows = matrix.GetLength(0);
            int cols = matrix.GetLength(1);
            int[] result = new int[rows * cols];
            int index = 0;

            for (int j = 0; j < cols; j++)
            {
                for (int i = 0; i < rows; i++)
                {
                    result[index++] = matrix[i, j];
                }
            }
            return result;
        }

        // 4. Matrix Multiplication: C = A × B
        public int[,] MultiplyMatrices(int[,] A, int[,] B)
        {
            int aRows = A.GetLength(0);
            int aCols = A.GetLength(1);
            int bRows = B.GetLength(0);
            int bCols = B.GetLength(1);

            if (aCols != bRows)
            {
                Console.WriteLine("Matrix multiplication not possible: incompatible dimensions.");
                return null;
            }

            int[,] C = new int[aRows, bCols];

            for (int i = 0; i < aRows; i++)
            {
                for (int j = 0; j < bCols; j++)
                {
                    for (int k = 0; k < aCols; k++)
                    {
                        C[i, j] += A[i, k] * B[k, j];
                    }
                }
            }

            return C;
        }

        // Utility function to print 1D array
        public void PrintArray(int[] arr)
        {
            foreach (int val in arr)
                Console.Write(val + " ");
            Console.WriteLine();
        }

        // Utility function to print 2D array
        public void PrintMatrix(int[,] matrix)
        {
            for (int i = 0; i < matrix.GetLength(0); i++)
            {
                for (int j = 0; j < matrix.GetLength(1); j++)
                    Console.Write(matrix[i, j] + " ");
                Console.WriteLine();
            }
        }
    }
}