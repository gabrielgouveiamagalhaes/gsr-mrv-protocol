# Protocolo MRV-P

**Versão 0.4 — minuta para comentários**
Protocolo aberto para mensuração auditável de aço recuperado em desmantelamento naval-portuário.

Publicado pela GSR Logística Reversa Naval. Livre para implementação por qualquer parte,
inclusive concorrentes.

> Tradução normativa do [SPEC.md](SPEC.md). Em caso de divergência entre as duas versões, prevalece
> a inglesa até que uma delas seja designada canônica.

---

## 0. Situação deste documento

Esta é uma **minuta para comentários**, não uma norma acabada. Ela codifica um método já
implementado e em operação, derivado de uma campanha integralmente instrumentada e de um conjunto
de trabalhos submetidos a revisão por pares. Não foi ratificada por nenhum organismo de
normalização, e ainda não existe esquema de avaliação da conformidade para ela.

É publicada abertamente por uma razão específica. Um método de mensuração que só o próprio autor
consegue executar não é um método de mensuração; é uma alegação comercial. O valor deste protocolo
está em que uma segunda parte consiga implementá-lo, rodá-lo no próprio pátio e obter um número
comparável — inclusive uma parte que concorra com o publicador.

**Linguagem normativa.** Conforme a convenção da ABNT e da ISO: **DEVE** exprime requisito de
conformidade; **NÃO DEVE**, proibição; **CONVÉM QUE**, recomendação forte; **PODE**, permissão.

## 1. Escopo

Este protocolo aplica-se ao desmantelamento de navios, equipamentos portuários e ativos
industriais comparáveis contendo aço, do momento em que o ativo é aceito para desmantelamento até
o momento em que o material recuperado é recebido pelo destinatário.

Ele especifica quatro coisas: a unidade em que a massa DEVE ser medida; a evidência que DEVE
sustentar cada medição; a aritmética pela qual o balanço de materiais de uma campanha é pontuado e
reconciliado; e o que o implementador DEVE publicar junto com o resultado.

**Fora de escopo.** Inventário de materiais perigosos do ativo antes do desmantelamento (regime do
IHM, sob a Convenção de Hong Kong), segurança do trabalho, licenciamento ambiental e certificação
metalúrgica a jusante. Este protocolo foi desenhado para ficar *entre* o IHM e o certificado de
usina, e para interoperar com ambos.

## 2. A unidade de medição é a carga, não a campanha

A falha que este protocolo existe para corrigir é a estimativa agregada. Na prática corrente, o
aço recuperável é estimado a partir da arqueação líquida em leve (LDT) ou de fichas de fabricante,
e raramente medido. Toda alegação a jusante — rastreabilidade, circularidade, carbono — herda o
erro dessa estimativa única.

> **Requisito 2.1.** A massa recuperada DEVE ser medida por carga que deixa o sítio, em balança com
> certificação metrológica legal válida, e NÃO DEVE ser derivada da divisão de um total de
> campanha.

**Definições.** **Lote** é a menor unidade que carrega balanço de materiais independente.
**Carga** é uma movimentação pesada de veículo. **Campanha** é o desmantelamento de um ativo. Cada
carga DEVE corresponder a exatamente um lote; cada lote, a exatamente uma campanha.

## 3. Camadas de evidência

Nem todo registro é igual, e um protocolo que os trate como iguais não pode ser auditado. Cada
medição DEVE carregar uma camada de evidência, e a camada DEVE ser registrada, não inferida.

| Camada | Definição | Peso |
|--------|-----------|------|
| `E1` | Ticket original e contemporâneo de balança certificada, retido | 1,00 |
| `E2` | Registro reconstruído a partir de fonte primária, quando o ticket original não está mais retido | 0,60 |
| `E3` | Valor estimado, modelado ou simulado, sem documento de lastro | 0,30 |

O implementador PODE estender a escala com camadas adicionais; as três acima DEVEM conservar estes
pesos, para que as pontuações permaneçam comparáveis entre implementações.

