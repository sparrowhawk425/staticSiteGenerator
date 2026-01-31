import unittest

from functions.textnodemanip import extract_markdown_images, extract_markdown_links, markdown_to_blocks, extract_title

class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_none(self):
        matches = extract_markdown_images("This is text without an image")
        self.assertListEqual([], matches)
        
    def test_extract_markdown_images_multi(self):
        matches = extract_markdown_images("Check out this funny ![cat](https://i.imgur.com/weoimisd.png) and this adorable ![dog](https://i.imgur.com/weoidm.png)")
        self.assertListEqual([("cat", "https://i.imgur.com/weoimisd.png"), ("dog", "https://i.imgur.com/weoidm.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a [link](https://www.boot.dev)")
        self.assertListEqual([("link", "https://www.boot.dev")], matches)

    def test_extract_markdown_links_none(self):
        matches = extract_markdown_links("This is text without a link")
        self.assertListEqual([], matches)
    
    def test_extract_markdown_links_multi(self):
        matches = extract_markdown_links("Check out my [website](https://www.toob.ved) or my [blog](https://backtv.moc)")
        self.assertListEqual([("website", "https://www.toob.ved"), ("blog", "https://backtv.moc")], matches)
    
    def test_markdown_to_blocks(self):
        md = """
This is a **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_no_blocks(self):
        md = "I'm just a _simple_ paragraph"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [md])

    def test_markdown_to_blocks_empty_block(self):
        md = """
This is a **bolded** paragraph

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a **bolded** paragraph"])

    def test_extract_title(self):
        md = """
# Fellow Travelers   

This is not a title
"""
        title = extract_title(md)
        self.assertEqual(title, "Fellow Travelers")

    def test_extract_title_none(self):
        md = """
## Not a title

still # not a title"""
        with self.assertRaises(Exception):
            extract_title(md)

if __name__ == "__main__":
    unittest.main()
