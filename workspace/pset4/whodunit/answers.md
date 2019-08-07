# Questions

## What's `stdint.h`?

It provides potable integer types

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

If we want platform neutral unsigned/signed one BYTE, two BYTES, or four BYTES integers then we use the above types.

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

A BYTE is one BYTE
A DWORD is four BYTES
A LONG is four BYTES
A WORD is two BYTES

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

0x42 Ox4d

## What's the difference between `bfSize` and `biSize`?

bfSize is the size of BITMAPFILEHEADER(14 BYTES) and biSize is the size of BITMAPINFOHEADER(40 BYTES).

## What does it mean if `biHeight` is negative?

The images orientation is upside down.

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

biBitCount specifies the number of bits per pixel.

## Why might `fopen` return `NULL` in lines 24 and 32 of `copy.c`?

fopen might return a NULL pointer if the file that fopen is trying to write to doesn't exist.
This can also happen if their are permission issues.

## Why is the third argument to `fread` always `1` in our code?

Because we always want to read 1 * size BYTES.

## What value does line 63 of `copy.c` assign to `padding` if `bi.biWidth` is `3`?

copy.c assigns padding to 3 if bi.biWidth is 3;

## What does `fseek` do?

It positions the file pointer at a specific location in the file.

## What is `SEEK_CUR`?

It positions the file pointer at a specific location in the file.
