# Corpus Builder

## What is Corpus Builder
Corpus Builder is used to generate the NMT dataset that include train, dev, test and vocaburary files. To generate them, Corpus Builder has the following functionalities:
- Clean the pre-downloaded HTML files by checking file corruption and unwanted files
- Parse HTML files and extract text sentenses, and store those sentenses into corpus files
- Generate the standard vocaburary file that include the very basic and general text charactors
- Read the corpus files and generate the NMT data source files

## What is Corpus Files
Corpus files are JSON formatted text files that contain the series of source/target pair texts. Corpus files are used as medium file before generating the NMT data set, for the purposes of storing data temporarily or organising different sources of data.

## How to setup
Refer to [README Setup Corpus Builder](README%20Setup%20Corpus%20Builder.md).

## How to run
Corpus Builder is a Python script which main script file is ```build.py```. First, run the command below to see the help.
```
python build.py -h
```

Corpus Builder has severl sub-commands. For example, when your parse HTML files and generate corpus files, you use ```html parse``` sub-command. The help can be shown with the command below.
```
python build.py html parse -h
```

## HTML Parsing
There are 3 different types of HTML analysis and parsing used. Each of them parses the same HTML and generate sorce/target pairs, but they analyze HTML in different ways.

#### A. Header/Body
The source text is extracted from the header texts (H1, H2, H3 etc). The target text is the body of the trailing paragraphs that appear following after the header. This text contains line breaks.

The resulted text in the source is a line of text, and the target is a chain of several paragraphs.

#### B. Atomic
The smallest block of text that is extracted from the whole part of HTML, delimited by '。', section, line break or any type of atomic block of text.

This will result in single line of text for source, single line of test for target, and the same number of lines will be loaded in to both source and target file.

#### C. Atomic Header/Body
Like the Header/Body parser, the header becomes the source and the body becomes the target. But the body text is broken into the atomic piece of text, like the atomic parser, and the each atomic text is linked to that section's header.

This will result in the same line of text appears in the source, where the series of target text lines share the common source text.

## Special Tokens
The following tokens will appear in the vocabulary file to indicate special directions to the seq2seq RNN.

### Structural Types
Followings are the ones which are required for structural purposes.

#### \<unk\>
Unknown token. This is defined as zero in the Tensorflow NMT code.
So this has to appear at the top of vocab file (indexed by zero).

#### \<s\>
Start of sentense.

#### \</s\>
End of sentense.

#### \<br\>
Line break.

#### \<sp\>
Space. This is the half-width space.

#### \<fp\>
This is the Full-width space.

\<br\> and \<sp\> are required because line-breaks and spaces compose the source and target files. Line-breaks are used to delimit the lines, and spaces are used to separate words in those files.

Thus you need to symbolize them in the source/target data, and later when NMT emits the output then they are converted back into the actual character code data and turned into the final output.

### Vocaburary Optimization Type
These symbols are not mandatory but are used to optimize and reduce the vocaburary size.

#### \<c1\>
The word following after this token has the top letter in capital. For example, "<c1> apple" describes "Apple".

#### \<c2\>
The word following after this token has all letters in capital. For example, "<c2> apple" describes "APPLE".

These tokens replace the need for registering the same word for different capital patterns, and all alphabetical words in the vocaburary file are converted to lower case.
