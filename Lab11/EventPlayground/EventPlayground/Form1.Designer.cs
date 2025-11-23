namespace EventPlayground
{
    partial class Form1
    {

        private System.ComponentModel.IContainer components = null;

        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code


        private void InitializeComponent()
        {
            btnChangeColor = new Button();
            btnChangeText = new Button();
            lblDisplay = new Label();
            cmbColors = new ComboBox();
            SuspendLayout();
            // 
            // btnChangeColor
            // 
            btnChangeColor.Font = new Font("Segoe UI", 9.75F, FontStyle.Regular, GraphicsUnit.Point, 0);
            btnChangeColor.Location = new Point(100, 346);
            btnChangeColor.Margin = new Padding(6, 7, 6, 7);
            btnChangeColor.Name = "btnChangeColor";
            btnChangeColor.Size = new Size(240, 92);
            btnChangeColor.TabIndex = 0;
            btnChangeColor.Text = "Change Color";
            btnChangeColor.UseVisualStyleBackColor = true;
            btnChangeColor.Click += btnChangeColor_Click;
            // 
            // btnChangeText
            // 
            btnChangeText.Font = new Font("Segoe UI", 9.75F, FontStyle.Regular, GraphicsUnit.Point, 0);
            btnChangeText.Location = new Point(400, 346);
            btnChangeText.Margin = new Padding(6, 7, 6, 7);
            btnChangeText.Name = "btnChangeText";
            btnChangeText.Size = new Size(240, 92);
            btnChangeText.TabIndex = 1;
            btnChangeText.Text = "Change Text";
            btnChangeText.UseVisualStyleBackColor = true;
            btnChangeText.Click += btnChangeText_Click;
            // 
            // lblDisplay
            // 
            lblDisplay.Font = new Font("Segoe UI", 14.25F, FontStyle.Bold, GraphicsUnit.Point, 0);
            lblDisplay.Location = new Point(24, 138);
            lblDisplay.Margin = new Padding(6, 0, 6, 0);
            lblDisplay.Name = "lblDisplay";
            lblDisplay.Size = new Size(692, 115);
            lblDisplay.TabIndex = 2;
            lblDisplay.Text = "Welcome to Events Lab";
            lblDisplay.TextAlign = ContentAlignment.MiddleCenter;
            //lblDisplay.Click += lblDisplay_Click;
            // 
            // cmbColors
            // 
            cmbColors.DropDownStyle = ComboBoxStyle.DropDownList;
            cmbColors.Font = new Font("Segoe UI", 9.75F, FontStyle.Regular, GraphicsUnit.Point, 0);
            cmbColors.FormattingEnabled = true;
            cmbColors.Location = new Point(100, 46);
            cmbColors.Margin = new Padding(6, 7, 6, 7);
            cmbColors.Name = "cmbColors";
            cmbColors.Size = new Size(536, 39);
            cmbColors.TabIndex = 3;
            // 
            // Form1
            // 
            AutoScaleDimensions = new SizeF(12F, 30F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(768, 487);
            Controls.Add(cmbColors);
            Controls.Add(lblDisplay);
            Controls.Add(btnChangeText);
            Controls.Add(btnChangeColor);
            FormBorderStyle = FormBorderStyle.FixedSingle;
            Margin = new Padding(6, 7, 6, 7);
            MaximizeBox = false;
            Name = "Form1";
            StartPosition = FormStartPosition.CenterScreen;
            Text = "Event Playground";
            Load += Form1_Load;
            ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.Button btnChangeColor;
        private System.Windows.Forms.Button btnChangeText;
        private System.Windows.Forms.Label lblDisplay;
        private System.Windows.Forms.ComboBox cmbColors;
    }
}