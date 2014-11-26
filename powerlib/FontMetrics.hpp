#ifndef __FONTMETRICS_H__
#define __FONTMETRICS_H__

#include "TObject.h"

class FontMetrics: 
    public TObject 
{
    public:
        static long GetTextWidth(int font, float size, char* text);
        static long GetTextHeight(int font, float size, char* text);
        
    ClassDef(FontMetrics, 1)
};
#endif