**Por que E2 existe, e por que não está escondida.** Um registro reconstruído não é falsificação e
não é ticket certificado. É uma terceira coisa, e o movimento honesto é nomeá-la e descontá-la. A
campanha de referência do próprio publicador contém registros E1 e E2, e o protocolo foi desenhado
assim por causa disso.

## 4. Pontuação de conformidade do lote

Cada lote DEVE carregar pontuação em seis dimensões, cada uma expressa de 0 a 100, combinadas por
pesos fixos.

```
S_MRV = 0,30·W + 0,20·D + 0,15·L + 0,15·C + 0,10·G + 0,10·A
```

| Símbolo | Dimensão | Peso | Significado |
|---------|----------|------|-------------|
| `W` | Certeza de pesagem | 0,30 | Classe do instrumento, validade da calibração, retenção do ticket |
| `D` | Documentação | 0,20 | MTR, nota fiscal, certificado de recebimento, relatório de pesagem |
| `L` | Rastreabilidade logística | 0,15 | Custódia ininterrupta do sítio ao destinatário |
| `C` | Conformidade | 0,15 | Licença ambiental, contrato, registro de material perigoso |
| `G` | Geolocalização | 0,10 | Coordenadas de origem e destino registradas |
| `A` | Auditabilidade | 0,10 | Completude e imutabilidade da trilha |

A pontuação DEVE ser calculada, nunca digitada. Na implementação de referência ela é uma coluna
gerada de banco de dados, de modo que nenhum operador consegue escrever uma pontuação diretamente.

### 4.1 Faixas de nota

| Nota | Pontuação | Leitura |
|------|-----------|---------|
| `A+` | ≥ 90 | Plenamente evidenciado; apto a asserção de terceiro |
| `A`  | ≥ 80 | Evidenciado, com lacunas menores |
| `B`  | ≥ 70 | Rastreável; documentação incompleta |
| `C`  | ≥ 60 | Parcial; inapto a alegações externas |
| `D`  | ≥ 50 | Fraco |
| `F`  | < 50 | Não evidenciado |

## 5. Faixa de confiança — uma segunda dimensão, independente

A pontuação diz quanta evidência existe. Não diz se essa evidência concorda consigo mesma. São
perguntas diferentes e NÃO DEVEM ser colapsadas num número só.

Cada lote DEVE, portanto, carregar também uma faixa de confiança, derivada da presença de
documentos *e* da extração automática do conteúdo desses documentos, reconciliada contra os
valores registrados.

| Faixa | Condição |
|-------|----------|
| `ALTA` | Nota fiscal, relatório de pesagem e MTR todos presentes, e ao menos duas extrações documentais independentes conferem com os valores registrados |
| `MÉDIA` | Nota fiscal ou relatório de pesagem presente, e ao menos uma extração confere |
| `BAIXA` | Somente evidência fotográfica |
| `NÃO VERIFICADA` | Nenhuma das anteriores |

> **Requisito 5.1 — travas.** Um lote NÃO DEVE ser usado para emitir instrumento transferível —
> token, certificado, direito negociável — abaixo de `ALTA`. Um lote NÃO DEVE ser usado para
> certificação de carbono abaixo de `MÉDIA`.

Pontuação alta com faixa baixa é uma alegação bem documentada que nada verificou.

## 6. Fluxo de governança da campanha

No nível de campanha o protocolo define um fluxo de cinco passos. Os passos 1 e 5 são os
estruturais; uma implementação conforme DEVE implementar ambos.

```
1. Gate de qualidade → 2. Contexto → 3. Predição → 4. Pontuação → 5. Reconciliação vs pesagem oficial
   integridade +         atributos     ŷ com          S = 0,4C          e/P > 0,15 ⇒ divergência
   outliers              do ciclo      intervalo      + 0,3K + 0,3E              │
        ▲                                                                       │
        └──────────── divergência ⇒ revisão de conformidade, ────────────────────┘
                      não ajuste silencioso
```

