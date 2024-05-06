# markup-ssg
quick and objectively bad html generator.  
usecase: i need stuff that markup cant do + pandoc is slow  

# notable differences
the following things were added:
- `[fg color]` where color can be any value CSS allows
- `[fg unset]` resets foreground color
- the same stuff with bg.
- new table syntax:
  ```
  [-header1, header2, header3-]
   data1  , data2  , data3
  ```
  the exact syntax is as follows:
  use `[- -]` to indicate the start of a table
  put comma-separated (backslash to escape) headers in there
  (or dont, i cant tell you what to do, in that case it just wont have headers (or break horribly))
  put comma separated data below. pad it with spaces if you want, any
  spaces preceding/following a comma will be discarded.
  a empty line indicates end of the thing.
  valid example 2:
  ```
  [-hi,there-]
  how,are,you
  ```
  has more data than headers, so a empty header will be added.
- super/subscript:
  _this_ is subscript (not italics, only `*` is allowed for that)
  ^this^ is superscript
- syntax highlighting
  use three backticks for a code block, put the language right after these (no space).
  by default plaintext, use `auto` as the language in order to auto-detect language
- mathjax
  ```
  [math
    mathjax stuff in here
  ]
  ```
  will render `mathjax stuff in here` using mathjax
  this will be in a div, you cant inline it yet
- spamton voicelines
  use `[[thing]]` to create a fragment at the line containing thing (will still display thing in the output).
  (use like domain.invalid/page.html#thing to get to that line)
  `<h1>` to `<h6>` will do that for you.
- `[embed url alt]` depends on the url. might be a `file://` thing.
  will try to embed videos/audio/text files, offers download links (named after the alt text) otherwise
- you now have to annotate the start and end of lists
  this is needed because i am going insane writing this thing and also the original syntax needs too much escaping
  ```
  [ul
    - entry
    - other entry
      with extra text
    - and one with
      [ol
        # a ordered sublist
        # of 2 entries
      ]
  ]
  ```
  
the following things were removed:
- using `*` for unordered lists, use `-` instead
- using anything but `*` for emphasis (_thing_ has been remapped to subscript)
- using double spaces for line breaks. every newline that isnt
  - a: inside a code block (will not be modified)  or
  - b: escaped by the line ending with a backslash (will be discarded)
  will simply be replaced with `<br>`.
- the previous table syntax. looked neat, but holy shit does it suck to create and parse
more coming soon i like breaking compatibility :33

# other stuff you might want to know
this implementation "supports" HTML tags by not caring about them
and letting them get into the output. its a feature now!

this implementation uses javascript for syntax highlighting and mathjax.
it defaults to using jsdelivr for that, but you can use `--embed-js` if you dont like that
(its a bad idea, your html file will grow. but it should allow the js stuff to work offline at least)

it doesnt show errors and will instead output broken and terrible HTML. good luck.
making errors is undefined behavior (the program is allowed to meow at you) and thus your fault :33

meow
