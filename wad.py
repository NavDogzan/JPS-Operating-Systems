import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import io
import os

from PIL import Image, ImageTk


def open_document():
	file_path = filedialog.askopenfilename(
		filetypes=[("PDF or DOCX", "*.pdf *.docx"), ("All files", "*.*")]
	)

	if not file_path:
		return

	try:
		if file_path.lower().endswith(".pdf"):
			show_pdf(file_path)
		else:
			from docx import Document

			text = "\n\n".join(paragraph.text for paragraph in Document(file_path).paragraphs)
			show_docx(text)
	except ImportError:
		messagebox.showerror(
			"Missing package",
			"Install PyMuPDF and python-docx first:\n\npip install PyMuPDF python-docx"
		)
		return
	except Exception as error:
		messagebox.showerror("Could not open file", str(error))
		return

	root.title(f"Document Viewer - {os.path.basename(file_path)}")


def clear_viewer():
	root.unbind_all("<MouseWheel>")
	for widget in viewer_frame.winfo_children():
		widget.destroy()


def show_docx(text):
	clear_viewer()
	viewer = tk.Text(viewer_frame, wrap="word")
	viewer.insert("1.0", text)
	viewer.pack(side="left", fill="both", expand=True)
	scrollbar = ttk.Scrollbar(viewer_frame, command=viewer.yview)
	scrollbar.pack(side="right", fill="y")
	viewer.config(yscrollcommand=scrollbar.set)


def show_pdf(file_path):
	import fitz

	clear_viewer()
	canvas = tk.Canvas(viewer_frame, highlightthickness=0)
	canvas.pack(side="left", fill="both", expand=True)

	scrollbar = ttk.Scrollbar(viewer_frame, orient="vertical", command=canvas.yview)
	scrollbar.pack(side="right", fill="y")
	canvas.config(yscrollcommand=scrollbar.set)

	page_frame = ttk.Frame(canvas)
	canvas.create_window((0, 0), window=page_frame, anchor="nw")
	pages = []

	def resize_pages(_event=None):
		page_width = max(canvas.winfo_width() - 20, 100)
		for original, page_label in pages:
			scale = page_width / original.width
			image_size = (page_width, int(original.height * scale))
			image = ImageTk.PhotoImage(original.resize(image_size, Image.LANCZOS))
			page_label.config(image=image)
			page_label.image = image

	page_frame.bind(
		"<Configure>",
		lambda event: canvas.configure(scrollregion=canvas.bbox("all"))
	)
	canvas.bind("<Configure>", resize_pages)
	root.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(-int(event.delta / 120), "units"))

	document = fitz.open(file_path)
	for page in document:
		pixmap = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5), alpha=False)
		original = Image.open(io.BytesIO(pixmap.tobytes("png")))
		page_label = tk.Label(page_frame)
		pages.append((original, page_label))
		page_label.pack(pady=5)
	document.close()
	resize_pages()


root = tk.Tk()
root.title("Simple Document Viewer")
root.geometry("700x500")

ttk.Button(root, text="Open PDF or DOCX", command=open_document).pack(pady=10)

viewer_frame = ttk.Frame(root)
viewer_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

root.mainloop()