### 6.1 Passo 1 — gate de qualidade dos dados

Registros operacionais DEVEM ser triados antes de qualquer inferência.

- Valores negativos DEVEM ser registrados como erro.
- Outliers univariados DEVEM ser sinalizados por escore z robusto (mediana e desvio absoluto
  mediano), com limiar `3,5`.
- Carga útil por viagem fora de `3–20 t` DEVE ser sinalizada como inconsistência logística.

### 6.2 Passo 4 — pontuação da campanha

```
S = 0,40·Completude + 0,30·Consistência + 0,30·Evidência

Completude   = fração dos campos operacionais requeridos preenchidos
Consistência = 0,60 · carga-na-faixa + 0,40 · livre-de-outliers
Evidência    = peso da camada da cláusula 3 (E1 = 1,00; E2 = 0,60; E3 = 0,30)
```

## 7. Reconciliação e a regra de divergência

Esta é a cláusula que o resto do protocolo existe para sustentar.

```
e = | P_oficial − ŷ |          e / P_oficial > δ  ⇒  divergência          (δ = 0,15)
```

> **Requisito 7.1.** Havendo divergência, o implementador DEVE registrá-la, DEVE encaminhá-la a
> revisão de conformidade, e NÃO DEVE resolvê-la revisando a estimativa para que ela coincida com a
> pesagem. A divergência DEVE permanecer visível no registro publicado da campanha após a
> resolução.

> **Requisito 7.2.** Toda verificação de reconciliação DEVE carregar a causa da sua diferença, ou
> DEVE ser marcada explicitamente como não explicada. Diferença dentro de `δ` **não** fica por isso
> dispensada de explicação: `δ` delimita quando uma divergência é *levantada*, não quando uma
> diferença pode ficar *sem investigação*. Verificação que não traga causa nem marcador explícito de
> não explicada é não conforme.

O requisito 7.2 entrou na v0.4 porque a declaração B1 do próprio publicador passou pela cláusula 7
sobre uma diferença de +6,30% — folgadamente dentro de `δ` — que era erro de intervalo na planilha de
origem, com causa exata e descobrível: a célula TOTAL somava até a linha 118 enquanto os registros de
carga iam até a 125, omitindo sete expedições que valem 42.930 kg. A matriz de rastreabilidade a
registrava havia meses como "ε físico de +6,3%", e nenhuma cláusula obrigava ninguém a perguntar por
quê.

Tolerância que dispensa investigação converte bug em conformidade. `δ` existe para decidir quando uma
diferença se torna *divergência sujeita a revisão*; nunca foi para decidir quando uma diferença
merece *explicação*. São perguntas diferentes, e a v0.3 respondia só a primeira.

`δ = 0,15` é tolerância escolhida, não derivada. Está declarada aqui para que implementadores usem
o mesmo limiar e para que qualquer um possa argumentar que ele está errado. O implementador PODE
aplicar δ mais estrito; quem aplicar δ mais frouxo DEVE declará-lo, e o resultado NÃO DEVE ser
descrito como conforme.

## 8. Fator de calibração — publique o próprio erro

Havendo levantamento de engenharia anterior à campanha, o implementador DEVE publicar a razão
entre massa pesada e massa prevista, e DEVE carregá-la adiante como correção das estimativas
subsequentes.

```
k = P_pesada / P_levantamento

Campanha de referência:  808,0 t pesadas ÷ 692,64 t de levantamento estrutural  ⇒  k = 1,167
```

Uma instalação que não consegue declarar o próprio erro de estimativa não consegue produzir balanço
de materiais auditável. Publicar `k` é a demonstração mais barata disponível de que o implementador
está medindo, e não asserindo.

### 8.1 `k` e `r` são grandezas diferentes

