import ayax_cgi as cgi # 入力値を取得するためのモジュール

# ブラウザへヘッダー情報を送信
print("Content-Type: text/html")
print() #　ヘッダーの終了を知らせる改行を送信

# 入力値を格納するための変数
data01 = data02 = data03 = data04 = data05 = data06 = ""

'''
ブラウザから送信された入力値は、グローバル変数POSTに辞書形式{name属性名:入力値}で設定されている。
各フィールドの入力値があれば変数へ代入
※その他命令は、「!Tutorial/Z.ライブラリ/ayax_cgi.html」を参照
'''
if 'field01' in POST:data01 = POST['field01']
if 'field02' in POST:data02 = POST['field02']
if 'field03' in POST:data03 = POST['field03']
if 'field04' in POST:data04 = POST['field04']
if 'field05' in POST:data05 = POST['field05']
if 'field06' in POST:data06 = POST['field06']

# ブラウザへ送信するためのHTMLを変数へ保存
string = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="./css/style.css" type="text/css">
    <title>Styled Form</title>
</head>
<body>
    <div>
        <h3>program01.pyで入力値を取得</h3>
        <div class="input">
            field01は、{data01}
        </div>
        <div class="input">
            field02は、{data02}
        </div>
        <div class="input">
            field03は、{data03}
        </div>
        <div class="input">
            field04は、{data04}
        </div>
        <div class="input">
            field05は、{data05}
        </div>
        <div class="input">
            field06は、{data06}
        </div>
    </div>
</body>
</html>
"""
 # format命令を使い、HTMLへ入力値を挿入する
string = string.format(data01=data01,data02=data02,data03=data03,data04=data04,data05=data05,data06=data06)

# ブラウザへHTMLを送信
print(string)




