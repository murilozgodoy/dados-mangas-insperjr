"""
Análise do perfil do produto Aroma / Extrato Natural
Calcula porcentagens de tipo_cliente (B2B/B2C) e mercado_principal (Interno/Externo/Ambos)
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

COR_AROMA = '#2E7D32'  # Verde escuro

# Carregar dados
df = pd.read_csv('BASE_1_Manga_Produtos_TRATADA.csv')
produto_foco = 'Aroma / extrato natural'

# Filtrar apenas Aroma/Extrato Natural
aroma = df[df['produto'] == produto_foco].copy()

print("=" * 70)
print("ANÁLISE DE PERFIL: AROMA / EXTRATO NATURAL")
print("=" * 70)
print(f"\nTotal de registros: {len(aroma)}")
print()

# 1. Análise de Tipo de Cliente (B2B vs B2C)
print("-" * 70)
print("1. TIPO DE CLIENTE")
print("-" * 70)

tipo_cliente_counts = aroma['tipo_cliente'].value_counts()
tipo_cliente_pct = aroma['tipo_cliente'].value_counts(normalize=True) * 100

print("\nDistribuição:")
for tipo, count in tipo_cliente_counts.items():
    pct = tipo_cliente_pct[tipo]
    print(f"  {tipo}: {count} registros ({pct:.2f}%)")

# Resposta específica para B2B
if 'B2B' in tipo_cliente_counts.index:
    pct_b2b = tipo_cliente_pct['B2B']
    print(f"\n>>> {pct_b2b:.2f}% dos registros são B2B")
else:
    print("\n>>> Nenhum registro B2B encontrado")

# 2. Análise de Mercado Principal (Interno vs Externo vs Ambos)
print("\n" + "-" * 70)
print("2. MERCADO PRINCIPAL")
print("-" * 70)

mercado_counts = aroma['mercado_principal'].value_counts()
mercado_pct = aroma['mercado_principal'].value_counts(normalize=True) * 100

print("\nDistribuição:")
for mercado, count in mercado_counts.items():
    pct = mercado_pct[mercado]
    print(f"  {mercado}: {count} registros ({pct:.2f}%)")

# Resposta específica para Interno
if 'Interno' in mercado_counts.index:
    pct_interno = mercado_pct['Interno']
    print(f"\n>>> {pct_interno:.2f}% dos registros são de mercado Interno")
else:
    print("\n>>> Nenhum registro de mercado Interno encontrado")

# 3. Análise combinada (B2B + Interno)
print("\n" + "-" * 70)
print("3. ANÁLISE COMBINADA")
print("-" * 70)

b2b_interno = len(aroma[(aroma['tipo_cliente'] == 'B2B') & (aroma['mercado_principal'] == 'Interno')])
pct_b2b_interno = (b2b_interno / len(aroma)) * 100

print(f"\nRegistros B2B E Mercado Interno: {b2b_interno} ({pct_b2b_interno:.2f}%)")

# Tabela cruzada
print("\nTabela Cruzada (Tipo Cliente x Mercado Principal):")
tabela_cruzada = pd.crosstab(aroma['tipo_cliente'], aroma['mercado_principal'], margins=True)
print(tabela_cruzada)

# Salvar tabela cruzada
tabela_cruzada.to_csv('tabela_cruzada_aroma_extrato.csv', encoding='utf-8-sig')
print("\n>>> Tabela cruzada salva: tabela_cruzada_aroma_extrato.csv")

# 4. Visualizações
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Gráfico 1: Tipo de Cliente
tipo_cliente_counts.plot(kind='bar', ax=axes[0], color=COR_AROMA, alpha=0.8, edgecolor='black')
axes[0].set_title('Distribuição por Tipo de Cliente\nAroma / Extrato Natural', 
                  fontsize=13, fontweight='bold')
axes[0].set_xlabel('Tipo de Cliente', fontsize=11)
axes[0].set_ylabel('Número de Registros', fontsize=11)
axes[0].tick_params(axis='x', rotation=0)
axes[0].grid(axis='y', alpha=0.3)

# Adicionar valores e porcentagens nas barras
for i, (tipo, count) in enumerate(tipo_cliente_counts.items()):
    pct = tipo_cliente_pct[tipo]
    axes[0].text(i, count + 0.5, f'{count}\n({pct:.1f}%)', 
                ha='center', va='bottom', fontsize=10, fontweight='bold')

# Gráfico 2: Mercado Principal
mercado_counts.plot(kind='bar', ax=axes[1], color=COR_AROMA, alpha=0.8, edgecolor='black')
axes[1].set_title('Distribuição por Mercado Principal\nAroma / Extrato Natural', 
                  fontsize=13, fontweight='bold')
axes[1].set_xlabel('Mercado Principal', fontsize=11)
axes[1].set_ylabel('Número de Registros', fontsize=11)
axes[1].tick_params(axis='x', rotation=45)
axes[1].grid(axis='y', alpha=0.3)

# Adicionar valores e porcentagens nas barras
for i, (mercado, count) in enumerate(mercado_counts.items()):
    pct = mercado_pct[mercado]
    axes[1].text(i, count + 0.5, f'{count}\n({pct:.1f}%)', 
                ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('grafico_perfil_aroma_extrato.png', bbox_inches='tight', facecolor='white', dpi=300)
print("\n>>> Gráfico salvo: grafico_perfil_aroma_extrato.png")
plt.close()

# 5. Resumo final
print("\n" + "=" * 70)
print("RESUMO FINAL")
print("=" * 70)
print(f"\nTotal de registros analisados: {len(aroma)}")
if 'B2B' in tipo_cliente_counts.index:
    print(f"Porcentagem B2B: {tipo_cliente_pct['B2B']:.2f}%")
if 'Interno' in mercado_counts.index:
    print(f"Porcentagem Mercado Interno: {mercado_pct['Interno']:.2f}%")
print(f"Porcentagem B2B E Mercado Interno: {pct_b2b_interno:.2f}%")
print("=" * 70)
