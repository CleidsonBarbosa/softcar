import tkinter as tk
import customtkinter as ctk

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

        # SOLUÇÃO DO ERRO: Criamos um frame interno estável para gerenciar o Grid perfeitamente
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

        # Dados fictícios idênticos à estrutura visual da imagem
        dados_ficticios = [
            ("Nome", "E-mail", "Telefone", "CPF", "Usuário"),
            ("Nome", "E-mail", "Telefone", "CPF", "Usuário"),
            ("Nome", "E-mail", "Telefone", "CPF", "Usuário"),
            ("Nome", "E-mail", "Telefone", "CPF", "Usuário"),
            ("Nome", "E-mail", "Telefone", "CPF", "Usuário"),
            ("Nome", "E-mail", "Telefone", "CPF", "Usuário"),
            ("Nome", "E-mail", "Telefone", "CPF", "Usuário"),
        ]

        # Renderizar as linhas da tabela
        for row_idx, data in enumerate(dados_ficticios, start=1):
            # Dados textuais
            for col_idx, text in enumerate(data):
                lbl = ctk.CTkLabel(
                    self.grid_container, 
                    text=text, 
                    font=("Arial", 14, "bold"), 
                    text_color="#ffffff"
                )
                lbl.grid(row=row_idx, column=col_idx, pady=18, padx=10, sticky="w")

            # Coluna de Ações (Botões Circulares)
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