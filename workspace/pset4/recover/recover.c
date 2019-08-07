#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t  BYTE;

int main(int argc, char *argv[])
{

    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Specify file to recover from\n");
        return 1;
    }

    FILE *inptr = fopen(argv[1], "rb");

    if (inptr == NULL)
    {
        fprintf(stderr, "Unable to open file %s\n", argv[1]);
        return 2;
    }

    int fileCount = 0;
    BYTE byteArray[512];
    int bytesRead = fread(byteArray, 1, 512, inptr);
    FILE *outptr = NULL;
    char filename[8];

    int i = 0;
    while (bytesRead > 0)
    {
        while (i < bytesRead)
        {
            if (byteArray[i] != 0xff && outptr == NULL)
            {
                i++;
                continue;
            }

            if (i + 3 < bytesRead && byteArray[i] == 0xff && byteArray[i + 1] == 0xd8 && byteArray[i + 2] == 0xff
                && (byteArray[i + 3] & 0xf0) == 0xe0)
            {
                if (outptr != NULL)
                {
                    fclose(outptr);
                    fileCount++;
                }

                sprintf(filename, "%03i.jpg", fileCount);
                outptr = fopen(filename, "wb");

                fwrite(&byteArray[i], 1, 1, outptr);
                fwrite(&byteArray[i + 1], 1, 1, outptr);
                fwrite(&byteArray[i + 2], 1, 1, outptr);
                fwrite(&byteArray[i + 3], 1, 1, outptr);

                i = i + 4;
            }
            else
            {
                fwrite(&byteArray[i], 1, 1, outptr);
                i++;
            }
        }
        i = 0;
        bytesRead = fread(byteArray, 1, 512, inptr);
    }
    return 0;
}