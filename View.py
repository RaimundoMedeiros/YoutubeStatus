import tkinter.ttk as ttk
import tkinter as tk

class View(ttk.LabelFrame):
    '''
    Widget container com tabela
    (tk.Treeview) e barras de rolagem.
    '''
    
    def __init__(self, mestre, texto, n_cols):
        super().__init__(text=texto)
        self.treeviewframe = tk.LabelFrame(mestre,text = 'Tabela de vídeos')
        self.abrirarquivo = tk.LabelFrame(mestre, padx=10, pady=10)
        self.buscar = tk.LabelFrame(mestre, padx=10, pady=10)
        self.graficosframe = tk.LabelFrame(mestre, padx=10, pady=10)
        style = ttk.Style()
        style.theme_use('default')

        self.nomes_colunas = [f'col{i}' for i in range(n_cols)]
        self.tv = ttk.Treeview(self.treeviewframe, columns=self.nomes_colunas, show='headings')

        # Barra de rolagem vertical
        sb_y = ttk.Scrollbar(self.treeviewframe, orient=tk.VERTICAL, command=self.tv.yview)
        self.tv.configure(yscroll=sb_y.set)

        # Barra de rolagem horizontal
        sb_x = ttk.Scrollbar(self.treeviewframe, orient=tk.HORIZONTAL, command=self.tv.xview)
        self.tv.configure(xscroll=sb_x.set)

        self.tv.grid(row=0, column=0, sticky='nswe')
        sb_y.grid(row=0, column=1, sticky='ns')
        sb_x.grid(row=1, column=0, sticky='we')

        self.columnconfigure(0, weight=1)
        self.headings = ['Canal', 'Título', 'Categoria', 'Visualizações', 'Comentários', 'Likes','Dislikes', 'Publicado']
   
        self.cabecalho()
        self.larguras = [(100, 200), (100, 200), (100, 100), (100, 100), (100, 80), (100, 70),(100, 70), (100, 200)]
        self.largura_colunas()

        
        self.labelDynTotal = LabelDinamico(self.treeviewframe, 'Total de Vídeos:')
        self.labelDynTotal.grid(row=2, column=0, sticky='w', pady = 5)

       
       
        #ABRIR ARQUIVO#
        self.AbrirArquivobtn = ttk.Button(self.abrirarquivo, text='Abrir Arquivo')
        self.AbrirArquivobtn.grid(row=0, column=0,pady = 5)
        self.AbrirArquivoLabel = ttk.Label(self.abrirarquivo, text='Caminho do Arquivo:')
        self.AbrirArquivoLabel.grid(row=1, column=0, sticky='w', pady = 5)
        self.labelDynArquivo = LabelDinamico(self.abrirarquivo, '')
        self.labelDynArquivo.grid(row=1, column=1, sticky='w', pady = 5)
        
        

        #BUSCAR#
        self.BuscarLabelText = ttk.Label(self.buscar, text='Buscar vídeos por:')
        self.BuscarLabelText.grid(row=0, column=0, sticky='w', pady = 5)
        self.BuscarLabelTextResposta = ttk.Label(self.buscar, text='')
        self.BuscarLabelTextResposta.grid(row=0, column=1, sticky='w', pady = 5)
        
        
        
        #Radio Buttons
        self.RadioTitulo = ttk.Radiobutton(self.buscar, text='')
        self.RadioTitulo.grid(row=1, column=0, sticky='w', pady = 5)
        self.BuscarLabelTextResposta.grid(row=0, column=1, sticky='w', pady = 5)
        self.RadioCanal = ttk.Radiobutton(self.buscar, text='')
        self.RadioCanal.grid(row=2, column=0, sticky='w', pady = 5)
        self.RadioPeriodo = ttk.Radiobutton(self.buscar, text='')
        self.RadioPeriodo.grid(row=3, column=0, sticky='w', pady = 5)
        self.RadioCategoria = ttk.Radiobutton(self.buscar, text='')
        self.RadioCategoria.grid(row=4, column=0, sticky='w', pady = 5)
        ##/Radio Buttons
        
        
        
        self.BuscarTitLabel = ttk.Label(self.buscar, text='Título')
        self.BuscarTitLabel.grid(row=1, column=0, sticky='n', pady=5)
        self.BuscarTitEntry = ttk.Entry(self.buscar, width=21)
        self.BuscarTitEntry.grid(row=1, column=1, sticky='w', pady = 5)
        self.BuscarCanalLabel = ttk.Label(self.buscar, text='Canal')
        self.BuscarCanalLabel.grid(row=2, column=0, sticky='n', pady=5)
        self.BuscarCanalEntry = ttk.Entry(self.buscar, width=21)
        self.BuscarCanalEntry.grid(row=2, column=1, sticky='w', pady = 5)
        self.BuscarPeriodoLabel = ttk.Label(self.buscar, text='Período')
        self.BuscarPeriodoLabel.grid(row=3, column=0, sticky='n', pady=5)
        self.BuscarPeriodoEntryInicio = ttk.Entry(self.buscar, width=10)
        self.BuscarPeriodoEntryInicio.grid(row=3, column=1, sticky='w', pady = 5)
        self.BuscarPeriodoEntryFim = ttk.Entry(self.buscar, width=10)
        self.BuscarPeriodoEntryFim.place(x=164, y=90)
        self.BuscarLabelExemplo = ttk.Label(self.buscar, text='(Início, Fim)(YYYY-MM-DD)')
        self.BuscarLabelExemplo.grid(row=3, column=2, sticky='n', pady=5)
        self.BuscarCatLabel = ttk.Label(self.buscar, text='Categoria')
        self.BuscarCatLabel.grid(row=4, column=0, sticky='n', pady=5)
        self.BuscarCatEntry = ttk.Combobox(self.buscar, width=20, state='readonly')
        self.BuscarCatEntry.grid(row=4, column=1, sticky='w', pady = 5)
        self.BuscarBtn = ttk.Button(self.buscar, text='Buscar')
        self.BuscarBtn.grid(row=5, column=1, columnspan=2, sticky='w', pady=5)
        self.LimparBtn = ttk.Button(self.buscar, text='Limpar Campos')
        self.LimparBtn.grid(row=5, column=2, columnspan=2, sticky='w', pady=5)
        
        #GRAFICOS
        self.selecaoGrafico = ttk.Label(self.graficosframe, text='Selecione um Gráfico para exibir:')
        self.selecaoGrafico.grid(row=0, column=0, sticky='w', pady = 5)
        self.RadioButtonsGraficoView = ttk.Radiobutton(self.graficosframe, text='Mais Views')
        self.RadioButtonsGraficoView.grid(row=1, column=0, sticky='w', pady = 5)
        self.RadioButtonsGraficoLike = ttk.Radiobutton(self.graficosframe, text='Mais Likes')
        self.RadioButtonsGraficoLike.grid(row=2, column=0, sticky='w', pady = 5)
        self.RadioButtonsGraficoComent = ttk.Radiobutton(self.graficosframe, text='Mais Comentários')
        self.RadioButtonsGraficoComent.grid(row=3, column=0, sticky='w', pady = 5)
        self.quantidadeLabel = ttk.Label(self.graficosframe, text='Quantidade de Vídeos no Gráfico:')
        self.quantidadeLabel.grid(row=4, column=0, sticky='w', pady = 5)
        self.quantidadeEntry = ttk.Entry(self.graficosframe, width=5)
        self.quantidadeEntry.grid(row=4, column=1, sticky='w', pady = 5,padx=5)
        self.AbrirGraficoBtn = ttk.Button(self.graficosframe, text='Abrir Gráfico')
        self.AbrirGraficoBtn.grid(row=5, column=0, sticky='w', pady = 5)
        




        self.abrirarquivo.pack()
        self.buscar.pack(fill=tk.BOTH)
        self.treeviewframe.pack()
        self.graficosframe.pack()


    



    def largura_colunas(self):
        for i, conf_coluna in enumerate(self.larguras):
            larg, larg_min = conf_coluna
            self.tv.column(f'col{i}', width=larg, minwidth=larg_min, anchor='center')
        self.tv.column(1, anchor='w')

    def cabecalho(self):
        for i, tit in enumerate(self.headings):
            self.tv.heading(f'col{i}', text=tit)
            
class LabelDinamico(tk.Label):
    def __init__(self, root, texto_inicial):
        self._texto = tk.StringVar() # StringVar encapsulada
        self._texto.set(texto_inicial) # texto_inicial deve ser str Python
        super().__init__(root, textvariable=self._texto)
        
    @property
    def texto(self):
        return self._texto.get() # retorna str Python
    
    @texto.setter
    def texto(self, t):
        self._texto.set(t) # t deve ser str Python

            