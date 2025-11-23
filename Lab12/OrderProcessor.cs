using System;
using System.Windows.Forms;

namespace LAB12
{
    public class OrderProcessor
    {
        public event EventHandler<OrderEventArgs> OrderCreated;
        public event EventHandler<RejectionEventArgs> OrderRejected;
        public event EventHandler<OrderEventArgs> OrderConfirmed;

        public event EventHandler<ShipEventArgs> OrderShipped;

        public void CreateOrder(string customer, string product, int quantity)
        {
            OrderCreated?.Invoke(this, new OrderEventArgs(customer, product, quantity));
        }

        // Validate - now also shows summary ONLY when valid
        public void ValidateOrder(object sender, OrderEventArgs e)
        {
            if (e.Quantity > 0)
            {
                // Show summary AFTER validation (fix for double MessageBox)
                MessageBox.Show($"Customer: {e.Customer}\nProduct: {e.Product}\nQuantity: {e.Quantity}",
                                "Order Summary");

                // valid -> raise confirmation
                OrderConfirmed?.Invoke(this, new OrderEventArgs(e.Customer, e.Product, e.Quantity));
            }
            else
            {
                OrderRejected?.Invoke(this, new RejectionEventArgs("Invalid quantity"));
            }
        }

        public void Ship(string product, bool express)
        {
            OrderShipped?.Invoke(this, new ShipEventArgs(product, express));
        }

        public void NotifyCourier(object sender, ShipEventArgs e)
        {
            if (e.Express)
            {
                MessageBox.Show("Express delivery initiated!");
            }
        }
    }
}