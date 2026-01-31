import unittest

from functions.textnodemanip import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType

class TestSplitNodes(unittest.TestCase):
    def test_split_nodes_delimiter_b(self):
        old_nodes = [
            TextNode("This is a **bold** statement", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" statement", TextType.TEXT)
        ]
        self.assertListEqual(new_nodes, expected_nodes)
    
    def test_split_nodes_delimiter_i(self):
        old_nodes = [
            TextNode("This is an _iconic_ statement", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
        expected_nodes = [
            TextNode("This is an ", TextType.TEXT),
            TextNode("iconic", TextType.ITALIC),
            TextNode(" statement", TextType.TEXT)
        ]
        self.assertListEqual(new_nodes, expected_nodes)
    
    def test_split_nodes_delimiter_code(self):
        old_nodes = [
            TextNode("This is a `nerdy` statement", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("nerdy", TextType.CODE),
            TextNode(" statement", TextType.TEXT)
        ]
        self.assertListEqual(new_nodes, expected_nodes)

    def test_split_nodes_delimiter_not_text(self):
        old_nodes = [ TextNode("check out my website", TextType.LINK, "https://www.boot.dev") ]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.LINK)
        self.assertListEqual(old_nodes, new_nodes)

    def test_split_nodes_delimiter_no_delim(self):
        old_nodes = [
            TextNode("This is a bold statement", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertListEqual(old_nodes, new_nodes)

    def test_split_nodes_delimiter_missing_delim(self):
        old_nodes = [
            TextNode("This is a **bold statement", TextType.TEXT)
        ]
        with self.assertRaises(Exception):
            split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

    def test_split_nodes_delimiter_empty_delim(self):
        old_nodes = [
            TextNode("This is a **bold** statement", TextType.TEXT)
        ]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(old_nodes, "", TextType.BOLD)

    def test_split_nodes_delimiter_end_of_line(self):
        old_nodes = [
            TextNode("This is **bold**", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD)
        ]
        self.assertListEqual(new_nodes, expected_nodes)

    
    def test_split_nodes_delimiter_multi(self):
        old_nodes = [
            TextNode("This is a **bold** statement.", TextType.TEXT),
            TextNode("I have **so** much **more** to say!", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" statement.", TextType.TEXT),
            TextNode("I have ", TextType.TEXT),
            TextNode("so", TextType.BOLD),
            TextNode(" much ", TextType.TEXT),
            TextNode("more", TextType.BOLD),
            TextNode(" to say!", TextType.TEXT)
        ]
        self.assertListEqual(new_nodes, expected_nodes)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_none(self):
        old_nodes = [TextNode("This has no image", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertListEqual(old_nodes, new_nodes)

    def test_split_images_bomb(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.boot.dev) and another [one](https://ved.toob.www)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("one", TextType.LINK, "https://ved.toob.www")
            ],
            new_nodes
        )
    
    def test_split_links_none(self):
        old_nodes = [TextNode("This has no link", TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)
        self.assertListEqual(old_nodes, new_nodes)

    def test_split_links_bomb(self):
        node = TextNode(
            "[link](https://www.boot.dev)[link2](https://ved.toob.www)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode("link2", TextType.LINK, "https://ved.toob.www")
            ],
            new_nodes
        )

    def test_text_to_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes
        )

if __name__ == "__main__":
    unittest.main()