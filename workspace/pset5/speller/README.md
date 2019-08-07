# Questions

## What is pneumonoultramicroscopicsilicovolcanoconiosis?

The artificial long word pneumonoultramicroscopicsilicovolcanoconiosis means a lung disease caused by inhaling fine dust and ash particles

## According to its man page, what does `getrusage` do?

it tells you information about the time and the amount of memory you have used.

## Per that same man page, how many members are in a variable of type `struct rusage`?

There are 16 members. 2 structs and 14 long variables

## Why do you think we pass `before` and `after` by reference (instead of by value) to `calculate`, even though we're not changing their contents?

We pass before and after rather than actual values is because of the size of rusage. If we had to copy the whole rusage onto the stack,
it would take up both time and memory which we dont want.

## Explain as precisely as possible, in a paragraph or more, how `main` goes about reading words from a file. In other words, convince us that you indeed understand how that function's `for` loop works.

After ensuring that the file has opened, the for loop checks that the current character is not the end of the file. c is then assigned the first character and it keeps incrementing unitl the
loop exits. The if statement inside the loop then checks to ensure that it is either an alphabet or an apostrophe(which is not at the beginning of the word). The character is then added
into the word array. If the word is too long, then index is set back to zero. If there are any numbers involved, we ignore them and set index up for a new word. If all fo these turn out
to be false, we can conclude that we have found a whole word and we terminate the array with the null character('\0'). We then check the spellings of each word and if they are misspelled we
print the word and increment the misspellings variable. Finally, we unload and close the file before we print out all the data we have collected.

## Why do you think we used `fgetc` to read each word's characters one at a time rather than use `fscanf` with a format string like `"%s"` to read whole words at a time? Put another way, what problems might arise by relying on `fscanf` alone?

The problem with using fscanf is that it does not know the difference between a character in the alphabet or a period, tab, slash, etc... In other words it only understands
that there is a new word if it catches a white space. fgetc on the other hand is more useful because you can use functions like isalpha() to help you out.

## Why do you think we declared the parameters for `check` and `load` as `const` (which means "constant")?

So that the they don't accidently get changed.
