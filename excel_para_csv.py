"""
Script para converter arquivos Excel (.xlsx, .xls) para CSV
"""

import pandas as pd
import sys
import os
from pathlib import Path

def excel_para_csv(arquivo_excel, pasta_saida=None, todas_planilhas=True):
    """
    Converte um arquivo Excel para CSV.
    
    Parâmetros:
    -----------
    arquivo_excel : str
        Caminho para o arquivo Excel
    pasta_saida : str, opcional
        Pasta onde salvar os arquivos CSV. Se None, salva na mesma pasta do Excel
    todas_planilhas : bool
        Se True, converte todas as planilhas. Se False, converte apenas a primeira
    """
    
    # Verifica se o arquivo existe
    if not os.path.exists(arquivo_excel):
        print(f"[ERRO] Arquivo '{arquivo_excel}' nao encontrado!")
        return
    
    # Define a pasta de saída
    if pasta_saida is None:
        pasta_saida = os.path.dirname(arquivo_excel) or '.'
    
    # Cria a pasta de saída se não existir
    os.makedirs(pasta_saida, exist_ok=True)
    
    # Nome base do arquivo (sem extensão)
    nome_base = Path(arquivo_excel).stem
    
    try:
        # Lê o arquivo Excel
        print(f"Lendo arquivo: {arquivo_excel}")
        
        # Lê todas as planilhas
        excel_file = pd.ExcelFile(arquivo_excel)
        planilhas = excel_file.sheet_names
        
        print(f"Encontradas {len(planilhas)} planilha(s): {', '.join(planilhas)}")
        
        # Converte cada planilha
        planilhas_convertidas = []
        
        for planilha in planilhas:
            # Lê a planilha
            df = pd.read_excel(excel_file, sheet_name=planilha)
            
            # Define o nome do arquivo CSV
            if len(planilhas) == 1:
                # Se há apenas uma planilha, usa o nome base
                arquivo_csv = os.path.join(pasta_saida, f"{nome_base}.csv")
            else:
                # Se há múltiplas planilhas, inclui o nome da planilha
                nome_planilha_limpo = planilha.replace('/', '_').replace('\\', '_')
                arquivo_csv = os.path.join(pasta_saida, f"{nome_base}_{nome_planilha_limpo}.csv")
            
            # Salva como CSV
            df.to_csv(arquivo_csv, index=False, encoding='utf-8-sig')
            print(f"[OK] Convertido: {arquivo_csv} ({len(df)} linhas, {len(df.columns)} colunas)")
            planilhas_convertidas.append(arquivo_csv)
            
            # Se não quer todas as planilhas, para após a primeira
            if not todas_planilhas:
                break
        
        print(f"\nConversao concluida! {len(planilhas_convertidas)} arquivo(s) CSV criado(s).")
        return planilhas_convertidas
        
    except Exception as e:
        print(f"[ERRO] Erro ao converter arquivo: {str(e)}")
        return None


def main():
    """Função principal para uso via linha de comando"""
    
    if len(sys.argv) < 2:
        print("=" * 60)
        print("Conversor de Excel para CSV")
        print("=" * 60)
        print("\nUso:")
        print("  python excel_para_csv.py <arquivo_excel> [pasta_saida]")
        print("\nExemplos:")
        print("  python excel_para_csv.py dados.xlsx")
        print("  python excel_para_csv.py dados.xlsx csv_output")
        print("  python excel_para_csv.py dados.xlsx . --primeira")
        print("\nOpcoes:")
        print("  --primeira    : Converte apenas a primeira planilha")
        print("=" * 60)
        
        # Modo interativo
        arquivo = input("\nDigite o caminho do arquivo Excel: ").strip().strip('"')
        if not arquivo:
            print("[ERRO] Nenhum arquivo especificado.")
            return
        
        pasta_saida = input("Pasta de saida (Enter para mesma pasta do Excel): ").strip().strip('"')
        if not pasta_saida:
            pasta_saida = None
        
        todas_planilhas = input("Converter todas as planilhas? (S/n): ").strip().lower() != 'n'
        
        excel_para_csv(arquivo, pasta_saida, todas_planilhas)
    else:
        # Modo linha de comando
        arquivo_excel = sys.argv[1]
        pasta_saida = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else None
        todas_planilhas = '--primeira' not in sys.argv
        
        excel_para_csv(arquivo_excel, pasta_saida, todas_planilhas)


if __name__ == "__main__":
    main()
