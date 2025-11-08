// See https://aka.ms/new-console-template for more information
// Console.WriteLine("Hello, World!");


using System;

namespace lab_program
{
    class Vehicle{
        protected int speed;
        protected int fuel;

        public virtual void ShowInfo(){
            Console.WriteLine($"Fuel: {fuel}, Speed:{speed}");
        }

        public virtual void Drive(){
            fuel = fuel - 5;
            Console.WriteLine("base class");
        }
    }

    class Car:Vehicle{
        public int passenger;

        public override void Drive(){
            fuel -= 10;
            Console.WriteLine($"Car is moving with passenger");
        }

        public override void ShowInfo()
        {
            base.ShowInfo(); 
            Console.WriteLine($"Fuel: {fuel}, Speed:{speed}, passenger : {passenger}");
        }
    }



    class Truck:Vehicle{
        public int cargoWeight;

        public override void Drive(){
            fuel = fuel - 15;
            Console.WriteLine($"Truck is moving with Cargo");
        }
        
        public override void ShowInfo(){
            base.ShowInfo();
            Console.WriteLine($"Fuel: {fuel}, Speed:{speed}, Cargo: {cargoWeight}");
        }


    }


    class Program
    {
        // private int field
        private int data;
        static int counter;

        // Constructor for the class 
        public Program(int x){
            data = x;
            counter++;
            Console.WriteLine($"Constructor Called with value assignment counter:{counter}");
        }

        public Program(){
            data = 0;
            counter++;
            Console.WriteLine($"Constructor Called data = 0  counter: {counter}");
        }

        // Destructor are nto public or private
        ~Program(){
            counter--;
            Console.WriteLine($"Destructor Called counter: {counter}");
        }


        public void show_data(){
            Console.WriteLine($"Value of data: {data}");
        }

        public void set_data(int x){
            data = x;
        }

        public static  void lol(){
            Program p1 = new Program(10);
            Program p2 = new Program();
            Program p3 = new Program(3);

            p1.set_data(10);
            p2.set_data(20);
            p3.set_data(30);

            p1.show_data();
            p2.show_data();
            p3.show_data();
        }

        public static void q2(){
            Vehicle v = new Vehicle();
            Car c = new Car();
            Truck t = new Truck();

            Vehicle[] arr = {v,c,t};

            for (int i = 0; i < 3; i++)
            {
                arr[i].Drive();
                arr[i].ShowInfo();
            }
        }

        // main function that gets called or the entry point for the program
        public static void Main(string[] args){
            Console.WriteLine("Hello World! We are inside main");

            // lol(); 



            q2();

            // force garbage collection
            GC.Collect();
            GC.WaitForPendingFinalizers();
            Console.WriteLine("End of Main");        
        }
    }
}
