namespace LAB12
{
    partial class Form1
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            txtCustomerName = new TextBox();
            label1 = new Label();
            label2 = new Label();
            label5 = new Label();
            cmbProduct = new ComboBox();
            numQuantity = new NumericUpDown();
            btnProcessOrder = new Button();
            lblStatus = new Label();
            chkExpress = new CheckBox();
            btnShipOrder = new Button();
            ((System.ComponentModel.ISupportInitialize)numQuantity).BeginInit();
            SuspendLayout();
            // 
            // txtCustomerName
            // 
            txtCustomerName.Location = new Point(188, 40);
            txtCustomerName.Name = "txtCustomerName";
            txtCustomerName.Size = new Size(232, 27);
            txtCustomerName.TabIndex = 0;
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Font = new Font("Segoe UI", 9F, FontStyle.Bold, GraphicsUnit.Point, 0);
            label1.Location = new Point(40, 43);
            label1.Name = "label1";
            label1.Size = new Size(123, 20);
            label1.TabIndex = 1;
            label1.Text = "Customer Name";
            // 
            // label2
            // 
            label2.AutoSize = true;
            label2.Font = new Font("Segoe UI", 9F, FontStyle.Bold, GraphicsUnit.Point, 0);
            label2.Location = new Point(40, 152);
            label2.Name = "label2";
            label2.Size = new Size(70, 20);
            label2.TabIndex = 2;
            label2.Text = "Quantity";
            // 
            // label5
            // 
            label5.AutoSize = true;
            label5.Font = new Font("Segoe UI", 9F, FontStyle.Bold, GraphicsUnit.Point, 0);
            label5.Location = new Point(40, 98);
            label5.Name = "label5";
            label5.Size = new Size(110, 20);
            label5.TabIndex = 5;
            label5.Text = "Product Name";
            // 
            // cmbProduct
            // 
            cmbProduct.FormattingEnabled = true;
            cmbProduct.Items.AddRange(new object[] { "Laptop", "Mouse", "Keyboard" });
            cmbProduct.Location = new Point(188, 95);
            cmbProduct.Name = "cmbProduct";
            cmbProduct.Size = new Size(151, 28);
            cmbProduct.TabIndex = 6;
            // 
            // numQuantity
            // 
            numQuantity.Location = new Point(189, 152);
            numQuantity.Name = "numQuantity";
            numQuantity.Size = new Size(150, 27);
            numQuantity.TabIndex = 7;
            // 
            // btnProcessOrder
            // 
            btnProcessOrder.Location = new Point(188, 205);
            btnProcessOrder.Name = "btnProcessOrder";
            btnProcessOrder.Size = new Size(150, 35);
            btnProcessOrder.TabIndex = 8;
            btnProcessOrder.Text = "Process Order";
            btnProcessOrder.UseVisualStyleBackColor = true;
            btnProcessOrder.Click += btnProcessOrder_Click;
            // 
            // lblStatus
            // 
            lblStatus.AutoSize = true;
            lblStatus.Font = new Font("Segoe UI", 9F, FontStyle.Bold, GraphicsUnit.Point, 0);
            lblStatus.Location = new Point(189, 258);
            lblStatus.Name = "lblStatus";
            lblStatus.Size = new Size(70, 20);
            lblStatus.TabIndex = 9;
            lblStatus.Text = "Quantity";
            lblStatus.Visible = false;
            lblStatus.Click += lblStatus_Click;
            // 
            // chkExpress
            // 
            chkExpress.AutoSize = true;
            chkExpress.Location = new Point(194, 301);
            chkExpress.Name = "chkExpress";
            chkExpress.Size = new Size(80, 24);
            chkExpress.TabIndex = 10;
            chkExpress.Text = "Express";
            chkExpress.UseVisualStyleBackColor = true;
            chkExpress.CheckedChanged += checkBox1_CheckedChanged;
            // 
            // btnShipOrder
            // 
            btnShipOrder.Location = new Point(188, 331);
            btnShipOrder.Name = "btnShipOrder";
            btnShipOrder.Size = new Size(150, 35);
            btnShipOrder.TabIndex = 11;
            btnShipOrder.Text = "Ship Order";
            btnShipOrder.UseVisualStyleBackColor = true;
            // 
            // Form1
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(553, 450);
            Controls.Add(btnShipOrder);
            Controls.Add(chkExpress);
            Controls.Add(lblStatus);
            Controls.Add(btnProcessOrder);
            Controls.Add(numQuantity);
            Controls.Add(cmbProduct);
            Controls.Add(label5);
            Controls.Add(label2);
            Controls.Add(label1);
            Controls.Add(txtCustomerName);
            Name = "Form1";
            Text = "OrderPipeline";
            Load += Form1_Load_1;
            ((System.ComponentModel.ISupportInitialize)numQuantity).EndInit();
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private TextBox txtCustomerName;
        private Label label1;
        private Label label2;
        private Label label5;
        private ComboBox cmbProduct;
        private NumericUpDown numQuantity;
        private Button btnProcessOrder;
        private Label lblStatus;
        private CheckBox chkExpress;
        private Button btnShipOrder;
    }
}
