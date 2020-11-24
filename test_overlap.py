
import re


if __name__ == '__main__':
    noverlap =  ['[E1]One[/E1] [E2]of the few items in our[/E2]  gym to cocktails , today  available in a plethora of styles and colours .',
                '[E1]One[/E1] of the [E2]few items in our  gym to cocktails[/E2] , today  available in a plethora of styles and colours .',
                '[E1]One[/E1] of the few items in our  gym to cocktails , today  available in a plethora of [E2]styles and colours[/E2] .',
                'One of the [E1]few items[/E1] [E2]in our  gym to cocktails[/E2] , today  available in a plethora of styles and colours .',
                'One of the [E1]few items[/E1] in our  gym to [E2]cocktails , today[/E2]  available in a plethora of styles and colours .',
                'One of the [E1]few items[/E1] in our  gym to cocktails , today  available in a plethora of [E2]styles and colours[/E2] .',
                '[E2]One[/E2] [E1]of the few items in our[/E1]  gym to cocktails , today  available in a plethora of styles and colours .',
                '[E2]One[/E2] of the [E1]few items in our  gym to cocktails[/E1] , today  available in a plethora of styles and colours .',
                '[E2]One[/E2] of the few items in our  gym to cocktails , today  available in a plethora of [E1]styles and colours[/E1] .',
                'One of the [E2]few items[/E2] [E1]in our  gym to cocktails[/E1] , today  available in a plethora of styles and colours .',
                'One of the [E2]few items[/E2] in our  gym to [E1]cocktails , today[/E1]  available in a plethora of styles and colours .',
                'One of the [E2]few items[/E2] in our  gym to cocktails , today  available in a plethora of [E1]styles and colours[/E1] .']

    woverlap = ['One of the [E1][E2]few items[/E2] in our  gym[/E1] to cocktails , today  available in a plethora of styles and colours .',
                'One of the [E1]few [E2]items in[/E2] our  gym[/E1] to cocktails , today  available in a plethora of styles and colours .',
                'One of the [E1]few items [E2]in our  gym[/E2][/E1] to cocktails , today  available in a plethora of styles and colours .',
                'One of the [E1][E2]few items in our  gym[/E1] to cocktails[/E2] , today  available in a plethora of styles and colours .',
                'One of the [E1]few [E2]items in our  gym[/E1] to cocktails[/E2] , today  available in a plethora of styles and colours .',
                'One of the [E1]few items [E2]in our  gym[/E1] to cocktails[/E2] , today  available in a plethora of styles and colours .',
                '[E1][E2]One of the[/E2] few items[/E1] in our  gym to cocktails , today  available in a plethora of styles and colours .',
                '[E1]One [E2]of the[/E2] few items[/E1] in our  gym to cocktails , today  available in a plethora of styles and colours .',
                '[E1][E2]One of the few items[/E1] in our  [/E2]gym to cocktails , today  available in a plethora of styles and colours .',
                '[E1]One [E2]of the few items[/E1] in our[/E2]  gym to cocktails , today  available in a plethora of styles and colours .',
                '[E1]One of the [E2]few items[/E2][/E1] in our  gym to cocktails , today  available in a plethora of styles and colours .',
                '[E1]One of the [E2]few items[/E1] in our  gym[/E2] to cocktails , today  available in a plethora of styles and colours .',
                'One of the [E2][E1]few items[/E1] in our  gym[/E2] to cocktails , today  available in a plethora of styles and colours .',
                'One of the [E2]few [E1]items in[/E1] our  gym[/E2] to cocktails , today  available in a plethora of styles and colours .',
                'One of the [E2]few items [E1]in our  gym[/E1][/E2] to cocktails , today  available in a plethora of styles and colours .',
                'One of the [E2][E1]few items in our  gym[/E2] to cocktails[/E1] , today  available in a plethora of styles and colours .',
                'One of the [E2]few [E1]items in our  gym[/E2] to cocktails[/E1] , today  available in a plethora of styles and colours .',
                'One of the [E2]few items [E1]in our  gym[/E2] to cocktails[/E1] , today  available in a plethora of styles and colours .',
                '[E2][E1]One of the[/E1] few items[/E2] in our  gym to cocktails , today  available in a plethora of styles and colours .',
                '[E2]One [E1]of the[/E1] few items[/E2] in our  gym to cocktails , today  available in a plethora of styles and colours .',
                '[E2][E1]One of the few items[/E2] in our  [/E1]gym to cocktails , today  available in a plethora of styles and colours .',
                '[E2]One [E1]of the few items[/E2] in our[/E1]  gym to cocktails , today  available in a plethora of styles and colours .',
                '[E2]One of the [E1]few items[/E1][/E2] in our  gym to cocktails , today  available in a plethora of styles and colours .',
                '[E2]One of the [E1]few items[/E2] in our  gym[/E1] to cocktails , today  available in a plethora of styles and colours .']

    overlap_pattern = re.compile('\[E1\]'
                                 '([\w \s/,\(\)\[\]]*)'
                                 '\[E2\]'
                                 '([\w \s/,\(\)\[\]]*)'
                                 '\[/E1\]'
                                 '|'
                                 '\[E2\]'
                                 '([\w \s/,\(\)\[\]]*)'
                                 '\[E1\]'
                                 '([\w \s/,\(\)\[\]]*)'
                                 '\[/E2\]'
                                      )
    print("noverlap:\n")
    for sent in noverlap:
        overlap = overlap_pattern.search(sent)
        if overlap is not None:
            print("False for : ", sent)
            print(overlap)
        else:
            print("true for: ", sent)

    print("\n overlap:\n")
    for sent in woverlap:
        overlap = overlap_pattern.search(sent)
        if overlap is None:
            print("False for : ", sent)

        else:
            print("true for: ", sent)
            print(overlap)
