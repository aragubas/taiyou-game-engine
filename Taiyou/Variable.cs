using System;
namespace TaiyouScriptEngine.Desktop.Taiyou
{
    public class Variable
    {
        // Object Properties
        public string Type;
        public string Tag;
        public dynamic Value;
        public string SearchPattern;
        public string GenericVarType;

        public Variable(string varType, dynamic varValue, string VarTag)
        {
            Tag = VarTag;
            Type = varType;
            SearchPattern = "$" + VarTag + "$";

            // Set the variable Generic Type
            SetVarGeneticType(varType);

            if (Convert.ToString(varValue).StartsWith("$", StringComparison.Ordinal))
            {
                int VarIndex = Global.VarList_Keys.IndexOf(varValue.Remove(0, 1));
                if (VarIndex == -1) { throw new Exception("Cannot find variable [" + varValue + "]."); }
                Variable varWax = Global.VarList[VarIndex];

                if (varWax.GenericVarType != GenericVarType) { throw new Exception("Cannot copy destination variable to current variable since they are different types of variable."); }

                Value = Global.VarList[VarIndex].Value;
                return;
            }

            // Set the Value
            try
            {
                switch (varType)
                {
                    case "Bool":
                        Value = Convert.ToBoolean(varValue);
                        break;

                    case "Int":
                        Value = Convert.ToInt32(varValue);
                        break;

                    case "Float":
                        Value = float.Parse(varValue);
                        break;

                    case "String":
                        Value = Convert.ToString(varValue);
                        break;

                    default:
                        throw new ArgumentException("Variable type [" + varType + "] is invalid.");

                }

            }
            catch (Exception ex)
            {
                Console.WriteLine("\n\n####################");
                Console.WriteLine(ex.Message);
                Console.WriteLine("VarTag: " + Tag);
                Console.WriteLine("VarType: " + Type);
                Console.WriteLine("VarValue: " + Value);
                Console.WriteLine("SeachPattern: " + SearchPattern);
                Console.WriteLine("== Arguments ==");
                Console.WriteLine("VarType: " + varType);
                Console.WriteLine("VarValue: " + varValue);
                Console.WriteLine("VarType: " + varType);
                Console.WriteLine("VarTag: " + VarTag);
                Console.WriteLine("####################\n\n");

                throw ex;
            }

        }

        /// <summary>
        /// Set the variable generic type
        /// </summary>
        /// <param name="input">Input.</param>
        private void SetVarGeneticType(string input)
        {
            switch (input)
            {
                case "Bool":
                    GenericVarType = "Boolean";
                    break;

                case "Int":
                    GenericVarType = "Number";
                    break;

                case "Float":
                    GenericVarType = "Number";
                    break;

                case "String":
                    GenericVarType = "String";
                    break;

                default:
                    throw new ArgumentException("Cannot set GenericType\nVariable type [" + input + "] is invalid.");

            }

        }

        /// <summary>
        /// Returns the value
        /// </summary>
        /// <returns>The value.</returns>
        public dynamic Get_Value()
        {
            return Value;
        }

        /// <summary>
        /// Set the Variable value
        /// </summary>
        /// <param name="NewValue">New value.</param>
        public void Set_Value(dynamic NewValue)
        {
            switch (Type)
            {
                case "String":
                    Value = Convert.ToString(NewValue);
                    return;

                case "Int":
                    Value = Convert.ToInt32(NewValue);
                    return;

                case "Float":
                    Value = float.Parse(NewValue);
                    return;

                case "Bool":
                    Value = Convert.ToBoolean(NewValue);
                    return;


            }
        }

    }
}
