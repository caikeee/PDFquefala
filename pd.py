import os
import PyPDF2
from gtts import gTTS
import pygame
import time
import tkinter as tk
from tkinter import filedialog, messagebox

def extract_text_from_pdf(pdf_path, start_page=None, end_page=None):
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ''
            if start_page is None or end_page is None:  # Caso o conteúdo completo seja selecionado
                for page in pdf_reader.pages:
                    text += page.extract_text() or ''
            else:
                for page_num in range(start_page, min(end_page, len(pdf_reader.pages))):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() or ''
            return text
    except Exception as e:
        print(f"Erro ao extrair texto do PDF: {e}")
        return None

def convert_text_to_speech(text, output_audio_path, language='pt'):
    try:
        tts = gTTS(text=text, lang=language)
        tts.save(output_audio_path)
        messagebox.showinfo("Sucesso", f"Áudio salvo em: {output_audio_path}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao converter texto em fala: {e}")

def play_audio_limited(audio_path, duration_seconds):
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()
        start_time = time.time()

        while pygame.mixer.music.get_busy():
            elapsed_time = time.time() - start_time
            if elapsed_time >= duration_seconds:
                pygame.mixer.music.stop()
                break
            pygame.time.Clock().tick(10)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao reproduzir áudio: {e}")

def select_pdf():
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if pdf_path:
        pdf_label.config(text=os.path.basename(pdf_path))
        global selected_pdf_path
        selected_pdf_path = pdf_path

def toggle_page_entries():
    """Função para habilitar/desabilitar as entradas de páginas."""
    if complete_var.get():
        entry_start_page.config(state='disabled')  # Desabilita entrada de página inicial
        entry_end_page.config(state='disabled')    # Desabilita entrada de página final
    else:
        entry_start_page.config(state='normal')    # Habilita entrada de página inicial
        entry_end_page.config(state='normal')      # Habilita entrada de página final

def convert_and_play():
    try:
        output_audio_path = os.path.join(os.path.dirname(selected_pdf_path), 'audiobook.mp3')
        
        # Verifica se a caixa de seleção "Conteúdo completo" está marcada
        if complete_var.get():
            text = extract_text_from_pdf(selected_pdf_path)  # Extrai todo o conteúdo do PDF
        else:
            # Verifica se os campos de páginas estão preenchidos corretamente
            start_page = int(entry_start_page.get()) - 1
            end_page = int(entry_end_page.get())
            if start_page >= 0 and end_page > start_page:
                text = extract_text_from_pdf(selected_pdf_path, start_page, end_page)
            else:
                messagebox.showerror("Erro", "Por favor, insira números de página válidos.")
                return

        if text:
            convert_text_to_speech(text, output_audio_path)
            play_audio_limited(output_audio_path, duration_seconds=120)
        else:
            messagebox.showerror("Erro", "Não foi possível extrair o texto.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao processar: {e}")

# Criando a interface gráfica
root = tk.Tk()
root.title("PDF que Fala")

# Label e botão para selecionar o PDF
pdf_label = tk.Label(root, text="Selecione um PDF", width=50)
pdf_label.pack(pady=10)

btn_select_pdf = tk.Button(root, text="Selecionar PDF", command=select_pdf)
btn_select_pdf.pack(pady=10)

# Entrada para as páginas de início e fim
frame_pages = tk.Frame(root)
frame_pages.pack(pady=10)

tk.Label(frame_pages, text="Página Inicial:").grid(row=0, column=0)
entry_start_page = tk.Entry(frame_pages, width=5)
entry_start_page.grid(row=0, column=1)

tk.Label(frame_pages, text="Página Final:").grid(row=1, column=0)
entry_end_page = tk.Entry(frame_pages, width=5)
entry_end_page.grid(row=1, column=1)

# Checkbox para selecionar o conteúdo completo
complete_var = tk.BooleanVar()
checkbox_complete = tk.Checkbutton(root, text="Converter o conteúdo completo", variable=complete_var, command=toggle_page_entries)
checkbox_complete.pack(pady=10)

# Botão para iniciar a conversão
btn_convert = tk.Button(root, text="Converter e Reproduzir", command=convert_and_play)
btn_convert.pack(pady=20)

# Rodar a aplicação
root.mainloop()