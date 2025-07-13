COMPRESSION_PROMPT = """
Compress the following text in a way that fits in a tweet (ideally) and such that you (GPT-4) can reconstruct the intention of the human who wrote text as close as possible to the original intention. This is for yourself. It does not need to be human readable or understandable. Abuse of language mixing, abbreviations, symbols (unicode and emoji), or any other encodings or internal representations is all permissible, as long as it, if pasted in a new inference cycle, will yield near-identical results as the original text. Numerical values and names are important, don't remove them.
"""

COMPRESSION_PROMPT_level_1  = """

"""

COMPRESSION_PROMPT_level_2 = """

"""

COMPRESSION_PROMPT_level_3 = """

"""

COMPRESSION_PROMPT_level_4 = """

"""

COMPRESSION_PROMPT_level_5 = """

"""