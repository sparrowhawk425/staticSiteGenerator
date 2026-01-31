import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("italics are _weird_", TextType.ITALIC)
        node2 = TextNode("code is where it's at", TextType.CODE)
        self.assertNotEqual(node, node2)
    
    def test_missing_url(self):
        node = TextNode("I'm a link", TextType.LINK, url="https://www.boot.dev")
        node2 = TextNode("I'm a link", TextType.LINK)
        self.assertNotEqual(node, node2)
    
    def test_different_types(self):
        node = TextNode("I'm Zelda", TextType.LINK)
        node2 = TextNode("I'm Zelda", TextType.IMAGE)
        self.assertNotEqual(node, node2)

    def test_different_text(self):
        node = TextNode("Happy", TextType.BOLD)
        node2 = TextNode("Sad", TextType.BOLD)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
