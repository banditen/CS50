/**
 * Recover.c
 * This program searches for hidden bytes
 * in the file "card.raw". This program can
 * be used with other .raw files, given that
 * the lost photos are in JPEG format. If not,
 * then we have to change the looping function
 * */

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

const int BLOCK_SIZE = 512;

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover file\n");
        return 1;
    }

    // open input file
    FILE *f = fopen(argv[1], "r");

    if (f == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", argv[1]);
        return 2;
    }

    // set pointer to outfile
    FILE *image = NULL;

    // create filename and buffer arrays
    unsigned char buff[BLOCK_SIZE];
    char filename[8];

    // set counter for images
    int counter = 0;

    // set flag to follow the progress of scanning
    bool flag = false;

    // read the input file until JPEG is found
    while (fread(buff, BLOCK_SIZE, 1, f) == 1)
    {
        // check if the first four bytes match
        if (buff[0] == 0xff && buff[1] == 0xd8 && buff[2] == 0xff && (buff[3] & 0xf0) == 0xe0)
        {
            // if true, then close and open next image
            if (flag == true)
            {
                fclose(image);
            }
            // set the condition for found JPEG
            else
            {
                flag = true;
            }

            // first, print image if it's true
            sprintf(filename, "%03i.jpg", counter);
            image = fopen(filename, "w");
            counter++;
        }

        if (flag == true)
        {
            // then write image if it's true
            fwrite(&buff, BLOCK_SIZE, 1, image);
        }
    }

    // close all files
    fclose(f);
    fclose(image);

    // exit & celebrate
    return 0;

}