import chardet
import json
import os


def get_json_files():
    json_files = list(filter(lambda x: x.endswith('.json'), os.listdir(os.path.curdir)))
    return json_files


def get_top_words(file):
    news = file['rss']['channel']['items']

    top_words = {}
    for item in news:
        words = item['description'].split()

        for word in words:
            if len(word) > 6:

                if word in top_words:
                    top_words[word] += 1
                else:
                    top_words[word] = 1

    top_words = list(zip(top_words.keys(), top_words.values()))

    top_words.sort(key=lambda d: d[1], reverse=True)
    return top_words[:10]


def read_file():
    json_files = get_json_files()
    statistics = {}
    for file in json_files:

        with open(file, 'rb') as byte_file:
            f = byte_file.read()
            result = chardet.detect(f)

            statistics[file] = get_top_words(json.loads(f.decode(result['encoding'])))
    return statistics


def main():
    statistics = read_file()
    for file in statistics:
        words_list = []
        for word in statistics[file]:
            words_list.append(word[0])
        print('В файле ' + file + ' самые встречаемые слова: ', end='')
        print(*words_list, sep=', ', end='.\n')

main()