import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class VideoYT:
    '''
    Representa um vídeo do Youtube.
    '''
    
    def __init__(self, dados):
        self._id_video = dados[0] #id_video
        self._titulo = dados[1] #titulo
        self._dt_publicacao = dados[2] #dt_publicacao
        self._id_canal = dados[3] #id_canal
        self._canal = dados[4] #canal
        self._dt_trending = dados[5] #dt_trending
        self._cont_views = dados[6] #cont_views
        self._likes = dados[7] #likes
        self._dislikes = dados[8] #dislikes
        self._cont_comentarios = dados[9] #cont_comentarios
        self._descricao = dados[10] #descricao
        self._categoria = dados[11] #categoria
    
    @property
    def id_video(self):
        '''
        Retorna identificador
        do vídeo no YT.
        '''
        return self._id_video

    @property
    def titulo(self):
        '''
        Retorna título
        do vídeo.
        '''
        return self._titulo

    @property
    def dt_publicacao(self):
        '''
        Retorna data de publicação
        do vídeo.
        '''
        return self._dt_publicacao

    @property
    def id_canal(self):
        '''
        Retorna identificado do canal
        do vídeo no YT.
        '''
        return self._id_canal

    @property
    def canal(self):
        '''
        Retorna nome do canal
        do vídeo.
        '''
        return self._canal

    @property
    def dt_trending(self):
        '''
        Retorna data de trending
        (tendência) do vídeo.
        '''
        return self._dt_trending

    @property
    def cont_views(self):
        '''
        Retorna total de visualizações
        do vídeo.
        '''
        return self._cont_views

    @property
    def likes(self):
        '''
        Retorna data de likes
        do vídeo.
        '''
        return self._likes

    @property
    def dislikes(self):
        '''
        Retorna data de dislikes
        do vídeo.
        '''
        return self._dislikes

    @property
    def cont_comentarios(self):
        '''
        Retorna total de comentários
        do vídeo.
        '''
        return self._cont_comentarios

    @property
    def descricao(self):
        '''
        Retorna descrição
        do vídeo.
        '''
        return self._descricao

    @property
    def categoria(self):
        '''
        Retorna categoria
        do vídeo.
        '''
        return self._categoria

    def __str__(self):
        s = f'Canal: {self.canal}\n'
        s += f'Título: {self.titulo}\n'
        s += f'Categoria: {self.categoria}\n'
        s += f'Visualizações: {self.cont_views}\n'
        s += f'Comentários: {self.cont_comentarios}\n'
        s += f'Likes: {self.likes}\n'
        s += f'Publicado em {self.dt_publicacao.day}/{self.dt_publicacao.month}/{self.dt_publicacao.year}\n'
        s += '----------------------------------------------'
        return s
    
    def __repr__(self):
        return f'VideoYT{self.id_video}'

