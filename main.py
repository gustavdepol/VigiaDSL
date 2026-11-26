import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

from vigia.interpretador import executar
from vigia.lexer import tokenizar
from vigia.modelo import ErroVigia
from vigia.parser import Parser
from vigia.semantico import validar


def main():
    cli = argparse.ArgumentParser(description="VigiaDSL — monitoramento com medições simuladas")
    cli.add_argument("arquivo", type=Path, help="código .vigia")
    cli.add_argument("--dados", type=Path, help="medições em JSON; obrigatório para executar")
    cli.add_argument("--tokens", action="store_true", help="mostrar tokens")
    cli.add_argument("--ast", action="store_true", help="mostrar árvore sintática")
    cli.add_argument("--validar", action="store_true", help="validar sem executar ou ler medições")
    args = cli.parse_args()
    if not args.validar and args.dados is None:
        cli.error("informe --dados arquivo.json ou use --validar")
    try:
        tokens = tokenizar(args.arquivo.read_text(encoding="utf-8-sig"))
        if args.tokens:
            for token in tokens:
                print(f"{token.linha}:{token.coluna}\t{token.tipo}\t{token.valor!r}")
        programa = Parser(tokens).programa()
        if args.ast:
            arvore = [{"tipo": type(no).__name__, **asdict(no)} for no in programa]
            print(json.dumps(arvore, ensure_ascii=False, indent=2))
        simbolos = validar(programa)
        if args.validar:
            print(f"Programa válido. Equipamentos cadastrados: {len(simbolos)}.")
            return 0
        dados = json.loads(args.dados.read_text(encoding="utf-8-sig"))
        avisos = executar(programa, simbolos, dados)
        print("Modo simulado: avaliação única das medições do JSON.")
        for aviso in avisos:
            print(aviso)
        print(f"Avisos emitidos: {len(avisos)}.")
        return 0
    except (ErroVigia, OSError, ValueError) as erro:
        print(str(erro), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
