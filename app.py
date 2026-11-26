"""Servidor local do laboratório. Apenas biblioteca padrão do Python."""
import argparse
import json
import mimetypes
import secrets
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit, parse_qs

from vigia.laboratorio import analisar
from vigia.operacao import codigo_v3 as codigo_inicial
from vigia.central import Central as Laboratorio
from vigia.modelo import ErroVigia

RAIZ = Path(__file__).resolve().parent


def iniciar(porta=8765, dados=None, abrir=True):
    destino = Path(dados) if dados else RAIZ / 'dados' / 'laboratorio.sqlite3'
    destino.parent.mkdir(parents=True, exist_ok=True)
    lab = Laboratorio(destino)
    lock = threading.RLock()
    stop = threading.Event()
    token = secrets.token_urlsafe(24)

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, formato, *args):
            pass

        def responder(self, valor, status=200):
            conteudo = json.dumps(valor, ensure_ascii=False, allow_nan=False).encode('utf-8')
            self.send_response(status)
            self.send_header('Content-Type','application/json; charset=utf-8')
            self.send_header('Cache-Control','no-store')
            self.send_header('X-Content-Type-Options','nosniff')
            self.send_header('Content-Length',str(len(conteudo)))
            self.end_headers()
            self.wfile.write(conteudo)

        def host_valido(self):
            return self.headers.get('Host') in (f'127.0.0.1:{porta}', f'localhost:{porta}')

        def do_GET(self):
            if not self.host_valido():
                return self.responder({'erro':'Host não permitido.'},403)
            caminho=urlsplit(self.path)
            with lock:
                if caminho.path=='/api/estado':
                    return self.responder(lab.snapshot())
                if caminho.path=='/api/config':
                    return self.responder(dict(codigo=lab.s['codigo'], versao=lab.s['versao'], exemplo=codigo_inicial(), token=token, analise=lab.analise))
                if caminho.path=='/api/sugestoes':
                    try:
                        aid=int(parse_qs(caminho.query).get('id',['0'])[0])
                        return self.responder(dict(itens=lab.sugestoes(lab.alerta(aid))))
                    except ValueError as e:
                        return self.responder({'erro':str(e)},400)
            arquivos={'/':'index.html','/style.css':'style.css','/app.js':'app.js','/central.js':'central.js','/boot.js':'boot.js','/central.css':'central.css'}
            nome=arquivos.get(caminho.path)
            if not nome:
                return self.responder({'erro':'Não encontrado'},404)
            conteudo=(RAIZ/'web'/nome).read_bytes()
            self.send_response(200)
            self.send_header('Content-Type',mimetypes.guess_type(nome)[0]+'; charset=utf-8')
            self.send_header('Content-Length',str(len(conteudo)))
            self.send_header('Cache-Control','no-store')
            self.send_header('X-Content-Type-Options','nosniff')
            self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; object-src 'none'; frame-ancestors 'none'")
            self.end_headers()
            self.wfile.write(conteudo)

        def do_POST(self):
            if not self.host_valido() or self.headers.get('X-Vigia-Token') != token:
                return self.responder({'erro':'Recarregue a página para iniciar uma sessão local.'},403)
            try:
                tamanho=int(self.headers.get('Content-Length','0'))
                if not 0<tamanho<=300000:
                    raise ValueError('Corpo da requisição inválido.')
                d=json.loads(self.rfile.read(tamanho))
                if not isinstance(d,dict):
                    raise ValueError('Requisição deve ser um objeto.')
                with lock:
                    if self.path=='/api/validar':
                        resultado=analisar(d.get('codigo'))
                    elif self.path=='/api/aplicar':
                        resultado=lab.aplicar(d.get('codigo'))
                    elif self.path=='/api/estresse':
                        lab.estressar(d.get('equipamento'),d.get('metrica'),d.get('intensidade'),d.get('duracao'))
                        resultado={'ok':True}
                    elif self.path=='/api/parar':
                        lab.parar(d.get('equipamento'),d.get('metrica','todas'),bool(d.get('limpar',False)))
                        resultado={'ok':True}
                    elif self.path=='/api/benchmark':
                        lab.benchmark(d.get('equipamento'))
                        resultado={'ok':True}
                    elif self.path=='/api/operar':
                        resultado=lab.operar(d)
                    elif self.path=='/api/alerta':
                        resultado=lab.tratar(d.get('id'),d.get('acao'),d)
                    else:
                        return self.responder({'erro':'Rota não encontrada'},404)
                    if self.path!='/api/validar':
                        lab.salvar()
                    return self.responder(resultado)
            except ErroVigia as e:
                return self.responder(dict(erro=str(e), fase=e.fase, linha=e.token.linha if e.token else None, coluna=e.token.coluna if e.token else None),400)
            except (ValueError, TypeError, KeyError, AttributeError) as e:
                return self.responder({'erro':str(e)},400)

    try:
        servidor=ThreadingHTTPServer(('127.0.0.1',porta),Handler)
    except OSError:
        lab.fechar()
        raise SystemExit(f'Porta {porta} ocupada. Feche a outra instância ou use: python app.py --porta 8766')

    def motor():
        anterior=time.monotonic()
        contador=0
        while not stop.wait(.5):
            atual=time.monotonic()
            with lock:
                lab.passo(atual-anterior, agora=time.time())
                contador+=1
                if contador%4==0:
                    lab.salvar()
            anterior=atual

    thread=threading.Thread(target=motor,daemon=True)
    thread.start()
    url=f'http://127.0.0.1:{porta}'
    print(f'VigiaDSL 4 | operação simulada\nAbra: {url}\nMantenha este terminal aberto. Ctrl+C encerra e salva os dados.', flush=True)
    if abrir:
        webbrowser.open(url)
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print('\nSalvando e encerrando...')
    finally:
        stop.set()
        thread.join()
        servidor.server_close()
        lab.fechar()


if __name__=='__main__':
    cli=argparse.ArgumentParser(description='VigiaDSL Studio — laboratório local')
    cli.add_argument('--porta',type=int,default=8765)
    cli.add_argument('--dados',help='Arquivo SQLite separado (opcional)')
    cli.add_argument('--sem-navegador',action='store_true')
    args=cli.parse_args()
    iniciar(args.porta,args.dados,not args.sem_navegador)
