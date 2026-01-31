import unittest

from functions.textnodemanip import block_to_block_type, BlockType

class TestTextBlocks(unittest.TestCase):
    def test_block_to_block_type_heading1(self):
        block = "# heading 1"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_heading2(self):
        block = "## heading 2"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_heading3(self):
        block = "### heading 3"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_heading4(self):
        block = "#### heading 4"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_heading5(self):
        block = "##### heading 5"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_heading6(self):
        block = "###### heading 6"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_code(self):
        block = "```\npublic static void main(String[] args){```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_block_type_quote(self):
        block = """> We choose to go to the Moon in this decade
>and do the other things, not because they are easy,
> but because they are hard; because that goal will serve
>to organize and measure the best of our energies and skills,
>because that challenge is one that we are willing to accept.
> one we are unwilling to postpone, and one we intend to win..."""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)
    
    def test_block_to_block_type_unordered_list(self):
        block = """- Do laundry
- Sweep floor
- Clean dishes"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list(self):
        block = """1. Use boot.dev
2. ???
3. Profit"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)
    
    def test_block_to_block_type_paragraph(self):
        block = """There's nothing **special** going on here
Nothing _at_ all with this `paragraph`
"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_malformed_list(self):
        block = """1. Hold
2. Hold
5. Right out
4. Thou shall not count
3. Throw"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()