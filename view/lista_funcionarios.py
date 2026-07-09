import tkinter as tk
import customtkinter as ctk

# Importações do projeto (Sempre no topo do arquivo)
try:
    from bemvindo import listar_todos
except ImportError:
    # Caso o banco de dados não exista ainda, criamos uma função genérica para o código não quebrar
    def listar_todos():
        return [
            ("Anakin Skywalker", "vader@empire.com", "(11) 99999-9999", "111.222.333-44", "vader", ""),
            ("Luke Skywalker", "luke@rebel.com", "(11) 88888-8888", "555.666.777-88", "luke", "")
        ]

# Configuração inicial do tema
ctk.set_appearance_mode("dark")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gerenciamento de Funcionários")
        self.geometry("1050x650")
        self.configure(fg_color="#1a2b3c") # Tom azul escuro de fundo

        # --- CONTAINER PRINCIPAL ---
        self.main_container = ctk.CTkFrame(self, fg_color="#243b53", corner_radius=25)
        self.main_container.pack(padx=40, pady=40, fill="both", expand=True)

        # --- TOPO: Barra de Pesquisa e Botão Cadastrar ---
        self.top_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.top_frame.pack(fill="x", padx=35, pady=(35, 25))

        # Campo de Pesquisa
        self.search_entry = ctk.CTkEntry(
            self.top_frame, 
            placeholder_text="Pesquisar CPF", 
            width=400, 
            height=42,
            corner_radius=20,
            fg_color="#1a2b3c",
            border_color="#486581",
            placeholder_text_color="#9fb3c8"
        )
        self.search_entry.pack(side="left")

        # Botão Cadastrar Funcionário
        self.btn_cadastrar = ctk.CTkButton(
            self.top_frame, 
            text="Cadastrar funcionário +", 
            height=42,
            corner_radius=20,
            fg_color="transparent",
            border_width=1,
            border_color="#ffffff",
            text_color="#ffffff",
            hover_color="#486581",
            font=("Arial", 13, "bold")
        )
        self.btn_cadastrar.pack(side="right")

        # --- TABELA DE FUNCIONÁRIOS ---
        self.table_frame = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent")
        self.table_frame.pack(fill="both", expand=True, padx=35, pady=(0, 35))

        # Frame interno estável para gerenciar o Grid
        self.grid_container = ctk.CTkFrame(self.table_frame, fg_color="transparent")
        self.grid_container.pack(fill="both", expand=True)

        # Força as colunas a se distribuírem igualmente dentro do container do grid
        for i in range(5):
            self.grid_container.grid_columnconfigure(i, weight=1)
        self.grid_container.grid_columnconfigure(5, weight=0) # Coluna de ações fixa na direita

        # Cabeçalho das Colunas
        headers = ["Nome", "E-mail", "Telefone", "CPF", "Usuário", ""]
        for col_idx, header in enumerate(headers):
            if header: 
                lbl = ctk.CTkLabel(
                    self.grid_container, 
                    text=header, 
                    font=("Arial", 14, "bold"), 
                    text_color="#ffffff"
                )
                lbl.grid(row=0, column=col_idx, pady=(10, 20), padx=10, sticky="w")

        # Busca os dados reais vindos do banco de dados (funcionarios_dao)
        dados_reais = listar_todos()

        # Renderizar as linhas da tabela dinamicamente
        for row_idx, data in enumerate(dados_reais, start=1):
            # Dados textuais da tupla/lista vinda do banco
            for col_idx, text in enumerate(data[:5]): # Limita a 5 colunas de texto (Nome até Usuário)
                lbl = ctk.CTkLabel(
                    self.grid_container, 
                    text=str(text), 
                    font=("Arial", 14, "bold"), 
                    text_color="#ffffff"
                )
                lbl.grid(row=row_idx, column=col_idx, pady=18, padx=10, sticky="w")

            # Coluna de Ações (Botões Circulares localizados na coluna 5)
            actions_frame = ctk.CTkFrame(self.grid_container, fg_color="transparent")
            actions_frame.grid(row=row_idx, column=5, pady=18, padx=(10, 20), sticky="e")

            # Botão Editar (Lápis)
            btn_edit = ctk.CTkButton(
                actions_frame, text="✏️", width=34, height=34, corner_radius=17,
                fg_color="#bcccdc", text_color="#102a43", hover_color="#9fb3c8",
                font=("Arial", 12)
            )
            btn_edit.pack(side="left", padx=6)

            # Botão Avançar (Seta)
            btn_next = ctk.CTkButton(
                actions_frame, text="➔", width=34, height=34, corner_radius=17,
                fg_color="#bcccdc", text_color="#102a43", hover_color="#9fb3c8",
                font=("Arial", 12)
            )
            btn_next.pack(side="left", padx=6)

if __name__ == "__main__":
    app = App()
    app.mainloop()