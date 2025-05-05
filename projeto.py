import tkinter as tk
import tkinter.messagebox as mb
from tkinter import filedialog

from traitlets import Int
import Model
import View

class ErroBase(Exception):
    pass

class ErroBuscaVazia(ErroBase):
    pass
class ErroEntryVazia(ErroBase):
    pass
class ErroValuePeriodo(ErroBase):
    pass

class ErroBuscaSemResultado(ErroBase):
    pass

class ErroQuantidadeGrafico(ErroBase):
    pass

class ErroArquivo(ErroBase):
    pass

class Controller():
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.caminhoArquivo = None
        self.bd = None
        self.buscaTitulo = tk.StringVar()
        self.buscaCanal = tk.StringVar()
        self.buscaPeriodoInicio = tk.StringVar()
        self.buscaPeriodoFim = tk.StringVar()
        self.buscaCategoria = tk.StringVar()
        self.RadioButtonBusca = tk.StringVar()
        self.RadioButtonGrafico = tk.StringVar()
        self.quantidadeGrafico = tk.IntVar()
        self.buscaSelecionada = None
        self.buscaGrafico = None
        self._configura_gui()
    
    def _configura_gui(self):
        self.view.AbrirArquivobtn['command'] = self.abrir_arquivo
        self.view.BuscarBtn['command'] = self.buscar 
        self.view.BuscarTitEntry['textvariable'] = self.buscaTitulo
        self.view.BuscarCanalEntry['textvariable'] = self.buscaCanal
        self.view.BuscarPeriodoEntryInicio['textvariable'] = self.buscaPeriodoInicio
        self.view.BuscarPeriodoEntryFim['textvariable'] = self.buscaPeriodoFim
        self.view.BuscarCatEntry['textvariable'] = self.buscaCategoria
        self.view.quantidadeEntry['textvariable'] = self.quantidadeGrafico
        
        
        #RadioButtonBusca
        self.view.RadioTitulo['variable'] = self.RadioButtonBusca
        self.view.RadioTitulo['value'] = 'Título'
        self.view.RadioTitulo['command'] = lambda: self.selecao(self.RadioButtonBusca.get())
        self.view.RadioCanal['variable'] = self.RadioButtonBusca
        self.view.RadioCanal['value'] = 'Canal'
        self.view.RadioCanal['command'] = lambda: self.selecao(self.RadioButtonBusca.get())
        self.view.RadioPeriodo['variable'] = self.RadioButtonBusca
        self.view.RadioPeriodo['value'] = 'Período'
        self.view.RadioPeriodo['command'] = lambda: self.selecao(self.RadioButtonBusca.get())
        self.view.RadioCategoria['variable'] = self.RadioButtonBusca
        self.view.RadioCategoria['value'] = 'Categoria'
        self.view.RadioCategoria['command'] = lambda: self.selecao(self.RadioButtonBusca.get())
        
        #RadioButtonGraficos
        self.view.RadioButtonsGraficoView['variable'] = self.RadioButtonGrafico
        self.view.RadioButtonsGraficoView['value'] = 'Views'
        self.view.RadioButtonsGraficoView['command'] = lambda: self.selecaoGrafico(self.RadioButtonGrafico.get())
        self.view.RadioButtonsGraficoLike['variable'] = self.RadioButtonGrafico
        self.view.RadioButtonsGraficoLike['value'] = 'Likes'
        self.view.RadioButtonsGraficoLike['command'] = lambda: self.selecaoGrafico(self.RadioButtonGrafico.get())
        self.view.RadioButtonsGraficoComent['variable'] = self.RadioButtonGrafico
        self.view.RadioButtonsGraficoComent['value'] = 'Comentários'
        self.view.RadioButtonsGraficoComent['command'] = lambda: self.selecaoGrafico(self.RadioButtonGrafico.get())
        
        #GraficosBuscabtn
        self.view.AbrirGraficoBtn['command'] = self.buscarGrafico
        
        
        self.view.LimparBtn['command'] = self.limparcampos
    
    def abrir_arquivo(self):
        self.caminhoArquivo = filedialog.askopenfilename(initialdir='/', title= 'Selecionar Arquivo CSV', filetypes=(('csv files', '*.csv'), ('all files', '*.*')))
        self.view.labelDynArquivo.texto = self.caminhoArquivo
        self.carrega_dados()
    def carrega_dados(self):
         
        self.bd = self.model.BancoDadosYT(self.caminhoArquivo)
        self.view.BuscarCatEntry['values'] = self.bd.categorias
        self.geraDados(self.bd.todos())
    def insere_linha(self, linha):
        id_linha = self.view.tv.insert('', tk.END, values=linha)

            
    #BUSCAS FRAME
    def buscar(self):
        try:
            if self.buscaSelecionada == 'Título':
                try:
                    self.buscarTitulo()
                except ErroEntryVazia as err:
                    mb.showerror('Busca', str(err))
            elif self.buscaSelecionada == 'Canal':
                try:
                    self.buscarCanal()
                except ErroEntryVazia as err:
                    mb.showerror('Busca', str(err))
            elif self.buscaSelecionada == 'Período':
                try:
                    self.buscarPeriodo()
                except ErroEntryVazia as err:
                    mb.showerror('Busca', str(err))
                except ValueError as err:
                    mb.showerror('Busca', str(err))
            elif self.buscaSelecionada == 'Categoria':
                try:
                    self.buscarCategoria()
                except ErroEntryVazia as err:
                    mb.showerror('Busca', str(err))
                else:
                    mb.showinfo('Busca', 'Busca Realizada com Sucesso')
            self.erroArquivo()
            self.buscaVazia(self.buscaSelecionada)
        except ErroBuscaVazia as err:
            mb.showerror('Busca', str(err))
        except ErroArquivo as err:
            mb.showerror('Busca', str(err))


    def buscarTitulo(self):
        tit = self.buscaTitulo.get()
        self.EntryVazia(tit)
        self.limpa()
        try:
            param = self.bd.busca_por_titulo(tit)
            self.geraDados(param)
            self.buscaSemResultado(param)
        except ErroBuscaSemResultado as err:
            mb.showwarning('Busca', str(err))
        else:
            mb.showinfo('Busca', 'Busca Realizada com sucesso!')

    def buscarCanal(self):
        canal = self.buscaCanal.get()
        self.EntryVazia(canal)
        self.limpa()
        try:
            param = self.bd.busca_por_canal(canal)
            self.geraDados(param)
            self.buscaSemResultado(param)
        except ErroBuscaSemResultado as err:
            mb.showwarning('Busca', str(err))
        else:
            mb.showinfo('Busca', 'Busca Realizada com sucesso!')

    def buscarPeriodo(self):
        inicio = self.buscaPeriodoInicio.get()
        fim = self.buscaPeriodoFim.get()
        self.EntryVaziaPeriodo(inicio,fim)
        self.ValueErrorPeriodo()
        self.limpa()
        try:
            param = self.bd.busca_por_periodo(inicio,fim)
            self.geraDados(param)
            self.buscaSemResultado(param)
        except ErroBuscaSemResultado as err:
            mb.showwarning('Busca', str(err))
        else:
            mb.showinfo('Busca', 'Busca Realizada com sucesso!')

    def buscarCategoria(self):
        categoria = self.buscaCategoria.get()
        self.EntryVazia(categoria)
        self.limpa()
        self.geraDados(self.bd.busca_por_categoria(categoria))
        
    ##GRAFICOS FRAME##
    def buscarGrafico(self):
        try:
            if self.buscaGrafico == 'Views':
                self.buscarGraficoViews()
            elif self.buscaGrafico == 'Likes':
                self.buscarGraficoLikes()
            elif self.buscaGrafico == 'Comentários':
                self.buscarGraficoComentarios()
            self.buscaVazia(self.buscaGrafico)
            self.erroQuantidadeGrafico(self.quantidadeGrafico)
        except ErroBuscaVazia:
            mb.showerror('Gráfico', 'Nenhum tipo de Gráfico Selecionado')
        except tk.TclError as err:
            mb.showerror('Gráfico', 'Digite um valor inteiro maior que 0')
    def buscarGraficoViews(self):
        self.bd.mostra_mais_assistidos(self.quantidadeGrafico.get())
    def buscarGraficoLikes(self):
        self.bd.mostra_mais_likes(self.quantidadeGrafico.get())
    def buscarGraficoComentarios(self):
        self.bd.mostra_mais_comentarios(self.quantidadeGrafico.get())


    ##MANUTENÇÃO##
    def limpa(self):
        for linha in self.view.tv.get_children():
            self.view.tv.delete(linha)

    def limparcampos(self):
        self.view.BuscarTitEntry.delete(0, tk.END)
        self.view.BuscarCanalEntry.delete(0, tk.END)
        self.view.BuscarPeriodoEntryInicio.delete(0, tk.END)
        self.view.BuscarPeriodoEntryFim.delete(0, tk.END)
        self.view.BuscarCatEntry.set('')
        self.RadioButtonBusca.set(None)
        self.RadioButtonGrafico.set(None)
        self.selecao('')

    def totalvideos(self, busca):
        self.view.labelDynTotal.texto = f'Total de Vídeos: {busca}'

    def geraDados(self, funcao):
        for i in funcao:
            dados = (i.canal, i.titulo, i.categoria, i.cont_views,i.cont_comentarios, i.likes,i.dislikes, i.dt_publicacao)
            self.insere_linha(dados)
            self.totalvideos(len(funcao))

    def selecao(self, texto):
        self.view.BuscarLabelTextResposta['text'] = texto
        self.buscaSelecionada = texto

    def selecaoGrafico(self, texto):
        self.buscaGrafico = texto

    def buscaVazia(self, param):
        if not param:
            raise ErroBuscaVazia('Nenhum Tipo de Busca Selecionada')

    def EntryVazia(self, parametro):
        if not parametro:
            raise ErroEntryVazia(f'Campo de {self.buscaSelecionada} Selecionado Vazio')

    def EntryVaziaPeriodo(self,inicio,fim):
        if not inicio or not fim:
            raise ErroEntryVazia('Período Vazio')

    def ValueErrorPeriodo(self):
        if ValueError == True:
            raise ErroValuePeriodo('Período Inválido')

    def buscaSemResultado(self, busca):
        if busca == []:
            self.totalvideos(0)
            raise ErroBuscaSemResultado('Nenhum Resultado Encontrado')
    def erroArquivo(self):
        if self.caminhoArquivo == None:
            raise ErroArquivo('Nenhum Arquivo Selecionado')

        

        
        




            
def main():
    root = tk.Tk()
    viewconf = View.View(root, 'Minha Tabela', 8) 
    model = Model
    app = Controller(viewconf, model)
    
    root.mainloop()
    
if __name__ == '__main__':
    main()