# taiyou-game-engine
Taiyou Game Engine is a Pygame simplification Framework, it have Sprite Management, Font Management and more!

==-How to render a sprite?
1 - drop the file to the /Source/SPRITE/ folder
2 - sprite.RenderSprite(DISPLAY, "/sprite_name.png", (20,20,50,50)
                        /\        /\                 /\
                        Surface   File Location      Rectangle

==-How to render a text?
1 - drop the file to the /Source/FONT/ folder
2 - sprite.RenderFont(DISPLAY,"/font_file.ttf",20,20,28)
                      /\        /\             /\/\/\
                      Surface   File Location  X Y Font Size
