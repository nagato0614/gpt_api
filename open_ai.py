import openai

res = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "あなたは賢いAIです。"},  # 役割設定（省略可）
        {"role": "user", "content": "1たす1は？"},  # 最初の質問
        {"role": "assistant", "content": "2です。"},  # 最初の答え
        {"role": "user", "content": "それを3倍して。"}  # 次の質問
    ],
    temperature=1
)
if __name__ == '__main__':
    str = ["- セミナーの留意事項を説明",
           "- セミナーは自動録画表示で、参加者の名前や顔は含まれない",
           "- 質問はセミナー中随時受け付けており、匿名で送信することができる",
           "- 日本電産株式会社主催の会社説明会を開催",
           "- 日本電産株式会社代表取締役会長最高経営責任者長森重信からプレゼンテーションを行う",
           "- 日本電産株式会社は小型モーターから観光船まで幅広い製品を提供しており、世界ナンバーワンシェアを誇る",
           "- 日本電産株式会社の強みは、世界一になれる製品をどんどん増やしていく企業文化にある",
           "に加えて、電子部品や自動運転技術など、幅広い事業分野で成長している日本電産。同社は、小さな会社を買収して成長を加速させるM & A戦略を展開し、2030",
           "には10兆円の売上目標を掲げている。また、世界の大波の中で、省エネやデジタル技術などの課題を解決する技術力が同社の強みである。株価も右肩上がりで、個人株主も増加している。",
           "・会社は品を広げ、工作機械の分野にも進出している。",
           "・電気自動車が成長の引っ張り手であり、モーター、インバーター、ギアが三位一体になっている。",
           "・電気自動車の時代は2025年からグワーッと増えると予測されている。",
           "・化石燃料エンジンの産業構造は部品が減るため、電動化に取り残される可能性がある。",
           "・電気自動車の部品だけで世界の7割8割を取る会社になる狙いがある。",
           "・冷蔵庫も静音かつ電気を消費しないモーターを使用する製品が増えている。",
           "・ゆるDCブラシレスモーターは静かで省エネルギーであり、地球環境の保全に貢献する技術である。",
           "・モーターは世界の消費電力の大部分を占めており、省エネルギー技術があれば世界の消費電力を減らすことができる。",
           "・ニデックは創業50周年を迎え、社名をニレックに変更する。",
           "・配当は30 % であり、今後も増やす予定。",
           "・株価については過去のグラフを示し、株主の損失を避けるために最善の努力をすると述べた。",
           "・会社は生協のための種をまかなうために投資をする。",
           "・50",
           "年を迎え、古い機会を全部捨てて新しいスタートを切る。",
           "・車載用のモーターで世界一を目指す。",
           "・株価は安く買って高く売るものである。",
           "・株主還元は配当性向30 % を決めているが、利益が上がっているため30 % には行かない。",
           "・成長企業であり、会社は伸び続ける必要がある。",
           "・投資せずに配当金を増やすことが大切",
           "・会社を大きくし、利益を増やすことで株価も上がり、大きなリターンがある",
           "・長期に株を持っている人には配当を出すことが貢献になる",
           "・後継者については、5人の副社長が選ばれている。長森会長は2024年で代表権を返上するが、会社には優秀な社員が多数いるため、肩書きが変わっても株価を上げていくことが人生であり、大きな会社に成長させて世界的な企業にすることが目標。結果は10年待たなくても出てくると思われる。",
           "- 日本電産は海外売上比率が圧倒的で、中国進出にも積極的",
           "- 世界どの国へ行ってもリスクはあるため、分散することが大切",
           "- 中国と台湾の将来についてはわからないが、戦略的に工場を持っているため大丈夫",
           "- EV事業の成長に期待しており、日本電産は世界トップに立てる可能性がある",
           "- 電気自動車は安い車が優れるということで、後進国での需要が高い",
           "- 現在の車の売れている量は8000万台程度で、将来的には5億台から6億台に増えると予想される。",
           "- 日本電産は世界に46カ国で300以上の工場を持っている。",
           "- 従業員たちに「今一番欲しいものは何か」という質問をして、78",
           "前は携帯電話が欲しいと言われ、最近は車が欲しいと言われるようになっている。",
           "- 現在のガソリン車を作っている会社は、安い車を作る気がないため、電気自動車が注目されている。",
           "- 日本電産は大量生産が得意で、2025年以降の小型車に注力している。",
           "- 日本電産はお客さんの作っているものと競合しない方針を持っており、EVメーカーにはならない。",
           "- 日本電産のモーターは静かで、モーターがついた車に乗りたいという人にはおすすめだと思われる。",
           "- モーターメーカーとしてだけでなく、ロボット分野にも注力している。",
           "- 重要な部品として、センサーやモーターがある。",
           "- 新しい工場をフランスや日本に建設し、工作機械も開発中。",
           "- プレス機械の需要が増えている。",
           "- ソリューション分野にも注力し、家電製品や掃除機などの省力化に貢献している。",
           "- モーター技術はスマホなどにも使われている。",
           "独自技術は、軽くて薄くて短いモーターの効率化や、消費電力の低減、静音性や振動の少なさなどが挙げられます。これらの技術は、世界中で需要が高まっており、特に貧しい国の人々にとっては、安価で静かでエコな車が求められています。今後も研究開発に力を入れ、新しいマーケットに進出することが必要であり、そのためには費用が必要ですが、それが踊り場であり、株主にとってもリターンが大きいことを説明しています。",
           "- 日本電産は多くの製品に使われるモーターを専門に作っている会社である。",
           "- 日本電産のモーターを使っていない製品は家庭では買わない。",
           "- 日本電産はM & Aを多く行っており、自力で売上を上げることとM & Aで成長していくことを目指している。",
           "- ドローンなど、モーターに何かをくっつけることで便利なものができる。",
           "- 社会に貢献するため、問題を解決する新しい技術を開発していく。",
           "- 日本電産はお客さんの声を大切にし、喜ばれる製品を開発している。",
           "- 自転車で幼稚園や保育園に子供を連れて行くために、電気自動車に適したモーターを供給してほしいと考えている。",
           "- 経営者として尊敬する人物は、オムロンの創業者である立石一真さんと、強制力の稲盛和夫さんである。",
           "- 学生たちの弱々しい姿勢に対しては、教育が間違っていると考えている。",
           "- 京都先端科学大学を創設し、外国語で英語を学ぶことで、若い時期に遊ばせながら楽しく勉強することが大切だと主張している。",
           "- 楽しく働けば良いと思う",
           "- 大学の偏差値だけでなく実力も必要",
           "- 子供たちは元気で楽しく働ける職場を望む",
           "- 株価の上下は長期的に見るべき",
           "- 投資とリターンの関係が重要",
           "- 10兆円を目指す日本電産の応援をする",
           "- 株の話ではなく、A株、B株、C株を買って欲しいという話",
           "- 会社の歴史や創業者の話",
           "- 人生哲学や考え方についての話",
           "- 1日に何度も株価をチェックしていること",
           "- 株価については特に何も思っていない",
           "- お会いする時には株価が上がっているように頑張るという話",
           "- 日本電産株式会社主催個人投資家向け会社説明会の終了の挨拶"]

    print(res["choices"][0]["message"]["content"])
    print(res["usage"]["prompt_tokens"],  # （履歴と）質問のトークン数
          res["usage"]["completion_tokens"],  # 答えのトークン数
          res["usage"]["total_tokens"])  # 合計
