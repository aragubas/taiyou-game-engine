using System;
namespace TaiyouScriptEngine.Desktop.Taiyou
{
    public class Variable
    {
        // Object Properties
        public string Type;
        public string Tag;
        public string Value;
        public string SearchPattern;

        public Variable(string varType, string varValue, string VarTag)
        {
            Tag = VarTag;
            Type = varType;
            Value = varValue;
            SearchPattern = "$" + VarTag + "$";

            if (Type == "Int" && Value.StartsWith("$", StringComparison.Ordinal))
            {
                int VarIndex = Global.VarList_Keys.IndexOf(Value.Remove(0, 1));
                if (VarIndex == -1) { throw new Exception("Cannot find typed variable [" + Value + "]."); }
                Value = Global.VarList[VarIndex].Value;
            }


            try
            {
                var Result = new Object();
                switch (Type)
                {
                    case "Bool":
                        Result = Convert.ToBoolean(Value);
                        break;

                    case "Int":
                        Result = Convert.ToInt32(Value);
                        break;

                    case "Float":
                        Result = float.Parse(Value);
                        break;

                }

                Console.WriteLine(Result);
            }
            catch (Exception)
            {
                Console.WriteLine(" -- The variable value is invalid for the variable type --");
                Console.WriteLine("VarTag: " + Tag);
                Console.WriteLine("VarType: " + Type);
                Console.WriteLine("VarValue: " + Value);
                Console.WriteLine("SeachPattern: " + SearchPattern);
                throw new Exception("The variable value is invalid for the variable type.");
            }

        }

        public object Get_Value()
        {
            switch (Type)
            {
                case "Bool":
                    return Convert.ToBoolean(Value);
                     
                case "Int":
                    return Convert.ToInt32(Value);
                     
                case "Float":
                    return float.Parse(Value);

                default:
                    return Value;

            }


        }
    }
}
