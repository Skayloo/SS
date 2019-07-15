using Parser.Core;
using Piesa.Core.Habra;
using System;
using System.Text;
using System.Windows.Forms;

namespace Piesa
{
    public partial class Form1 : Form
    {
        ParserWorker<string[]> parser;
        public Form1()
        {
            InitializeComponent();
            parser = new ParserWorker<string[]>(
                                new HabraParser()
                            );

            parser.OnCompleted += Parser_OnCompleted;
            parser.OnNewData += Parser_OnNewData;
        }

        private void Parser_OnNewData(object arg1, string[] arg2)
        {
            StringBuilder sb = new StringBuilder();
            ListTitles.Items.AddRange(arg2);
        }

        private void Parser_OnCompleted(object obj)
        {
            MessageBox.Show("All works done!");
        }
        private void ButtonStart_Click(object sender, EventArgs e)
        {
            ListTitles.Items.Clear();
            parser.Settings = new HabraSettings((int)NumericStart.Value, (int)NumericEnd.Value);
            parser.Start();
        }

        private void ButtonStop_Click(object sender, EventArgs e)
        {
            parser.Abort();
        }
    }
}
