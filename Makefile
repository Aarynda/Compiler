FILE=test_mult.c

full_test:
	cd python/parser_generation/ && python parse_gen.py --input_file ../test_files/$(FILE)
	cd python/ast_generation/ && python ast_gen.py --input_file ../parser_generation/out.tokens
	cd python/code_generation/ && python code_generation.py