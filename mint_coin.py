import requests 
from bitcoin import *
import time

def compose_fairmint(address, asset, quantity, exact_fee):
    url = f"http://127.0.0.1:4000/v2/addresses/{address}/compose/fairmint"
    params = {
        "asset": asset,
        "quantity": quantity,
        "allow_unconfirmed_inputs": True,
        "exact_fee": exact_fee
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()

        # 检查是否有错误信息
        if "error" in data:
            print(f"等待重试，勿关闭: {data['error']}") 
            return None 
        else:
            rawtransaction = data["result"]["rawtransaction"]
            return rawtransaction

    except requests.exceptions.RequestException as e: 
        print(f"等待重试，勿关闭: {e}") 
        return None
    except ValueError as ve:
        print(f"等待重试，勿关闭: {ve}") 
        return None

 
 
# 生成地址 
def genaddr(private_key) : 
    public_key = privtopub(private_key)
    address = pubtoaddr(public_key)
    return address

# 签名 rawtransaction
def sign_transaction(rawtransaction, private_key):
    signed_tx = sign(rawtransaction, 0, private_key)
    return signed_tx

# 广播
def broadcast_transaction(signed_transaction, rpc_user, rpc_pass):
    url = "http://127.0.0.1:8332"  # 替换为你的比特币节点地址
    headers = {
        'Content-Type': 'application/json',
    }
    
    payload = {
        "jsonrpc": "1.0",
        "id": "curltext",
        "method": "sendrawtransaction",
        "params": [signed_transaction]
    }

    try:
        response = requests.post(url, json=payload, headers=headers, auth=(rpc_user, rpc_pass))  # 替换为你的用户名和密码
        response.raise_for_status()  # 检查请求是否成功
        result = response.json()
        
        if 'error' in result and result['error'] is not None:
            return f"广播错误: {result['error']}"
        return f"广播成功: {result['result']}"

    except requests.exceptions.RequestException as e:
        return f"请求异常: {e}"
    except ValueError as ve:
        return f"解析 JSON 失败: {ve}"
    
    

if __name__ == "__main__":
    #################################################   修改下面值   ############################################## 
    private_key = "私钥" # 你的WIF格式私钥
     
    asset = "XCPTWO"    # 打的币名
    quantity = 100      # 单次mint数量 
    gas_fee = 5         # 矿工费用. 整数
    mintNum = 2        # 打多少张
    
    # 节点用户名和密码, 通过教程安装的不需要变，默认都是rpc
    rpc_user = "rpc"
    rpc_pass = "rpc" 
    #################################################      end      ##############################################
    
    exact_fee = 223 * gas_fee #粗略计算矿工费用
    address = genaddr(private_key)
    print(f"你的地址： {address}")
    
    
    count = 0 
    while True:
        print(f"第 {count + 1} 张")
        count += 1
        if count >= mintNum:
            break   
        
        while True :
            rawtransaction = compose_fairmint(address, asset, quantity, exact_fee)
            if rawtransaction is not None :
                break
            else :
                time.sleep(2)
            
        if rawtransaction is not None: 
            signed_transaction = sign_transaction(rawtransaction, private_key)
            res = broadcast_transaction(signed_transaction, rpc_user, rpc_pass)
            print(res)
        else:
            print("获取的 rawtransaction 无效或为空")
        
        
 
