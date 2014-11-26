#include "FontMetrics.hpp"
#include "TTF.h"

ClassImp(FontMetrics)

long FontMetrics::GetTextWidth(int font, float size, char* text)
{
   UInt_t w = 0;
   UInt_t h = 0;
   TTF::SetTextFont(font);
   TTF::SetTextSize(size);
   TTF::GetTextExtent(w,h,text);
   return w;
}

long FontMetrics::GetTextHeight(int font, float size, char* text)
{
   UInt_t w = 0;
   UInt_t h = 0;
   TTF::SetTextFont(font);
   TTF::SetTextSize(size);
   TTF::GetTextExtent(w,h,text);
   return h;
}  