Um levantamento estrutural e uma figura declarada de registro — arqueação em leve, massa de
fabricante, declaração aduaneira — não são a mesma base, e as razões calculadas contra elas NÃO
DEVEM ser reportadas sob o mesmo símbolo.

```
k = P_pesada / P_levantamento      levantamento = soma membro a membro, do engenheiro
r = P_recuperada / P_declarada     declarada    = figura de registro ou de fabricante
```

> **Requisito 8.2.** O implementador que publicar uma razão DEVE declarar se ela é `k` ou `r`, e
> DEVE nomear a base do denominador. O implementador NÃO DEVE calcular `k` substituindo o
> levantamento estrutural por uma figura declarada.

`k` mede **o quanto a engenharia errou**. `r` mede **quanto de uma massa declarada efetivamente
deixa o sítio como determinado material**. Uma instalação com `k` excelente pode ter `r` baixo
simplesmente porque a figura de registro contabiliza máquinas, acabamento e massa não-ferrosa que
nunca estiveram no escopo.

| Campanha | Razão | Valor | Base do denominador |
|----------|-------|-------|---------------------|
| `P2` | `k` | **1,167** | Levantamento estrutural selado, 692,64 t |
| `B1` | `r` | **0,753** | LDT declarada, 962,38 t (ferroso recuperado 724,695 t) |

Estes dois números NÃO DEVEM ser comparados entre si. São publicados juntos para tornar a
distinção concreta.

## 9. Contabilidade de carbono

> **Requisito 9.1.** O fator de emissão DEVE ser estabelecido por campanha, e DEVE ser publicado
> junto com **o denominador sobre o qual foi calculado**. Fator derivado de uma campanha NÃO DEVE
> ser aplicado a outra.

A metade do requisito relativa ao denominador é a que costuma ser esquecida, e é onde mora o erro
maior. Duas campanhas do próprio registro do publicador ilustram:

| Campanha | Fator | Denominador | Proveniência |
|----------|-------|-------------|--------------|
| `P2` | 1,80 tCO₂e/t | Peso líquido de lote, todos os materiais | 107 lotes pesados · 808,0 t → 1.454,4 tCO₂e |
| `B1` | 1,50 tCO₂e/t | Somente ferroso recuperado | 682 t de ferroso → 1.023 tCO₂e |

Os fatores diferem em 20 %. Mas aplicar o fator do P2 à *arqueação em leve declarada* do B1, de
962 t, reportaria **1.731,6 tCO₂e contra as 1.023 efetivamente registradas — 69 % de
superestimação**, sobre uma cifra vendida como auditável. A maior parte desse erro não é o fator; é
a substituição silenciosa de um denominador por outro.

Não havendo fator de campanha para um ativo, o implementador PODE aplicar um padrão modelado, e
DEVE rotular o resultado como modelado, e não medido, no ponto de exibição.

Todo fator publicado DEVE trazer metodologia declarada e banda de incerteza. Resultados de carbono
DEVEM ser reportados com a faixa de confiança dos lotes subjacentes, e NÃO DEVEM ser reportados
para lotes abaixo de `MÉDIA`.

**Uma regra que custa algo ao publicador.** Sob a 9.1, o publicador não pode declarar um número de
carbono único para a empresa. Toda cifra fica atada a uma campanha e a um denominador. É uma
posição de marketing pior e uma posição probatória melhor, e essa troca é o ponto do protocolo.

## 10. Trilha de auditoria

- O registro DEVE ser somente-acréscimo: entradas podem ser adicionadas e lidas, nunca reescritas
  ou apagadas.
- Havendo valor desnormalizado por desempenho, uma cópia DEVE ser designada fonte da verdade, e
  qualquer inconsistência entre cópias DEVE bloquear a certificação até resolução.
- CONVÉM QUE cada lote carregue identificador público resolvível que permita a terceiro recuperar
  seu passaporte sem acesso aos sistemas do implementador.

## 11. Níveis de conformidade

