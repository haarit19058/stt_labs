using System;

namespace LAB12
{
    // Event args for the initial order creation (gives full order context)
    public class OrderEventArgs : EventArgs
    {
        public string Customer { get; }
        public string Product { get; }
        public int Quantity { get; }

        public OrderEventArgs(string customer, string product, int quantity)
        {
            Customer = customer;
            Product = product;
            Quantity = quantity;
        }
    }

    // For shipping events (task 2) — only product + express required
    public class ShipEventArgs : EventArgs
    {
        public string Product { get; }
        public bool Express { get; }

        public ShipEventArgs(string product, bool express)
        {
            Product = product;
            Express = express;
        }
    }

    public class RejectionEventArgs : EventArgs
    {
        public string Reason { get; }
        public RejectionEventArgs(string reason) => Reason = reason;
    }
}
