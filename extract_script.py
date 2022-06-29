import argparse
import itertools
import glob
import re

from os import path, walk

STRING_RE = re.compile(r"'([^']*)?'", re.S)
PERCENT_RE = re.compile(r'%\(([^\)]*)\)', re.S)

TITLE = 0
NAME = 1
TEXT = 2
VOICE = 3
VOLUME = 4
WAIT = 5
COLOR = 6
CONTINUE = 7
FURIGANA = 8
SPEED = 9
TEXT_SIZE = 10
OB = 11
EB = 12
PIPE = 13
AFTER_PIPE = 14
TAG_CONTENT = 15
TEXT_PARALLEL = 16
ASPEED = 17

def get_strings(s):
    """
    Returns a list of strings from s.
    """

    strings = []

    # ''
    i = iter(STRING_RE.split(s))
    next(i)

    while True:

        try:
            text = next(i)
            next(i)

            strings.append(text)

        except StopIteration:
            break

    # %()
    # not the best way
    j = iter(PERCENT_RE.split(s))
    next(j)

    while True:

        try:
            text = next(j)
            next(j)

            strings.append(text)

        except StopIteration:
            break

    return strings

def tokenize(dialogue):

    """
    Analyze dialogue string.
    Dealing with dialogue commands r, v, k, |, y, o, b with <> and {}

    r - probably starts a new line of dialogue
    v - plays voice file (or just defines which voice file to play)
    k - extends text
    | and y - both are always together, they do some effects apperently
    o - volume maybe?
    {} - I don't know what these brackets do
    b with <> - used for furigana

    returns a list of tuple like (NAME, CONTENT), (VOICE, CONTENT)

    """

    components = re.split(r'(?=@.)', dialogue)
    strings = []
    furi1 = ""
    furi2 = ""
    text_continue = False

    for i, e in enumerate(components):
        
        text = ""
        TYPE = TEXT
        
        if e.startswith("@"):
            tag, content = e[0:2], e[2:]
        
            if tag == "@r":
                newline = True
                TYPE = TEXT
            elif tag == "@k":
                strings.append((CONTINUE, content))
                continue
            elif tag == "@v":
                voice, text_after = content.split('.', maxsplit=1)
                text += text_after
                TYPE = TAG_CONTENT
                strings.append((VOICE, voice))
            elif tag == "@o":
                volume = content[:-1]
                strings.append((VOLUME, volume))
                continue
            elif tag == "@w":
                wait_time, text_after = content.split('.', maxsplit=1)
                text += text_after
                TYPE = TAG_CONTENT
                strings.append((WAIT, wait_time))
            elif tag == "@c":
                color, text_after = content.split('.', maxsplit=1)
                text += text_after
                TYPE = TAG_CONTENT
                strings.append((COLOR, color))
            elif tag == "@b":
                furi1 = content[:-1]
                continue
            elif tag == "@<":
                furi2 = content
                continue
            elif tag == "@>":
                strings.append((FURIGANA, (furi1, furi2)))
            elif tag == "@s":
                speed, text_after = content.split('.', maxsplit=1)
                text += text_after
                TYPE = TAG_CONTENT
                strings.append((SPEED, speed))
            elif tag == "@z":
                percent_size, text_after = content.split('.', maxsplit=1)
                text += text_after
                TYPE = TAG_CONTENT
                strings.append((TEXT_SIZE, percent_size))
            elif tag == "@{":
                strings.append((OB, content))
                continue
            elif tag == "@}":
                strings.append((EB, content))
                continue
            elif tag == "@|":
                strings.append((PIPE, content))
                continue
            elif tag == "@y":
                strings.append((AFTER_PIPE, content))
                continue
            elif tag == "@a":
                aspeed, text_after = content.split('.', maxsplit=1)
                text += text_after
                TYPE = TAG_CONTENT
                strings.append((ASPEED, aspeed))
            #elif tag == "@e":
            #elif tag == "@-": Can be ignored?
            elif tag == "@t":
                TYPE = TEXT_PARALLEL

            if not text and TYPE != TAG_CONTENT:
                text = content
            
            if text:
                strings.append((TYPE, text))

        else:
            if len(components) == 1:
                strings.append((TITLE, e))
            else:
                strings.append((NAME, e))

    return strings

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, nargs='+')
    args = parser.parse_args()

    def glob_or_complain(s):
        retval = glob.glob(s)
        if not retval:
            print("File not found: " + s)
        return retval

    files_dirs = map(glob_or_complain, args.file)
    files_dirs = list(itertools.chain(*files_dirs))

    filenames = [ ]

    for i in files_dirs:
        if path.isdir(i):
            for dirpath, dirnames, fns in walk(i):
                filenames.extend(path.join(dirpath, j) for j in fns if len(j) >= 4)
        else:
            filenames.append(i)

    for fn in filenames:
        filepath, extension = path.splitext(fn)
        fn_e = filepath + "_extracted" + extension

        if "_extracted" in fn:
            continue

        dialogues = [ ]

        with open(fn, "r", encoding="utf-8") as file:

            lines = file.readlines()

            for l in lines:
                l = l.replace("\\'", "\\в†•")

                strings = get_strings(l)

                for string in strings:
                    token = tokenize(string)
                    for t in token:
                        if t[0] in (TEXT, TAG_CONTENT, TITLE, TEXT_PARALLEL, PIPE, AFTER_PIPE, CONTINUE):
                            if t[1] != "" and t[1] != " ":
                                dialogues.append(t[1])
                        elif t[0] == OB or t[0] == EB:
                            if dialogues:
                                dialogues[-1] += t[1]
                        elif t[0] == FURIGANA:
                            dialogues.append(t[1][0])
                            dialogues.append(t[1][1])


        with open(fn_e, "w", encoding="utf-8") as extracted_file:

            for i in dialogues:
                i = i.replace("в†•", "'")
                i = i.replace("|y", "")
                if i.startswith(" "):
                	i = i[1:]
                extracted_file.write(i+"\n")

if __name__ == '__main__':
    main()
