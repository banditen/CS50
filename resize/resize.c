// Resizes a BMP file

#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        printf("Usage: ./resize n infile outfile\n");
        return 1;
    }

    // store the resizing number in argv[1]
    int n = atoi(argv[1]);

    // set resizing boundaries
    if (n < 1 || n > 100)
    {
        fprintf(stderr, "Scale must be between 1 and 100\n");
        return 1;
    }

    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

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
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    //writing the outfile's BITMAPFILEHEADER and BITMAPINFOHEADER
    BITMAPFILEHEADER new_bf = bf;
    BITMAPINFOHEADER new_bi = bi;

    //rescaling the outfile's width and height
    new_bi.biWidth *= n;
    new_bi.biHeight *= n;

    // determine padding for scanlines for both files
    int in_padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int out_padding = (4 - (new_bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // determine the outfile biSizeImage and bfSize (biSizeImage + 54 bytes header files)
    new_bi.biSizeImage = abs(new_bi.biHeight) * (new_bi.biWidth * sizeof(RGBTRIPLE) + out_padding);
    new_bf.bfSize = (new_bi.biSizeImage + 54);

    // write outfile's BITMAPFILEHEADER
    fwrite(&new_bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&new_bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
    {
        for (int j = 0; j < n; j++)
        {
            // set pointer to the beginning of scanline
            fseek(inptr, 54 + (bi.biWidth * 3 + in_padding) * i, SEEK_SET);

            // iterate over pixels in scanline
            for (int k = 0; k < bi.biWidth; k++)
            {
                // temporary storage
                RGBTRIPLE triple;

                // read RGB triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

                // resize each pixel at a time
                for (int l = 0; l < n; l++)
                {
                    // write RGB triple to outfile
                    fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                }
            }

            // then add it back to oufile
            for (int m = 0; m < out_padding; m++)
            {
                fputc(0x00, outptr);
            }
        }
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
