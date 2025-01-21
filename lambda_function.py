from fuga import hoge

print("lambda_function.pyのグローバルスコープを実行中")

def lambda_handler(event, context):
    print("lambda_handler実行開始")
    result = hoge()
    return result