O implementador DEVE declarar um nível. Os níveis existem para que um pátio com balança e sem
software consiga começar.

| Nível | Nome | Requisitos |
|-------|------|------------|
| **1** | Medido | Pesagem por carga em equipamento certificado (2.1), camada de evidência registrada por carga (3), fator de calibração publicado (8). Sem exigência de pontuação. |
| **2** | Pontuado | Nível 1, mais pontuação de conformidade do lote (4) e faixa de confiança (5) calculadas, mais a regra de reconciliação (7) aplicada e divergências retidas. |
| **3** | Atestado | Nível 2, mais trilha somente-acréscimo (10), fatores de carbono por campanha (9) e atestação independente de terceiro do registro da campanha. |

O publicador opera hoje no **Nível 2**, com o Nível 3 não atingido: nenhuma atestação independente
de registro de campanha foi obtida. Suas próprias declarações estão em
[conformance/declarations/](conformance/declarations/) — um Nível 2 e uma não-conformidade.

### 11.1 Escopo da declaração

A declaração DEVE nomear seu escopo. O escopo PODE ser uma campanha inteira ou uma **corrente de
material nomeada** dentro da campanha.

> **Requisito 11.2.** Feita declaração com escopo de corrente, o implementador DEVE arquivar também
> o resultado com escopo de campanha, inclusive não-conformidade, e NÃO DEVE apresentar nível de
> corrente como se aplicasse à campanha.

Sem escopo por corrente, o implementador que detém uma corrente bem medida dentro de uma campanha
mal medida não tem como reportar a parte sólida, e a resposta racional passa a ser não reportar
nada.

## 12. Limites conhecidos desta versão

Leia isto antes de citar o protocolo.

- Os pesos das cláusulas 4 e 6 são **atribuídos por especialista, não derivados empiricamente**.
  Codificam um juízo sobre o que importa, e nenhum estudo demonstra ainda que estes coeficientes
  específicos superem alternativas.
- `δ = 0,15` é, do mesmo modo, tolerância escolhida.
- O fator de calibração `k = 1,167` continua vindo de **um ativo de um tipo**. Uma segunda campanha
  foi testada contra ele e não o resolveu: aquela campanha não tem levantamento estrutural, apenas
  LDT declarada, e portanto produz `r`, não `k`.
- `r = 0,753` igualmente repousa sobre uma campanha de um tipo de ativo.
- Não existe esquema de avaliação da conformidade. Ninguém pode hoje certificar alegação de Nível
  3, inclusive o publicador.
- O protocolo não foi testado contra ativo com frações compósitas significativas.

Estes limites são declarados porque um protocolo que os esconde vale menos que um que não esconde.
Cada um é um convite: quem testar os pesos contra os próprios dados, ou fornecer um segundo fator
de calibração, melhora materialmente a versão 0.4.

## 13. Proveniência

Duas campanhas são publicadas como referência.

**P2** — pórtico de cais em terminal portuário brasileiro: 808,0 t recuperadas em 107 cargas
pesadas contra levantamento estrutural de 692,64 t, sob plano de corte selado por engenheiro
registrado. Ver [reference/p2-campaign.md](reference/p2-campaign.md).

**B1** — duas barcas históricas de passageiros, 2020: 724,695 t de aço ferroso pesadas em 123
expedições contra LDT declarada de 962,38 t. Incluída na v0.2 para testar a cláusula 8, o que não
confirmou; produziu a cláusula 8.1 em seu lugar. Ver
[reference/b1-campaign.md](reference/b1-campaign.md).

O método está documentado em três artigos em coautoria com a Profa. Fernanda Baião, na PUC-Rio —
dois apresentados no II Simpósio de Descomissionamento (CONIDS, UFRJ), sobre o framework de ciência
de dados e sobre transferibilidade multi-caso, e um aceito no SBPO 2026, sobre mensuração
físico-financeira e a proposta de MRV. O fluxo de campanha segue o Algoritmo 1 desse trabalho.
