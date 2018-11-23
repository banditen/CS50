# Questions

## What is pneumonoultramicroscopicsilicovolcanoconiosis?

It's a invented word to work as a synonym to the disease silicosis

## According to its man page, what does `getrusage` do?

It measures the usage of resources in a process, and in this situation, the amount of time used in scanning through the words

## Per that same man page, how many members are in a variable of type `struct rusage`?

16

## Why do you think we pass `before` and `after` by reference (instead of by value) to `calculate`, even though we're not changing their contents?

Because we use `before` and `after` several times in the program, so it is cleaner and better to referenve to it rather than using the value

## Explain as precisely as possible, in a paragraph or more, how `main` goes about reading words from a file. In other words, convince us that you indeed understand how that function's `for` loop works.

First we initialize the file with function `fgetc`, which fetches each character in the given text-file, and increment the loop until it's at the end of the file. `isalpha()` let's us search only for alphabetical characters,
and if true, then we append each character to a word-array. When we meet a space, then the word is 'created' (word[index] = '\0';), and when it is 'created', then we check the spelling of the word.

## Why do you think we used `fgetc` to read each word's characters one at a time rather than use `fscanf` with a format string like `"%s"` to read whole words at a time? Put another way, what problems might arise by relying on `fscanf` alone?

Because with `fscanf` take's special characters in consideration, such as junk memory (i.e. `\0` value). That's why spellchecking with `fscanf` would lead to a error/problem

## Why do you think we declared the parameters for `check` and `load` as `const` (which means "constant")?

Because we want them to remain as a constants in the pointer-file's `a` and `b`
