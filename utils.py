"""便利な機能の実装"""
from datetime import datetime
import os, datetime
import matplotlib.pyplot as plt
import torch
import pickle
import json
import os, datetime
import numpy as np
from sklearn.preprocessing import StandardScaler



# データ値のスケールを変更する関数
def scale_change(scaler_name, data, scaler=None):
    if scaler_name == "scaler":
        input, label = data[:, 1:], data[:, 0]
        if scaler==None:
            scaler = StandardScaler()
            # 訓練データをもとに平均，標準偏差を算出
            scaler.fit(input)
        # 訓練データの平均，分散をもとに訓練データを標準化
        input = scaler.transform(input)
        label = label[:, np.newaxis]
        data = np.hstack([input, label])
        data = torch.from_numpy(data.astype(np.float32)).clone()

    return data, scaler


def print_info(epoch, num_epochs, mode, loss, acc=None):
    if acc is None:
        print ('{:>5} Epoch [{:2d}/{:2d}] loss: {:.3f}'
                .format(mode.upper(), epoch+1, num_epochs, loss))
    else:
        print ('{:>5} Epoch [{:2d}/{:2d}] loss: {:.3f} acc: {:.3f}%'
                .format(mode.upper(), epoch+1, num_epochs, loss, acc))


# resultfolderを作成する関数
def make_result_folder():
    # 結果の保存場所を指定
    result_dir =  "./result-folder"
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)
    result_dir += "/Neural_Network"
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)

    t_now = datetime.datetime.now()

    result_dir+= "/{}".format(t_now.strftime('%Y%m%d_%H%M%S'))
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)
    
    return result_dir


# モデルのパラメータを保存する関数
def save_model(result_dir, model, scaler):
  torch.save(model, result_dir+"/model.pth")
  with open(result_dir+"/scaler.bin", 'wb') as f:
      pickle.dump(scaler, f)



# パラメータを保存する関数
def save_params(result_dir, config):
    with open(result_dir+"/params.json", mode="w") as f:
        json.dump(config.__dict__, f, indent=4)


# lossや訓練accをグラフに描画する関数
def save_row_data(result_dir, epoch, history):
    
    # 結果の出力と描画
    plt.figure()
    plt.plot(range(1, epoch+1), history['train_loss'], label='train_loss')
    plt.plot(range(1, epoch+1), history['test_loss'], label='test_loss')
    plt.title('train test loss')
    plt.xlabel('epoch')
    plt.legend()
    plt.savefig(result_dir+'/loss.png')

    plt.figure()
    plt.plot(range(1, epoch+1), history['train_acc'], label='train_acc')
    plt.plot(range(1, epoch+1), history['test_acc'], label='test_acc')
    plt.title('train test accuracy')
    plt.xlabel('epoch')
    plt.legend()
    plt.savefig(result_dir+'/acc.png')

# accuracyを保存する関数
def save_text_data(result_dir, best_test_acc, best_test_loss, best_idx, best_epoch, best_lr):
    # 設定と結果をテキストファイルに保存

    text_file = result_dir + "/model.txt"
    with open(text_file, 'w', newline='') as f:
        f.write('最良のモデルの設定\n')
        f.write('best_val_acc : {}\n'.format(best_test_acc))
        f.write('best_test_loss : {}\n'.format(best_test_loss))
        f.write('best_fold_idx : {}\n'.format(best_idx))
        f.write('best_epoch : {}\n'.format(best_epoch))
        f.write('best_lr : {}\n'.format(best_lr))

def save_test_data(result_dir, test_loss, test_acc):
    # 設定と結果をテキストファイルに保存
    text_file = result_dir + "/test_result.txt"
    with open(text_file, 'w', newline='') as f:
        f.write('test_loss : {}\n'.format(test_loss))
        f.write('test_acc : {}\n'.format(test_acc))
        


if __name__ == '__main__':
    #create_logdir("ddh", 15, "scaler", "random")
    #train_set, test_set=load_data("ddh", "../data_ddh/data_1000_65541.csv", 0.2, 4)
    print()
