import html
import os
import re
import tkinter as tk
from html.parser import HTMLParser
from tkinter import filedialog, messagebox, ttk
from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus, urljoin, urlparse
from urllib.request import Request, urlopen


HOME_URL = "https://example.com"
USER_AGENT = "JPS-Tkinter-Browser/1.0"


class PageParser(HTMLParser):
    """Turn a web page into readable text and clickable link targets."""

    SKIPPED_TAGS = {"script", "style", "noscript", "svg", "head"}
    BLOCK_TAGS = {
        "address", "article", "aside", "blockquote", "br", "dd", "div",
        "dl", "dt", "footer", "h1", "h2", "h3", "h4", "h5", "h6",
        "header", "hr", "li", "main", "nav", "ol", "p", "pre", "section",
        "table", "tr", "ul",
    }

    def __init__(self, base_url):
        super().__init__(convert_charrefs=True)
        self.base_url = base_url
        self.parts = []
        self.links = []
        self.skip_depth = 0
        self.link_target = None

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        attributes = dict(attrs)
        if tag == "body":
            self.skip_depth = 0
        if tag in self.SKIPPED_TAGS:
            self.skip_depth += 1
        if tag == "a" and self.skip_depth == 0:
            target = attributes.get("href")
            if target:
                self.link_target = urljoin(self.base_url, target)
        if tag in self.BLOCK_TAGS and self.parts and not self.parts[-1].endswith("\n"):
            self.parts.append("\n")

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in self.SKIPPED_TAGS and self.skip_depth:
            self.skip_depth -= 1
        if tag == "a":
            self.link_target = None
        if tag in self.BLOCK_TAGS and self.parts and not self.parts[-1].endswith("\n"):
            self.parts.append("\n")

    def handle_data(self, data):
        if self.skip_depth:
            return
        text = re.sub(r"\s+", " ", html.unescape(data)).strip()
        if not text:
            return
        if self.link_target:
            link_index = len(self.links)
            self.links.append(self.link_target)
            self.parts.append((text, link_index))
        else:
            self.parts.append(text)

    def result(self):
        text = ""
        link_ranges = []
        for part in self.parts:
            if isinstance(part, tuple):
                start = len(text)
                text += part[0]
                link_ranges.append((start, len(text), part[1]))
            else:
                text += part
        text = re.sub(r"[ \t]+\n", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text).strip()
        return text, link_ranges


