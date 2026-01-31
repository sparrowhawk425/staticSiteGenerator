import unittest

from functions.textnodemanip import text_node_to_html_node, markdown_to_html_node

from textnode import TextNode, TextType
from htmlnode import ParentNode, LeafNode

class TestSiteGenerator(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a brave node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a brave node")

    def test_italic(self):
        node = TextNode("This is an excited node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an excited node")

    def test_code(self):
        node = TextNode("This is a nerdy node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a nerdy node")

    def test_link(self):
        node = TextNode("This is a Zelda node", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a Zelda node")
        self.assertTrue("href" in html_node.props)
        self.assertEqual(html_node.props["href"], "https://www.boot.dev")

    def test_image(self):
        node = TextNode("This is a statement node", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertTrue("src" in html_node.props)
        self.assertEqual(html_node.props["src"], "https://www.boot.dev")
        self.assertTrue("alt" in html_node.props)
        self.assertEqual(html_node.props["alt"], "This is a statement node")
        
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )
    
    def test_headings(self):
        md = """
# Title

## Subtitle

### Subsubtitle

#### Subsubsubtitle

##### Subsubsubsubtitle

###### Subsubsubsubsubtitle
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Title</h1><h2>Subtitle</h2><h3>Subsubtitle</h3><h4>Subsubsubtitle</h4><h5>Subsubsubsubtitle</h5><h6>Subsubsubsubsubtitle</h6></div>"
        )
    
    def test_blockquote(self):
        md = """
> We shall fight on the beaches, we shall fight on the landing grounds,
> we shall fight in the fields and in the streets, we shall fight in the hills; we shall never surrender.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.maxDiff = None
        self.assertEqual(
            html,
            "<div><blockquote>We shall fight on the beaches, we shall fight on the landing grounds, we shall fight in the fields and in the streets, we shall fight in the hills; we shall never surrender.</blockquote></div>"
        )

    def test_unordered_list(self):
        md = """
- Do laundry
- Wash dishes
- Televise revolution
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Do laundry</li><li>Wash dishes</li><li>Televise revolution</li></ul></div>"
        )
    
    def test_ordered_list(self):
        md = """
1. Learn
2. ???
3. Profit
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Learn</li><li>???</li><li>Profit</li></ol></div>"
        )

    def test_image(self):
        md = """
![sitting](/images/sitting.png)
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p><img src="/images/sitting.png" alt="sitting"></img></p></div>'
        )
    
    def test_link(self):
        md = """
[my website](https://www.boot.dev)
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p><a href="https://www.boot.dev">my website</a></p></div>'
        )

if __name__ == "__main__":
    unittest.main()
