using System;
using System.Collections;
public class Program
{
int x;
public static void Main(string[] args)
{
ArrayList L=new ArrayList();
L.Add(new Program());
L.Add(new Program());
for (int i=0;i<L.Count;i++)
Console.WriteLine(++((Program)L[i]).x);
L[0]=L[1];
((Program)L[0]).x = 202;
for (int i=0;i<L.Count;i++)
Console.WriteLine(((Program)L[i]).x);
((Program)L[0]).x = 111;
L.RemoveAt(0);
Console.WriteLine(L.Count);
Console.WriteLine(((Program)L[0]).x);
}
}
