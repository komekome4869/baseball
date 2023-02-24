import numpy as np
import csv, os, math, random, datetime
import sys
import torch
import utils
import argparse
from torch import nn
from copy import deepcopy
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader
import pandas as pd
from model.NN import NN

def parse_config():
    parser = argparse.ArgumentParser()
    parser.add_argument('--gpu', type=list, default=['0'], help="使用するGPU")                  #GPU                
    parser.add_argument("--batch_size", type=int, default=200)          
    parser.add_argument('--epoch',type=int, default=50, help="エポック数")
    parser.add_argument("--lr", type=float, default=0.001 , help="学習率")
    parser.add_argument('--clip_value',type=float, default=1, help="勾配クリッピング")
    parser.add_argument("--optimizer_name", type=str, default="Adam")
    parser.add_argument('--n_nodes', type=int, default=500, help="NNのノード数")
    parser.add_argument('--n_layers', type=int, default=3, help="NNの層数")
    parser.add_argument('--n_fold', type=int, default=5, help="交差検証の分割数")
    parser.add_argument('--dropout', type=float, default=0.5, help="ドロップアウトの比率")
    parser.add_argument("--cross_valid", action="store_true", help="交差検証をするかしないか")
    parser.add_argument('--scaler_name',type=str, default="scaler", help="スケールの変更")

    return parser.parse_args()



def valid_train(input_data, config, result_main_folder, device):#,divisor):

    # 変数の定義
    num_feature = input_data.shape[1] - 1
    best_test_loss = 1000.0
    lr = config.lr
    
    # 結果の保存場所を指定
    result_valid_folder = result_main_folder+"/valid"
    if not os.path.exists(result_valid_folder):
            os.mkdir(result_valid_folder)
        

    
    # result-folder
    print("\n##  valid {}  ##".format(1))
    history = {
        'train_loss': [],
        'train_acc': [],
        'test_loss': [],
        'test_acc': [],
    }
    epoch_header = ['epoch', 'train_loss', 'train_acc', 'test_loss', 'test_acc']
    

    # 交差検証ごとの結果の保存場所を指定
    result_folder = result_valid_folder+"/result-valid{}".format(1)#, t_now.strftime('%Y%m%d_%H%M%S'))
    train_file_name = "/result.csv"
    if not os.path.exists(result_folder):
        os.mkdir(result_folder)

    # Data
    # train_data, valid_data
    train_data, valid_data = train_test_split(input_data, test_size=0.2, random_state=0)
    train_data, valid_data = np.array(train_data), np.array(valid_data)
    # 標準化
    train_data, scaler_obj = utils.scale_change(config.scaler_name, train_data)
    valid_data, _ = utils.scale_change(config.scaler_name, valid_data, scaler_obj)
    # DataLoader
    train_loader = DataLoader(train_data, batch_size=config.batch_size, shuffle=True)
    test_loader = DataLoader(valid_data, batch_size=config.batch_size, shuffle=True)
    num_train, num_test = len(train_data), len(valid_data)
    
    
    ## modelの定義
    model = NN(num_input=num_feature, n_nodes=config.n_nodes, n_layers=config.n_layers).to(device)
    if torch.cuda.is_available():
        # list内の文字を数値に変換
        gpu = list(map(int, config.gpu))
        # 指定したgpuを使う
        model = torch.nn.DataParallel(model,device_ids=gpu)
    loss_func = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)



    with open(result_folder+train_file_name, 'w', newline='') as csv_epoch:
        writer_epoch = csv.DictWriter(csv_epoch, fieldnames=epoch_header)
        writer_epoch.writeheader()

        for e in range(config.epoch):
            """ Training Part """
            loss = None
            train_loss, correct, train_acc = 0, 0, 0
            model.train(True)
            for i, data in enumerate(train_loader):
                input = data[:, :num_feature].to(device)
                target = data[:, num_feature].to(torch.long).to(device)
                optimizer.zero_grad()
                pred = model(input)
                loss = loss_func(pred, target)
                train_loss += loss.item() * data.size()[0] / num_train
                loss.backward()
                nn.utils.clip_grad_norm_(model.parameters(), config.clip_value)
                optimizer.step()
                pred = pred.argmax(dim=1, keepdim=True)
                correct += pred.eq(target.view_as(pred)).sum().item()

                if i % 100 == 0:
                    print('Training log: {} epoch ({} / {} train. data). Loss: {}, Acc: {}'.format(
                    e+1, (i+1)*config.batch_size, num_train, loss.item(), correct / ((i+1)*config.batch_size) ) )

            train_acc = correct / num_train

            """ Test Part """
            model.train(False)
            test_loss = 0
            correct, test_acc = 0, 0
            with torch.no_grad():
                for data in test_loader:
                    input = data[:, :num_feature].to(device)
                    target = data[:, num_feature].to(torch.long).to(device)
                    pred = model(input)
                    test_loss += loss_func(pred, target).item() * data.size()[0] / num_test
                    pred = pred.argmax(dim=1, keepdim=True)
                    correct += pred.eq(target.view_as(pred)).sum().item()

            test_acc = correct / num_test
            print('Valid loss (avg): {}, Acc: {}'.format(test_loss, test_acc))

            # 最良のモデルを保存
            if test_loss < best_test_loss:
                best_test_loss = test_loss
                best_test_acc = test_acc
                weights_best = deepcopy(model.state_dict())
                best_epoch = e
                best_lr = lr
                best_scaler = scaler_obj
            
            # エポックごとに結果を保存
            history['train_loss'].append(train_loss)
            history['train_acc'].append(train_acc)
            history['test_loss'].append(test_loss)
            history['test_acc'].append(test_acc)
            epoch_logger = {'epoch': e + 1,
                    'train_loss': train_loss,
                    'train_acc': train_acc,
                    'test_loss': test_loss,
                    'test_acc': test_acc,
                    }
            writer_epoch.writerows([epoch_logger])
            del epoch_logger

    
        #結果
        
        # Lossやaccをグラフにする
        utils.save_row_data(result_folder, config.epoch, history)

        # validationごとに学習率を変える
        lr = 10*lr

    # テキストデータに保存
    utils.save_text_data(result_main_folder, best_test_acc, best_test_loss, 1, best_epoch, best_lr)
    
    # 最良のモデルをファイルに保存
    utils.save_model(result_main_folder, weights_best, best_scaler)


if __name__ == '__main__':

    config = parse_config()
    input_data = pd.read_csv('data/input_data/data.csv')
    input_data = torch.tensor(input_data.values.astype(np.float32))
    input_data = input_data[:,1:]
    result_main_folder = utils.make_result_folder()
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    valid_train(input_data, config, result_main_folder, device)