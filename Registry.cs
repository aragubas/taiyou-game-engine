using System;
using System.Collections.Generic;
using System.IO;
using Microsoft.Xna.Framework;

namespace TaiyouScriptEngine.Desktop
{
    public static class Registry
    {
        public static List<string> LoadedKeysNames = new List<string>();
        public static List<string> LoadedKeysValues = new List<string>();


        public static string ReadKeyValue(string KeyName)
        {
            int KeyIndex = LoadedKeysNames.IndexOf(KeyName);

            try
            {
                string ValToReturn = LoadedKeysValues[KeyIndex];

                return ValToReturn;
            }catch (Exception) { throw new FileNotFoundException("Key:" + KeyName + " does not exist."); }
        }
         
        public static bool KeyExists(string KeyName)
        {
            int KeyIndex = LoadedKeysNames.IndexOf(KeyName);

            if (KeyIndex == -1) { return false; }
            return true;
        }

        public static void WriteKey(string KeyName, string KeyValue)
        {
            File.WriteAllText("/Data/REG" + KeyName + ".data", KeyValue,new System.Text.UTF8Encoding()); 

        }

        public static void Initialize(string Path)
        {
            LoadedKeysNames.Clear();
            LoadedKeysValues.Clear();

            Console.WriteLine("Registry.Initialize : Start");
                

            string[] AllKeys = Directory.GetFiles(Path, "*.data", SearchOption.AllDirectories);

            for (int i = 0; i < AllKeys.Length; i++)
            {
                string KeyNameFiltred = AllKeys[i].Replace(Path, "");
                KeyNameFiltred = KeyNameFiltred.Replace(".data", "");

                LoadedKeysNames.Add(KeyNameFiltred);
                LoadedKeysValues.Add(File.ReadAllText(Path + KeyNameFiltred + ".data").Replace("\n",""));
                LoadedKeysValues[i] = LoadedKeysValues[i].Replace("%n",Environment.NewLine);
                LoadedKeysValues[i] = LoadedKeysValues[i].Replace("%usr",Environment.UserName);
                LoadedKeysValues[i] = LoadedKeysValues[i].Replace("%current_dir",Environment.CurrentDirectory);
                LoadedKeysValues[i] = LoadedKeysValues[i].Replace("%machine_name",Environment.MachineName);
                LoadedKeysValues[i] = LoadedKeysValues[i].Replace("%processor_count",Convert.ToString(Environment.ProcessorCount));

                Console.WriteLine("\nKeyName: " + LoadedKeysNames[i]);
                Console.WriteLine("\nKeyValue: " + LoadedKeysValues[i]);

            }

            Console.WriteLine("Registry.Initialize : Operation");
            

        }
    }
}
