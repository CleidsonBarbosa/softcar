import customtkinter as ctk

# Configuração inicial da janela
ctk.set_appearance_mode("dark")  # Modo escuro
ctk.set_default_color_theme("blue")  # Tema azul padrão

class SoftCarApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Soft Car - Listar Serviço")
        self.geometry("1000x600")
        self.configure(fg_color="#1a2b3c")  # Fundo escuro levemente azulado baseado na imagem

        # Configurar grid principal (Coluna 0: Menu, Coluna 1: Conteúdo)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=4)
        self.grid_rowconfigure(0, weight=1)

        self.criar_menu_lateral()
        self.criar_painel_central()

    def criar_menu_lateral(self):
        # Frame do Menu Lateral
        menu_frame = ctk.CTkFrame(self, fg_color="#243b55", corner_radius=0)
        menu_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        
        # Logo / Título do App
        logo_label = ctk.CTkLabel(menu_frame, text="SOFT CAR", font=ctk.CTkFont(size=22, weight="bold"), text_color="white")
        logo_label.pack(pady=(30, 40))

        # Botões do Menu Lateral
        opcoes_menu = ["Cliente", "Serviços", "Funcionários", "Materiais", "Relatórios"]
        for opcao in opcoes_menu:
            btn = ctk.CTkButton(
                menu_frame, 
                text=opcao, 
                fg_color="transparent", 
                text_color="white",
                anchor="w", 
                font=ctk.CTkFont(size=15),
                hover_color="#2c4a6f",
                height=40
            )
            # Dica: Na versão final, você pode adicionar o argumento `image=` para colocar os ícones
            btn.pack(fill="x", padx=20, pady=5)

    def criar_painel_central(self):
        # Container do lado direito (onde ficam a busca, botão de cadastrar e a tabela)
        conteudo_frame = ctk.CTkFrame(self, fg_color="transparent")
        conteudo_frame.grid(row=0, column=1, sticky="nsew", padx=30, pady=20)
        
        # --- LINHA SUPERIOR: Busca e Cadastrar ---
        topo_frame = ctk.CTkFrame(conteudo_frame, fg_color="transparent")
        topo_frame.pack(fill="x", pady=(0, 20))

        campo_busca = ctk.CTkEntry(
            topo_frame, 
            placeholder_text="Pesquisar Serviço 🔍", 
            width=300, 
            height=35,
            corner_radius=15,
            fg_color="#1f334d",
            border_color="#34495e"
        )
        campo_busca.pack(side="left")

        btn_cadastrar = ctk.CTkButton(
            topo_frame, 
            text="Cadastrar serviço +", 
            width=150, 
            height=35,
            corner_radius=15,
            fg_color="#1f334d",
            hover_color="#2c4a6f",
            border_width=1,
            border_color="#34495e"
        )
        btn_cadastrar.pack(side="right")

        # --- TABELA DE SERVIÇOS (Card Arredondado Translucido) ---
        tabela_card = ctk.CTkFrame(conteudo_frame, fg_color="#2a3d54", corner_radius=20)
        tabela_card.pack(fill="both", expand=True, pady=(0, 10))
        
        # Configurar colunas dentro da tabela
        # Colunas: Nome (0), Tipo (1), Preço (2), Descrição (3), Checkbox (4), Editar (5), Avançar (6)
        tabela_card.grid_columnconfigure((0, 1, 2, 3), weight=2)
        tabela_card.grid_columnconfigure((4, 5, 6), weight=1)

        # Cabeçalho da Tabela
        colunas = ["Nome", "Tipo", "Preço", "Descrição"]
        for i, col_nome in enumerate(colunas):
            lbl = ctk.CTkLabel(tabela_card, text=col_nome, font=ctk.CTkFont(size=14, weight="bold"), text_color="white")
            lbl.grid(row=0, column=i, padx=15, pady=15, sticky="w")

        # Simulação de linhas de dados (baseado na sua imagem que repete as linhas)
        for row_idx in range(1, 7):
            # Textos base
            ctk.CTkLabel(tabela_card, text="Nome", text_color="#b0c4de").grid(row=row_idx, column=0, padx=15, pady=10, sticky="w")
            ctk.CTkLabel(tabela_card, text="Tipo", text_color="#b0c4de").grid(row=row_idx, column=1, padx=15, pady=10, sticky="w")
            ctk.CTkLabel(tabela_card, text="Preço", text_color="#b0c4de").grid(row=row_idx, column=2, padx=15, pady=10, sticky="w")
            ctk.CTkLabel(tabela_card, text="Descrição", text_color="#b0c4de").grid(row=row_idx, column=3, padx=15, pady=10, sticky="w")
            
            # Checkbox de seleção
            chk = ctk.CTkCheckBox(tabela_card, text="", width=20, checkbox_width=20, checkbox_height=20)
            chk.grid(row=row_idx, column=4, padx=5, pady=10)

            # Botão Editar (Ícone de Lápis simulado por "✏️")
            btn_edit = ctk.CTkButton(tabela_card, text="✏️", width=30, height=30, corner_radius=15, fg_color="#7f8c8d", hover_color="#95a5a6")
            btn_edit.grid(row=row_idx, column=5, padx=5, pady=10)

            # Botão Avançar/Detalhes (Seta simulada por "➔")
            btn_next = ctk.CTkButton(tabela_card, text="➔", width=30, height=30, corner_radius=15, fg_color="#7f8c8d", hover_color="#95a5a6")
            btn_next.grid(row=row_idx, column=6, padx=5, pady=10)

        # --- LINHA DE BOTÕES INFERIORES (Orçamento e Salvar) ---
        botoes_inferiores_frame = ctk.CTkFrame(conteudo_frame, fg_color="transparent")
        botoes_inferiores_frame.pack(fill="x", side="bottom", pady=10)

        btn_orcamento = ctk.CTkButton(
            botoes_inferiores_frame, 
            text="Orçamento  R$", 
            fg_color="#a0aab5", 
            text_color="black", 
            hover_color="#bdc3c7",
            height=35,
            corner_radius=15,
            font=ctk.CTkFont(weight="bold")
        )
        btn_orcamento.pack(side="left", padx=(100, 0))

        btn_salvar = ctk.CTkButton(
            botoes_inferiores_frame, 
            text="Salvar  💾", 
            fg_color="#a0aab5", 
            text_color="black", 
            hover_color="#bdc3c7",
            height=35,
            corner_radius=15,
            font=ctk.CTkFont(weight="bold")
        )
        btn_salvar.pack(side="right", padx=(0, 100))

if __name__ == "__main__":
    app = SoftCarApp()
    app.mainloop()