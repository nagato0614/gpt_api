from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import UnicodeNormalizeCharFilter
from janome.tokenfilter import POSStopFilter, ExtractAttributeFilter


def split_sentences(text):
    tokenizer = Tokenizer()
    char_filters = [UnicodeNormalizeCharFilter()]
    token_filters = [POSStopFilter([])]

    analyzer = Analyzer(char_filters=char_filters, tokenizer=tokenizer, token_filters=token_filters)

    sentences = []
    sentence = ''

    for token in analyzer.analyze(text):
        print(token)
        print(type(token))
        # sentence += token
        # if token in ('。', '！', '？', 'ます', 'です', 'です'):
        #     sentences.append(sentence)
        #     sentence = ''

    if sentence:
        sentences.append(sentence)

    return sentences

# スクリプトを実行する
if __name__ == '__main__':
    text = "今日は晴れですね昨日は雨でした明日はどうなるでしょうか楽しみです"
    sentences = split_sentences(text)

    for s in sentences:
        print(s)
