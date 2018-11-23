# Questions

## What's `stdint.h`?

stdint.h is a header file to allow programmers to write portable code by providing a set of typedefs that specify i.e. exact-width
integer types, together with the defined minimum and maximum allowable values for each type, using macros.

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

A `uint` is an unsigned integer, and the number represents its bit length (i.e. `uint8_t` is an unsigned 8-bit integer with max
value of 255 (2^8), while `uint16_t` is an unsigned 16-bit integer with a max value of 65535 (2^16)). This way we can use the
data in a certain way

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

`BYTE` = 1 bytes (8-bit)
`DWORD` = 4 bytes (32-bit)
`LONG` = 4 bytes (32-bit)
`WORD` = 2 bytes (16-bit)

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats(with high probability) are generally called "magic numbers."

The two first bytes must be BM (ASCII), 6677 (decimal), 0x424d (hexadecimal)

## What's the difference between `bfSize` and `biSize`?

`bfSize` = The size of the bitmap file (in bytes)
`biSize` = The number of bytes required by the structure

## What does it mean if `biHeight` is negative?

If `biHeight` is negative, the bitmap is a top-down DIB (device-independent bitmap) and its origin is the upper-left corner

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

The `biBitCount`

## Why might `fopen` return `NULL` in lines 24 and 32 of `copy.c`?

Because if it does not find the input and/or output file, then it will return NULL

## Why is the third argument to `fread` always `1` in our code?

We do always read 1 struct in our code, and `fread` specifies how many elements we want to read

## What value does line 63 of `copy.c` assign to `padding` if `bi.biWidth` is `3`?

It specifies that the padding is 3 (3 pixels * 3 bytes per pixel * 3 padding = 12), and 12 is a multiple of 4

## What does `fseek` do?

`fseek` let's us move to a specific location in a file

## What is `SEEK_CUR`?

An integer constant which specifies the offset relative to the current position of the file