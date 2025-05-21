import tkinter as tk
from tkinter import ttk, filedialog
from Bio import pairwise2
from Bio.pairwise2 import format_alignment

#  Character sets
DNA_CHARS = set("ACGTN")
PROTEIN_CHARS = set("ACDEFGHIKLMNPQRSTVWY")

# Window   
root = tk.Tk()
root.title("🔬 Sequence Aligner")
root.geometry("950x650")
root.configure(padx=20, pady=20, bg="#f7f9fc")

style = ttk.Style()
style.configure("TLabel", font=("Segoe UI", 10), background="#f7f9fc")
style.configure("TButton", font=("Segoe UI", 10), padding=5)
style.configure("TMenubutton", font=("Segoe UI", 10))

#Sequence type dropdown   
ttk.Label(root, text="Sequence Type:").grid(row=0, column=0, sticky="e", pady=10)
seq_type_var = tk.StringVar(value="DNA")
seq_type_menu = ttk.OptionMenu(root, seq_type_var, "DNA", "DNA", "Protein")
seq_type_menu.grid(row=0, column=1, sticky="w")

#  Sequence 1 
ttk.Label(root, text="Sequence 1:").grid(row=1, column=0, sticky="ne", pady=10)
seq1_input = tk.Text(root, height=5, width=85, font=("Consolas", 10))
seq1_input.grid(row=1, column=1, pady=5)
ttk.Button(root, text="📂 Load File", command=lambda: load_file(seq1_input)).grid(row=1, column=2, padx=10)

#Sequence 2
ttk.Label(root, text="Sequence 2:").grid(row=2, column=0, sticky="ne", pady=10)
seq2_input = tk.Text(root, height=5, width=85, font=("Consolas", 10))
seq2_input.grid(row=2, column=1, pady=5)
ttk.Button(root, text="📂 Load File", command=lambda: load_file(seq2_input)).grid(row=2, column=2, padx=10)

# Align Button
ttk.Button(root, text="🔍 Align Sequences", command=lambda: align_sequences()).grid(row=3, column=1, sticky="w", pady=20)

#Result Output
ttk.Label(root, text="Alignment Result:").grid(row=4, column=0, sticky="ne", pady=10)
result_box = tk.Text(root, height=15, width=85, font=("Courier New", 10), bg="#f0f0f0", wrap="none")
result_box.grid(row=4, column=1, pady=10)
result_box.config(state="disabled")

# Load File Function
def load_file(target_box):
    file_path = filedialog.askopenfilename(
        filetypes=[("Text Files", "*.txt *.fasta *.fa"), ("All Files", "*.*")]
    )
    if not file_path:
        return
    try:
        with open(file_path, "r") as f:
            lines = f.readlines()
            sequence = "".join(line.strip() for line in lines if not line.startswith(">"))
            target_box.delete("1.0", tk.END)
            target_box.insert(tk.END, sequence)
    except Exception as e:
        _display(f"❌ Failed to load file: {e}")

# Alignment Function
def align_sequences():
    seq1 = seq1_input.get("1.0", tk.END).strip().upper()
    seq2 = seq2_input.get("1.0", tk.END).strip().upper()
    seq_type = seq_type_var.get()

    if not seq1 or not seq2:
        _display("⚠️ Please enter or load both sequences.")
        return

    invalid1 = set(seq1) - (DNA_CHARS if seq_type == "DNA" else PROTEIN_CHARS)
    invalid2 = set(seq2) - (DNA_CHARS if seq_type == "DNA" else PROTEIN_CHARS)

    if invalid1 or invalid2:
        _display(f"❌ Invalid characters found:\nSeq1: {invalid1}\nSeq2: {invalid2}")
        return

    alignments = pairwise2.align.globalxx(seq1, seq2)
    best = alignments[0]
    pretty = format_alignment(*best)
    _display(pretty)

#Output Display
def _display(text):
    result_box.config(state="normal")
    result_box.delete("1.0", tk.END)
    result_box.insert(tk.END, text)
    result_box.config(state="disabled")

root.mainloop()