class Browser(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("JPS Browser")
        self.geometry("1000x700")
        self.minsize(650, 420)
        self.configure(bg="#eef2f5")

        self.history = []
        self.history_index = -1
        self.current_url = ""
        self.current_links = []
        self.link_tags = {}
        self.loading = False

        self._build_ui()
        self.bind("<Alt-Left>", lambda _event: self.go_back())
        self.bind("<Alt-Right>", lambda _event: self.go_forward())
        self.bind("<Control-L>", self.focus_address)
        self.after(100, lambda: self.navigate(HOME_URL))

    def _build_ui(self):
        toolbar = tk.Frame(self, bg="#263238", padx=8, pady=8)
        toolbar.pack(fill="x")

        button_style = {
            "bg": "#37474f", "fg": "white", "activebackground": "#546e7a",
            "activeforeground": "white", "relief": "flat", "font": ("Segoe UI", 11),
            "width": 3, "cursor": "hand2",
        }
        self.back_button = tk.Button(toolbar, text="<", command=self.go_back, **button_style)
        self.back_button.pack(side="left", padx=(0, 4))
        self.forward_button = tk.Button(toolbar, text=">", command=self.go_forward, **button_style)
        self.forward_button.pack(side="left", padx=(0, 4))
        tk.Button(toolbar, text="R", command=self.reload, **button_style).pack(side="left", padx=(0, 8))

        self.address = ttk.Entry(toolbar, font=("Segoe UI", 11))
        self.address.pack(side="left", fill="x", expand=True, ipady=5)
        self.address.bind("<Return>", lambda _event: self.navigate_from_address())
        ttk.Button(toolbar, text="Go", command=self.navigate_from_address).pack(side="left", padx=(8, 0))
        ttk.Button(toolbar, text="Open file", command=self.open_file).pack(side="left", padx=(8, 0))

        self.status = tk.StringVar(value="Ready")
        tk.Label(self, textvariable=self.status, anchor="w", bg="#d7e0e5", fg="#455a64", padx=10).pack(fill="x")

        content = tk.Frame(self, bg="white")
        content.pack(fill="both", expand=True, padx=10, pady=10)
        self.page = tk.Text(
            content, wrap="word", bg="white", fg="#263238", relief="flat",
            padx=35, pady=25, font=("Segoe UI", 12), cursor="arrow",
        )
        scrollbar = ttk.Scrollbar(content, orient="vertical", command=self.page.yview)
        self.page.configure(yscrollcommand=scrollbar.set)
        self.page.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.page.tag_configure("title", font=("Segoe UI", 20, "bold"), foreground="#16324f", spacing3=10)
        self.page.tag_configure("link", foreground="#1565c0", underline=True)
        self.page.tag_configure("error", foreground="#b3261e")
        self.page.configure(state="disabled")
        self.page.bind("<Motion>", self.update_cursor)
        self.page.bind("<Button-1>", self.open_clicked_link)

    def focus_address(self, _event=None):
        self.address.focus_set()
        self.address.selection_range(0, "end")

    def normalize_url(self, value):
        value = value.strip()
        if not value:
            return HOME_URL
        if os.path.exists(value):
            return "file://" + os.path.abspath(value)
        if " " in value or ("." not in value and "://" not in value):
            return "https://www.google.com/search?q=" + quote_plus(value)
        if not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", value):
            value = "https://" + value
        return value

    def navigate_from_address(self):
        self.navigate(self.normalize_url(self.address.get()))

    def navigate(self, url, add_history=True):
        if self.loading:
            return
        self.loading = True
        self.status.set("Loading...")
        self.update_idletasks()
        try:
            content, final_url = self.fetch(url)
            self.display_page(content, final_url)
            if add_history:
                self.history = self.history[: self.history_index + 1]
                self.history.append(final_url)
                self.history_index += 1
            self.current_url = final_url
            self.address.delete(0, "end")
            self.address.insert(0, final_url)
            self.status.set(f"Loaded {final_url}")
        except (HTTPError, URLError, OSError, ValueError) as error:
            self.show_error(f"Could not load this page.\n\n{error}")
        finally:
            self.loading = False
            self.update_navigation_buttons()

    def fetch(self, url):
        parsed = urlparse(url)
        if parsed.scheme == "file":
            path = url[7:]
            with open(path, "rb") as file:
                data = file.read()
            return data.decode("utf-8", errors="replace"), url
        if parsed.scheme not in {"http", "https"}:
            raise ValueError("Only HTTP, HTTPS, and local HTML files are supported")
        request = Request(url, headers={"User-Agent": USER_AGENT})
        with urlopen(request, timeout=12) as response:
            data = response.read()
            final_url = response.geturl()
            charset = response.headers.get_content_charset() or "utf-8"
        return data.decode(charset, errors="replace"), final_url

    def display_page(self, content, url):
        parser = PageParser(url)
        parser.feed(content)
        text, link_ranges = parser.result()
        self.current_links = parser.links
        self.link_tags = {}
        self.page.configure(state="normal")
        self.page.delete("1.0", "end")
        self.page.insert("1.0", text or "(This page has no readable text.)")
        for number, (start, end, link_index) in enumerate(link_ranges):
            start_index = "1.0 + %d chars" % start
            end_index = "1.0 + %d chars" % end
            tag = f"link_{number}"
            self.page.tag_add(tag, start_index, end_index)
            self.page.tag_configure(tag, foreground="#1565c0", underline=True)
            self.link_tags[tag] = link_index
        self.page.configure(state="disabled")
        self.page.yview_moveto(0)

    def show_error(self, message):
        self.page.configure(state="normal")
        self.page.delete("1.0", "end")
        self.page.insert("1.0", message, "error")
        self.page.configure(state="disabled")
        self.status.set("Page load failed")

    def open_clicked_link(self, event):
        index = self.page.index(f"@{event.x},{event.y}")
        tags = self.page.tag_names(index)
        for tag in tags:
            if tag in self.link_tags:
                self.navigate(self.current_links[self.link_tags[tag]])
                return

    def update_cursor(self, event):
        index = self.page.index(f"@{event.x},{event.y}")
        is_link = any(tag in self.link_tags for tag in self.page.tag_names(index))
        self.page.configure(cursor="hand2" if is_link else "arrow")

    def go_back(self):
        if self.history_index > 0:
            self.history_index -= 1
            self.navigate(self.history[self.history_index], add_history=False)

    def go_forward(self):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.navigate(self.history[self.history_index], add_history=False)

    def reload(self):
        if self.current_url:
            self.navigate(self.current_url, add_history=False)

    def update_navigation_buttons(self):
        self.back_button.configure(state="normal" if self.history_index > 0 else "disabled")
        self.forward_button.configure(
            state="normal" if self.history_index < len(self.history) - 1 else "disabled"
        )

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[("HTML files", "*.html *.htm"), ("All files", "*.*")])
        if path:
            self.navigate("file://" + os.path.abspath(path))


if __name__ == "__main__":
    Browser().mainloop()
