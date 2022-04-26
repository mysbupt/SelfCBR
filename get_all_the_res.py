import os
import glob
import json
import argparse


def get_cmd():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--sort_by", default="ndcg", type=str, help="by which key to sort the results, options: model, recall, ndcg")
    parser.add_argument("-d", "--dataset", default="all", type=str, help="print which dataset's results, options: all, iFashion, Youshu, NetEase")
    parser.add_argument("-m", "--models", default="", type=str, help="print which models' results: default is empty, you can put the model names split by comma")
    parser.add_argument("-k", "--topk", default=10, type=int, help="topk settings to present for each model")
    parser.add_argument("-p", "--path", default="./log", type=str, help="the log path")
    parser.add_argument("-f", "--filter", default="none", type=str, help="the key string used to filter out the modelname, default: none")
    args = parser.parse_args()
    return args


def main(print_type="csv"):
    paras = get_cmd()
    sort_by = paras.sort_by
    which_data = paras.dataset
    res_topk = paras.topk
    keyword = paras.filter
    path = paras.path
    model_list = []
    if paras.models != "":
        model_list = paras.models.split(",")

    assert sort_by in ["model", "recall", "ndcg"], "-s only support: model, recall, ndcg"
    assert which_data in ["all", "iFashion", "Youshu", "NetEase"], "-d only support: all, iFashion, Youshu, NetEase"

    res = {}
    for each_file in glob.glob(os.path.join(path, "*/*/*")):
        x = each_file.split("/")
        dataset = x[2]
        model = x[3]
        setting = x[4]

        if len(model_list) != 0 and model not in model_list:
            continue

        if keyword != "none" and keyword not in setting:
            continue

        if dataset not in res:
            res[dataset] = {}

        if model not in res[dataset]:
            res[dataset][model] = {}

        if setting not in res[dataset][model]:
            res[dataset][model][setting] = {}

        topk_resstr = {}
        for line in open(each_file):
            for topk in ["20", "40", "60"]:
                if topk not in topk_resstr:
                    topk_resstr[topk] = []
                if "Best in epoch" in line and "TOP %s: REC_T" %(topk) in line:
                    topk_resstr[topk].append(line)

        for topk, res_str in topk_resstr.items():
            if len(res_str) <= 0:
                continue
            y = res_str[-1].strip().split(",")
            epoch = int(y[1].split(" ")[-1])
            recall = float(y[2].split("=")[-1])
            ndcg = float(y[3].split("=")[-1])

            res[dataset][model][setting][topk] = {"recall": recall, "ndcg": ndcg}

    topk_sortby = "20"
    if print_type == "csv":
        for dataset, x in res.items():
            if which_data == "all" or which_data in dataset:
                print("%s:" %(dataset))
                for model, z in sorted(x.items(), key=lambda i: i[0]):
                    print("\t%s:" %(model))
                    sorted_res = None
                    if sort_by == "model":
                        sorted_res = sorted(z.items(), key=lambda i: i[0])
                    else:
                        sorted_res = sorted(z.items(), key=lambda i: i[1][topk_sortby][sort_by], reverse=True)

                    print("\t\trank:\tRecall@20\tNDCG@20 \tRecall@40\tNDCG@40 \tModelName")
                    for rank, (setting, m) in enumerate(sorted_res[:res_topk]):
                        print("\t\t%d:\t%f\t%f\t%f\t%f\t%s" %(rank, m["20"]["recall"], m["20"]["ndcg"], m["40"]["recall"], m["40"]["ndcg"], setting))
    else:
        print(json.dumps(res, indent=4))


if __name__ == "__main__":
    main()
