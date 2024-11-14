#MODE=SERVER(ayax)
'''
ブラックジャックゲーム

ルール補足
・Aは1又は11とできます。
・倍賭け(d)：掛け金を倍にし、次にもう一枚だけ引きます。
・降参(b)：掛け金が半分戻ってきます。
・最初の2枚で21になったら「ナチュラルブラックジャック」です

作成者:ayax
コメント:プログラムを改造してみてください。より理解が深まると思います。再帰処理(calc_loop)は難しいところですが、読み解いてみてください。

'''
import random
import copy

#カードデータ
ACE = 777
data1 = ["♠","♡","♣","♢"]
data2 = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
data3 = [ACE,2,3,4,5,6,7,8,9,10,10,10,10]
#ステータス情報
FIRST = 1 # ゲーム開始、プレイヤー最初の手番
PLAYER = 2 # プレイヤー手番
DEALER = 3 # ディーラー手番
BURST_PLAYER = 4 # プレイヤーが21を超える
BURST_DEALER = 5 # ディーラーが21を超える
SURRENDER_PLAYER = 6 #プレイヤーが降りる
GAMEEND = 7
END = 8

SYOJIKIN = 100 # 所持金定額
BLACK_JACK = 21
#Player選択情報
HIT = 1 # もう一枚
STAND = 2 # 勝負!
DOUBLE = 3 # 倍掛け
SURRENDER = 4 # 降りる

money = SYOJIKIN #所持金 
kakekin = 0 #掛け金　
status = FIRST
DEALER_HIT = 16 #ディーラー最低ライン

#カード作成　♠A,♠2,♠3・・・♢J,♢Q,♢Kを作成
card_origin = [j+i  for j in data1 for i in data2] #!Tutorial/07.繰り返し/06.生成が参考になります
card = [] # プレイ用カード
#点数表作成(辞書 例 ♡K:10 ※ハートのキングは10点)
ten={}
num = 0
for key in card_origin:
    ten[key] = data3[num]
    num += 1
    if num >= len(data3): num = 0 #if文内の処理が1行なら短縮した形で記述可能

dealer = [] #ディーラーのカード
dealer_ten = [] #ディーラーの点
player = [] #プレイヤーのカード
player_ten = [] #プレイヤーの点

def shuffle(): #カードシャフル
    global card
    card =  copy.deepcopy(card_origin) # オリジナルのカードをデータごとコピー
    random.shuffle(card) #シャッフル

#表示
def disp(): 
    print("🔹🔹🔹🔹🔹🔹🔹🔹🔹")
    #残金
    print("所持金:"+str(money)+"💰"+" 収支:"+str((money-SYOJIKIN)))

    if status != GAMEEND:
        print("掛け金:"+str(kakekin)+"💸")
        print("")
        tmp = " ".join(dealer)
        if status != DEALER: tmp = tmp[0:3] +  "🀫"
        tmp2 = ""
        if status == DEALER:
            tmp2 = " 合計:" + ",".join([str(i) for i in dealer_ten])
        print("ディーラー:"+tmp+tmp2)
        #print("")
        print("プレイヤー:"+" ".join(player)+" 合計:" + \
                           ",".join([str(i) for i in player_ten]))
        print("")
 
#点計算
def calc(target):
    target_ten = [[0,0] for i in range(len(target))] # 点用の配列作成
    for idx,_card in enumerate(target): # Aを考慮した組合せを作成
        if  ten[_card] == ACE: #Aの場合1,11を選べる
            target_ten[idx][0] = 1
            target_ten[idx][1] = 11
        else:
            target_ten[idx][0] = ten[_card]
            del target_ten[idx][1]
                        
    add_ten = set() # 集合(set)の初期化(集合はダブり(同じ値)を許さないので利用)
    add_ten = calc_loop(target_ten,0,0,add_ten) # 全組合せを加算   
    add_ten = list(add_ten) # 集合からリストへ変換(リストの方が扱いやすいから)
    add_ten.sort() # 小さい順に並び替え
    return add_ten

'''
target:カードの点
idx:何枚目か
num:点合計
add_ten:点数表
'''
def calc_loop(target,idx,num,add_ten):
    for i in target[idx]: # iには点が入る
        if len(target)-1 > idx: # 次のカードがあるか
            add_ten = calc_loop(target,idx+1,num+i,add_ten) # 次のカードを加算するため再帰処理
        else:
            add_ten.add(num+i)
           
    return add_ten

#プレイヤーの入力
def player_action():
    global status,player,player_ten
    while(True):
        if status == FIRST:
            x = input("もう1枚(h),勝負!(s),倍賭け(d),降参(b):")
            if x != 'h' and x != 's' and x != 'd' and x != 'b':
                print("入力が間違っています")
                continue
            if x == 'h':
                player,player_ten = draw(player,player_ten)
                return HIT
            if x == 's':
                return STAND
            if x == 'd':
                double()
                player,player_ten = draw(player,player_ten)
                return DOUBLE
            if x == 'b':
                surrender()
                return SURRENDER                    
            break
        elif status == PLAYER:
            x = input("もう1枚(h),勝負!(s):")
            if x != 'h' and x != 's':
                print("入力が間違っています")
                continue              
            if x == 'h':
                player,player_ten = draw(player,player_ten)
                return HIT
            if x == 's':
                return STAND
            break
        elif status == GAMEEND:
            print("")
            x = input("play?(y):")
            if x != 'y':
                status = END
            break

