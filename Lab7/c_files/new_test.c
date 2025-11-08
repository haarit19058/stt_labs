#include <stdio.h>

int main()
{
    int z;
    int y = 3;
    int x = 10;
    if(y>0)
    {
        x = 1;
        y = 2;
    }
    else
    {
        z = x;
        x = 4;
    }
    z = y;
    x = z;
}