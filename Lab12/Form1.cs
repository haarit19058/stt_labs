using System;
using System.Windows.Forms;

namespace LAB12
{
    public partial class Form1 : Form
    {
        private OrderProcessor orderProcessor;
        private bool lastOrderConfirmed = false;

        public Form1()
        {
            InitializeComponent();

            // initialize processor and UI elements
            orderProcessor = new OrderProcessor();

            // populate product combo
            cmbProduct.SelectedIndex = 0;

            // subscribe once (do NOT subscribe inside the button click)
            orderProcessor.OrderCreated += orderProcessor.ValidateOrder;
            //orderProcessor.OrderCreated += orderProcessor.DisplayOrderInfo;
            orderProcessor.OrderRejected += OnOrderRejected;
            orderProcessor.OrderConfirmed += OnOrderConfirmed;
            //orderProcessor.OrderConfirmed += orderProcessor.DisplayOrderInfo;

            // ShowDispatch (updates label) subscribed to shipping event
            orderProcessor.OrderShipped += OnShowDispatch;

            // wire button clicks
            btnProcessOrder.Click += btnProcessOrder_Click;
            btnShipOrder.Click += btnShipOrder_Click;
        }

        private void btnProcessOrder_Click(object sender, EventArgs e)
        {
            lblStatus.Visible = true;
            lblStatus.Text = "Processing...";

            string customer = txtCustomerName.Text.Trim();
            string product = cmbProduct.SelectedItem?.ToString() ?? "Unknown";
            int quantity = (int)numQuantity.Value;

            // reset confirmed flag before processing new order
            lastOrderConfirmed = false;
            
            orderProcessor.CreateOrder(customer, product, quantity);
        }

        // Called when OrderRejected event is raised
        private void OnOrderRejected(object sender, RejectionEventArgs e)
        {
            lastOrderConfirmed = false;
            lblStatus.Text = "Order Invalid – Please retry";
        }

        // Called when OrderConfirmed event is raised
        private void OnOrderConfirmed(object sender, OrderEventArgs e)
        {
            lastOrderConfirmed = true;
            lblStatus.Text = $"Order Processed Successfully for {e.Customer}";
        }

        // Shipping label update
        private void OnShowDispatch(object sender, ShipEventArgs e)
        {
            lblStatus.Text = $"Product dispatched: {e.Product}";
        }

        // Ship button: only works if previous order was confirmed
        private void btnShipOrder_Click(object sender, EventArgs e)
        {
            if (!lastOrderConfirmed)
            {
                MessageBox.Show("Previous order not confirmed. Cannot ship.");
                return;
            }

            string product = cmbProduct.SelectedItem?.ToString() ?? "Unknown";
            bool express = chkExpress?.Checked ?? false;

            // Ensure NotifyCourier is added only when express is checked.
            // We remove first to avoid duplicate subscription, then add if needed.
            orderProcessor.OrderShipped -= orderProcessor.NotifyCourier;
            if (express)
            {
                orderProcessor.OrderShipped += orderProcessor.NotifyCourier;
            }

            // raise shipping event
            orderProcessor.Ship(product, express);
        }
private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void label2_Click(object sender, EventArgs e)
        {

        }

        private void label4_Click(object sender, EventArgs e)
        {

        }


        private void lblStatus_Click(object sender, EventArgs e)
        {

        }

        private void Form1_Load_1(object sender, EventArgs e)
        {

        }

        private void checkBox1_CheckedChanged(object sender, EventArgs e)
        {

        }
    }
}