#降りる
def surrender():
    global money,kakekin,status
    status = SURRENDER_PLAYER
    money += int(kakekin/2)
    kakekin = 0
    
#倍掛け
def double():
    global money,kakekin
    kakekin_tmp = kakekin
    if kakekin_tmp > money:
        kakekin_tmp = money        
    kakekin  += kakekin_tmp
    money -= kakekin_tmp
    
#掛け金入力    
def latch():
    global money,kakekin
    #残金
    while(True):
        print("所持金:"+str(money)+"💰")
        x = input("掛け金:")
        kakekin = int(x)
        if(money < kakekin):
            print("所持金が足りません")
            continue
        money -= kakekin
        break
        
#21をこえているか        
def isBurst(target):
    if target[0] > BLACK_JACK:
        disp()
        print("21を超えました")
        return True
    return False

#ディラーアクション
def dealer_action():
    global dealer,dealer_ten
    x = input("ENTERを押してください:")
    while(True):
        #17～21を抽出
        tmp = [i for i in dealer_ten if i > DEALER_HIT and i <= BLACK_JACK] 
        if dealer_ten[0] <= DEALER_HIT and len(tmp) == 0: # 最低点に達せず17~21が1枚もない
            dealer,dealer_ten = draw(dealer,dealer_ten) #もう一枚ひく
            disp()
            x = input("ENTERを押してください:")
            continue
        break
    return

#カードを配る
def draw(target,target_ten):
    if len(card) == 0 : shuffle() # カードが無くなったら
    target.append(card.pop())
    target_ten = calc(target) # 点計算
    return target,target_ten

#ナチュラルブラックジャック判定
def black_jack(ten,target):
    if ten == BLACK_JACK and len(target) == 2:
        return True
    else:
        return False
    
#勝敗判定    
def judge():
    global money
 
    print("🔹🔹🔹🔹🔹🔹🔹🔹🔹")
    if status == BURST_PLAYER or status == SURRENDER_PLAYER:
        print("😰😰😰 敗北です 😰😰😰")
        return
    
    #合計点から21以上を省く
    p = [i for i in player_ten if i <= 21]
    d = [i for i in dealer_ten if i <= 21]
    #最高点を求める(全て21を超えている場合は0)
    p_ten = p.pop() if len(p) != 0 else 0
    d_ten = d.pop() if len(d) != 0 else 0
       
    if black_jack(p_ten,player): #Playerがナチュラルブラックジャック
        if black_jack(d_ten,dealer):
            print("引き分けです") #ナチュラルブラックジャック同士
            money += kakekin
            return
        else:
            black_jack_disp()
            return  
        
    if  p_ten > d_ten or status == BURST_DEALER:
        print("😀😀😀 あなたの勝利です 😀😀😀")
        money += kakekin * 2
        return
    elif p_ten == d_ten:
        print("引き分けです")
        money += kakekin
    else:
        print("😰😰😰 敗北です 😰😰😰")
        
#ナチュラルブラックジャック表示
def black_jack_disp():
    global money    
    print("✨✨✨✨✨✨✨✨✨✨✨✨✨✨")
    print("✨ ナチュラルブラックジャックです ✨")
    print("✨✨✨✨✨✨✨✨✨✨✨✨✨✨")
    print("🎁 掛け金の1.5倍! 🎁")
    money += int(kakekin * 2.5)

shuffle() # カードシャルフ

#メイン処理    
while(status != END):
    status = FIRST
    dealer = []
    player = []
    #カードを配る
    dealer,dealer_ten = draw(dealer,dealer_ten)
    dealer,dealer_ten = draw(dealer,dealer_ten)
    player,player_ten = draw(player,player_ten)
    player,player_ten = draw(player,player_ten)
    latch() #掛け金入力
    disp()
    rc = player_action() # プレイヤー入力
    
    if isBurst(player_ten): #21を超えているか
        status = BURST_PLAYER 
    
    while(rc == HIT and status != BURST_PLAYER): # プレイヤー　もう一枚
        status = PLAYER
        disp()
        rc = player_action()
        if isBurst(player_ten): # 21をこえているか
            status = BURST_PLAYER

    #ディーラーアクション        
    if (rc == STAND or rc == DOUBLE) and status != BURST_PLAYER:
        status = DEALER
        disp()
        dealer_action()
        if isBurst(dealer_ten): # 21をこえているか
            status = BURST_DEALER
 
    judge() #勝敗判定       
    kakekin = 0 
    status = GAMEEND
    disp()
    if money <= 0:
        print("☔☔☔☔☔☔☔☔☔☔☔☔")
        print("☔☔☔ 破産しました ☔☔☔")
        print("☔☔☔☔☔☔☔☔☔☔☔☔")
        break
    player_action()

print("END")


