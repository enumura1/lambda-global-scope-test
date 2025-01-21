# 概要
AWS Lambda関数において、別ファイルのグローバルスコープで初期化した変数のタイミングを確認するためのテストコードとそのメモです。
個人的なメモになります。

# 環境
- Python 3.13
- Lambda
  
# テストコード
```python
# fuga.py
print("fuga.pyのグローバルスコープを実行中")
client = "dummy client"

def hoge():
    print("hogeメソッドを実行中")
    return "テスト実行完了"

# lambda_function.py
from fuga import hoge

print("lambda_function.pyのグローバルスコープを実行中")

def lambda_handler(event, context):
    print("lambda_handler実行開始")
    result = hoge()
    return result
```

# 自分の環境で試した見た結果の実行順書

## 1. コールドスタート時、初期化
```
1. INIT_START
2. fuga.py のグローバルスコープ実行
   - client 変数の初期化
3. lambda_function.py のグローバルスコープ実行
```

## 2. ウォームスタート時
```
1. START RequestId: xxx
2. lambda_handler 実行開始
3. hoge 関数実行
```

# 自分の環境で試した結果
- `fuga.py` のグローバルスコープの初期化はコールドスタート時のみ実行される
- グローバルスコープはLambda関数のコンテナ初期化時に一度だけ実行され、以降の連続したリクエスト（コールドスタートでない環境）では再実行されない
- `fuga.py` のグローバルスコープは `lambda_function.py` より先に実行される

## 実行結果例（1回目）
```
2025-01-22T02:50:11.473+09:00 INIT_START Runtime Version: python:3.13.v13
2025-01-22T02:50:11.554+09:00 fuga.pyのグローバルスコープを実行中
2025-01-22T02:50:11.554+09:00 lambda_function.pyのグローバルスコープを実行中
2025-01-22T02:50:11.558+09:00 START RequestId: 18300d18-cc44-47bc-9cb0-93418838d9d1 Version: $LATEST
2025-01-22T02:50:11.558+09:00 lambda_handler実行開始
2025-01-22T02:50:11.558+09:00 hogeメソッドを実行中
```

![image](https://github.com/user-attachments/assets/d9dbd93f-369f-47c7-bbbf-36659b7423c0)

## 実行結果例（2回目）

![image](https://github.com/user-attachments/assets/ca5a3d26-9aa2-49c3-9211-5c5481885140)
