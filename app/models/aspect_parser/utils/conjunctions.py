""" This module describes conjunctions, pair conjunctions and conjunctive adverbs """


def conjunctions(language: str) -> set:
    """
    :param language: language to get conunctions for
    :return: set of all conjunctions in language
    """
    try:
        return {'ru': {"а", "будто", "где", "едва", "да", "дабы", "ежели", "если", "зато", "зачем", "и", "ибо", "или",
                       "кабы", "как", "каков", "какой", "когда", "коли", "который", "кто", "куда", "лишь", "насколько",
                       "нежели", "но", "однако", "откуда", "отчего", "пока", "поскольку", "потому", "почему", "поэтому",
                       "пускай", "пусть", "раз", "сколько", "словно", "также", "тоже", "только", "точно", "хотя", "чей",
                       "чем", "что", "чтобы"},
                'en': {"and", "as", "for", "or", "yet", "but", "till", "as", "if", "after", "until", "because", "and",
                       "or", "nor", "so", "before", "since", "that", "unless", "whether", "while", "where", "when",
                       "why", "what", "how", "whenever", "although", "though", "once", "than", "whereas", "thus",
                       "in case", "on condition", "who", "which", "whose"},
                'fr': {'car', 'comme', 'dont', 'et', 'laquelle', 'laquelles', 'lequel', 'lequels', 'lesquelles',
                       'lesquels', 'lorsque', 'lorsque', 'moins', 'ni', 'ou', 'où', 'plus', 'puisque', 'quand',
                       'quand', 'que', 'quoique', 'si', 'tantôt'},
                'es': {'apenas', 'aunque', 'bien', 'como', 'como', 'conque', 'cuando', 'donde', 'e', 'luego',
                       'mientras', 'ni', 'o', 'pero', 'porque', 'pues', 'que', 'que', 'según', 'si', 'sino', 'y', 'ya'}
                }[language]
    except KeyError:
        raise Exception("Language %s is not supported" % language)


def pair_conjunctions(language: str) -> set:
    """
    :param language: language to get pair conunctions for
    :return: set of all pair conjunctions (as tuples) in language
    """
    try:
        return {'ru': {},
                'en': {("both", "and"), ("either", "or"), ("not only", "but"), ("not only", "but also"),
                       ("rather", "or"), ("just as", "so"), ("neither", "nor"), ("whether", "or"), ("if", "then")},
                'fr': {("afin", "que"), ("alors", "que"), ("avant", "que"), ("bien", "que"), ("comme", "si"),
                       ("d’", "où"), ("dès", "que"), ("durant", "que"), ("malgré", "que"), ("non", "que"),
                       ("par", "où"), ("parce", "que"), ("pendant", "que"), ("pour", "que"), ("pourvu", "que"),
                       ("soit", "que"), ("tandis", "que"), ("tant", "que")},
                'es': {("a", "donde"), ("antes", "que"), ("así", "como"), ("así", "que"), ("como", "que"),
                       ("como", "si"), ("de", "donde"), ("en", "donde"), ("en", "tanto"), ("es", "decir"),
                       ("hasta", "que"), ("luego", "que"), ("para", "que"), ("por", "donde"), ("tal", "como"),
                       ("tanto", "como")}
                }[language]
    except KeyError:
        raise Exception("Language %s is not supported" % language)


def conjunctive_adverbs(language: str) -> set:
    """
    :param language: language to get conjuctive adverbs for
    :return: set of all conjuctive adverbs in language
    """
    try:
        return {'ru': {("благодаря", "тому", "что"), ("в", "связи", "с"), ("в", "связи", "с", "тем", "что"),
                       ("в", "то", "время", "как"), ("ввиду", "того", "что"), ("вследствие", "того", "что"),
                       ("для", "того", "чтобы"), ("до", "тех", "пор", "пока"), ("если", "бы"), ("затем", "чтобы"),
                       ("из-за", "того", "что"), ("как", "будто"), ("как", "если", "бы"), ("как", "только"),
                       ("лишь", "только"), ("не", "смотря", "на", "то", "что"), ("оттого", "что"),
                       ("перед", "тем", "как"), ("по", "мере", "того", "как"), ("подобно", "тому", "как"),
                       ("пока", "не"), ("после", "того", "как"), ("потому", "что"), ("прежде", "чем"),
                       ("с", "тем", "чтобы"), ("с", "тех", "пор", "как"), ("так", "как"), ("так", "что")},
                'en': {("after", "all"), ("also",), ("as", "a", "result"), ("besides",), ("consequently",),
                       ("for", "example"), ("however",), ("in", "addition"), ("in", "fact"), ("in", "other", "words"),
                       ("meanwhile",), ("moreover",), ("on", "the", "other", "hand"), ("therefore",), ("thus",),
                       ("then",)},
                'fr': {("à", "condition", "que"), ("à", "mesure", "que"), ("à", "tel", "point", "que"),
                       ("au", "cas", "que"), ("au", "point", "que"), ("aussi", "longtemps", "que"),
                       ("de", "façon", "que"), ("de", "manière", "que"), ("de", "sorte", "que"),
                       ("du", "moment", "que"), ("en", "cas", "que"), ("jusqu’à", "ce", "que"), ("non", "pas", "que"),
                       ("pour", "peu", "que"), ("si", "bien", "que")},
                'es': {("antes", "de", "que"), ("de", "manera", "que"), ("por", "lo", "tanto")}
                }[language]
    except KeyError:
        raise Exception("Language %s is not supported" % language)
