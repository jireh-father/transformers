import argparse
import random
import jsonlines
import os
import csv


def main(args):
    for arg in vars(args):
        print(arg, getattr(args, arg))

    os.makedirs(args.output_dir, exist_ok=True)

    if args.replace_special_chars:
        summaries = [s.replace('\n', '').replace('<unk>', '').replace('</s>', '') for s in
                     open(args.generated_file).readlines()]
    else:
        summaries = [s.replace('\n', '') for s in open(args.generated_file).readlines()]
    ids = []
    with jsonlines.open(args.test_file) as f:
        for i, line in enumerate(f.iter()):
            ids.append(line['id'])

    rows = zip(ids, summaries)
    with open(os.path.join(args.output_dir, "submission.csv"), "w+") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "summary"])
        for row in rows:
            writer.writerow(row)

    print("done")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--generated_file', type=str,
                        default='/media/irelin/data_disk/dataset/dacon_summury/abstractive/abstractive_test_v2.jsonl')
    parser.add_argument('--test_file', type=str,
                        default='/media/irelin/data_disk/dataset/dacon_summury/abstractive/abstractive_test_v2.jsonl')
    parser.add_argument('--output_dir', type=str,
                        default='/media/irelin/data_disk/dataset/dacon_summury/abstractive/preprocessed')
    parser.add_argument('--replace_special_chars', action='store_true', default=False)

    main(parser.parse_args())
