
SET USER_CSV_PATH=C:\prg\aplac\MeCab\MeCab_UserDictionary.csv
SET IPA_DIC_PATH="C:\Program Files (x86)\MeCab\dic\ipadic"
SET USER_DIC_NAME=user.dic
SET CHAR_ENCODING=utf8

mecab-dict-index.exe -d %IPA_DIC_PATH% -u %USER_DIC_NAME% -f %CHAR_ENCODING% -t %CHAR_ENCODING% %USER_CSV_PATH%



