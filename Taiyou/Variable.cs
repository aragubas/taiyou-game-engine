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
