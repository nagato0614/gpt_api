import tiktoken  # type: ignore[import]


def to_str(b: bytes) -> str:
    """
    バイト列を文字列に変換する関数
    :param b:
    :return:
    """
    return b.decode()


def join_bytes(bs: list[bytes]) -> bytes:
    """
    バイト列を結合する関数
    :param bs:
    :return:
    """
    return b"".join(bs)


def join_indices(indices: list[int]) -> str:
    """
    トークンのインデックスを結合する関数
    :param indices:
    :return:
    """
    return "-".join(str(i) for i in indices)


def join_ids(ids: list[int]) -> str:
    """
    トークンIDを結合する関数
    :param ids:
    :return:
    """
    return ", ".join(str(id) for id in ids)


token_list = []


def print_if_decoded(b: bytes, indices: str, ids: str) -> None:
    """
    デコードできたらprintする関数
    :param b:
    :param indices:
    :param ids:
    :return:
    """
    try:
        s = to_str(b)
    except UnicodeDecodeError as err:
        raise err
    else:
        print(indices, f"{s!r} ({ids})")
        token_list.append(s)
        pass


class TextSplitter:
    """
    chatGPTに渡すテキストを分割するクラス
    """

    # 入力された文字列
    input_text: str

    # 分割された文字列
    split_text: list[str]

    # 分割された文字, 単語のトークン数
    token_list: list[int]

    # 分割されたデータ
    rest_tokens: list[tuple[int, bytes, int]]

    def __init__(self, text: str, model: str = "gpt-4"):
        """
        コンストラクタ
        :param text: 分割するテキスト
        :param model: 使用するモデル
        """
        self.text = text
        self.model = model
        self.token_list = []
        self.split_text = []

        # テキストを分割する
        self.encoding = tiktoken.encoding_for_model(model)
        self.token_ids = self.encoding.encode(text)
        self.byte_tokens = self.encoding.decode_tokens_bytes(self.token_ids)
        self.split()

    def add_token(self, b: bytes, indices: str, ids: str) -> None:
        """
        トークンを追加する関数
        :param b:
        :param indices:
        :param ids:
        :return:
        """
        try:
            s = to_str(b)
        except UnicodeDecodeError as err:
            raise err
        else:
            # 文字を保存
            self.split_text.append(s)

            # トークン数を計算し保存
            indices_list = indices.split("-")
            token_num = len(indices_list)
            if token_num == 1:
                self.token_list.append(1)
            elif token_num >= 2:
                size = int(indices_list[-1]) - int(indices_list[0]) + 1
                self.token_list.append(size)
            else:
                print(indices_list)
                raise ValueError("indices_listの要素数が不正です")

    def split(self):
        self.rest_tokens = []

        # トークンを分割する
        for i, (token_id, token) in enumerate(
                zip(self.token_ids, self.byte_tokens)):
            try:
                self.add_token(token, str(i), str(token_id))
            except UnicodeDecodeError:
                try:
                    # トークンを結合してデコードする
                    joined_token = join_bytes(
                        [p[1] for p in self.rest_tokens] + [token])
                    joined_indices = join_indices(
                        [p[0] for p in self.rest_tokens] + [i])
                    token_ids = join_ids(
                        [p[2] for p in self.rest_tokens] + [token_id])
                    self.add_token(joined_token, joined_indices, token_ids)
                except UnicodeDecodeError:
                    # デコードできなかったら次のトークンに移す
                    self.rest_tokens.append((i, token, token_id))
                else:
                    # デコードできたらリストをクリアする
                    self.rest_tokens.clear()


# スクリプトを実行する
if __name__ == '__main__':
    text = "今日は晴れですね昨日は雨でした明日はどうなるでしょうか楽しみです" \
           "Hello World!"
    encoding = tiktoken.encoding_for_model("gpt-4")
    token_ids = encoding.encode(text)
    byte_tokens = encoding.decode_tokens_bytes(token_ids)

    splitter = TextSplitter(text)
    print(splitter.token_list)
    print(splitter.split_text)
    print(len(splitter.token_list))
    print(len(splitter.split_text))
