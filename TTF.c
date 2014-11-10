#include "TTF.h"

#include <iostream>

gSystem.Load("libGraf.so");

long getTextWidth(int font, float size, const char* text)
{
   UInt_t w = 0;
   UInt_t h = 0;
   TTF::SetTextFont(font);
   TTF::SetTextSize(size);
   TTF::GetTextExtent(w,h,text);
   return w;
}

long getTextHeight(int font, float size, const char* text)
{
   UInt_t w = 0;
   UInt_t h = 0;
   TTF::SetTextFont(font);
   TTF::SetTextSize(size);
   TTF::GetTextExtent(w,h,text);
   return h;
}
