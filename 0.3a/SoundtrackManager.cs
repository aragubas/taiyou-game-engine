/*
   ####### BEGIN APACHE 2.0 LICENSE #######
   Copyright 2019 Parallex Software

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

   ####### END APACHE 2.0 LICENSE #######




   ####### BEGIN MONOGAME LICENSE #######
   THIS GAME-ENGINE WAS CREATED USING THE MONOGAME FRAMEWORK
   Github: https://github.com/MonoGame/MonoGame#license 

   MONOGAME WAS CREATED BY MONOGAME TEAM

   THE MONOGAME LICENSE IS IN THE MONOGAME_License.txt file on the root folder. 

   ####### END MONOGAME LICENSE ####### 





*/

using System;
using System.Collections.Generic;
using System.Globalization;
using Microsoft.Xna.Framework.Audio;

namespace TaiyouGameEngine.Desktop
{
    public class SoundtrackManager
    {
        // BGM Vars
        public static List<string> Current_BGM_Name = new List<string>() ;
        public static List<string> Current_BGM_Command = new List<string>();
        public static List<SoundEffectInstance> Current_BGM_Instances = new List<SoundEffectInstance>();


        public static void SendBGMCommand(string BGM_NAME, string BGM_COMMAND)
        {
            if (BGM_NAME == "@ALL_BGM")
            {
                for (int i = 0; i < Current_BGM_Name.Count; i++)
                {
                    Current_BGM_Command[i] = BGM_COMMAND;
                }
                return;
            }
            int BGMNameIndex = Current_BGM_Name.IndexOf(BGM_NAME);
            if (BGMNameIndex == -1) { throw new Exception("The BGM [" + BGM_NAME + "] does not exist."); }
            Current_BGM_Command[BGMNameIndex] = BGM_COMMAND;
            

        }

        public static void CreateBGMInstances()
        {
            for (int i = 0; i < SoundLoader.AllLoadedSounds_Names.Count; i++)
            {
                if (SoundLoader.AllLoadedSounds_Names[i].StartsWith("BGM_"))
                {
                    Current_BGM_Name.Add(SoundLoader.AllLoadedSounds_Names[i].Replace("BGM_",""));
                    Current_BGM_Instances.Add(SoundLoader.AllLoadedSounds_Content[i].CreateInstance());
                    Current_BGM_Command.Add("");
                }
            }
        }

        public static void Update()
        {

            for (int i = 0; i < Current_BGM_Name.Count; i++)
            {
                SoundEffectInstance SoundInstance = Current_BGM_Instances[i];

                if (Current_BGM_Command.Count == 0) { return; }

                if (Current_BGM_Command[i].Contains("LOOP"))
                {
                    string[] Slippted = Current_BGM_Command[i].Split('|');

                    if (Slippted[1] == "TRUE")
                    {
                        SoundInstance.IsLooped = true;
                    }
                    else if (Slippted[1] == "FALSE")
                    {
                        SoundInstance.IsLooped = false;
                    }
                    else
                    {
                        throw new Exception("Wrong parameter Setting");
                    }


                }

                if (Current_BGM_Command[i].Contains("PLAY"))
                {
                    string[] Slippted = Current_BGM_Command[i].Split('|');

                    if (SoundInstance.State == SoundState.Paused)
                    {
                        SoundInstance.Resume();
                    }
                    else
                    {
                        SoundInstance.Play();
                    }

                }


                if (Current_BGM_Command[i].Contains("STOP"))
                {
                    string[] Slippted = Current_BGM_Command[i].Split('|');

                    SoundInstance.Stop();

                }

                if (Current_BGM_Command[i].Contains("PAUSE"))
                {
                    string[] Slippted = Current_BGM_Command[i].Split('|');

                    SoundInstance.Pause();

                }

                if (Current_BGM_Command[i].Contains("PAN"))
                {
                    string[] Slippted = Current_BGM_Command[i].Split('|');
                    float SoundPan = float.Parse(Slippted[1], CultureInfo.InvariantCulture.NumberFormat);

                    SoundInstance.Pan = SoundPan;

                }

                if (Current_BGM_Command[i].Contains("VOLUME"))
                {
                    string[] Slippted = Current_BGM_Command[i].Split('|');
                    float SoundVolume = float.Parse(Slippted[1], CultureInfo.InvariantCulture.NumberFormat);

                    SoundInstance.Volume = SoundVolume;

                }

                if (Current_BGM_Command[i].Contains("PITCH"))
                {
                    string[] Slippted = Current_BGM_Command[i].Split('|');
                    float PitchValue = float.Parse(Slippted[1], CultureInfo.InvariantCulture.NumberFormat);


                    SoundInstance.Pitch = PitchValue;

                }






            }

        }


    }
}
