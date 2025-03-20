import unittest

from block import BlockType, block_to_block_type


class BlockTest(unittest.TestCase):
    def test_block_to_block_type_heading(self):
        for i in range(1, 7):
            test_block = "#" * i + " heading test"
            self.assertEqual(BlockType.HEADING, block_to_block_type(test_block))
        i += 1
        test_block = "#" * i + " heading test"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(test_block))

    def test_block_to_block_type_code(self):
        test_block = "```This should be a code block```\n"
        self.assertEqual(BlockType.CODE, block_to_block_type(test_block))

    def test_block_to_block_type_list(self):
        test_block = "- This\n- Should\n- Be\n- A\n- Unorder\n- List\n"
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(test_block))

    def test_block_to_block_type(self):
        test_block = "1. This\n2. Should\n3. Be\n4. A\n5. Orderedr\n6. List\n"
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(test_block))

    def test_block_to_block_type_quote(self):
        test_block = "> This\n> Should\n> Be\n> A\n> Quote\n"
        self.assertEqual(BlockType.QUOTE, block_to_block_type(test_block))


    def test_block_to_block_type_paragraph(self):
        test_block = "1. Typoed\n1. Ordered List\n2. is a\n3. Paragraph\n"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(test_block))


if __name__ == "__main__":
    unittest.main()
