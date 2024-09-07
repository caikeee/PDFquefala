import os  # para interagir com o sistema operacional, da pra manipular caminhos de arquivos e pastas.
import PyPDF2  # Biblioteca para ler PDF.
from gtts import gTTS  # Google Text-to-Speech, para converter texto em fala.
import pygame  # Biblioteca para reprodução de áudio e outras funcionalidades multimídia.
import time  # Módulo para manipulação de tempo, usado aqui para controlar a duração da reprodução do áudio,

def extract_text_from_pdf(pdf_path, start_page, end_page):
    """
    Função para extrair texto de um PDF, a partir de uma página inicial até uma página final.
    
    :param pdf_path: Caminho do arquivo PDF.
    :param start_page: Número da página inicial (baseado em 0).
    :param end_page: Número da página final (baseado em 0, não inclusivo).
    :return: O texto extraído do PDF.
    """
    try:
        with open(pdf_path, 'rb') as file:  # Abre o arquivo PDF em modo binário de leitura.
            pdf_reader = PyPDF2.PdfReader(file)  # Cria um objeto leitor do PDF.
            text = ''  # Inicializa uma string vazia para armazenar o texto extraído.
            for page_num in range(start_page, min(end_page, len(pdf_reader.pages))):  # Itera pelas páginas definidas.
                page = pdf_reader.pages[page_num]  # Acessa a página atual.
                text += page.extract_text() or ''  # Extrai o texto da página e adiciona à string; se não houver texto, adiciona uma string vazia.
            return text  # Retorna o texto extraído.
    except Exception as e:  # Captura e trata qualquer exceção que possa ocorrer.
        print(f"Erro ao extrair texto do PDF: {e}")  # Exibe a mensagem de erro.
        return None  # Retorna None se ocorrer um erro.

def convert_text_to_speech(text, output_audio_path, language='pt'):
    """
    Função para converter texto em fala e salvar em um arquivo de áudio.
    
    :param text: O texto a ser convertido em fala.
    :param output_audio_path: O caminho do arquivo de saída onde o áudio será salvo.
    :param language: O código do idioma para a conversão (padrão é português).
    """
    try:
        tts = gTTS(text=text, lang=language)  # Converte o texto em fala usando gTTS.
        tts.save(output_audio_path)  # Salva o áudio gerado no caminho especificado.
        print(f"Áudio salvo em: {output_audio_path}")  # Informa que o áudio foi salvo com sucesso.
    except Exception as e:  # Captura e trata qualquer exceção que possa ocorrer.
        print(f"Erro ao converter texto em fala: {e}")  # Exibe a mensagem de erro.

def play_audio_limited(audio_path, duration_seconds):
    """
    Função para reproduzir um arquivo de áudio com um limite de tempo.
    
    :param audio_path: O caminho do arquivo de áudio a ser reproduzido.
    :param duration_seconds: A duração máxima em segundos para reproduzir o áudio.
    """
    try:
        pygame.mixer.init()  # Inicializa o mixer do pygame para reprodução de áudio.
        pygame.mixer.music.load(audio_path)  # Carrega o arquivo de áudio.
        pygame.mixer.music.play()  # Inicia a reprodução do áudio.
        start_time = time.time()  # Marca o tempo inicial da reprodução.
        
        print("Iniciando reprodução...")  # Informa que a reprodução começou.
        while pygame.mixer.music.get_busy():  # Enquanto o áudio estiver tocando...
            elapsed_time = time.time() - start_time  # Calcula o tempo decorrido.
            if elapsed_time >= duration_seconds:  # Se o tempo decorrido atingir o limite...
                pygame.mixer.music.stop()  # Para a reprodução do áudio.
                print(f"Reprodução interrompida após {duration_seconds} segundos.")  # Informa que a reprodução foi interrompida.
                break  # Sai do loop.
            pygame.time.Clock().tick(10)  # Limita o loop a 10 iterações por segundo.
        else:
            print(f"Áudio reproduzido até o final: {audio_path}")  # Se o áudio terminar antes do limite, informa que a reprodução foi concluída.
    except Exception as e:  # Captura e trata qualquer exceção que possa ocorrer.
        print(f"Erro ao reproduzir áudio: {e}")  # Exibe a mensagem de erro.

def main():
    """
    Função principal que coordena a execução das outras funções.
    """
    # Obter o diretório atual do script
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Obtém o caminho do diretório onde o script está localizado.
    
    # Construir o caminho completo para o arquivo PDF
    pdf_filename = 'O programador-pragmatico.pdf'  # Nome do arquivo PDF.
    pdf_path = os.path.join(script_dir, pdf_filename)  # Constrói o caminho completo para o arquivo PDF.

    # Verificar se o arquivo PDF existe
    if not os.path.exists(pdf_path):  # Verifica se o arquivo PDF não existe.
        print(f"O arquivo PDF não foi encontrado: {pdf_path}")  # Informa que o arquivo PDF não foi encontrado.
        return  # Sai da função main() se o arquivo PDF não existir.
    else:
        print(f"O arquivo PDF foi encontrado: {pdf_path}")  # Informa que o arquivo PDF foi encontrado.

    # Definir o caminho para o arquivo de áudio de saída
    output_audio_path = os.path.join(script_dir, 'audiobook.mp3')  # Define o caminho para salvar o arquivo de áudio.

    # Definir as páginas para processar em cada parte
    pages_per_part = 10  # Número de páginas por parte.
    pdf_reader = PyPDF2.PdfReader(pdf_path)  # Cria um leitor de PDF.
    total_pages = len(pdf_reader.pages)  # Obtém o número total de páginas no PDF.

    # Processa o PDF em partes, conforme o número de páginas por parte definido
    for start_page in range(0, total_pages, pages_per_part):
        end_page = start_page + pages_per_part  # Define a última página da parte atual.
        text = extract_text_from_pdf(pdf_path, start_page, end_page)  # Extrai o texto do PDF para a parte atual.

        if text:  # Se o texto foi extraído com sucesso...
            part_audio_path = os.path.join(script_dir, f'audiobook_{start_page + 1}_to_{end_page}.mp3')  # Define o nome do arquivo de áudio para a parte.
            convert_text_to_speech(text, part_audio_path, language='pt')  # Converte o texto em fala e salva o áudio.
            print(f"Texto convertido para {part_audio_path}.")  # Informa que o texto foi convertido e salvo.
            
            # Reproduzir o áudio limitado a 2 minutos
            play_audio_limited(part_audio_path, duration_seconds=120)  # Reproduz o áudio por até 2 minutos.
        else:
            print("Não foi possível extrair texto do PDF.")  # Informa que não foi possível extrair texto do PDF.

if __name__ == '__main__':
    main()  # Chama a função principal para iniciar o programa.
