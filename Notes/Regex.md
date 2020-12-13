^[ \t]+print\*

<br>
<br>
<br>
| Regex Find | Regex Replace | function |  | use case | reference links |
| ---------- | ------------- | -------- | --- | -------- | --------------- |
| (^[ \t]+)print\* | $1# ZAQ print | matches indented print statements |  | FIND ALL COMMENTS<br><br>when final code is not, but almost, and want to comment out all the print statements (before bringing them back) | [https://stackoverflow.com/questions/19603306/is-there-a-smarter-way-to-keep-the-indentation-when-replacing-characters-with-a](https://stackoverflow.com/questions/19603306/is-there-a-smarter-way-to-keep-the-indentation-when-replacing-characters-with-a)<br>[https://stackoverflow.com/questions/34618383/vscode-regex-find-replace-submatch-math](https://stackoverflow.com/questions/34618383/vscode-regex-find-replace-submatch-math) |
| (^[ \t]+)# ZAQ print | $1print |  |  |  |  |
| \(\(?<=\#\)\.\*\|\#\|^$\n\|^\s\*$\n\|\[ \t\]\+$\|\(?<=print\\\(\)\.\*\|print\\\(\) |  | remove all comments |  | clean code | or = \|<br>(?<=#).\*           = everything after hashtag<br>#                      = hashtag<br>^$\n =              = lines completely empty<br>^\s\*$\n             = lines with only spaces<br>[ \t]+$               = trailing spaces<br>(?<=print\\().\*    = removes everything after print(<br>\|print\\\(              = removes print\( |
| ^zx.\*\n.\*\n.\*\n.\*\n.\*\n.\* |  |  |  |  | last 7 lines (function that creates pretty backup copy). |
| ^.\*print.\*$\n |  |  |  |  | string contains |
| \(\(?<=\#\)\.\*\|\#\|^$\n\|^\s\*$\n\|\[ \t\]\+$\|\(?<=print\\\(\)\.\*\|print\\\(\)^\(?\!\.\*QAZ\) |  |  |  |  |  |
| ^(?!.\*QAZ) |  |  |  |  |  |
| **find**<br>^(.\*) df\_html\_tall<br>**replace**<br>\# df\_html\_tall |  | comment out all lines containing word |  | need to test something | #\1 logging |

autoflake --in-place --remove-unused-variables "Scripts\FMP\_Profile.py"

^\(?=\.\*\(\(?<=\#\)\.\*\|\#\|^$\n\|^\s\*$\n\|\[ \t\]\+$\|\(?<=print\\\(\)\.\*\|print\\\(\)\)\(?\!\.\*QAZ\)\.\*

\(?<=print\\\(\)\.\*\(\|print\\\( \)

\(\(?<=\#\)\.\*\|\#\|^$\n\|^\s\*$\n\|\[ \t\]\+$\|\(?<=print\\\(\)\.\*\|print\\\(\)

^(?!.\*details\\.cfm).\*print.\*$
^((?!QAZ).)\*$((?<=print\\().\*)

^(?!.\*^((?!QAZ).)\*$).\*print.\*$

\(\(?<=\#\)\.\*\|\#\|^$\n\|^\s\*$\n\|\[ \t\]\+$\|\(?<=print\\\(\)\.\*\|print\\\(\)

^\(?\!\.\*\(cat\|girl\)\)\.\*\(dog\|house\)\.\*

<br>
```
^(?=.*((?<=#).*|#|^$\n|^\s*$\n|[ \t]+$|(?<=print\().*|print\())(?=.*QAZ).*
.*strA.*$
```

^((?!QAZ).)\*$

^\s\*$\n\|\[ \t\]\+$

\(\(\(?<=\#\)\.\*\|\#\|^$\n\|^\s\*$\n\|\[ \t\]\+$\n\|\(?<=print\\\(\)\.\*\|print\\\(\)\(^\(\(?\!QAZ\)\.\)\*$\)\)\| \(\(^\(\(?\!QAZ\)\.\)\*$\)\|\(\(?<=\#\)\.\*\|\#\|^$\n\|^\s\*$\n\|\[ \t\]\+$\n\|\(?<=print\\\(\)\.\*\|print\\\(\)\)
\(\(?<=\#\)\.\*\|\#\|^$\n\|^\s\*$\n\|\[ \t\]\+$\|\(?<=print\\\(\)\.\*\|print\\\(\)