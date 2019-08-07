// Copies a BMP file

#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{

    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: copy infile outfile\n");
        return 1;
    }

    // remember filenames
    int factor = atoi(argv[1]);
    char *infile = argv[2];
    char *outfile = argv[3];

    if (factor < 1 || factor > 100)
    {
        printf("Factor must be in range 1..100!\n");
        return 1;
    }

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf, bfNew;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);
    bfNew = bf;

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi, biNew;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);
    biNew = bi;

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    // Determine the new dimensions
    biNew.biWidth  = bi.biWidth * factor;
    biNew.biHeight = bi.biHeight * factor;

    // Determine the old and new paddings
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) %4) % 4;
    int res_padding = (4 - (biNew.biWidth * sizeof(RGBTRIPLE)) %4) % 4;

    // Determine new image sizes
    biNew.biSizeImage = (biNew.biWidth * sizeof(RGBTRIPLE) + res_padding) * abs(biNew.biHeight);
    bfNew.bfSize = bf.bfSize - bi.biSizeImage + biNew.biSizeImage;

    // write outfile's BITMAPFILEHEADER
    fwrite(&bfNew, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&biNew, sizeof(BITMAPINFOHEADER), 1, outptr);

    // iterate over infile's scanlines
    int count = 0;
    RGBTRIPLE pixels[biNew.biWidth];

    for (int i = 0; i < abs(bi.biHeight); i++)
    {
        count = 0;
        // iterate over pixels in scanline
        for (int j = 0; j < bi.biWidth; j++)
        {
            RGBTRIPLE rgb;

            // read RGB triple from infile
            fread(&rgb, sizeof(RGBTRIPLE), 1, inptr);

            // write RGB triple to outfile
            for (int l = 0; l < factor; l++) {
                pixels[count] = rgb;
                count++;
            }
        }

        RGBTRIPLE pixel;
        for(int p = 0; p < factor; p++){
            for(int l = 0; l < biNew.biWidth; l++){
                pixel = pixels[l];
                fwrite(&pixel, sizeof(RGBTRIPLE), 1, outptr);
            }
            // then add it back (to demonstrate how)
            for (int k = 0; k < res_padding; k++)
            {
                fputc(0x00, outptr);
            }
        }
        // skip over padding, if any
        fseek(inptr, padding, SEEK_CUR);
    }
    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}