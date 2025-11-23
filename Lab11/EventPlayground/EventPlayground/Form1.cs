//namespace EventPlayground
//{
//    public partial class Form1 : Form
//    {

//        public delegate void ColorChangedEventHandler(object sender, EventArgs e);
//        public delegate void TextChangedEventHandler(object sender, EventArgs e);

//        public event ColorChangedEventHandler ColorChangedEvent;
//        public event TextChangedEventHandler TextChangedEvent;

//        public Form1()
//        {
//            InitializeComponent();

//            this.ColorChangedEvent += new ColorChangedEventHandler(OnColorChanged);
//            this.TextChangedEvent += new TextChangedEventHandler(OnTextChanged);
//        }

//        private void Form1_Load(object sender, EventArgs e)
//        {

//            cmbColors.Items.Add("Red");
//            cmbColors.Items.Add("Green");
//            cmbColors.Items.Add("Blue");

//            cmbColors.SelectedIndex = 0;
//        }

//        private void btnChangeColor_Click(object sender, EventArgs e)
//        {
//            ColorChangedEvent?.Invoke(this, EventArgs.Empty);
//        }

//        private void btnChangeText_Click(object sender, EventArgs e)
//        {
//            TextChangedEvent?.Invoke(this, EventArgs.Empty);
//        }

//        private void OnColorChanged(object sender, EventArgs e)
//        {
//            string selectedColor = cmbColors.SelectedItem.ToString();

//            switch (selectedColor)
//            {
//                case "Red":
//                    lblDisplay.ForeColor = Color.Red;
//                    break;
//                case "Green":
//                    lblDisplay.ForeColor = Color.Green;
//                    break;
//                case "Blue":
//                    lblDisplay.ForeColor = Color.Blue;
//                    break;
//                default:
//                    lblDisplay.ForeColor = Color.Black;
//                    break;
//            }
//        }
//        private void OnTextChanged(object sender, EventArgs e)
//        {
//            lblDisplay.Text = DateTime.Now.ToString("F");
//        }

//        private void lblDisplay_Click(object sender, EventArgs e)
//        {

//        }
//    }
//}
























using System;
using System.Drawing;
using System.Windows.Forms;

namespace EventPlayground
{
    public partial class Form1 : Form
    {
        public class ColorEventArgs : EventArgs
        {
            public string SelectedColor { get; }
            public ColorEventArgs(string colorName)
            {
                SelectedColor = colorName;
            }
        }



        public delegate void ColorChangedEventHandler(object sender, ColorEventArgs e);
        public delegate void TextChangedEventHandler(object sender, EventArgs e);


        public event ColorChangedEventHandler ColorChangedEvent;
        public event TextChangedEventHandler TextChangedEvent;

        public Form1()
        {
            InitializeComponent();

            this.ColorChangedEvent += new ColorChangedEventHandler(UpdateLabelColor);
            this.ColorChangedEvent += new ColorChangedEventHandler(ShowNotification);

            this.TextChangedEvent += new TextChangedEventHandler(OnTextChanged);
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            cmbColors.Items.Add("Red");
            cmbColors.Items.Add("Green");
            cmbColors.Items.Add("Blue");

            cmbColors.SelectedIndex = 0;
        }



        private void btnChangeColor_Click(object sender, EventArgs e)
        {
            string selectedColor = cmbColors.SelectedItem.ToString();

            ColorEventArgs args = new ColorEventArgs(selectedColor);

            ColorChangedEvent?.Invoke(this, args);
        }

        private void btnChangeText_Click(object sender, EventArgs e)
        {
            TextChangedEvent?.Invoke(this, EventArgs.Empty);
        }

        private void UpdateLabelColor(object sender, ColorEventArgs e)
        {
            string selectedColor = e.SelectedColor;

            switch (selectedColor)
            {
                case "Red":
                    lblDisplay.ForeColor = Color.Red;
                    break;
                case "Green":
                    lblDisplay.ForeColor = Color.Green;
                    break;
                case "Blue":
                    lblDisplay.ForeColor = Color.Blue;
                    break;
                default:
                    lblDisplay.ForeColor = Color.Black;
                    break;
            }
        }

        private void ShowNotification(object sender, ColorEventArgs e)
        {
            string selectedColor = e.SelectedColor;
            MessageBox.Show($"The color has been changed to {selectedColor}.", "Color Change Notification");
        }

        private void OnTextChanged(object sender, EventArgs e)
        {
            lblDisplay.Text = DateTime.Now.ToString("F");
        }
    }
}