class BancoDadosYT:
    '''
    Representa um Banco de Dados com
    sobre vídeos do Youtube BR.

    Tem a capacidade de realizar vários
    tipos de consultas. 

    (Abstrai o uso de um Pandas.Dataframe).
    '''
    
    def __init__(self, nome_arq=None):
        '''
        Inicializa banco de dados a partir
        de um arquivo .csv
        '''

        self._df = None # dataframe Pandas encapsulado
        self._nome = '' # nome do arquivo do Banco de Dados

        if nome_arq:
            self.inicializa(nome_arq)
    
    def inicializa(self, nome_arq):
        '''
        Carrega banco de dados do arquivo,
        deixando-o pronto para buscas.
        '''

        try:
            print(f'Abrindo arquivo {nome_arq}')
            self._nome = nome_arq
            self._df = pd.read_csv(nome_arq, lineterminator='\n')
            self._df= self._df[self._df['categoria'].notna()]
        except FileNotFoundError as err:
            print(err)
            raise err # levanta exc. novamente para ser tratada em outro módulo
        else:
            ## altera tipo da coluna
            self._df.dt_publicacao = pd.to_datetime(self._df.dt_publicacao)
            self._df.dt_trending = pd.to_datetime(self._df.dt_trending)

    def _df_para_lista(self, df):
        '''
        Converte Pandas.Dataframe para uma lista
        de tuplas (implementação com tempo de
        execução reduzido).
        Cada tupla na lista contém todos os
        dados de um vídeo, cada um em uma string:
        (id_video, titulo, dt_publicacao, ...
         categoria)
        '''
        
        res = [tup for tup in zip(df['id_video'], df['titulo'],
                                df['dt_publicacao'], df['id_canal'],
                                df['canal'], df['dt_trending'],
                                df['cont_views'], df['likes'],
                                df['dislikes'], df['cont_comentarios'],
                                df['descricao'], df['categoria'])]
        
        return res
    
    def _df_para_videos(self, df):
        '''
        Converte Pandas.Dataframe para uma lista
        de VideosYT.
        '''
        lista = self._df_para_lista(df)
        return [VideoYT(t) for t in lista]
        
    


    @property
    def nome(self):
        '''
        Retorna o nome
        do arquivo do 
        banco de dados.
        '''
        return self._nome

    @property
    def categorias(self):
        '''
        Retorna uma lista de strings
        contendo as categorias de vídeos
        no banco de dados.
        '''
        return list(self._df.categoria.unique())
    
    @property
    def total(self):
        '''
        Retorna a quantidade
        de vídeos no banco de dados.
        '''
        return len(self._df)

    def imprime_info(self):
        '''
        Imprime informações sobre o
        banco de dados.
        '''

        print(f'Arquivo: {self.nome}')
        print(f'Possui dados dos vídeos em tendência no Youtube BR')
        print(f'Total de vídeos: {self.total}')
        print(f'Período: {self._df.dt_publicacao.min()} até {self._df.dt_publicacao.max()}')
        print(f'Dados dos vídeos:')
        for c in self._df.columns.to_list():
            print(c, end=', ')
        print('\n')

    def todos(self):
        '''
        Retorna lista de VideosYT
        com dados de todo o Banco de Dados.
        '''
        return self._df_para_videos(self._df)
    #imprime um video
    def imprime_video(self, id_video):
        '''
        Imprime informações sobre um vídeo
        do Banco de Dados.
        '''
        print(self._df.loc[self._df['id_video'] == id_video])


    def busca_por_titulo(self, t):
        '''
        Retorna lista de VideosYT
        com resultados de busca por título.
        '''
        print(f'Busca por título: {t}')
        df = self._df[self._df.titulo.str.contains(t, case=False, na=False)]
        return self._df_para_videos(df)
    
    def busca_por_canal(self, c):
        '''
        Retorna lista de VideosYT
        com resultados de busca por canal.
        '''
        print(f'Busca por canal: {c}')
        df = self._df[self._df.canal.str.contains(c, case=False, na=False)]
        return self._df_para_videos(df)
    
    def busca_por_categoria(self, c):
        '''
        Retorna lista de VideosYT
        com resultados de busca por categoria.
        '''
        print(f'Busca por categoria: {c}')
        df = self._df[self._df.categoria.str.contains(c, case=False, na=False)]
        return self._df_para_videos(df)
    
    def busca_por_periodo(self, ini, fim):
        '''
        Retorna lista de VideosYT
        com resultados de busca por período.
        '''
        print(f'Busca por período: {ini}, {fim}')
        mascara = (self._df.dt_publicacao.dt.date >= pd.to_datetime(ini)) & (self._df.dt_publicacao.dt.date <= pd.to_datetime(fim))
        df = self._df[mascara]
        return self._df_para_videos(df)

    def mostra_mais_assistidos(self, n=10):
        '''
        Exibe gráfico de barras com
        os n vídeos mais assistidos.
        '''
        df_top_videos = self._df.sort_values(by=['cont_views'], ascending=False).head(n)
        grafico_barras(df_top_videos, 'titulo',
                                               'cont_views',
                                               'Título',
                                               'Views')

    def mostra_mais_likes(self, n=10):
        '''
        Exibe gráfico de barras com
        os n vídeos com mais likes.
        '''
        df_top_videos = self._df.sort_values(by=['likes'], ascending=False).head(n)
        grafico_barras(df_top_videos, 'titulo',
                                               'likes',
                                               'Título',
                                               'Likes')

    def mostra_mais_comentarios(self, n=10):
        '''
        Exibe gráfico de barras com
        os n vídeos com mais comentários.
        '''
        df_top_videos = self._df.sort_values(by=['cont_comentarios'], ascending=False).head(n)
        grafico_barras(df_top_videos, 'titulo',
                                               'cont_comentarios',
                                               'Título',
                                               'Comentários')
   

def grafico_barras(df, col_x, col_y, leg_x, leg_y):
    '''
    Mostra gráfico de barras
    de um dataframe Pandas.
    '''
    sns.catplot(data=df, x=col_x, y=col_y, kind='bar',
                ci=None, legend_out=False, aspect=2)

    plt.ylabel(leg_y)
    plt.xlabel(leg_x)
    plt.xticks(rotation=90)
    plt.ticklabel_format(style='plain', axis='y')
    
    plt.show(block=True)
        
def imprime_resultado(res):
    '''
    Função auxiliar para imprimir o resultado
    de uma busca no BancoDadosYT.
    '''
    for v in res:
        print(v)
